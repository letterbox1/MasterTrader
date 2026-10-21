---
id: P2-T150
kind: task
title: Weekly five-worst-trades and realised-vs-modelled cost report
phase: 2
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T102, P2-T106]
requirements: []
roadmap_todos: [T2.81]
modules: [M7, M16]
dashboards: [D04, D05]
branch: p2/P2-T150-weekly-worst-trades-report
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T150 · Weekly five-worst-trades and realised-vs-modelled cost report

## Goal / expected outcome

A Prefect flow that every Monday 08:00 AEST/AEDT produces the weekly review pack — the five worst paper trades per sleeve with context, and realised-vs-modelled cost ratios — delivered as a Telegram digest link and an HTML report.

## Context & references

- Roadmap: ToDo T2.81 · [14 §4 discipline/review](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (weekly review of the five worst trades) · [14 §4 execution](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (implementation shortfall per order)
- TCA per order (R2.34) is computed by part A (T2.26); this flow only reads it (part A (P2-T001–T099))
- [D05 TCA tab](../../../docs/ui/dashboards/D05-execution.md) (realised vs modelled alert > 1.5×)

## Requirements

- Per sleeve: five worst closed paper trades by R-multiple (and by $), each with entry/exit, signal reasons, slippage vs decision/arrival, costs, chart deep link, and whether the exit plan was followed.
- Costs: realised vs modelled ratio per strategy × venue × instrument for the week and trailing 4 weeks; ratio > 1.5× highlighted.
- Delivered via `alert.info.weekly_review` (Telegram link + notification centre); HTML stored as an artefact; review notes captured via `journal.note.add` once P3 journal exists (until then a notes field on the report).
- Runs on the paper clock data (P2-T180) and stays useful into P7.

## ToDo

- [ ] Implement Prefect flow `weekly-review` in `mt_lab/reports/weekly.py`
- [ ] HTML template + deep links
- [ ] Schedule Monday 08:00 Australia/Sydney
- [ ] Tests with fixture fills

## Verification

### Tests
- Unit: worst-five selection by R-multiple with ties broken by $ loss.
- Integration: fixture week renders a report with cost ratios.

### Scenarios
- Given a week with fewer than five closed trades, then the report lists all of them and says so.
- Given TCA data missing for some fills, then those rows show 'no TCA' and are excluded from ratios (counted).

### Stress / failure injection
- n/a: weekly batch over small data.

## Acceptance criteria

- [ ] Flow scheduled and delivering
- [ ] Ratios > 1.5× highlighted
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DST transitions: schedule in Australia/Sydney timezone via Prefect cron with tz.

## Cardinal rules (do NOT)

- Do NOT include Telegram message text in the report or any model prompt.
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: report contents.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.81 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T150-weekly-worst-trades-report`
- PR title: `P2-T150: Weekly five-worst-trades and realised-vs-modelled cost report`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T150` run

## Progress log

- 2026-10-21 00:00 · planner · created
