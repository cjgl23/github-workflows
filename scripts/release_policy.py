from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
BREAKING = re.compile(r"BREAKING CHANGE:|^[a-z]+(?:\([^)]+\))?!:", re.IGNORECASE | re.MULTILINE)
FEATURE = re.compile(r"^feat(?:\([^)]+\))?:|^(Add|Build|Create|Enable|Implement|Introduce|Support)\s", re.IGNORECASE | re.MULTILINE)


def bump_version(tag: str, bump: str) -> str:
    match = SEMVER.fullmatch(tag.strip())
    if not match:
        raise ValueError(f"invalid semantic version tag: {tag}")
    major, minor, patch = map(int, match.groups())
    if bump == "major":
        major, minor, patch = major + 1, 0, 0
    elif bump == "minor":
        minor, patch = minor + 1, 0
    elif bump == "patch":
        patch += 1
    else:
        raise ValueError(f"invalid bump: {bump}")
    return f"v{major}.{minor}.{patch}"


def _product_changed(files: list[str]) -> bool:
    for raw in files:
        file = raw.strip().replace("\\", "/")
        if not file:
            continue
        if file == "LICENSE" or file.lower().endswith(".md"):
            continue
        if file.startswith((".github/", "docs/", "memory-bank/", "tests/")):
            continue
        return True
    return False


def decide_release(last_tag: str, commits: list[str], changed_files: list[str]) -> dict[str, object]:
    if not _product_changed(changed_files):
        return {"release_needed": False, "last_tag": last_tag, "next_tag": "", "bump": "none"}

    text = "\n".join(commits)
    if BREAKING.search(text):
        bump = "major"
    elif FEATURE.search(text):
        bump = "minor"
    else:
        bump = "patch"

    return {
        "release_needed": True,
        "last_tag": last_tag,
        "next_tag": bump_version(last_tag, bump),
        "bump": bump,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--last-tag", required=True)
    parser.add_argument("--commits-file", type=Path, required=True)
    parser.add_argument("--files-file", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    commits = args.commits_file.read_text(encoding="utf-8").splitlines()
    files = args.files_file.read_text(encoding="utf-8").splitlines()
    decision = decide_release(args.last_tag, commits, files)

    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            for key in ("release_needed", "last_tag", "next_tag", "bump"):
                value = decision[key]
                if isinstance(value, bool):
                    value = str(value).lower()
                handle.write(f"{key}={value}\n")
    print(json.dumps(decision, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
