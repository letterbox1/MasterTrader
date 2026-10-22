---
id: P0-T004
kind: task
title: Keep the GitHub repo private and enable secret scanning
phase: 0
type: USER
status: ready
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.N1, R0.N5]
roadmap_todos: [T0.05]
modules: [ops]
dashboards: []
tools: [git, gh]
mcp: []
env: []
services: [github]
branch: p0/P0-T004-github-private-secret-scanning
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T004 · Keep the GitHub repo private and enable secret scanning

## Goal / expected outcome

The MasterTrader repository is private, GitHub secret scanning and push protection are enabled (or the gap is logged and gitleaks covers it), Dependabot alerts are on, and `main` is protected so CI must pass before merge.

## Context & references

- [Roadmap P0 T0.05](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN8)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain)
- [03 §9 hygiene](../../../docs/03-build-spec.md#9-future-proof-hygiene)
- Related: P0-T015 (required checks)
- Unblocks: P0-T015 branch protection

## Requirements

- Repo visibility **private**; your account has 2FA (hardware key or TOTP).
- Settings → Code security: secret scanning **on**, push protection **on**, Dependabot alerts **on** (if a feature isn't available on your plan for private repos, log it and rely on gitleaks in pre-commit + CI).
- Branch protection on `main`: require PR, require status checks (added by P0-T015), no force-push, no deletion.
- No deploy keys or PATs with write scope beyond what CI needs.

## ToDo

- [ ] Confirm visibility is private.
- [ ] Turn on 2FA on your GitHub account if not already.
- [ ] Enable secret scanning, push protection and Dependabot alerts; log which features your plan provides.
- [ ] Add a branch protection rule (or ruleset) for `main` as above; add required checks once P0-T015's workflow has run once.
- [ ] Review deploy keys and PATs; revoke anything unused.

## Verification

### Tests
- Push-protection probe: on a throwaway branch, commit GitHub's documented sample test token; push must be blocked (or gitleaks blocks it locally). Delete the branch.

### Scenarios
- Given a secret-looking string is committed, when pushing, then push protection blocks it and gitleaks (pre-commit) would have caught it earlier.

### Stress / failure injection
- n/a: settings change.

## Acceptance criteria

- [ ] Repo private; account 2FA on
- [ ] Secret scanning + push protection on (or gap logged with gitleaks as fallback)
- [ ] `main` protected; required checks set after P0-T015
- [ ] Probe push blocked

## Exceptions & edge cases

- Some security features need GitHub Advanced Security on private repos: if unavailable for free, log it; gitleaks in pre-commit + CI (P0-T014/P0-T015) is the guaranteed control.

## Cardinal rules (do NOT)

- Do NOT make the repo public, even briefly.
- Do NOT add collaborators or third-party apps with repo write access.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/07-security-notes.md` §2: note the fallback if a GitHub feature is unavailable.
- `docs/roadmap/phase-0-foundations.md`: tick T0.05 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T004-github-private-secret-scanning`
- PR title: `P0-T004: Keep the GitHub repo private and enable secret scanning`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; run fields added)
