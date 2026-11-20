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
depends_on: [P2-T102, P2-T106, P2-T029, P1-T077]
requirements: []
roadmap_todos: [T2.81]
modules: [M7, M16]
dashboards: [D04, D05]
tools: [cargo]
mcp: []
env: []
services: [supabase-postgres, supabase-storage, mt-scheduler]
branch: p2/P2-T150-weekly-worst-trades-report
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T150 · Weekly five-worst-trades and realised-vs-modelled cost report

## Goal / expected outcome

An `mt-scheduler` job (Rust, `mt_lab_core::reports::weekly`) that every Monday 08:00 AEST/AEDT produces the weekly review pack — the five worst paper trades per sleeve with context, and realised-vs-modelled cost ratios — delivered as a Telegram digest link and an HTML report stored in a private Supabase Storage bucket (18 §4.5).

## Context & references

- Roadmap: ToDo T2.81 · [14 §4 discipline/review](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (weekly review of the five worst trades) · [14 §4 execution](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (implementation shortfall per order)
- TCA per order (R2.34) is computed by part A (T2.26); this job only reads it (part A (P2-T001–T099))
- Scheduler: `mt-scheduler` (P1-T077) cron with timezone
- Scenario twin ([18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool)): when P6-T075 runs, its weekly per-bot report is linked from this pack; paper weeks before it exists simply have no twin section (no dependency)
- [D05 TCA tab](../../../docs/ui/dashboards/D05-execution.md) (realised vs modelled alert > 1.5×)

## Requirements

- Per sleeve: five worst closed paper trades by R-multiple (and by $), each with entry/exit, signal reasons, slippage vs decision/arrival, costs, chart deep link, and whether the exit plan was followed.
- Costs: realised vs modelled ratio per strategy × venue × instrument for the week and trailing 4 weeks; ratio > 1.5× highlighted.
- Delivered via `alert.info.weekly_review` (Telegram link + notification centre); HTML stored as an artefact; review notes captured via `journal.note.add` once P3 journal exists (until then a notes field on the report).
- Runs on the paper clock data (P2-T180) and stays useful into P7.

## ToDo

- [ ] Implement the `weekly-review` job in `crates/mt-lab-core/src/reports/weekly.rs`
- [ ] HTML template (`minijinja`) + deep links; optional link to the scenario-twin report when present
- [ ] Schedule Monday 08:00 Australia/Sydney
- [ ] Tests with fixture fills

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core weekly`.
- Unit: worst-five selection by R-multiple with ties broken by $ loss.
- Integration: fixture week renders a report with cost ratios.

### Scenarios
- Given a week with fewer than five closed trades, then the report lists all of them and says so.
- Given TCA data missing for some fills, then those rows show 'no TCA' and are excluded from ratios (counted).

### Stress / failure injection
- n/a: weekly batch over small data.

## Acceptance criteria

- [ ] Job scheduled and delivering
- [ ] Ratios > 1.5× highlighted
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test -p mt-lab-core`, `pit` check

## Exceptions & edge cases

- DST transitions: schedule in Australia/Sydney timezone via `mt-scheduler` cron with tz.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; reads TCA from P2-T029)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line; report in a private Supabase Storage bucket; services [postgres] → [supabase-postgres, supabase-storage])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Prefect flow (Python, `mt_lab`) → `mt-scheduler` job in `mt-lab-core` (Rust, `minijinja`); scenario-twin report linked when present (no dependency); depends_on + P1-T077; same tests; tools [uv] → [cargo]; services + mt-scheduler)
