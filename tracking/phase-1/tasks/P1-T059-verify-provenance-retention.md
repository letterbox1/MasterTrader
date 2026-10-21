---
id: P1-T059
kind: task
title: Verify provenance tagging and retention end to end
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T008, P1-T029]
requirements: [R1.09]
roadmap_todos: [T1.63]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T059-verify-provenance-retention
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T059 · Verify provenance tagging and retention end to end

## Goal / expected outcome

On the running stack, CoinGecko rows disappear after 24 h, untagged writes are rejected for every ingest table, and purpose filters exclude disallowed rows.

## Context & references

- Roadmap: requirements [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.63](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.63 · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Depends on (this phase): P1-T008, P1-T029

## Requirements

- Time-travel test (DB clock offset or `ingest_time` back-dating in a test schema): CoinGecko rows aged 25 h removed by the next retention run
- For every ingest table, an untagged insert as the app role fails
- `provenance.filter(purpose="model_input")` excludes `model_input_ok=false` rows; `train` excludes `train_ok=false`
- WORM guard: retention job refuses `audit.*`
- Report stored under `reports/verify/P1-T059/`

## ToDo

- [ ] Write `tests/e2e/provenance_retention.py`
- [ ] Run on the dev stack and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- E2E suite as described; nightly in CI

### Scenarios

- Given the retention job is paused for 2 days, when it resumes, then all expired rows are removed in one run and an alert noted the overdue rows

### Stress / failure injection

- n/a: verification

## Acceptance criteria

- [ ] All assertions pass; report stored
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Rows with NULL retention stay forever (asserted)

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.63 once every task traced to it in PHASE.md is done; note P1-T059 next to it.
- `docs/12-policy-and-compliance.md` §5: link the verification report

## Branch & PR

- Branch: `p1/P1-T059-verify-provenance-retention`
- PR title: `P1-T059: Verify provenance tagging and retention end to end`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
