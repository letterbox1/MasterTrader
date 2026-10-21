---
id: P3-T054
kind: task
title: Phase 3 exit demo
phase: 3
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T001, P3-T038, P3-T013, P3-T014, P3-T027, P3-T028, P3-T040, P3-T041, P3-T045, P3-T046, P3-T047, P3-T048, P3-T049, P3-T050, P3-T051, P3-T052, P3-T053]
requirements: [R3.01, R3.03, R3.06, R3.07, R3.12, R3.14]
roadmap_todos: []
modules: [M18]
dashboards: [D14, D15]
branch: p3/P3-T054-phase-exit-demo
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md, docs/04-plan-of-action.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T054 · Phase 3 exit demo

## Goal / expected outcome

A recorded demo proves all three roadmap exit criteria on the production stack and confirms all phase tasks are done/cancelled with no open S1/S2 bugs, so PHASE.md's exit boxes can be ticked.

## Context & references

- Roadmap: [§6 exit criteria](../../../docs/roadmap/phase-3-journal-and-tax.md#6-exit-criteria-demo)
- PHASE.md exit criteria list
- Evidence items: P3-T045…P3-T053

## Requirements

- EC1: every paper trade, fee and funding payment of the demo day appears automatically in the journal in native/USD/AUD (query: `audit.fill` count = journal fill events; ledger funding = journal funding; all three currency fields non-null).
- EC2: D15 shows FY2026-27 to date both ways (investor vs trader) and the PAYG estimate, each with rule version + FX source (screenshots at 1920×1080 and 390×844).
- EC3: `/tasks?type=TAX_QUESTION` lists the questions; P3-T001 progress log shows the agent engaged.
- Also shown: golden suite + WORM suite + prompt audit green; snapshot dry-run report; Beancount/Fava; first 7 days of the 1-month run clean.
- Phase checks: `./kanban validate --phase 3` 0 errors; all tasks done/cancelled; no open S1/S2 gaps (P3-B001/P3-B002 resolved or downgraded with a decision).

## ToDo

- [ ] Prepare a demo checklist script `tools/journal/exit_demo.sh` (read-only queries)
- [ ] Run the demo; capture screenshots/query outputs into the PR description
- [ ] Tick PHASE.md exit criteria boxes with links to evidence
- [ ] Run `./kanban done P3-T054`

## Verification

### Tests

- The demo script's assertions (counts, non-null fields, provenance fields present).

### Scenarios

- Given the demo day, when the script runs, then all EC1–EC3 assertions pass and evidence links are recorded.

### Stress / failure injection

- n/a: covered by P3-T052

## Acceptance criteria

- [ ] EC1 proven
- [ ] EC2 proven
- [ ] EC3 proven
- [ ] All P3 tasks done/cancelled; no open S1/S2 bugs
- [ ] PHASE.md exit boxes ticked with evidence

## Exceptions & edge cases

- If the 1-month run is still in progress, the phase may close with it handed to P7 (P3-T053 close condition).

## Cardinal rules (do NOT)

- Do NOT tick an exit box without linked evidence.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md` §6: mark the demo date; `docs/04-plan-of-action.md` Phase 3 checklist ticks (main agent).
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-T054-phase-exit-demo`
- PR title: `P3-T054: Phase 3 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
