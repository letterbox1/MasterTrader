---
id: P0-B002
kind: gap
title: C3 approval channel doesn't exist until P2, so P0 C3 commands (kill OFF) can't complete
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B002-c3-approval-channel-before-p2
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md R0.08 / T0.24
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

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
