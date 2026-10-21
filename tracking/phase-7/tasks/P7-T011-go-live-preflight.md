---
id: P7-T011
kind: task
title: Go-live preflight: entry-criteria checker and runbook drill log
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T010]
requirements: [R7.02, R7.13, R7.04]
roadmap_todos: [T7.60, T7.63]
modules: [M11, M17]
dashboards: [D16, D06, D03]
branch: p7/P7-T011-go-live-preflight
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T011 · Go-live preflight: entry-criteria checker and runbook drill log

## Goal / expected outcome

A single preflight (`/system/preflight`, D16 card, `mt preflight` CLI) evaluates every Phase 7 entry criterion per strategy/venue and **blocks funding, live mode and capital steps** until all pass; runbook drills are recorded in a WORM drill log it reads.

## Context & references

- Roadmap: [R7.02, R7.13, R7.04 · ToDo T7.60, T7.63](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §2 entry criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (AUSTRAC re-check quarterly) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (runbooks) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) item 7 (paper ≥ 8 weeks P1)
- Cross-phase: P2 T2.80 (paper clock start), P3 T3.01 (tax agent), P0/P1/P2/P5 runbooks (T0.90, T2.90, T5.90).
- Related: P7-T001, P7-T010, P7-T046 (VERIFY of the registry check), P7-T044/T045 (drills that write the log)

## Requirements

- Checks (each returns pass/fail + evidence link): (1) each P1 sleeve has ≥ 8 weeks (56 days) of paper through the real policy/risk/execution path, counted from `strategy.run` mode=paper rows with no gap > 24 h; (2) tax regime set for the current FY; (3) every target venue/product `allowed` with AUSTRAC `checked_at` < 90 days; (4) each runbook (kill, keys leaked, server down with open positions, bad data, wallet drained) drilled at least once with result `pass`; (5) all `PRO_ADVICE` items answered or deferred (deferred keeps products blocked); (6) live keys audited (P7-T032) for the sub-account.
- New WORM table `ops.drill_log(id, runbook, started_at, ended_at, result, evidence_ref, notes, chain fields)`; command `ops.drill.record` (C1).
- Enforcement hooks: `strategy.set_mode` → any live mode, `bot.set_mode` → live hitl/autonomous, `risk.capital_step.approve`, and sub-account funding confirmation all call preflight and reject with the failing check list.
- Non-functional: preflight runs in < 2 s; results cached 60 s; every evaluation written to `audit.command` context.

## ToDo

- [ ] `packages/mt_risk/preflight/` with one check class per criterion and a `Preflight.evaluate(scope)` API.
- [ ] Migration for `ops.drill_log` (WORM) and `ops.drill.record` command.
- [ ] Paper-period calculator reading `strategy.run`/`audit.fill` (paper) with gap detection.
- [ ] Hook preflight into the commands listed; problem+json `preflight_failed` with failing checks.
- [ ] Query `/system/preflight?strategy=&venue=`; D16 'Go-live preflight' card; D03 Gates tab shows the same rows.
- [ ] CLI `mt preflight --strategy <id>` for drills and the exit demo.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each check with pass/fail fixtures (55 vs 56 days; 89 vs 91 days since AUSTRAC check; gap of 25 h resets the clock).
- Integration: `bot.set_mode autonomous` on a live sub-account is rejected when any check fails, accepted when all pass.
- WORM: UPDATE/DELETE on `ops.drill_log` fails for app roles.

### Scenarios
- Given trend-on-majors has 55 days of paper, when you try to fund, then preflight lists 'paper period 55/56 days'.
- Given the wallet-drained runbook was never drilled, then the drills check fails naming that runbook.
- Given all checks pass, when a venue's registry row flips to `read_only`, then the next evaluation fails and live-mode commands are refused.

### Stress / failure injection
- Evaluate preflight for 50 strategies × 10 venues in a loop: p95 < 2 s; DB down → preflight returns `unknown` and **blocks** (fail closed).

## Acceptance criteria

- [ ] All six checks implemented with evidence links.
- [ ] Live-mode, funding and capital-step commands are refused when preflight fails.
- [ ] `ops.drill_log` is WORM and readable in D16.
- [ ] CI green.

## Exceptions & edge cases

- Clock skew/timezone: paper days are counted in UTC from fill timestamps (`clock_timestamp()`), not wall clock.
- Strategy version changes during paper: a new version restarts its own clock unless the change is parameter-only and marked `non_material` (default: restart).
- Postgres down: fail closed (no live enablement).

## Cardinal rules (do NOT)

- Do NOT add a bypass flag or 'force' option to preflight.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: add `/system/preflight`, `ops.drill.record`.
- `docs/ui/dashboards/D16-system.md`: preflight card.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.60, T7.63 when this item is done.

## Branch & PR

- Branch: `p7/P7-T011-go-live-preflight`
- PR title: `P7-T011: Go-live preflight: entry-criteria checker and runbook drill log`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
