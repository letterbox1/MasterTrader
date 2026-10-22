---
id: P5-B003
kind: gap
title: Signer callers: "airdrop-exec only" (02 §3.1) vs "policy service" (13 §2), and P6/P7 needs
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B003-signer-allowed-callers-conflict
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: done
found_in: "docs/02-v1-architecture.md §3.1; docs/13-wallets-treasury-and-onchain.md §2"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §B P5-B003): the signer accepts intents only from the policy service; `airdrop-exec` is the policy service in P5 (claims, revokes, sweeps); treasury (P6) and DEX execution (P7) go through it
- [x] Docs carry it: 02 §3.1 (`signer` network row), 02 §3.2 (`airdrop-exec` + `signer` rows), 13 §2 (interface), roadmap R5.02
- [x] P5 tasks aligned: P5-T013 (caller auth), P5-T017 (network), P5-T054 (isolation test), P5-T044 (policy service)

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

- `docs/02-v1-architecture.md`: align with the resolution
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B003-signer-allowed-callers-conflict`
- PR title: `P5-B003: Signer callers: "airdrop-exec only" (02 §3.1) vs "policy service" (13 §2), and P6/P7 needs`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B003): the signer accepts intents only from the policy service; `airdrop-exec` is the policy service in P5 (claims, revokes, sweeps); treasury (P6) and DEX execution (P7) go through it. Docs checked: 02 §3.1 (`signer` network row), 02 §3.2 (`airdrop-exec` + `signer` rows), 13 §2 (interface), roadmap R5.02. Implementation owned by P5-T013 (caller auth), P5-T017 (network), P5-T054 (isolation test), P5-T044 (policy service)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B003); docs updated: 02 §3.1 (`signer` network row), 02 §3.2 (`airdrop-exec` + `signer` rows), 13 §2 (interface), roadmap R5.02; implementation owned by P5-T013 (caller auth), P5-T017 (network), P5-T054 (isolation test), P5-T044 (policy service)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
