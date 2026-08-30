# github-workflows

Secure reusable GitHub Actions workflows for CI, repository security scanning, and automatic GitHub Releases.

## What this repository provides

- `ci.yml`: auto-detects common project types and dispatches to conservative language adapters.
- `security.yml`: runs Trivy vulnerability, secret, and misconfiguration scanning.
- `release.yml`: versions and releases an exact CI-tested commit without running application code.

Supported CI profiles in v1: Node/JavaScript/TypeScript, Python, Go, Maven, Gradle, .NET, Rust, generic/static, and mixed/monorepo layouts.

## Mandatory security rule

Consumer repositories **must pin the reusable workflow to a full 40-character commit SHA**:

```yaml
jobs:
  ci:
    uses: cjgl23/github-workflows/.github/workflows/ci.yml@0123456789abcdef0123456789abcdef01234567
```

Do not use `@main` or a movable tag for private repositories.

This repository is intentionally public. It contains automation code only and must never contain application credentials, cloud credentials, private keys, API tokens, or other secrets.

See `docs/USAGE.md`, `docs/SECURITY-MODEL.md`, and `docs/MIGRATION.md`.
