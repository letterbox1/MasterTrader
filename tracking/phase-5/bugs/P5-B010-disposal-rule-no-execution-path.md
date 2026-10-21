---
id: P5-B010
kind: gap
title: Disposal rule (sell 50% via M11) has no execution path for tokens not on an allowed CEX before P7
phase: 5
type: DOC
status: backlog
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
branch: p5/P5-B010-disposal-rule-no-execution-path
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md]
doc_sync_status: n/a
found_in: "docs/08-airdrops-and-token-launches.md §Wallet discipline"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- `docs/08-airdrops-and-token-launches.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B010-disposal-rule-no-execution-path`
- PR title: `P5-B010: Disposal rule (sell 50% via M11) has no execution path for tokens not on an allowed CEX before P7`

## Progress log

- 2026-10-21 00:00 · planner · opened
