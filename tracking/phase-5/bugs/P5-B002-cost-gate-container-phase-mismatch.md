---
id: P5-B002
kind: gap
title: On-chain cost gate is required in P5 but placed in the P6 treasury container
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.04]
roadmap_todos: []
modules: [M22]
dashboards: []
branch: p5/P5-B002-cost-gate-container-phase-mismatch
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: "docs/02-v1-architecture.md §3.2 (containers table)"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B002 · On-chain cost gate is required in P5 but placed in the P6 treasury container

## Goal / expected outcome

02 §3.2 states where the cost gate runs in P5 (library `mt_treasury.costgate` used by airdrop-exec, signer and mt-api) and that the P6 `treasury` container reuses it.

## Context & references

- 02 §3.2: `treasury` (phase 6) = "M22 hold-and-earn + treasury allocation, on-chain cost gate"
- Roadmap R5.04 / T5.21 require the gate in P5; tasks P5-T019/T020

## Requirements

- **Steps to reproduce:** Compare the 02 §3.2 container table with the P5 roadmap R5.04.
- **Expected:** The cost gate is available in P5 without the P6 container.
- **Actual:** It is only listed under the phase-6 `treasury` container.
- **Suggested fix:** Edit 02 §3.2: move "on-chain cost gate" to a P5 library row (`mt_treasury.costgate`) used by `airdrop-exec`/`signer`/`mt-api`; the P6 `treasury` container consumes it.
- **Impact:** S3: planning ambiguity; resolved in P5 tasks by building it as a library.

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

## Branch & PR

- Branch: `p5/P5-B002-cost-gate-container-phase-mismatch`
- PR title: `P5-B002: On-chain cost gate is required in P5 but placed in the P6 treasury container`

## Progress log

- 2026-10-21 00:00 · planner · opened
