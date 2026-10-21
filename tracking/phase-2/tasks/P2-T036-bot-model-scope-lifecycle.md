---
id: P2-T036
kind: task
title: Trading bot model, scope resolver and bot lifecycle commands
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T006, P2-T010, P2-T019]
requirements: [R2.53]
roadmap_todos: [T2.34]
modules: [M0, M11, M15]
dashboards: [D03]
branch: p2/P2-T036-bot-model-scope-lifecycle
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T036 · Trading bot model, scope resolver and bot lifecycle commands

## Goal / expected outcome

A bot = one pinned strategy version × market scope (single instrument, explicit list or dynamic selection) × venue/sub-account × sleeve × mode × approval policy, stored in `strategy.bot` + WORM `strategy.bot_version`, managed by `bot.create|update_scope|update_params|start|pause|resume|stop`, with tighter-only risk overrides.

## Context & references

- Roadmap: [R2.53](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.34
- Design: [15 §1.1 what a bot is](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.5 API, data, UI](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)
- API: [02 §7.2 bot commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Related: P2-T037 modes/policy, P2-T041 Bots tab, P2-T061 scenarios.

## Requirements

- `strategy.bot(id, name, status draft|running|paused|stopped|halted, current_version_id)`; `strategy.bot_version(id, bot_id, strategy_version_id, scope jsonb, venue, account, sleeve, timeframes, schedule, param_overrides, risk_overrides, mode, approval_policy, created_at, created_by, supersedes_id)` — every change is a new row (WORM).
- Scope resolver: `single` | `list` | `dynamic(rule, max_concurrent)`; rules e.g. 'top-20 liquid USDT spot on allowed venues', 'FX majors', 'US sector ETFs'; filters by venue registry `allowed` and instrument min resolution; re-evaluated on schedule (default hourly) with membership diff logged; never more than `max_concurrent` instruments.
- Param overrides validated against the strategy's param schema; risk overrides validated **tighter-only** against the effective policy via P2-T019 classifier (looser → rejected, not C3).
- Commands: `bot.create` (C1, starts `draft`), `bot.update_scope` / `bot.update_params` (C1; widening an autonomous bot's scope C3), `bot.start|pause|resume|stop` (C1).
- Queries `/bots`, `/bots/{id}`; NATS `bot.{id}.status`; engine instantiates one strategy instance per bot (strategy id + bot id tagged on every intent).
- Two bots on the same strategy are isolated (own state, positions attribution, sleeve, mode).

## ToDo

- [ ] Migrations (register `strategy.bot_version` with WORM)
- [ ] `packages/mt_strategy/bots/` model, resolver, service
- [ ] mt_api routers + commands
- [ ] Engine bot loader
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: scope resolver for each kind; registry filter; max_concurrent.
- Unit: looser risk override rejected; tighter accepted.
- Integration: two bots on one strategy version, different instruments/modes → separate intents tagged with bot ids.
- WORM: UPDATE on `strategy.bot_version` fails.

### Scenarios
- Given 'Trend v3 on BTC/ETH: autonomous' and 'Trend v3 on gold: HITL', when both run, then BTC orders submit directly and gold orders produce approval cards.
- Given a dynamic bot's rule now selects a newly listed instrument, when the resolver runs, then the instrument is added and (if escalation 'new instruments' is on) its first order needs approval.

### Stress / failure injection
- Dynamic bot over a 300-instrument universe re-evaluated every minute for 1 h: resolver < 2 s per run; no instrument churn beyond rule changes.

## Acceptance criteria

- [ ] Bot entities, versions (WORM) and lifecycle commands live
- [ ] Tighter-only overrides enforced
- [ ] Bots isolated in the engine
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Strategy version archived: bot keeps running its pinned version; new bots can't pick it.
- Resolver data stale: keep last membership, alert.

## Cardinal rules (do NOT)

- Do NOT allow a bot override to loosen risk.
- Do NOT mutate a bot version row.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1.5: tables and resolver rules as built.
- `docs/02-v1-architecture.md` §7: bot endpoints.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T036-bot-model-scope-lifecycle`
- PR title: `P2-T036: Trading bot model, scope resolver and bot lifecycle commands`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
