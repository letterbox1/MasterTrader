---
id: P2-T035
kind: task
title: Telegram v1 commands, C3 TOTP prompt and /kill NATS fallback
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T020, P2-T031]
requirements: [R2.52, R2.51, R2.19]
roadmap_todos: [T2.33]
modules: [M15]
dashboards: []
branch: p2/P2-T035-telegram-v1-commands-c3
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T035 · Telegram v1 commands, C3 TOTP prompt and /kill NATS fallback

## Goal / expected outcome

The `telegram-bot` service (alerts-only since P1) gains `/kill` (confirm button), `/status`, `/pnl`, `/positions`, `/pause <strategy>`, `/resume <strategy>` and the C3 confirmation flow (Approve → TOTP → cool-down → Applied); `/kill` keeps working when `mt-api` is down by publishing `kill.set` straight to NATS.

## Context & references

- Roadmap: [R2.52, R2.51](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.33
- Spec: [03 M15 Telegram bot](../../../docs/03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api) · [mob §3 Telegram bot](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [mob §4 acceptance](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria)
- Degraded: [02 §9.3 mt-api down](../../../docs/02-v1-architecture.md#93-degraded-modes) · API: [02 §7.4 Telegram](../../../docs/02-v1-architecture.md#7-api-contract-mt_api)
- Cross-phase: bot token + user id (P0 T0.06), alerts consumer (P1 T1.31), TOTP verification in mt_api (P0 T0.24).
- Related: P2-B012 (audit path for NATS-direct kill), P2-T039/T040 bot commands, P2-T059 degraded test.

## Requirements

- Bound to your Telegram user id only; any other user id → ignored + `alert.warning.telegram_foreign_user` (no reply).
- All commands call `mt_api` with a scoped token (commands: `risk.kill.on`, `strategy.pause|resume`, approvals, C3 confirm) and source `telegram`.
- `/kill`: shows a confirm button; on tap → `risk.kill.on` via mt_api; if mt_api fails/times out in 300 ms → publish `kill.set` on NATS with a signed payload (NATS account `telegram` may publish only `kill.set` and `audit.telegram.*`) and write an `audit.telegram.kill` event to JetStream for later ingestion into `audit.command`.
- Kill latency: confirm tap → KV ON < 300 ms on the NATS path, and all cancels < 1 s end to end.
- C3 flow: message 'Approve risk change: raise BTC max position 0.5 → 0.8?' → Approve → bot asks for TOTP → mt_api verifies → 'Cool-down 15:00' message edited each minute → 'Applied' (or 'Cancelled').
- `/status`: trading allowed Y/N, kill, ladder rung, modes, DQ-paused instruments; `/pnl`: today/30d per sleeve; `/positions`: open positions (compact).
- No message text received by the bot is stored beyond the command parse (and never fed to any model).

## ToDo

- [ ] Command handlers in `packages/mt_ui/telegram/commands/`
- [ ] Scoped token + NATS account config
- [ ] C3 conversation state machine (TOTP prompt with 120 s timeout)
- [ ] Audit ingestion of `audit.telegram.*` when mt-api returns
- [ ] Tests (python-telegram-bot test harness with fake Bot API)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: foreign user id ignored.
- Integration: `/kill` with mt-api up → command audited; with mt-api stopped → KV `kill=ON` via NATS and later ingested into `audit.command`.
- Flow test: C3 approve with wrong TOTP rejected; right TOTP → cool-down → applied.

### Scenarios
- Given mt-api is down, when you send `/kill` and tap confirm, then the engine halts within 1 s and the bot replies 'Halted (via NATS)'.
- Given a pending loosen, when you tap Approve and enter the TOTP, then the bot shows the cool-down and 'Applied' when it ends.

### Stress / failure injection
- Telegram API latency injected 2 s: kill confirm still publishes immediately (handler doesn't wait on outbound message edits).

## Acceptance criteria

- [ ] All v1 commands work against paper
- [ ] `/kill` works with mt-api down
- [ ] C3 completes end to end on a phone
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Telegram API outage: kill via web HALT and ntfy-linked web route remain; C3 loosenings can't complete (by design).
- Duplicate button taps: idempotency key per card.

## Cardinal rules (do NOT)

- Do NOT accept commands from any user id but yours.
- Do NOT store or forward Telegram message text to any model or index.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.
- No Telegram text in any model, RAG index or training set (12 §4–5).

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §3: NATS fallback details.
- `docs/02-v1-architecture.md` §7.4: Telegram NATS permissions.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.33 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T035-telegram-v1-commands-c3`
- PR title: `P2-T035: Telegram v1 commands, C3 TOTP prompt and /kill NATS fallback`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
