from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

PROFILES = ("node", "python", "go", "maven", "gradle", "dotnet", "rust", "generic")
PRUNE = {".git", "node_modules", "vendor", "target", "bin", "obj", ".venv", "venv", "dist", "build"}


def _empty() -> dict[str, list[str]]:
    return {name: [] for name in PROFILES}


def _rel(root: Path, path: Path) -> str:
    rel = path.resolve().relative_to(root.resolve())
    return "." if str(rel) == "." else rel.as_posix()


def _profiles_for_dir(path: Path) -> set[str]:
    names = {p.name for p in path.iterdir() if p.is_file()}
    found: set[str] = set()
    if "package.json" in names:
        found.add("node")
    if {"pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"} & names:
        found.add("python")
    if "go.mod" in names:
        found.add("go")
    if "pom.xml" in names:
        found.add("maven")
    if {"build.gradle", "build.gradle.kts"} & names:
        found.add("gradle")
    if any(name.endswith((".sln", ".csproj", ".fsproj")) for name in names):
        found.add("dotnet")
    if "Cargo.toml" in names:
        found.add("rust")
    return found


def detect(root: Path, max_depth: int = 3) -> dict[str, list[str]]:
    root = root.resolve()
    result = _empty()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")

    for current, dirs, _files in os.walk(root):
        current_path = Path(current)
        rel_parts = current_path.relative_to(root).parts
        depth = len(rel_parts)
        dirs[:] = sorted(d for d in dirs if d not in PRUNE and depth < max_depth)
        for profile in sorted(_profiles_for_dir(current_path)):
            result[profile].append(_rel(root, current_path))

    for key in result:
        result[key] = sorted(set(result[key]))

    if not any(result[name] for name in PROFILES if name != "generic"):
        result["generic"] = ["."]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--project-type", default="auto", choices=("auto",) + PROFILES)
    parser.add_argument("--working-directory", default=".")
    parser.add_argument("--max-depth", type=int, default=3)
    args = parser.parse_args()

    if args.project_type != "auto":
        result = _empty()
        result[args.project_type] = [args.working_directory]
    else:
        search_root = Path(args.root) / args.working_directory
        detected = detect(search_root, args.max_depth)
        result = _empty()
        for key, paths in detected.items():
            if args.working_directory == ".":
                result[key] = paths
            else:
                base = Path(args.working_directory)
                result[key] = [base.as_posix() if p == "." else (base / p).as_posix() for p in paths]

    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
