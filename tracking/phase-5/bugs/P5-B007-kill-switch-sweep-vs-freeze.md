---
id: P5-B007
kind: gap
title: Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.N2, R5.07]
roadmap_todos: []
modules: [M22, M11]
dashboards: [D18, D12]
branch: p5/P5-B007-kill-switch-sweep-vs-freeze
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D18-wallets-treasury.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: "docs/14-strategy-evidence-and-validation.md §5 rung 6; docs/ui/dashboards/D18-wallets-treasury.md §Rules; docs/02-v1-architecture.md F6"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B007 · Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)

## Goal / expected outcome

The docs say explicitly that kill ON freezes auto-claims, treasury moves and new exposure, while protective actions (sweep to the vault, revoke approvals, exits) still run.

## Context & references

- 14 §5 rung 6: "hot balances sweep to the vault address"
- D18: "Kill switch ON: treasury moves … are frozen; exits stay available"; F6 lists "airdrop-exec freezes" without the sweep
- Tasks P5-T028, P5-T058

## Requirements

- **Steps to reproduce:** Read the three passages; a sweep is a treasury move.
- **Expected:** Explicit exemption for protective sweeps/revokes.
- **Actual:** Contradictory reading possible.
- **Suggested fix:** Add to F6 and D18: "kill ON also sweeps hot/identity/burner balances above gas reserve to the vault; revokes and sweeps-to-vault are exempt from the freeze".
- **Impact:** S3: implementers could block the protective sweep.

## ToDo

- [ ] Agree the resolution with the user (or record the decision in the progress log)
- [ ] Edit the source docs listed under Doc sync so they agree
- [ ] Update the affected P5 task files if the numbers/names change

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Docs listed under Doc sync are consistent
- [ ] Affected P5 tasks reference the resolved value/name
- [ ] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: align with the resolution
- `docs/ui/dashboards/D18-wallets-treasury.md`: align with the resolution
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B007-kill-switch-sweep-vs-freeze`
- PR title: `P5-B007: Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)`

## Progress log

- 2026-10-21 00:00 · planner · opened
