---
id: P3-T038
kind: task
title: Store tax-agent questions as TAX_QUESTION tasks
phase: 3
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005]
requirements: [R3.07, R3.14]
roadmap_todos: [T3.30]
modules: [M18, M19]
dashboards: [D15]
branch: p3/P3-T038-tax-question-tasks-store
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T038 · Store tax-agent questions as TAX_QUESTION tasks

## Goal / expected outcome

The seven 09 tax-agent questions (plus the 2027 follow-ups and any engine-raised questions) are stored now as `TAX_QUESTION` user tasks with status, answer text and answer reference, readable at `/tasks?type=TAX_QUESTION` for D15 Questions, so exit criterion 3 ("questions are logged") is met before the full M19 queue lands in P5.

## Context & references

- Roadmap: [T3.30, R3.07](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 3
- [09 questions](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) · M19 queue [03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation) · D15 Questions tab [D15](../../../docs/ui/dashboards/D15-tax.md)
- Boundary: P5 T5.30 builds the full `mt_curation` queue (ranking, digests, Telegram buttons) on the same table
- Gap: P3-B012 (who owns `curation.task` DDL before P5)

## Requirements

- Minimal `curation.task` (if P0 didn't create it): `task_id`, `type` (enum incl. `TAX_QUESTION`, `PRO_ADVICE`), title, body, status (`open|sent|answered|closed`), answer (text, append-only versions), `answer_ref`, created/updated, provenance; WORM-style append-only versions (latest row per task id).
- Seed migration with Q1–Q7 from 09 + the 2027 sub-questions (a)–(e) from P3-T002 + "perps treatment", "fee-in-crypto disposal", "stablecoins as foreign currency" raised by P3-T018/T020/T024.
- Commands: `task.done` (C0) and new `task.answer` (C1, stores answer + ref; propose in 02 §7.2); answer ids are what `tax.regime.set` (P3-T025) requires.
- Query `/tasks?type=TAX_QUESTION` (read).

## ToDo

- [ ] Migration + seed in `packages/mt_curation/` minimal module (or `mt_journal.questions` if curation package is still a stub)
- [ ] Command handlers + query
- [ ] Tests; docs

## Verification

### Tests

- Integration: seed produces the expected question set; `/tasks?type=TAX_QUESTION` returns them.
- Unit: answering creates a new version row; history kept.

### Scenarios

- Given Q1 is answered, when `tax.regime.set` is called with its answer id, then the regime change is accepted (P3-T025).

### Stress / failure injection

- n/a: tiny table

## Acceptance criteria

- [ ] All questions logged with status
- [ ] Answers versioned and referenceable
- [ ] Exit criterion 3 checkable via the query
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- P5 later migrates/extends the table; no data loss (migration must be additive).

## Cardinal rules (do NOT)

- Do NOT put personal identifiers in question text or answers.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: add `task.answer` (C1).
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.30 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T038-tax-question-tasks-store`
- PR title: `P3-T038: Store tax-agent questions as TAX_QUESTION tasks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
