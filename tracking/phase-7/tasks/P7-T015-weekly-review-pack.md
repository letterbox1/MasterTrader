---
id: P7-T015
kind: task
title: Weekly review pack generator
phase: 7
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T013, P2-T150, P3-T034, P6-T075, P6-T080]
requirements: [R7.03]
roadmap_todos: [T7.05]
modules: [M16, M18, M7]
dashboards: [D14, D07]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, nats, telegram bot api]
branch: p7/P7-T015-weekly-review-pack
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/ui/dashboards/D14-journal.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T015 · Weekly review pack generator

## Goal / expected outcome

Every Monday 07:00 Australia/Sydney a weekly review pack is generated per strategy and for the portfolio, covering the five R7.03 sections, so the 30–45 minute review (P7-T060) needs no manual data gathering. Once the scenario twin runs (P6-T075), the pack also carries its weekly report per bot, labelled Simulated and informational only.

## Context & references

- Reading: llm-trading-lab's forward-only experiment record and evaluation paper, for how to judge LLM-made decisions in weekly reviews (no licence: reading only, no code) ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).
- Roadmap: [R7.03 · ToDo T7.05](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [04 Phase 7](../../../docs/04-plan-of-action.md#phase-7--prove-it-then-go-small-live-months-710) (weekly review items) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (five worst trades weekly) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (time budget) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor-always-on-autonomous) (TCA, DQ) · [D14](../../../docs/ui/dashboards/D14-journal.md) · [D07](../../../docs/ui/dashboards/D07-data-quality.md)
- Cross-phase (`depends_on`): P2-T150 (weekly five-worst and realised-vs-modelled cost report this extends), P3-T034 (journal ↔ venue recon).
- Related: P7-T013 (tracking metrics), P7-T016 (sign-off), P7-T025 (recon)
- Scenario twin: P6-T075 (R6.33) produces the weekly per-bot report from `mt-crowdsim` scenarios ([18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)); it is an extra input, not a gate (16 §2.14b sets no gate)

## Requirements

- Sections: (1) paper/live vs backtest tracking error for the week and since start; (2) realised vs modelled costs per strategy × venue × instrument (ratio, delay/spread-impact/fees breakdown); (3) DQ incidents from `audit.dq_event` touching traded instruments; (4) journal reconciliation status (open breaks, explained/unexplained); (5) five worst trades by R-multiple with provenance links.
- (6) **Scenario-twin report per bot** (R7.03, R6.33) when one exists for the week: each bot's behaviour under the week's simulated shocks (default 3 scenarios, `crowdsim.scenarios_per_week`), read from P6-T075's stored report, labelled **Simulated** (`synthetic = true`). Informational only: it never changes a gate, a clean week, a capital step or a kill criterion; weeks with no twin report say "no scenario-twin report this week".
- Also: capital-step state and clean-week status per bot/sleeve against the [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) definition (from P7-T018), kill-criteria/decay warnings, approvals expired count.
- Stored as `journal.weekly_review_pack` (WORM) with an HTML artefact; Telegram digest with a deep link to D14 → Reviews.
- Generation < 2 min; uses only PIT reads.

## ToDo

- [ ] Scheduled job `weekly_review_pack` in `mt-journal` (cron `0 7 * * MON`, tz Australia/Sydney).
- [ ] Section builders in `crates/mt-journal/src/review/` (paper-tracking figures read from P7-T013's stored rows).
- [ ] SQL migration (`supabase/migrations/`) `journal.weekly_review_pack`.
- [ ] Section (6) builder reading the P6-T075 twin report (labelled Simulated; absent → a one-line note).
- [ ] Telegram digest template (no free text from Telegram sources).
- [ ] Tests; docs.

## Verification

### Tests
- `cargo test -p mt-journal review` and `cargo clippy`; `supabase test db`.
- Golden: fixture week produces the expected five sections (numbers match fixture fills/fees).
- Golden: fixture week with a twin report adds section (6) labelled Simulated; the same week without one shows the "no scenario-twin report" note; clean-week and capital-step figures are identical in both (the twin never feeds them).
- Unit: five-worst ordering by R; ties broken by absolute loss.
- Integration: digest message sent with a working deep link.

### Scenarios
- Given no live trades this week, then the pack still generates with paper data and 'no live trades' noted.
- Given an unexplained recon break, then section 4 shows it first in red and links to D07.

### Stress / failure injection
- Generate for 30 strategies with 10k fills/week: < 2 min; journal DB slow → retry ×3 then alert, never a partial pack marked complete.

## Acceptance criteria

- [ ] Pack generated weekly with all five sections plus step/kill status, and the scenario-twin section (labelled Simulated) when a twin report exists.
- [ ] Digest delivered to Telegram with deep link.
- [ ] CI green.

## Exceptions & edge cases

- DST transitions in Sydney: cron is timezone-aware; week = Mon 00:00–Sun 23:59 Australia/Sydney.
- Generation failure: alert `alert.warning.review_pack` and retry hourly.

## Cardinal rules (do NOT)

- Do NOT include Telegram-derived text in the pack or send pack content to any model.
- Do NOT let simulated (`synthetic = true`) results count toward any gate, clean week, capital step or kill criterion, or feed features, training or RAG (18 §2.4).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT put Telegram text into any model, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: weekly review content.
- `docs/ui/dashboards/D14-journal.md`: Reviews tab source.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.05 when this item is done.

## Branch & PR

- Branch: `p7/P7-T015-weekly-review-pack`
- PR title: `P7-T015: Weekly review pack generator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (clean-week status per 16 §2.5; deps on P2-T150/P3-T034)
- 2026-11-19 00:00 · coordinator · llm-trading-lab added as reading for weekly reviews (17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (review-pack builders in the Rust `mt-journal` crate as a scheduled job (no Prefect); SQL migration in `supabase/`; tools cargo/supabase)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (R7.03: section (6) scenario-twin report per bot from P6-T075 (+dep), labelled Simulated, informational, not a gate (16 §2.14b))
- 2026-11-20 00:00 · main · depends on P6-T080 (scenario simulator / weekly twin run) per 17 §H.
