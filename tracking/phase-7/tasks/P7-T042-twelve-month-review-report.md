---
id: P7-T042
kind: task
title: 12-month review report generator
phase: 7
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T020, P7-T014]
requirements: [R7.05]
roadmap_todos: [T7.10, T7.82]
modules: [M11, M18, M7]
dashboards: [D03, D14]
branch: p7/P7-T042-twelve-month-review-report
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T042 · 12-month review report generator

## Goal / expected outcome

A report (`lab.review12m.generate`) evaluates each live sleeve against the pre-committed 12-month keep criteria and proposes keep/retire per sleeve, so the review (P7-T063) is evidence-driven.

## Context & references

- Roadmap: [R7.05 · ToDo T7.10, T7.82](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (12-month review: keep only sleeves with positive live net P&L, live Sharpe > 0.5 over 12 months, and beating the benchmark) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (benchmark rule; capital of failing strategies to hold-and-earn)
- Related: P7-T062 (clock), P7-T063 (your review), gap P7-B012

## Requirements

- Per sleeve over its live window (target 12 months; report shows actual length): net P&L after all costs (journal), annualised Sharpe of daily returns, benchmark return over the same dates, kill/decay events, capital-step history.
- Proposal: `keep` only if all three criteria pass; else `retire` (capital to hold-and-earn task).
- Generatable any time (interim) but marked 'interim' before 365 days.
- Stored WORM with artefact; linked from D03 and D14.

## ToDo

- [ ] Report builder in `packages/mt_lab/reviews/twelve_month.py`.
- [ ] Command + WORM table `strategy.review_12m`.
- [ ] Tests; docs.

## Verification

### Tests
- Golden: fixture sleeve with Sharpe 0.49 → retire; 0.51 + positive P&L + beats benchmark → keep.

### Scenarios
- Given an interim run at month 6, then the report is labelled interim and makes no proposal.

### Stress / failure injection
- n/a: monthly/annual batch job.

## Acceptance criteria

- [ ] Report produces correct keep/retire proposals on fixtures.
- [ ] CI green.

## Exceptions & edge cases

- Sleeve live < 12 months at programme review: interim only.
- Benchmark data gap: criterion `unknown` → proposal `retire` (fail closed).

## Cardinal rules (do NOT)

- Do NOT change keep criteria after the live clock starts except tighter (C1).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: link the 12-month report.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.10, T7.82 when this item is done.

## Branch & PR

- Branch: `p7/P7-T042-twelve-month-review-report`
- PR title: `P7-T042: 12-month review report generator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
