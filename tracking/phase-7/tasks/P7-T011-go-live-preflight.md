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
depends_on: [P7-T010, P2-T033, P1-T071]
requirements: [R7.02, R7.13, R7.04, R7.14, R7.01]
roadmap_todos: [T7.60, T7.63]
modules: [M11, M17]
dashboards: [D16, D06, D03]
tools: [git, uv, pnpm, docker]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p7/P7-T011-go-live-preflight
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T011 · Go-live preflight: entry-criteria checker and runbook drill log

## Goal / expected outcome

A single preflight (`/system/preflight`, D16 card, `mt preflight` CLI) evaluates every Phase 7 entry criterion per strategy/venue and **blocks funding, live mode and capital steps** until all pass; runbook drills are recorded in a WORM drill log it reads.

## Context & references

- Roadmap: [R7.02, R7.13, R7.04 · ToDo T7.60, T7.63](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §2 entry criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (AUSTRAC re-check quarterly) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (runbooks) · [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) (paper/HITL period: ≥ 8 weeks and ≥ 50 trades; P1 ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (egress check) · [17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions) (wallet-drained drill only if a hot/burner wallet exists)
- Cross-phase: P2-T033 (modes and approval routing) and P1-T071 (`egress.status`) are `depends_on`; reads P2-T180 (paper clock), P3-T001 (tax agent) and the runbooks from P0-T060/P0-T061, P2-T068 and (only if a hot/burner wallet exists) P5-T051.
- Related: P7-T001, P7-T010, P7-T046 (VERIFY of the registry check), P7-T044/T045 (drills that write the log)

## Requirements

- Checks (each returns pass/fail + evidence link): (1) the bot's paper/HITL period meets its gate profile (16 §2.4 defaults: ≥ 8 weeks **and** ≥ 50 trades; P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency bots ≥ 26 weeks) through the real policy/risk/execution path, counted from paper/HITL fills with no gap > 24 h; (2) tax regime set for the current FY; (3) every target venue/product `allowed` with AUSTRAC `checked_at` < 90 days; (4) runbooks drilled at least once with result `pass`: kill, keys leaked, server down with open positions, bad data, and wallet drained **only if** `ops.wallets` holds a hot/burner wallet (17 §D P7-B011); (5) all `PRO_ADVICE` items answered or deferred (deferred keeps products blocked); (6) live keys audited (P7-T032) for the sub-account; (7) `egress.status = ok` on the exit-node IP (16 §3.2). Thresholds come from the effective gate profile/policy, never hard-coded.
- New WORM table `ops.drill_log(id, runbook, started_at, ended_at, result, evidence_ref, notes, chain fields)`; command `ops.drill.record` (C1).
- Enforcement hooks: `strategy.set_mode` → any live mode, `bot.set_mode` → live hitl/autonomous, `risk.capital_step.approve`, and sub-account funding confirmation all call preflight and reject with the failing check list.
- Non-functional: preflight runs in < 2 s; results cached 60 s; every evaluation written to `audit.command` context.

## ToDo

- [ ] `packages/mt_risk/preflight/` with one check class per criterion and a `Preflight.evaluate(scope)` API.
- [ ] Migration for `ops.drill_log` (WORM) and `ops.drill.record` command.
- [ ] Paper/HITL-period calculator (weeks and trades per the gate profile) reading `strategy.run`/`audit.fill` with gap detection.
- [ ] Hook preflight into the commands listed; problem+json `preflight_failed` with failing checks.
- [ ] Query `/system/preflight?strategy=&venue=`; D16 'Go-live preflight' card; D03 Gates tab shows the same rows.
- [ ] CLI `mt preflight --strategy <id>` for drills and the exit demo.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each check with pass/fail fixtures (55 vs 56 days and 49 vs 50 trades for the default profile; 26-week window for a low-frequency bot; 89 vs 91 days since AUSTRAC check; gap of 25 h resets the clock; wallet-drained drill required only when a hot/burner wallet is registered; egress `ip_mismatch` fails).
- Integration: `bot.set_mode autonomous` on a live sub-account is rejected when any check fails, accepted when all pass.
- WORM: UPDATE/DELETE on `ops.drill_log` fails for app roles.

### Scenarios
- Given trend-on-majors has 55 days of paper, when you try to fund, then preflight lists 'paper period 55/56 days'.
- Given a hot wallet is registered in `ops.wallets` and the wallet-drained runbook was never drilled, then the drills check fails naming that runbook; with no hot/burner wallet it shows `n/a`.
- Given all checks pass, when a venue's registry row flips to `read_only`, then the next evaluation fails and live-mode commands are refused.

### Stress / failure injection
- Evaluate preflight for 50 strategies × 10 venues in a loop: p95 < 2 s; DB down → preflight returns `unknown` and **blocks** (fail closed).

## Acceptance criteria

- [ ] All seven checks implemented with evidence links.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper/HITL period per the 16 §2.4 gate profile; wallet-drained drill only if a hot/burner wallet exists (P7-B011); egress check (16 §3.2); deps)
