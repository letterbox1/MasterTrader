---
id: P5-B016
kind: gap
title: Proof of control for registering addresses is required but no method is specified
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.05]
roadmap_todos: []
modules: [M22]
dashboards: [D18]
branch: p5/P5-B016-proof-of-control-method-unspecified
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: n/a
found_in: "docs/ui/dashboards/D18-wallets-treasury.md §Actions ("Register wallet/address (proof of control)")"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B016 · Proof of control for registering addresses is required but no method is specified

## Goal / expected outcome

Docs define acceptable proof methods that fit the security model (no site-requested signatures; Ellipal has no EIP-712).

## Context & references

- D18 requires proof of control; 13 §3 does not define it
- 08 never-automated forbids the system requesting `personal_sign` of arbitrary payloads
- Task P5-T021 proposes: micro self-transfer, on-device message signature pasted back, or `manual_attested`

## Requirements

- **Steps to reproduce:** Try to specify how the vault address proves control.
- **Expected:** Method list with strengths.
- **Actual:** Unspecified.
- **Suggested fix:** Adopt the three P5-T021 methods in 13 §3 and D18.
- **Impact:** S3: blocks the registration UX design.

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

- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution
- `docs/ui/dashboards/D18-wallets-treasury.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B016-proof-of-control-method-unspecified`
- PR title: `P5-B016: Proof of control for registering addresses is required but no method is specified`

## Progress log

- 2026-10-21 00:00 · planner · opened
