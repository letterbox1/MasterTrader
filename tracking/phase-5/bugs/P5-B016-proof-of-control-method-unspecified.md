---
id: P5-B016
kind: gap
title: Proof of control for registering addresses is required but no method is specified
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B016-proof-of-control-method-unspecified
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: done
found_in: "docs/ui/dashboards/D18-wallets-treasury.md §Actions ("Register wallet/address (proof of control)")"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §B P5-B016): proof of control = you sign a one-time challenge in your own wallet app (EIP-4361-style text / Solana `signMessage`) or make a tiny self-transfer; the system never signs it; signer-created wallets register themselves
- [x] Docs carry it: 13 §3 step 1 (proof of control), D18 actions (register), roadmap R5.25/T5.04/T5.32/T5.67
- [x] P5 tasks aligned: P5-T067 (challenge + verifiers), P5-T021 (`wallet.register`), P5-T069 (test), P5-T005 (USER registration), P5-T050 (wizard)

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

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
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B016): proof of control = you sign a one-time challenge in your own wallet app (EIP-4361-style text / Solana `signMessage`) or make a tiny self-transfer; the system never signs it; signer-created wallets register themselves. Docs checked: 13 §3 step 1 (proof of control), D18 actions (register), roadmap R5.25/T5.04/T5.32/T5.67. Implementation owned by P5-T067 (challenge + verifiers), P5-T021 (`wallet.register`), P5-T069 (test), P5-T005 (USER registration), P5-T050 (wizard)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B016); docs updated: 13 §3 step 1 (proof of control), D18 actions (register), roadmap R5.25/T5.04/T5.32/T5.67; implementation owned by P5-T067 (challenge + verifiers), P5-T021 (`wallet.register`), P5-T069 (test), P5-T005 (USER registration), P5-T050 (wizard)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
