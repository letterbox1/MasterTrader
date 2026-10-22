---
id: P1-B013
kind: gap
title: IBKR paper reconciliation needs IB Gateway, which no container list includes
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.12]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B013-ibkr-gateway-container-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: done
found_in: docs/roadmap/phase-1-data-and-monitoring.md T1.29; docs/02-v1-architecture.md §3.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B013 · IBKR paper reconciliation needs IB Gateway, which no container list includes

## Goal / expected outcome

02 §3.2 lists an `ib-gateway` container (phase 1 or 2) with its network, restart/re-login behaviour and secrets

## Context & references

- Found in: T1.29 reconciles "IBKR paper"; IBKR's API requires a running IB Gateway/TWS session with login (and periodic re-auth); [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) lists no such container in any phase
- Related items: P1-T042, P1-T064

## Requirements

- **Where:** T1.29 reconciles "IBKR paper"; IBKR's API requires a running IB Gateway/TWS session with login (and periodic re-auth); [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) lists no such container in any phase
- **Expected:** 02 §3.2 lists an `ib-gateway` container (phase 1 or 2) with its network, restart/re-login behaviour and secrets
- **Actual:** No container, no login procedure
- **Suggested fix:** Add `ib-gateway` (digest-pinned, read-only API mode for P1) to 02 §3.2 and a USER step for the paper login; or defer IBKR recon to P2 with the engine
- **Impact:** IBKR part of R1.12 cannot be met (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B013): add an `ib-gateway` container (IBC-managed) when IBKR is used
- [x] Aligned docs carry it: 02 §3.2 (`ib-gateway` row), 02 §3.1 (`core` members); roadmap T1.44, R1.12
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T070 (new OPS task, T1.44), P1-T042, P1-T074

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (02 §3.2 (`ib-gateway` row), 02 §3.1 (`core` members); roadmap T1.44, R1.12)
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B013-ibkr-gateway-container-missing`
- PR title: `P1-B013: IBKR paper reconciliation needs IB Gateway, which no container list includes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B013` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B013; docs carry it (02 §3.2 (`ib-gateway` row), 02 §3.1 (`core` members); roadmap T1.44, R1.12); implementation owned by P1-T070 (new OPS task, T1.44), P1-T042, P1-T074
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B013); docs updated: 02 §3.2 (`ib-gateway` row), 02 §3.1 (`core` members); roadmap T1.44, R1.12; implementation owned by P1-T070 (new OPS task, T1.44), P1-T042, P1-T074
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
