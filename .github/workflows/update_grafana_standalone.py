#!/usr/bin/env python3
"""
Update the Grafana standalone URLs and SHA-256 checksums in manifest.toml.

This script is intended to run from GitHub Actions after a ci-auto-update-*
branch has been created. The Grafana main source is already updated by the
YunoHost updater; this script derives the standalone source values from it.
"""

import hashlib
import logging
import re
from pathlib import Path
from typing import Any

import requests
import tomlkit

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

MANIFEST_PATH = Path("manifest.toml")
ARCHITECTURES = ("amd64", "arm64", "armhf")
GITHUB_RELEASE_PREFIX = ("https://github.com/grafana/grafana/releases/download/v")


# ========================================================================== #
# Functions customizable by app maintainer


def extract_release_fragment(main_amd64_url: str) -> str:
    """Extract '<version>/grafana_<version>_<build>' from main.amd64.url."""
    pattern = re.compile(
        re.escape(GITHUB_RELEASE_PREFIX)
        + r"(?P<fragment>[^\"']+?)_linux"
    )

    match = pattern.search(main_amd64_url)
    if match is None:
        raise ValueError(
            "Unable to extract the Grafana release fragment from "
            f"{main_amd64_url}"
        )

    return match.group("fragment")


def update_standalone_url(url: str, release_fragment: str) -> str:
    """Replace the version/artifact fragment immediately before '_linux'."""
    old_fragment_pattern = re.compile(
        r"\d+\.\d+\.\d+/grafana_[^/\s\"']+?(?=_linux)"
    )

    updated_url, replacements = old_fragment_pattern.subn(
        release_fragment,
        url,
        count=1,
    )

    if replacements == 1:
        return updated_url

    if release_fragment in url:
        return url

    raise ValueError(f"No Grafana release fragment found in URL: {url}")


def sha256sum_of_url(url: str) -> str:
    """Compute a remote file checksum without saving the file locally."""
    logger.info("Calculating SHA-256 for %s", url)

    response = requests.get(
        url,
        headers={"User-Agent": "github-actions"},
        stream=True,
        timeout=300,
    )
    response.raise_for_status()

    checksum = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            checksum.update(chunk)

    return checksum.hexdigest()


# ========================================================================== #
# Core script


def as_string(value: Any) -> str:
    """Return a plain string from a TOMLKit value or a regular string."""
    return value.value if hasattr(value, "value") else str(value)


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"{MANIFEST_PATH} not found")

    with MANIFEST_PATH.open("r", encoding="utf-8") as manifest_file:
        manifest = tomlkit.load(manifest_file)

    sources = manifest["resources"]["sources"]
    main_source = sources["main"]
    standalone_source = sources["standalone"]

    main_amd64_url = as_string(main_source["amd64"]["url"])
    release_fragment = extract_release_fragment(main_amd64_url)
    logger.info("Grafana release fragment: %s", release_fragment)

    for architecture in ARCHITECTURES:
        source = standalone_source[architecture]
        current_url = as_string(source["url"])
        updated_url = update_standalone_url(
            current_url,
            release_fragment,
        )

        if updated_url != current_url:
            logger.info("Updating %s URL", architecture)
            source["url"] = updated_url
        else:
            logger.info("%s URL is already up to date", architecture)

        source["sha256"] = sha256sum_of_url(updated_url)
        logger.info(
            "%s.sha256 = %s",
            architecture,
            as_string(source["sha256"]),
        )

    with MANIFEST_PATH.open("w", encoding="utf-8") as manifest_file:
        tomlkit.dump(manifest, manifest_file)

    logger.info("Updated %s successfully", MANIFEST_PATH)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, requests.RequestException) as exc:
        logger.error("Update failed: %s", exc)
        raise SystemExit(1) from exc
