#!/usr/bin/env python3
"""
Update every `requirements*.in` file in the repo root to the latest stable
version *within the current major*, and warn about packages that have a newer
major available so you can decide whether to bump them by hand.

Usage:
    scripts/update_requirements.py            # rewrite the .in files
    scripts/update_requirements.py --dry-run  # print what would change

After it runs, regenerate the lock files:
    uv pip compile requirements.in     -o requirements.txt
    uv pip compile requirements.dev.in -o requirements.dev.txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from packaging.version import InvalidVersion, Version

REPO_ROOT = Path(__file__).resolve().parent.parent
PIN_RE = re.compile(r"^(?P<name>[^=\s#]+)==(?P<version>[^\s#]+)(?P<trail>.*)$")

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class Pin:
    raw_name: str        # may include extras, e.g. "requests[security]"
    pypi_name: str       # extras stripped, used for the PyPI lookup
    current: Version
    trail: str           # anything after the version on the line


def parse_pin(line: str) -> Pin | None:
    m = PIN_RE.match(line)
    if not m:
        return None
    raw_name = m["name"]
    try:
        current = Version(m["version"])
    except InvalidVersion:
        return None
    pypi_name = raw_name.split("[", 1)[0]
    return Pin(raw_name=raw_name, pypi_name=pypi_name, current=current, trail=m["trail"])


def fetch_stable_versions(pkg: str) -> list[Version]:
    """All non-yanked, non-prerelease, non-dev releases for `pkg`, ascending."""
    url = f"https://pypi.org/pypi/{pkg}/json"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)

    out: list[Version] = []
    for v_str, files in data.get("releases", {}).items():
        if not files or all(f.get("yanked") for f in files):
            continue
        try:
            v = Version(v_str)
        except InvalidVersion:
            continue
        if v.is_prerelease or v.is_devrelease:
            continue
        out.append(v)
    out.sort()
    return out


@dataclass
class Resolution:
    pin: Pin
    latest_in_major: Version | None
    latest_overall: Version | None
    error: str | None = None

    @property
    def has_in_major_update(self) -> bool:
        return (
            self.latest_in_major is not None
            and self.latest_in_major != self.pin.current
        )

    @property
    def has_new_major(self) -> bool:
        return (
            self.latest_overall is not None
            and self.latest_overall.major > self.pin.current.major
        )


def resolve(pin: Pin) -> Resolution:
    try:
        versions = fetch_stable_versions(pin.pypi_name)
    except Exception as e:
        return Resolution(pin, None, None, error=str(e))
    same_major = [v for v in versions if v.major == pin.current.major]
    return Resolution(
        pin=pin,
        latest_in_major=same_major[-1] if same_major else None,
        latest_overall=versions[-1] if versions else None,
    )


def process_file(path: Path, dry_run: bool) -> list[str]:
    """Rewrite `path` (unless dry_run). Returns the list of major-bump warnings."""
    print(f"\n{BLUE}== {path.name} =={RESET}")
    lines = path.read_text().splitlines(keepends=False)

    pins: list[tuple[int, Pin]] = []
    for i, line in enumerate(lines):
        pin = parse_pin(line)
        if pin is not None:
            pins.append((i, pin))

    # Fetch in parallel — one HTTP call per pinned package.
    with ThreadPoolExecutor(max_workers=8) as pool:
        resolutions = list(pool.map(lambda ip: (ip[0], resolve(ip[1])), pins))

    warnings: list[str] = []
    for idx, res in resolutions:
        pin = res.pin
        if res.error:
            print(f"  {RED}!{RESET} {pin.raw_name:<40} PyPI lookup failed: {res.error}")
            continue

        if res.has_in_major_update:
            new_ver = res.latest_in_major
            print(f"  {GREEN}^{RESET} {pin.raw_name:<40} {pin.current} -> {new_ver}")
            lines[idx] = f"{pin.raw_name}=={new_ver}{pin.trail}"
        else:
            print(f"  {DIM}={RESET} {pin.raw_name:<40} {pin.current}")

        if res.has_new_major:
            msg = (
                f"{pin.raw_name}: new major {res.latest_overall} available "
                f"(currently on {pin.current.major}.x)"
            )
            warnings.append(msg)
            print(f"  {YELLOW}!{RESET} {msg}")

    if not dry_run:
        path.write_text("\n".join(lines) + "\n")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--dry-run", action="store_true", help="don't write files")
    args = parser.parse_args()

    files = sorted(REPO_ROOT.glob("requirements*.in"))
    if not files:
        print(f"No requirements*.in files found in {REPO_ROOT}", file=sys.stderr)
        return 1

    all_warnings: list[str] = []
    for f in files:
        all_warnings.extend(process_file(f, dry_run=args.dry_run))

    print(f"\n{BLUE}== Summary =={RESET}")
    if not all_warnings:
        print(f"  {GREEN}No new major versions available.{RESET}")
    else:
        print(f"  {YELLOW}New majors available (not auto-updated, review manually):{RESET}")
        for w in all_warnings:
            print(f"    - {w}")

    if args.dry_run:
        print(f"\n{DIM}(dry-run: no files modified){RESET}")
    else:
        print("\nNext: regenerate lock files with")
        print("  uv pip compile requirements.in     -o requirements.txt")
        print("  uv pip compile requirements.dev.in -o requirements.dev.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
