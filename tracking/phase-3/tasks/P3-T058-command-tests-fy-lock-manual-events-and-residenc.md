---
id: P3-T058
kind: task
title: "Command tests: FY lock, manual events and residency loosening via C3"
phase: 3
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T055, P3-T031, P3-T033, P3-T038, P3-T021]
requirements: [R3.16]
roadmap_todos: [T3.65]
modules: [M18, M11, mt_api]
dashboards: [D14, D15]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p3/P3-T058-command-tests-fy-lock-manual-events-and-residenc
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T058 · Command tests: FY lock, manual events and residency loosening via C3

## Goal / expected outcome

An automated suite proves the R3.16 contract on the full stack: a locked FY rejects (holds) new events until a C3 unlock; `journal.manual_event.add` needs C2; `task.answer` needs C1; and a residency change that would loosen the venue registry waits for C3 while tightening applies at once and M11 fails closed in between.

## Context & references

- Roadmap: [R3.16, T3.65](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Under test: P3-T055 (commands + residency contract), P3-T031 (`tax.residency.add`), P3-T033 (Egypt block via registry), P3-T038 (`task.answer`), P3-T021 (manual opening lots)
- Levels: [17 §D P0-B003](../../../docs/17-decisions-register.md#d-other-decisions) · cool-down [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · contract [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats), [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)

## Requirements

- Suite `tests/e2e/journal/test_commands_r316.py` against the staging compose (paper engine, test TOTP seed, Telegram approval stub that exercises the real C3 service path; cool-down shortened via the test settings profile, never in code).
- Cases: (1) lock FY → event dated in it held, lot select / regime set / manual event → 423; (2) unlock without reason → 422; unlock with C3 → held events released once; (3) `journal.manual_event.add` with C1 only → refused; with a valid C2 preview hash + fresh session → accepted, `audit.command` row; stale session (> 12 h default) → refused; (4) `task.answer` without the C1 confirm token → refused, with it → new answer version; (5) add EG residency → registry tightens immediately, crypto entry rejected, reduce-only exit allowed; (6) remove EG → registry unchanged and a C3 request pending; after approval + cool-down → loosened; (7) residency saved but recompute consumer stopped → M11 fails closed for residency-dependent products.

## ToDo

- [ ] Write the suite and fixtures
- [ ] Run on staging compose; record results and timings in the progress log
- [ ] File bugs for any deviation (`./kanban new --kind bug --found-in P3-T058`)

## Verification

### Tests
- The seven cases above, automated with pass/fail assertions on HTTP status, `audit.command` rows, held-event counts and M11 reasons.

### Scenarios
- Given FY2026-27 locked, when a late fill for 30 June 2027 arrives, then it is held and appears only after a C3 unlock.
- Given a residency change removes the Egypt block, when nobody approves, then crypto entries stay blocked indefinitely.

### Stress / failure injection
- Restart `mt-api` during case 6 (pending C3) → the request survives, nothing loosens early.

## Acceptance criteria

- [ ] All seven cases pass on staging
- [ ] No loosening applied without C3 in any case
- [ ] Results recorded in the progress log

## Exceptions & edge cases

- Shortened cool-downs exist only in the test settings profile; production defaults stay as in 16 §2.3.

## Cardinal rules (do NOT)

- Do NOT stub M11 or the C3 service; the real components must decide.
- Do NOT run against production data.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.65 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T058-command-tests-fy-lock-manual-events-and-residenc`
- PR title: `P3-T058: Command tests: FY lock, manual events and residency loosening via C3`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T058` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.16/T3.65 (docs/16–17 alignment)
