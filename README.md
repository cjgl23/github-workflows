# github-workflows

Secure, reusable GitHub Actions workflows for CI, security scanning, and automated releases across multiple repository types.

## Security-first usage

Consumer repositories must pin reusable workflows to a full 40-character commit SHA. Do not reference `@main` or a movable version tag from private repositories.

This repository contains public automation only. It must never contain application credentials, cloud credentials, private keys, access tokens, or other secrets.

Implementation is being developed and validated on a feature branch before promotion to `main`.
