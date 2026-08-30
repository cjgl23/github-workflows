# Migration

## Safe rollout sequence

1. Validate the central repository itself.
2. Record a known-good full commit SHA.
3. Migrate one non-standard repository and verify its native checks still pass.
4. Migrate one standard Node repository and verify lint/test/build behaviour.
5. Only then migrate additional repositories selectively.

Do not mass-update consumers automatically in v1.

## Upgrade procedure

A central change is merged and validated first. A consumer upgrades by changing one 40-character SHA to another in a pull request. The consumer's own CI and security checks must pass before that SHA change is merged.

## Fallback

Keep existing local workflows until the central equivalent has passed in that repository. If auto-detection is ambiguous, set `project-type` and `working-directory` explicitly or use static custom commands under read-only CI permissions.
