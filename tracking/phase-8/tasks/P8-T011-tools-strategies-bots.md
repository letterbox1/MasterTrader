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
depends_on: [P8-T003, P8-T004, P8-T005, P8-T006, P8-T007, P2-T006, P2-T036, P2-T037, P2-T117]
requirements: [R8.03, R8.05]
roadmap_todos: [T8.20]
modules: [M0, M7, M11, M20]
dashboards: [D03, D04, D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats, mlflow]
branch: p8/P8-T011-tools-strategies-bots
pr: ""
doc_sync: [docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T011 · Strategies & bots tool group

## Goal / expected outcome

Claude can create and edit strategies and bots, run backtests/sweeps/validation, promote/demote and pause/resume, using the same `strategy.*`, `bot.*` and `lab.*` commands as the UI and Telegram, under the `strategy` scope. Gates still apply. C2 commands create your approval card; anything C3 (switching a bot to `autonomous`, allowing autonomous on a strategy, loosening bot parameters, scope or approval policy) goes through Telegram + TOTP + cool-down. Tested on the sandbox and paper venues.

## Context & references

- Roadmap: [R8.03, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §B P2-B053/P7-B009](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (modes `paper`/`hitl`/`autonomous` per bot) · [17 §B P2-B005](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (paper → hitl is C2) · [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (L4 bot: tighten C1, loosen C3) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (strategy mode ceiling, C3 cool-down 15 min) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (`strategy` scope; creating it is C3)
- Spec: [03 M20 Strategies row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2 Strategies, Bots, Lab rows](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F7](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Bots: [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui) ("MCP (Phase 8): bot commands within each token's scopes … autonomous and any other loosening stays C3")
- Cross-phase (depends_on): P2-T006 (strategy registry + commands), P2-T036 (bot model + lifecycle commands), P2-T037 (bot modes, approval policy), P2-T117 (lab commands).

## Requirements

- Levels follow 02 §7.2; for `source = mcp`: C1 runs with the `strategy` scope, C2 creates your approval card (TTL default 5 min), C3 runs the Telegram + TOTP + cool-down flow.
- Strategies (scope `strategy`, default disabled): `strategy.create` (C1, never-build validator runs), `strategy.update_params` (C1 paper; C2 live; C3 if it increases risk), `strategy.clone`, `strategy.archive`, `strategy.start`, `strategy.pause/resume/stop` (C1), `strategy.promote` (C1; autonomous stage C3), `strategy.demote` (C1), `strategy.set_mode` (restrict C1, allow `hitl` C2, allow `autonomous` C3).
- Bots: `bot.create` (C1), `bot.update_scope` / `bot.update_params` (tighten C1; loosen C3, incl. widening an autonomous bot's scope and `on_system_failure`), `bot.set_mode` (`paper` C1, `paper` → `hitl` C2, `autonomous` → `hitl` C1, → `autonomous` C3), `bot.start/pause/resume/stop` (C1), `bot.approval_policy.set` (tighten C1, loosen C3).
- Lab: `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.job.cancel` (C1; results via read tools). Disabled by default: `lab.generate_strategy` (uses LLM budget). Not exposed: `lab.leakage.waive` (C2, needs your reasoned waiver in the UI).
- Risk overrides on bots are tighter-only (15 §1.1); a looser override goes the C3 route, never silently.
- Tool descriptions state the level and that C3 needs your Telegram + TOTP and a cool-down (default 15 min).
- Commands count as writes (default 10 writes/min per token, P8-T030).

## ToDo

- [ ] Add the registry entries (scope `strategy`, default disabled) with levels and regenerate the snapshot.
- [ ] Integration tests through the full stack (sandbox + paper, fake Telegram + TOTP harness, injected clock).
- [ ] Update docs.

## Verification

### Tests
- Golden: each command via MCP → expected level/outcome (C1 immediate, C2 card, C3 pending with cool-down).
- Integration: `bot.create` (Trend v3 on gold, `hitl`) → C1 draft bot; `bot.set_mode autonomous` → C3 pending; approve + TOTP → applied after the cool-down only if the gates pass.
- Integration: `bot.set_mode paper → hitl` → approval card.
- Integration: promote a strategy that fails a gate → rejected with gate reasons.
- Integration: `strategy.create` with a never-build pattern (e.g. sniping) → rejected by the validator.

### Scenarios
- Given an autonomous bot, when Claude sets it to `hitl`, then the change applies immediately (tightening, C1).
- Given Claude asks to widen an autonomous bot to "top-20 perps", then the change waits for C3.
- Given Claude runs a sweep, when it finishes, then results are readable with `get_lab_backtests` and the MLflow run id.

### Stress / failure injection
- 20 backtests requested via MCP in 1 min → writes beyond 10/min get 429; admitted ones queued by the lab worker; engine latency unaffected.

## Acceptance criteria

- [ ] Strategies, bots and lab commands exposed one-to-one under the `strategy` scope with 02 §7.2 levels
- [ ] Autonomous mode and every loosening are C3 via MCP; C2 commands create your card
- [ ] Gate and validator rejections surface to Claude with reasons
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Auto-downgrade of an autonomous bot (decay, DQ, ladder) while a C3 upgrade is in cool-down: the upgrade is cancelled and audited.
- Sandbox down: `lab.*` returns 503; nothing is run outside the sandbox.
- Concurrent edits from web and MCP: version rows (`strategy.bot_version`) keep both; stale version → 409.

## Cardinal rules (do NOT)

- Do NOT let MCP shortcut autonomous mode or any loosening (always C3 via Telegram + TOTP + cool-down).
- Do NOT use the retired mode names "approve"/"auto"; modes are `paper`/`hitl`/`autonomous`.
- Do NOT run generated code outside the sandbox.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`strategy` scope, modes `paper`/`hitl`/`autonomous`, paper → hitl C2 → card, bot param/scope loosening C3 per 02 §7.2, 10 writes/min; cross-phase deps P2-T006/T036/T037/T117; tools/env/services)
