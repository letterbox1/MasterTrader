---
id: P2-T031
kind: task
title: "Kill switch: KV state, manual and automatic triggers, cancel/flatten actions"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T021, P0-T035, P1-T004]
requirements: [R2.18, R2.N1]
roadmap_todos: [T2.23]
modules: [M11, M12]
dashboards: [D06, D01]
tools: [uv]
mcp: []
env: []
services: [nats]
branch: p2/P2-T031-kill-switch
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T031 · Kill switch: KV state, manual and automatic triggers, cancel/flatten actions

## Goal / expected outcome

A global and per-sleeve kill switch lives in NATS KV `kill`; it can be set from any client (web HALT, Telegram `/kill`, later MCP) and by the automatic triggers (system drawdown stage 2, unexplained reconciliation mismatch), and the engine stops new trading, cancels all open orders within 1 s, applies each bot's `on_system_failure` policy, freezes new treasury/earn moves (no vault sweep in P2), and blocks new orders until a C3 turn-off with the cause cleared.

## Context & references

- Roadmap: [R2.18, R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.23
- Flow: [02 F6 kill & dead-man](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · Spec: [03 M11 kill switch](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- SLO: [02 §9.2 kill → all cancels < 1 s](../../../docs/02-v1-architecture.md#92-observability--slos) · [mob §4 /kill within 1 s](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria)
- Decisions: [17 §B P2-B010](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (kill actions; no sweep in P2) · [17 §D P2-B012](../../../docs/17-decisions-register.md#d-other-decisions) (Telegram NATS credentials limited to `kill.set`; the engine writes the WORM kill event with source `telegram`) · [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) (`on_system_failure` per bot, default `flatten`) · triggers per [03 M11 kill switch](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp).
- Cross-phase (`depends_on`): kill confirmation level (single confirm, never blocked) in the P0 confirmation engine (P0-T035); NATS accounts/streams (P1-T004).
- Related: P2-T035 Telegram `/kill` NATS path, P2-T054 drill, P2-T018 ladder rung 6; P5 R5.07 adds the hot-wallet sweep.

## Requirements

- KV `kill` value `{state: ON|OFF, scope: global|sleeve:<id>, source, reason, ts, cause_ref}`; `kill.set` subject accepted from mt-api, telegram-bot and monitor NATS accounts only.
- Commands: `risk.kill.on` (Kill level: single confirm, never blocked), `risk.kill.off` (C3 + cause cleared check).
- Automatic triggers (03 M11, 16 §2.1/§2.9): **system drawdown stage 2** (default 25% → flatten + 30-day lock) and an **unexplained reconciliation mismatch** (not matched to a journal event within 24 h → halts everything). Smaller breaches act more narrowly and are **not** kill triggers: daily loss halts the sleeve, sleeve drawdowns halve then halt the sleeve, API errors pause the venue, a cost blow-out pauses the bot, DQ stale pauses affected bots, a WORM verify mismatch sets `audit.integrity` (`block_new_entries`, P2-T070).
- Engine actions on ON: block new orders in the gate (first check), `cancel_all_orders` on every venue in parallel, then apply each bot's **`on_system_failure`** (default `flatten` with reduce-only market/IOC orders; `cancel_orders_only` keeps the position under its resting venue stop; `hold`; hold-and-earn positions exempt), freeze new treasury/earn moves; the vault-sweep step is a logged no-op hook until P5 (R5.07). Hummingbot/airdrop-exec subscribers come later (P5/P6).
- Every kill ON/OFF is a WORM row (`audit.command`, source `web`/`telegram`/`mcp`/`system`); a `kill.set` arriving directly on NATS (Telegram fallback) is written by the engine with source `telegram`.
- Metric `mt_kill_to_cancels_seconds` (KV set → last cancel ack sent) with target < 1 s; `risk.event{type: kill}`; alert critical on all channels.
- UI: global red banner via WS `kill`.

## ToDo

- [ ] `packages/mt_risk/kill.py` (KV model, triggers)
- [ ] Engine subscriber + parallel cancel/flatten
- [ ] NATS account permissions for `kill.set`
- [ ] Commands + WS topic
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: system drawdown stage 2 and an unexplained recon mismatch set kill with the right reason; daily loss, sleeve drawdown, API errors and cost blow-out do **not** set the global kill (they act on sleeve/venue/bot).
- Unit: per-bot `on_system_failure` honoured: `flatten` closes, `cancel_orders_only` leaves the position with its resting stop, `hold` leaves it.
- Integration (sandbox, 3 venues, 100 open orders): KV ON → all cancels sent < 1 s.
- Unit: `risk.kill.off` refused while the trigger condition persists; requires C3 otherwise.

### Scenarios
- Given 40 open orders across the sandbox venue and mock Binance/OANDA venues (no keys; the live drill runs in P2-T054/P2-T071), when you tap HALT, then all cancels are sent within 1 s and new intents are rejected `kill`.
- Given kill was triggered by system drawdown stage 2, when you request OFF, then it is refused until the 30-day review lock ends or you clear it with C3.
- Given kill ON, when a treasury/earn move is requested, then it is refused (frozen) and the vault-sweep hook logs `not available in P2`.

### Stress / failure injection
- Kill during a burst of 1k intents/s: zero orders submitted after the KV ON timestamp (checked in audit).
- NATS restart during kill ON: KV state persists; engine re-reads on reconnect and stays halted.

## Acceptance criteria

- [ ] Kill → all cancels sent < 1 s (metric)
- [ ] Kill ON never blocked; OFF is C3 + cause cleared
- [ ] Automatic triggers wired (system drawdown stage 2, unexplained recon mismatch)
- [ ] Per-bot `on_system_failure` applied on kill
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue unreachable during cancel: retry with backoff, mark orders `cancel_pending`, rely on broker-side protections; alert.
- mt-api down: Telegram publishes `kill.set` directly (P2-T035).

## Cardinal rules (do NOT)

- Do NOT put any confirmation beyond a single confirm on Kill ON.
- Do NOT allow kill OFF without C3.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` F6 + `docs/03-build-spec.md` M11: KV schema and trigger list as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.23 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T031-kill-switch`
- PR title: `P2-T031: Kill switch: KV state, manual and automatic triggers, cancel/flatten actions`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (kill triggers and actions per 03 M11/17 §B (on_system_failure per bot, freeze treasury, no sweep in P2), WORM source telegram)
