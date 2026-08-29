from pathlib import Path
import re

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
PERMISSIONS_BLOCK = re.compile(r"^permissions:\s*\n((?:^[ \t]+[^\n]*\n?)*)", re.MULTILINE)
PERMISSION_ENTRY = re.compile(r"^\s+([a-z-]+):\s*([^\s#]+)", re.MULTILINE)
PROHIBITED_WRITES = {"id-token", "packages", "issues", "pull-requests", "actions", "deployments", "checks"}


def _top_permissions(text: str) -> dict[str, str]:
    match = PERMISSIONS_BLOCK.search(text)
    if not match:
        return {}
    return {key: value for key, value in PERMISSION_ENTRY.findall(match.group(1))}


def scan_repository(root: Path) -> list[str]:
    issues: list[str] = []
    workflows = root / ".github" / "workflows"
    if not workflows.exists():
        return issues

    for path in sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()

        if "secrets: inherit" in text:
            issues.append(f"{rel}: secrets: inherit is prohibited")

        for ref in USES.findall(text):
            if ref.startswith("./") or ref.startswith("$/"):
                continue
            if "@" not in ref or not FULL_SHA.fullmatch(ref.rsplit("@", 1)[1]):
                issues.append(f"{rel}: external uses reference must use a full commit SHA: {ref}")

        if "actions/checkout@" in text:
            blocks = re.split(r"(?=^\s*-\s+name:|^\s*-\s+uses:)", text, flags=re.MULTILINE)
            for block in blocks:
                if "actions/checkout@" in block and "persist-credentials: false" not in block:
                    issues.append(f"{rel}: checkout must set persist-credentials: false")

        permissions = _top_permissions(text)
        if path.name == "release.yml":
            if permissions != {"contents": "write"}:
                issues.append(f"{rel}: release permissions must be exactly contents: write")
        else:
            if permissions != {"contents": "read"}:
                issues.append(f"{rel}: permissions must be exactly contents: read")

        for permission, value in permissions.items():
            if permission in PROHIBITED_WRITES and value == "write":
                issues.append(f"{rel}: prohibited permission {permission}: write")

    return issues


if __name__ == "__main__":
    problems = scan_repository(Path("."))
    for problem in problems:
        print(problem)
    raise SystemExit(1 if problems else 0)
