#!/usr/bin/env python3
"""
Update additional_dependencies pins in .pre-commit-hooks.yaml to the
latest PyPI release for each package.

Requires: pip install ruamel.yaml

Usage:
    python update_hooks.py [path/to/.pre-commit-hooks.yaml]
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from ruamel.yaml import YAML

PYPI_URL = "https://pypi.org/pypi/{name}/json"

# pkg[extras] == version ; optional trailing environment marker
DEP_RE = re.compile(
    r"^(?P<pkg>[A-Za-z0-9_.\-]+)"
    r"(?P<extras>\[[^\]]+\])?"
    r"==(?P<ver>[A-Za-z0-9_.\-]+)"
    r"(?P<marker>\s*;.*)?$"
)


def latest_version(package: str) -> str | None:
    url = PYPI_URL.format(name=package)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        return data["info"]["version"]
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        print(f"  ! failed to fetch {package}: {exc}", file=sys.stderr)
        return None


def update_file(path: Path) -> bool:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # avoid re-wrapping long lines

    data = yaml.load(path.read_text())
    changed = False
    cache: dict[str, str | None] = {}

    for hook in data:
        deps = hook.get("additional_dependencies")
        if not deps:
            continue

        for i, dep in enumerate(deps):
            m = DEP_RE.match(str(dep))
            if not m:
                print(f"  ? skipped (unrecognized): {dep}", file=sys.stderr)
                continue

            pkg = m.group("pkg")
            current = m.group("ver")
            extras = m.group("extras") or ""
            marker = m.group("marker") or ""

            if pkg not in cache:
                cache[pkg] = latest_version(pkg)
            latest = cache[pkg]

            if latest and latest != current:
                print(f"  {hook.get('id', '?')}: {pkg} {current} -> {latest}")
                deps[i] = f"{pkg}{extras}=={latest}{marker}"
                changed = True
            else:
                print(f"  {hook.get('id', '?')}: {pkg} {current} (up to date)")

    if changed:
        yaml.dump(data, path)
    return changed


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".pre-commit-hooks.yaml")
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"Checking {path} ...")
    changed = update_file(path)

    print("Updated." if changed else "No changes.")
    sys.exit(0)


if __name__ == "__main__":
    main()
