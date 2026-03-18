#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-bump Grafana (OSS) for YunoHost manifest.

What it does:
- Scrape official download pages (hardcoded URLs below) for linux_amd64 and linux_arm64.
- Supports versions like "12.4.1" and "12.3.2+security-01".
- Picks the latest version that exists for BOTH architectures.
- Compares with manifest.toml (ignores "~ynhX" suffix).
- If newer: read sha256 from the HTML page ONLY (no fallback), update manifest.toml,
  and print GitHub Actions outputs (changed/new_version/urls/sha256).

Environment variables:
- MANIFEST (optional): path to manifest.toml (default: "manifest.toml")
- GITHUB_OUTPUT (optional): if set, key=value pairs are appended for downstream steps.

Dependencies:
- tomlkit (preserves format/comments), packaging (robust version compare).
"""

import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import List, Tuple, Optional
from packaging.version import Version
import tomlkit

# ---------------------------------------------------------------------------
# Hardcoded pages (as requested)
# ---------------------------------------------------------------------------
AMD64_PAGE = "https://grafana.com/grafana/download?edition=oss&pg=oss-graf&platform=linux"
ARM64_PAGE = "https://grafana.com/grafana/download?edition=oss&pg=oss-graf&platform=arm"

# Manifest location (can be overridden via env if needed)
MANIFEST = Path(os.environ.get("MANIFEST", "manifest.toml"))

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")


def fetch(url: str, timeout: int = 60) -> str:
    """Fetch a URL and return decoded text (utf-8, ignore errors)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data.decode("utf-8", errors="ignore")


def find_assets(html: str, arch_tag: str) -> List[Tuple[str, str]]:
    """
    Extract download URLs and versions for a given arch.
    Accept versions like '12.4.1' and '12.3.2+security-01'.

    Returns a list of (version_str, url).
    """
    ver = r"(\d+\.\d+\.\d+(?:\+[A-Za-z0-9\.-]+)?)"
    patterns = [
        # Modern format with build id: grafana_<ver>_<build>_linux_<arch>.tar.gz
        rf"(https://dl\.grafana\.com/grafana/release/{ver}/grafana_\2_\d+_linux_{arch_tag}\.tar\.gz)",
        # Legacy format without build id: grafana-<ver>.linux-<arch>.tar.gz
        rf"(https://dl\.grafana\.com/grafana/release/{ver}/grafana-\2\.linux-{arch_tag}\.tar\.gz)",
    ]
    out: List[Tuple[str, str]] = []
    for pat in patterns:
        for m in re.finditer(pat, html):
            url, version = m.group(1), m.group(2)
            out.append((version, url))
    # Deduplicate by URL
    uniq = {}
    for version, url in out:
        uniq[url] = version
    return [(v, u) for u, v in uniq.items()]


def pick_latest_common(amd64_pairs: List[Tuple[str, str]],
                       arm64_pairs: List[Tuple[str, str]]) -> str:
    """
    Choose the latest version present on BOTH pages to avoid mismatches.
    """
    amd64_versions = {v for v, _ in amd64_pairs}
    arm64_versions = {v for v, _ in arm64_pairs}
    common = amd64_versions & arm64_versions
    if not common:
        raise RuntimeError(
            "No common Grafana version between amd64 and arm64 pages.\n"
            f"amd64: {sorted(amd64_versions)}\narm64: {sorted(arm64_versions)}"
        )
    latest = max((Version(v) for v in common))
    return str(latest)


def url_for_version(pairs: List[Tuple[str, str]], version_str: str) -> Optional[str]:
    for v, u in pairs:
        if v == version_str:
            return u
    return None


def extract_sha256_from_html(html: str, asset_url: str) -> Optional[str]:
    """
    Try to find a 64-hex SHA256 in the HTML near the asset URL.
    Strategy:
      - Search around each occurrence of the asset URL and look ahead/behind a window
        for a 64-hex digest. We keep the window reasonably large to be resilient
        to HTML structure changes.
    """
    sha_pat = re.compile(r"\b([a-fA-F0-9]{64})\b")
    # Search all occurrences of the asset URL
    for m in re.finditer(re.escape(asset_url), html):
        start = max(0, m.start() - 1500)   # 1500 chars before
        end   = min(len(html), m.end() + 1500)  # 1500 chars after
        window = html[start:end]
        msha = sha_pat.search(window)
        if msha:
            return msha.group(1).lower()
    return None


def read_sha256_from_page(linux_html: str, arm_html: str, asset_url: str, arch: str) -> str:
    """
    Read SHA256 from the corresponding download page (no fallback).
    """
    page_html = linux_html if arch == "amd64" else arm_html
    sha = extract_sha256_from_html(page_html, asset_url)
    if not sha:
        raise RuntimeError(f"Unable to find sha256 on page for asset: {asset_url}")
    return sha


def write_outputs(**kv):
    """
    Write GitHub Actions outputs if GITHUB_OUTPUT is available.
    """
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main():
    # Fetch pages
    linux_html = fetch(AMD64_PAGE)
    arm_html = fetch(ARM64_PAGE)

    # Parse candidate assets
    amd64_pairs = find_assets(linux_html, "amd64")
    arm64_pairs = find_assets(arm_html, "arm64")

    if not amd64_pairs or not arm64_pairs:
        print("::error::Unable to locate download URLs for amd64 and/or arm64.", file=sys.stderr)
        sys.exit(1)

    # Select latest common version
    latest_version = pick_latest_common(amd64_pairs, arm64_pairs)
    latest_amd64_url = url_for_version(amd64_pairs, latest_version)
    latest_arm64_url = url_for_version(arm64_pairs, latest_version)

    if not latest_amd64_url or not latest_arm64_url:
        print("::error::Selected latest version missing for one architecture.", file=sys.stderr)
        sys.exit(1)

    # Load manifest
    text = MANIFEST.read_text(encoding="utf-8")
    doc = tomlkit.parse(text)

    # Current version and base (remove "~ynhX")
    current_version = str(doc["version"])
    base_version = current_version.split("~", 1)[0]

    # Compare versions using packaging.Version (handles "+security-xx")
    if Version(base_version) == Version(latest_version):
        print(f"No update needed. Current={current_version}, Latest={latest_version}")
        write_outputs(changed="false")
        return

    # Read checksums from pages ONLY (no .sha256 sidecar, no download)
    print(f"Found new Grafana version: {latest_version} (current {current_version})")
    print("Reading sha256 from Grafana pages (no fallback)...")
    amd64_sha256 = read_sha256_from_page(linux_html, arm_html, latest_amd64_url, "amd64")
    arm64_sha256 = read_sha256_from_page(linux_html, arm_html, latest_arm64_url, "arm64")

    # Update manifest
    doc["version"] = f"{latest_version}~ynh1"
    # [resources.sources.main].amd64.*
    doc["resources"]["sources"]["main"]["amd64"]["url"] = latest_amd64_url
    doc["resources"]["sources"]["main"]["amd64"]["sha256"] = amd64_sha256
    # [resources.sources.arm64].arm64.*
    doc["resources"]["sources"]["arm64"]["arm64"]["url"] = latest_arm64_url
    doc["resources"]["sources"]["arm64"]["arm64"]["sha256"] = arm64_sha256

    MANIFEST.write_text(tomlkit.dumps(doc), encoding="utf-8")

    # Expose outputs for PR step
    write_outputs(
        changed="true",
        new_version=latest_version,
        linux_url=latest_amd64_url,
        linux_sha256=amd64_sha256,
        arm64_url=latest_arm64_url,
        arm64_sha256=arm64_sha256,
    )
    print("manifest.toml updated successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"::error::{e}", file=sys.stderr)
        sys.exit(1)
