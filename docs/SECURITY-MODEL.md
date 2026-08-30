# Security Model

## Trust boundaries

The public shared-workflow repository is treated as untrusted for future changes. Consumer repositories trust only the exact full commit SHA written in their wrapper workflow.

A malicious future commit to this public repository therefore cannot change the code executed by an existing consumer until the consumer's SHA pin is explicitly changed.

## Permissions

- CI: `contents: read`.
- Security: `contents: read`.
- Release: `contents: write` only.

No baseline workflow grants `id-token: write`, `packages: write`, `issues: write`, `pull-requests: write`, or `actions: write`.

## Secrets

Baseline shared workflows do not use `secrets: inherit`. CI/security receive no application secrets. Release uses only the caller repository's scoped `GITHUB_TOKEN` for tag and GitHub Release creation.

## Checkout credentials

All checkout steps set `persist-credentials: false`. Application build/test code therefore cannot read a persisted checkout token from Git configuration.

## Release isolation

The release workflow checks out the exact CI-tested SHA, verifies it is on the caller's default branch, computes the version from Git metadata, and creates the tag and GitHub Release. It does not execute caller package-manager, build, test, or deployment commands.

## Third-party tooling

GitHub-maintained Actions are pinned to full commit SHAs. Trivy and actionlint are downloaded from versioned upstream releases and verified against fixed SHA-256 checksums before execution.

## Residual risk

Any workflow with `contents: write` can modify repository content if the exact trusted workflow revision itself is malicious. Full-SHA pinning and explicit consumer SHA upgrade PRs are the primary control against silent propagation.
