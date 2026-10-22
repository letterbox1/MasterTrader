---
id: P0-B002
kind: gap
title: C3 approval channel doesn't exist until P2, so P0 C3 commands (kill OFF) can't complete
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
roadmap_todos: [T0.24, T0.62]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B002-c3-approval-channel-before-p2
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md R0.08 / T0.24
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B002 · C3 approval channel doesn't exist until P2, so P0 C3 commands (kill OFF) can't complete

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Document a host-only break-glass channel (`mt-admin approve <id>` over SSH on Tailscale + TOTP), audited `source=system`, kept as a fallback after P2; add it to 02 §7.2 and 07 §6.

## Context & references

- Found in: `docs/roadmap/phase-0-foundations.md R0.08 / T0.24`
- Related: P0-T035, P0-T054
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- [P2 roadmap](../../../docs/roadmap/phase-2-strategies-risk-lab.md) (T2.33)

## Requirements

- **Steps to reproduce:** Follow R0.08 (C3 = approve + TOTP + cool-down) and look for the approval channel: Telegram commands and the C3 TOTP prompt are T2.33 (P2).
- **Expected:** A defined P0 approval channel so C3 is testable and kill OFF is possible before the Telegram bot exists.
- **Actual:** 02 §7.2 / 07 §6 make Telegram the only C3 channel; P0 scope excludes Telegram commands. In P0, `risk.kill.off` and any C3 change would stay pending forever.
- **Impact:** P0 can test C3 only with fakes; a real kill ON in P0 has no supported way back off.
- **Suggested fix:** Document a host-only break-glass channel (`mt-admin approve <id>` over SSH on Tailscale + TOTP), audited `source=system`, kept as a fallback after P2; add it to 02 §7.2 and 07 §6.

## ToDo

- [x] Decision taken: 17 §D P0-B002 (ratified in 17 §E)
- [x] Docs updated so they agree: 02 §7.2 (break-glass paragraph) and §7.4 Telegram row; 07 §6; 03 M11 (C3 note); ui README §3.3; ui mobile-and-telegram C3 row; 04 Phase 0; roadmap P0 R0.08/R0.12/T0.27/T0.62 and P2 R2.19/T2.24
- [x] Affected P0 task files reference the resolution: P0-T033, P0-T035, P0-T049, P0-T054
- [x] Regression check owned: P0-T054 C3 suite through `mtctl approve`

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B002 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T035 (`mtctl approve` channel), P0-T054 (tests)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/07-security-notes.md`: reconcile as described.
- `docs/roadmap/phase-0-foundations.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B002-c3-approval-channel-before-p2`
- PR title: `P0-B002: fix c3 approval channel doesn't exist until P2, so P0 C3 commands (kill OFF) can't complete`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B002` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B002; docs checked: 02 §7.2 (break-glass paragraph) and §7.4 Telegram row; 07 §6; 03 M11 (C3 note); ui README §3.3; ui mobile-and-telegram C3 row; 04 Phase 0; roadmap P0 R0.08/R0.12/T0.27/T0.62 and P2 R2.19/T2.24. Root cause: C3 was defined only via Telegram, which the plan builds in P2. Implementation owned by P0-T035 (`mtctl approve` channel), P0-T054 (tests).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B002); docs updated: 02 §7.2 (break-glass paragraph) and §7.4 Telegram row; 07 §6; 03 M11 (C3 note); ui README §3.3; ui mobile-and-telegram C3 row; 04 Phase 0; roadmap P0 R0.08/R0.12/T0.27/T0.62 and P2 R2.19/T2.24; implementation owned by P0-T035 (`mtctl approve` channel), P0-T054 (tests)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
