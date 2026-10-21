---
id: P5-B003
kind: gap
title: Signer callers: "airdrop-exec only" (02 §3.1) vs "policy service" (13 §2), and P6/P7 needs
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.02, R5.N1]
roadmap_todos: []
modules: [M22]
dashboards: []
branch: p5/P5-B003-signer-allowed-callers-conflict
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: "docs/02-v1-architecture.md §3.1; docs/13-wallets-treasury-and-onchain.md §2"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B003 · Signer callers: "airdrop-exec only" (02 §3.1) vs "policy service" (13 §2), and P6/P7 needs

## Goal / expected outcome

One definition of who may call the signer: in P5 `airdrop-exec` (the policy service for claims/revokes/sweeps), later `treasury` (P6) and the DEX execution path (P7), each with its own client certificate and allowed intent types.

## Context & references

- 02 §3.1: `signer` "reachable only from airdrop-exec"
- 13 §2: "accepts intents … from the policy service only"; 02 §3.2 says the extended signer "also serves DEX execution"
- Tasks P5-T013, P5-T017, P5-T054

## Requirements

- **Steps to reproduce:** Read both sections; the sweep scheduler and later treasury/DEX paths are not airdrop-exec.
- **Expected:** A caller table: caller identity → allowed intent types.
- **Actual:** Two different statements; sweeps' caller unclear.
- **Suggested fix:** Define "policy service" = airdrop-exec in P5 (hosting claims, revokes and sweeps); add `treasury` (P6) and `engine`/DEX path (P7) rows with per-caller intent allow-lists.
- **Impact:** S3: affects network rules and mTLS config; P5 tasks assume airdrop-exec hosts sweeps.

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
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B003-signer-allowed-callers-conflict`
- PR title: `P5-B003: Signer callers: "airdrop-exec only" (02 §3.1) vs "policy service" (13 §2), and P6/P7 needs`

## Progress log

- 2026-10-21 00:00 · planner · opened
