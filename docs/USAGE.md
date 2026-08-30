# Usage

Every consumer repository keeps small wrapper workflows and pins this repository by a full 40-character commit SHA.

## CI wrapper

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  ci:
    uses: cjgl23/github-workflows/.github/workflows/ci.yml@FULL_40_CHARACTER_SHA
```

Optional inputs include `project-type`, `working-directory`, `runner-os`, `runtime-version`, `run-lint`, `run-tests`, `run-build`, and static `custom-*-command` overrides.

Custom commands are trusted repository configuration. Never build them from PR titles, branch names, issue text, commit messages, or other untrusted event data.

## Security wrapper

```yaml
name: Security
on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: '17 3 * * 1'

permissions:
  contents: read

jobs:
  security:
    uses: cjgl23/github-workflows/.github/workflows/security.yml@FULL_40_CHARACTER_SHA
```

## Release wrapper

The release wrapper is triggered only after CI completes successfully for a push to the default branch:

```yaml
name: Release
on:
  workflow_run:
    workflows: [CI]
    types: [completed]

permissions:
  contents: write

jobs:
  release:
    if: >-
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.event == 'push' &&
      github.event.workflow_run.head_branch == github.event.repository.default_branch
    uses: cjgl23/github-workflows/.github/workflows/release.yml@FULL_40_CHARACTER_SHA
    with:
      target-sha: ${{ github.event.workflow_run.head_sha }}
      default-branch: ${{ github.event.repository.default_branch }}
```

Do not pass application secrets to these baseline workflows.
