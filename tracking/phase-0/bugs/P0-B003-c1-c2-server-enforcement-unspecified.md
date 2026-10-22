---
id: P0-B003
kind: gap
title: Server-side enforcement of C1/C2 confirmations is unspecified
phase: 0
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.08]
roadmap_todos: [T0.24]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B003-c1-c2-server-enforcement-unspecified
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/README.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B003 · Server-side enforcement of C1/C2 confirmations is unspecified

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Adopt the preview-token contract from P0-T035; document it in 02 §7.2 and ui §3.3.

## Context & references

- Found in: `docs/02-v1-architecture.md §7.2`
- Related: P0-T035
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)

## Requirements

- **Steps to reproduce:** Read 02 §7.2: body is `{args, idempotency_key, reason}`; levels are 'enforced server-side, never only in the UI'.
- **Expected:** A contract showing how the server knows a C1/C2 confirm happened (e.g. `POST /commands/{c}/preview` → `confirmation_token` bound to args, required on execute, 428 when missing).
- **Actual:** No field or endpoint carries a confirmation; as written, C1/C2 can only be enforced in the UI.
- **Impact:** Implementers may ship UI-only confirmations, contradicting the doc's own rule.
- **Suggested fix:** Adopt the preview-token contract from P0-T035; document it in 02 §7.2 and ui §3.3.

## ToDo

- [x] Decision taken: 17 §D P0-B003 (ratified in 17 §E)
- [x] Docs updated so they agree: 02 §7.2 (preview call, `confirm_token`, 428, C1/C2 server checks); ui README §3.3 (server enforcement) and §3.6 (12 h re-auth); roadmap P0 R0.08/T0.24/T0.62
- [x] Affected P0 task files reference the resolution: P0-T033, P0-T035, P0-T048, P0-T054, P0-T058
- [x] Regression check owned: P0-T054 C1/C2 negative cases

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B003 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T035 (token + preview hash + re-auth checks), P0-T033 (`/auth/reauth`), P0-T054 (tests)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/ui/README.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B003-c1-c2-server-enforcement-unspecified`
- PR title: `P0-B003: fix server-side enforcement of C1/C2 confirmations is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B003` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B003; docs checked: 02 §7.2 (preview call, `confirm_token`, 428, C1/C2 server checks); ui README §3.3 (server enforcement) and §3.6 (12 h re-auth); roadmap P0 R0.08/T0.24/T0.62. Root cause: 02 §7.2 stated server-side enforcement without a request field or endpoint to carry it. Implementation owned by P0-T035 (token + preview hash + re-auth checks), P0-T033 (`/auth/reauth`), P0-T054 (tests).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B003); docs updated: 02 §7.2 (preview call, `confirm_token`, 428, C1/C2 server checks); ui README §3.3 (server enforcement) and §3.6 (12 h re-auth); roadmap P0 R0.08/T0.24/T0.62; implementation owned by P0-T035 (token + preview hash + re-auth checks), P0-T033 (`/auth/reauth`), P0-T054 (tests)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
