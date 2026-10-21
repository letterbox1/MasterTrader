---
id: P7-T014
kind: task
title: Gate report: rendering, WORM storage, API and D03 Gates tab
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T012, P7-T013]
requirements: [R7.01, R7.02]
roadmap_todos: [T7.20]
modules: [M0, M15, M17]
dashboards: [D03]
branch: p7/P7-T014-gate-report-render-and-store
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md, docs/02-v1-architecture.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T014 · Gate report: rendering, WORM storage, API and D03 Gates tab

## Goal / expected outcome

Each evaluation is stored as an immutable `strategy.gate_report` row (WORM, hash-chained) with a rendered HTML/PDF report, served at `/strategies/{id}/gate-report` and shown in D03 → Gates, and every promotion references the report id it relied on.

## Context & references

- Roadmap: [R7.01, R7.02 · ToDo T7.20](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [D03](../../../docs/ui/dashboards/D03-strategies.md) (Gates tab, 'auto mode disabled until all gates pass') · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (WORM) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (commands)
- Related: P7-T012, P7-T013, P7-T028 (bot promotion checks the latest passing report), P7-T057 (funding needs a passing report)

## Requirements

- Command `lab.gate_report.generate {strategy_version}` (C1); scheduled nightly for every strategy in paper/hitl/autonomous.
- Row: version, verdict, gate results JSON, inputs hash, report artefact hash; artefact stored in MLflow artefacts + immutable export.
- Report sections: summary verdict; each gate with value/threshold/evidence link; per-year/per-regime table; 2×/3× cost table; trial counter; worst fold; benchmark comparison; paper section; waivers; kill criteria from the manifest.
- `strategy.promote`, `strategy.set_mode`, `bot.set_mode` (live) store `gate_report_id` in their audit context and refuse if the latest report is not `pass` or is older than 7 days.
- D03 Gates tab lists the latest report, history, and a 'Download PDF' action; phones get the summary card.

## ToDo

- [ ] Migration `strategy.gate_report` (WORM).
- [ ] Renderer (Jinja → HTML; WeasyPrint → PDF, licence-clean) in `packages/mt_lab/gates/render.py`.
- [ ] API query + command; nightly Prefect flow.
- [ ] D03 Gates tab component consuming `/strategies/{id}/gate-report` (+ viewport matrix).
- [ ] Hook report id into promotion/mode commands.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: renderer snapshot (HTML) for pass and fail fixtures.
- Integration: promotion refused with a stale (8-day-old) report; accepted with a fresh passing one; audit row carries `gate_report_id`.
- WORM: report rows cannot be updated; regenerated report is a new row.
- Playwright: Gates tab passes the DESIGN.md §6.8 matrix + axe.

### Scenarios
- Given a failing gate, when you open D03 Gates on a phone, then the failing gate is first with its value and threshold.
- Given a report passed last week but a new trial was run, when nightly regeneration fails a gate, then autonomous mode is disabled for new promotions (existing bots handled by P7-T029).

### Stress / failure injection
- Generate 50 reports concurrently: < 5 min; PDF renderer crash → HTML still stored and verdict unaffected.

## Acceptance criteria

- [ ] Reports stored as WORM rows with artefact hashes.
- [ ] Promotions and live-mode changes reference a passing report ≤ 7 days old.
- [ ] D03 Gates tab live; viewport matrix green.
- [ ] CI green.

## Exceptions & edge cases

- Report artefact store unavailable: verdict row still written; artefact retried; promotion allowed only when the artefact exists.
- Strategy archived: reports retained ≥ 7 years.

## Cardinal rules (do NOT)

- Do NOT allow editing a report; regenerate as a new row.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: Gates tab report history + PDF.
- `docs/02-v1-architecture.md` §7: `/strategies/{id}/gate-report`, `lab.gate_report.generate`.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.20 when this item is done.

## Branch & PR

- Branch: `p7/P7-T014-gate-report-render-and-store`
- PR title: `P7-T014: Gate report: rendering, WORM storage, API and D03 Gates tab`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
