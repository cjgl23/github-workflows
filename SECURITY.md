# Security Policy

This repository contains **public automation only**. No user, application, repository, cloud, database, or deployment secrets belong here.

## Supply-chain rules

- Consumer repositories pin reusable workflows to a full commit SHA.
- External Actions used here are pinned to a full commit SHA.
- Baseline CI and security workflows receive `contents: read` only.
- The release workflow receives only `contents: write` and does not execute caller application code.
- Checkout credentials are not persisted.
- Baseline examples and workflows do not use `secrets: inherit`.

Report a suspected vulnerability privately through GitHub's security reporting mechanism when enabled. Do not publish real credentials in an issue.
