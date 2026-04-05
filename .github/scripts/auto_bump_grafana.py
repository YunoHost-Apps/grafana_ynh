#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-bump Grafana for GitHub Actions.
"""

import os
import re
import sys
import requests
from pathlib import Path
from typing import Optional
import tomlkit
from packaging import version as pkg_version


AMD64_PAGE = "https://grafana.com/grafana/download?edition=oss&pg=oss-graf&platform=linux"
ARM64_PAGE  = "https://grafana.com/grafana/download?edition=oss&pg=oss-graf&platform=arm"

UA = "Mozilla/5.0 (X11; Linux x86_64) AutoBumpGrafana/1.0"


##########################################################################
# GitHub Actions helpers
##########################################################################

def gha_output(key: str, value: str) -> None:
    """Append a key=value pair to the GitHub Actions output file."""
    gh_env = os.environ.get("GITHUB_OUTPUT")
    if gh_env:
        with open(gh_env, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
    else:
        # Local debug fallback
        with open("/tmp/GITHUB_OUTPUT.tmp", "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")


def gha_error(msg: str) -> None:
    """Print a GHA error annotation (shown in red in the Actions UI)."""
    print(f"::error::{msg}")


def gha_warning(msg: str) -> None:
    """Print a GHA warning annotation."""
    print(f"::warning::{msg}")


def gha_notice(msg: str) -> None:
    """Print a GHA notice annotation."""
    print(f"::notice::{msg}")


##########################################################################
# Fetch HTTP
##########################################################################

def fetch(url: str) -> str:
    """
    Return the RAW page text — without html.unescape().

    WHY: Grafana embeds asset metadata as JSON in the page with slashes
    escaped as \\u002F.  Calling html.unescape() moves the URL ~1 000 000
    chars away from the matching sha256, breaking extraction.
    Keeping the raw text guarantees URL and sha256 are ~30 chars apart.
    """
    headers = {"User-Agent": UA}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text   # do NOT call html.unescape()


##########################################################################
# Asset extraction
##########################################################################

def _normalize_url(u: str) -> str:
    """Decode \\u002F-escaped slashes from the Grafana JSON."""
    return u.replace("\\u002F", "/").replace("\\/", "/")


def extract_asset_from_download_page(raw_html: str, arch: str) -> dict:
    """
    Extract url + sha256 + version for linux_<arch>.tar.gz
    from embedded escaped JSON in Grafana download page.
    """

    # Grafana embeds JSON with escaped quotes -> normalize first
    text = raw_html.replace('\\"', '"')

    url_re = re.compile(
        rf'"url"\s*:\s*"(?P<url>'
        rf'https://dl\.grafana\.com/grafana/release/(?P<version>[^/]+)/'
        rf'grafana_[^"]+_linux_{arch}\.tar\.gz)"'
    )

    match = url_re.search(text)
    if not match:
        raise RuntimeError(f"linux_{arch} tar.gz URL not found")

    url = match.group("url")
    version = match.group("version")

    # sha256 is located AFTER the url in the same JSON object
    window = text[match.end(): match.end() + 800]

    sha_match = re.search(
        r'"sha256"\s*:\s*"([0-9a-fA-F]{64})"',
        window,
    )
    if not sha_match:
        raise RuntimeError(f"sha256 not found for linux_{arch}")

    return {
        "url": url,
        "sha256": sha_match.group(1).lower(),
        "version": version,
    }


##########################################################################
# Manifest helpers
##########################################################################

def read_manifest_version(path: Path) -> Optional[str]:
    try:
        doc = tomlkit.parse(path.read_text(encoding="utf-8"))
        raw = doc["version"].strip()
        return re.sub(r'\s*~ynh\d+\s*$', '', raw)
    except Exception as exc:
        gha_warning(f"Could not read manifest version: {exc}")
        return None


def update_manifest(path: Path, version: str, amd64: dict, arm64: dict) -> None:
    doc = tomlkit.parse(path.read_text(encoding="utf-8"))

    doc["version"] = f"{version}~ynh1"

    try:
        main = doc["resources"]["sources"]["main"]
    except (KeyError, TypeError):
        raise KeyError("Missing [resources.sources.main] in manifest.toml")

    for sub in ("amd64", "arm64"):
        if sub not in main or not isinstance(main[sub], dict):
            raise KeyError(f"Missing subtable [resources.sources.main.{sub}]")

    main["amd64"]["url"]    = amd64["url"]
    main["amd64"]["sha256"] = amd64["sha256"]
    main["arm64"]["url"]    = arm64["url"]
    main["arm64"]["sha256"] = arm64["sha256"]

    path.write_text(tomlkit.dumps(doc), encoding="utf-8")


##########################################################################
# Main
##########################################################################

def main() -> None:
    manifest_path = Path(os.environ.get("MANIFEST", "manifest.toml")).resolve()

    # 1. Read current version
    current = read_manifest_version(manifest_path)
    if current is None:
        gha_error("Cannot read current version from manifest.toml")
        sys.exit(1)

    # 2. Fetch pages
    try:
        amd_html = fetch(AMD64_PAGE)
        arm_html = fetch(ARM64_PAGE)
    except requests.RequestException as exc:
        gha_error(f"Network error: {exc}")
        sys.exit(1)

    # 3. Extract assets
    try:
        amd = extract_asset(amd_html, "amd64")
        arm = extract_asset(arm_html, "arm64")
    except RuntimeError as exc:
        gha_error(str(exc))
        sys.exit(1)

    # 4. Log extracted values (essential for CI debugging)
    gha_notice(f"amd64: {amd['url']} (sha256: {amd['sha256']})")
    gha_notice(f"arm64: {arm['url']} (sha256: {arm['sha256']})")

    # 5. Sanity check
    if amd["version"] != arm["version"]:
        gha_error(f"Upstream version mismatch: amd64={amd['version']} arm64={arm['version']}")
        sys.exit(1)

    new_ver = amd["version"]

    # 6. Compare versions
    try:
        bump_needed = (current is None) or (
            pkg_version.parse(new_ver) > pkg_version.parse(current)
        )
    except pkg_version.InvalidVersion:
        bump_needed = (new_ver != current)

    if not bump_needed:
        gha_output("changed", "false")
        gha_notice(f"⚠️⚠️⚠️ No update needed (current={current}, upstream={new_ver}) ⚠️⚠️⚠️")
        return

    # 7. Emit GHA outputs BEFORE writing the manifest
    gha_output("changed",       "true")
    gha_output("new_version",   new_ver)
    gha_output("linux_url",     amd["url"])
    gha_output("linux_sha256",  amd["sha256"])
    gha_output("arm64_url",     arm["url"])
    gha_output("arm64_sha256",  arm["sha256"])

    # 8. Update manifest
    try:
        update_manifest(manifest_path, new_ver, amd, arm)
    except (KeyError, OSError) as exc:
        gha_error(f"Failed to update manifest: {exc}")
        sys.exit(1)

    gha_notice(f"🔵🔵🔵 Bumped Grafana to {new_ver}~ynh1 🔵🔵🔵")


if __name__ == "__main__":
    main()
