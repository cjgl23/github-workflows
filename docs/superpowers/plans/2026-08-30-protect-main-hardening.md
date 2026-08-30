# Protect Main Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create one stable aggregate validation check for `github-workflows`, then use it as the required merge gate for the `Protect Main` ruleset while also strengthening `repo-template` branch protections.

**Architecture:** Keep the existing validation matrix unchanged and add a final `validation-complete` job that runs with `always()`, depends on every top-level validation/fixture job, and fails unless every dependency reports `success`. The repository rulesets should then require pull requests plus stable required status checks, require branches to be up to date, block deletion and force-pushes, and expose no bypass actors.

**Tech Stack:** GitHub Actions YAML, Python `unittest`, GitHub repository rulesets.

**Spec:** Approved in the conversation: protect the default branch, require PRs with zero approvals, require up-to-date successful checks, prevent deletion/force-push, and keep bypasses empty.

## Global Constraints

- `github-workflows` required check must represent the complete validation matrix, not only the `validate` job.
- Existing fixture jobs and reusable-workflow behavior must remain unchanged.
- No new workflow permissions or secrets.
- `repo-template` keeps only CI + Security; no Release workflow is added.
- Rulesets target `~DEFAULT_BRANCH` and remain `active`.
- Required approvals: `0`.
- No bypass actors.

---

### Task 1: Add a test-first aggregate validation contract

**Files:**
- Create: `tests/test_validate_workflow.py`
- Modify: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: the existing top-level jobs `validate`, `fixture-node`, `fixture-python`, `fixture-go`, `fixture-maven`, `fixture-gradle`, `fixture-dotnet`, `fixture-rust`, `fixture-generic`, and `fixture-monorepo`.
- Produces: one stable top-level job/check named `validation-complete`.

- [ ] **Step 1: Write the failing test**

Create a `unittest` that reads `.github/workflows/validate.yml` and requires a `validation-complete` job, `if: ${{ always() }}`, all ten existing top-level dependencies under `needs`, and an explicit failure path for any dependency result other than `success`.

- [ ] **Step 2: Verify RED**

Open a PR with the test-only commit and confirm `Validate Shared Workflows` fails because `validation-complete` is absent.

- [ ] **Step 3: Implement the minimal aggregate job**

Append a job that depends on all ten jobs, serializes `needs` with `toJSON(needs)`, and uses Python to exit non-zero when any result is not `success`.

- [ ] **Step 4: Verify GREEN**

Confirm the PR's full `Validate Shared Workflows` run succeeds and that the new `validation-complete` check succeeds after all dependencies finish.

- [ ] **Step 5: Keep the final diff focused**

Remove this implementation-only plan before merge so the central workflow repository gains only the test and workflow gate.

### Task 2: Harden repository rulesets

**Files:**
- Repository setting: `cjgl23/github-workflows` → Rules → Rulesets → `Protect Main`
- Repository setting: `cjgl23/repo-template` → Rules → Rulesets → `Protect Main`

**Interfaces:**
- Consumes: `validation-complete` in `github-workflows`; stable CI/Security checks in `repo-template`.
- Produces: enforced default-branch merge gates.

- [ ] **Step 1: Update `github-workflows` Protect Main**

Require pull requests with `0` approvals, require `validation-complete`, require the branch to be up to date before merging, prevent deletion, prevent force pushes, and configure no bypass actors.

- [ ] **Step 2: Update `repo-template` Protect Main**

Require pull requests with `0` approvals, require the stable CI and Security checks, require the branch to be up to date before merging, prevent deletion, prevent force pushes, and configure no bypass actors.

- [ ] **Step 3: Re-read both rulesets**

Verify both are active, target `~DEFAULT_BRANCH`, contain PR and required-status-check rules, retain deletion/non-fast-forward protection, and have no bypass actors.
