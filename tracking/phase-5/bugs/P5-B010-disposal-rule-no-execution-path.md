---
id: P5-B010
kind: gap
title: Disposal rule (sell 50% via M11) has no execution path for tokens not on an allowed CEX before P7
phase: 5
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.17]
roadmap_todos: []
modules: [M4, M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B010-disposal-rule-no-execution-path
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md]
doc_sync_status: done
found_in: "docs/08-airdrops-and-token-launches.md §Wallet discipline"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B010 · Disposal rule (sell 50% via M11) has no execution path for tokens not on an allowed CEX before P7

## Goal / expected outcome

08 says what happens when the disposal sell has no allowed venue (most fresh airdrop tokens trade only on DEXs, which arrive in P7).

## Context & references

- 08: "The sale is an order through the risk manager"
- DEX execution is P7 (roadmap header: P5 unlocks P7 DEX path)
- Task P5-T045 falls back to a manual sell task

## Requirements

- **Steps to reproduce:** Claim a token listed only on a DEX in P5.
- **Expected:** Defined fallback.
- **Actual:** Undefined.
- **Suggested fix:** Document: if no allowed venue path exists, a `ONCHAIN_ACTION_MANUAL` sell task with cost-gate numbers is created; from P7 the DEX path via M11 takes over.
- **Impact:** S3: unmanaged positions could accumulate silently.

## ToDo

- [x] Resolution recorded: Decided (17 §B P5-B010): before P7 the airdrop disposal (default sell 50% on claim) is a USER task (`ONCHAIN_ACTION_MANUAL` manual sale with cost-gate numbers); automated via M11 only once live execution passes the P7 gates
- [x] Docs carry it: 08 wallet discipline (disposal rule: before/from Phase 7), 03 M4 (disposal is a USER task until P7), D12 rules (Disposal), roadmap R5.17/T5.09/T5.28
- [x] P5 tasks aligned: P5-T045 (creates the manual-sale task, no automated sale), P5-T066 (USER manual sales), P5-T053 (policy test)

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

- `docs/08-airdrops-and-token-launches.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B010-disposal-rule-no-execution-path`
- PR title: `P5-B010: Disposal rule (sell 50% via M11) has no execution path for tokens not on an allowed CEX before P7`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B010): before P7 the airdrop disposal (default sell 50% on claim) is a USER task (`ONCHAIN_ACTION_MANUAL` manual sale with cost-gate numbers); automated via M11 only once live execution passes the P7 gates. Docs checked: 08 wallet discipline (disposal rule: before/from Phase 7), 03 M4 (disposal is a USER task until P7), D12 rules (Disposal), roadmap R5.17/T5.09/T5.28. Implementation owned by P5-T045 (creates the manual-sale task, no automated sale), P5-T066 (USER manual sales), P5-T053 (policy test)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B010); docs updated: 08 wallet discipline (disposal rule: before/from Phase 7), 03 M4 (disposal is a USER task until P7), D12 rules (Disposal), roadmap R5.17/T5.09/T5.28; implementation owned by P5-T045 (creates the manual-sale task, no automated sale), P5-T066 (USER manual sales), P5-T053 (policy test)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
