---
id: P8-T011
kind: task
title: Strategies & bots tool group
phase: 8
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T005, P8-T006, P8-T007]
requirements: [R8.03, R8.05]
roadmap_todos: [T8.20]
modules: [M0, M7, M11, M20]
dashboards: [D03, D04, D17]
branch: p8/P8-T011-tools-strategies-bots
pr: ""
doc_sync: [docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T011 · Strategies & bots tool group

## Goal / expected outcome

Claude can create and edit strategies and bots, run backtests/sweeps/validation, promote/demote and pause/resume. It uses the same `strategy.*`, `bot.*` and `lab.*` commands as the UI and Telegram. Gates still apply, and anything that makes a strategy or bot autonomous (or loosens a bot's approval policy) stays **C3**.

## Context & references

- Roadmap: [R8.03, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Strategies row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2 Strategies, Bots, Lab groups](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F7 lifecycle](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Bots: [15 §1.2 modes](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui) ("MCP (Phase 8): the same commands. Autonomous is still C3")
- Cross-phase: P2 R2.04–R2.06 (manifest, never-build validator, lifecycle gates), R2.53 / R2.54 / T2.34 (bots, HITL), R2.40–R2.44 (lab).

## Requirements

- Strategies (group `strategies`, default disabled): `strategy.create` (C1, never-build validator runs), `strategy.update_params` (C1, within the parameter schema), `strategy.clone`, `strategy.archive`, `strategy.pause/resume/stop` (C1), `strategy.start` (C2 when live in approve mode), `strategy.promote/demote` (gates apply; promotion to `auto` = C3), `strategy.set_mode` (paper/hitl C1, autonomous C3).
- Bots: `bot.create` (C1), `bot.update_scope` / `bot.update_params` (C1; widening an autonomous bot's scope = C3), `bot.set_mode` (paper/hitl C1, autonomous **C3**), `bot.start/pause/resume/stop` (C1), `bot.approval_policy.set` (tighten C1, loosen C3).
- Lab: `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.job.cancel` (C1; results via read tools).
- Disabled by default (enable only via D17): `lab.generate_strategy` (outside the M20 scope list).
- Risk overrides on bots are tighter-only (15 §1.1); a looser override is rejected, not escalated.
- Tool descriptions state the level and that C3 needs your Telegram + TOTP and a 15-min cool-down.

## ToDo

- [ ] Add the registry entries (group `strategies`) with levels and regenerate the snapshot.
- [ ] Integration tests through the full stack (sandbox + paper).
- [ ] Update docs.

## Verification

### Tests
- Golden: each command via MCP → expected level/outcome (C1 immediate, C2 approval, C3 pending with cool-down).
- Integration: `bot.create` (Trend v3 on gold, hitl) → draft bot; `bot.set_mode autonomous` → C3 pending; approve + TOTP → applied after cool-down only if the gates pass.
- Integration: promote a strategy that fails a gate → rejected with gate reasons.
- Integration: `strategy.create` with a never-build pattern (e.g. sniping) → rejected by the validator.

### Scenarios
- Given an autonomous bot, when Claude sets it to hitl, then the change applies immediately (tightening).
- Given Claude asks to widen an autonomous bot to "top-20 perps", then the change waits for C3.
- Given Claude runs a sweep, when it finishes, then results are readable with `get_lab_backtests` and the MLflow run id.

### Stress / failure injection
- 20 backtests queued via MCP in 1 min → rate limited (10/min) and queued by the lab worker; engine latency unaffected.

## Acceptance criteria

- [ ] Strategies, bots and lab commands exposed one-to-one with correct levels
- [ ] Autonomous mode and approval-policy loosening are C3 via MCP
- [ ] Gate and validator rejections surface to Claude with reasons
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Auto-downgrade of an autonomous bot (decay, DQ, ladder) while a C3 upgrade is in cool-down: the upgrade is cancelled and audited.
- Sandbox down: `lab.*` returns 503; nothing is run outside the sandbox.
- Concurrent edits from web and MCP: version rows (`strategy.bot_version`) keep both; the last write wins with a version check (409 on stale version).

## Cardinal rules (do NOT)

- Do NOT let MCP policy or auto rules shortcut autonomous mode, promotion to auto or approval-policy loosening (always C3).
- Do NOT run generated code outside the sandbox.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/03-build-spec.md` M20: strategies/bots tool list.
- `docs/15-bots-hitl-and-worm-audit.md` §1.5: MCP mapping confirmed.
- `docs/ui/dashboards/D17-mcp-console.md`: Strategies group.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T011-tools-strategies-bots`
- PR title: `P8-T011: Strategies & bots tool group`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
