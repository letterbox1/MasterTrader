---
id: P2-T072
kind: task
title: "Dead-man layer 2: external deadman sidecar with its own keys and venue connections"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T032, P2-T044, P2-T023, P2-T036]
requirements: [R2.56, R2.18]
roadmap_todos: [T2.36]
modules: [M11, M12]
dashboards: [D06]
tools: [uv, docker]
mcp: []
env: []
services: [nats]
branch: p2/P2-T072-deadman-sidecar-layer-2
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T072 · Dead-man layer 2: external deadman sidecar with its own keys and venue connections

## Goal / expected outcome

A small `deadman` sidecar (`mt_risk.deadman`, its own container) watches the **engine's** heartbeat with its own trade-only keys and its own venue connections: engine heartbeat missing **5 s → cancel all open orders**; missing **10 s → flatten per each bot's `on_system_failure`**. It covers the case the in-engine watchdog can't: the engine itself dying.

## Context & references

- Roadmap: [R2.56](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.36 · verified by P2-T075 (T2.70) and live in P2-T071
- Decisions: [16 §3.1 layer 2](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) · [17 §A P2-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [02 §3.2 `deadman` container](../../../docs/02-v1-architecture.md#32-containers) · [07 §3 deadman keys](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- Related: P2-T032 (heartbeat library, layer 1), P2-T044 (container, limits, secret scoping), P2-T023 (deadman account block per venue), P2-T036 (`on_system_failure` per bot), P2-T073 (layer 3), P2-T074 (restart flat).
- Build first, keys last: built and tested against mock venue servers (external emulator containers) with dummy secrets; your real deadman keys are exercised in P2-T071.

## Requirements

- Subscribes `sys.heartbeat.engine` (1 s); uses its monotonic receive time; publishes `sys.heartbeat.deadman`.
- Keeps an independent, periodically refreshed view of open orders and positions per venue account via its **own** venue connections (REST polling, default every 5 s) and of each bot's `on_system_failure` (KV snapshot replicated from the policy; last known value used if NATS is down).
- Engine missing **5 s** → `cancel_all` per venue account (venue cancel-all endpoints; per-order cancel fallback). Missing **10 s** → per bot: `flatten` → reduce-only market/IOC close; `cancel_orders_only` → nothing more (position keeps its resting venue stop); `hold` → nothing; hold-and-earn exempt. Timers are L1 settings (defaults 5 s / 10 s).
- **Can only cancel and flatten:** the code has no path to open or increase a position (reduce-only flag enforced client-side and checked against the position snapshot); a CI test asserts it.
- Every action written to WORM (`audit.command` source `system`, actor `deadman`) via JetStream when Postgres is unreachable; critical alert on every channel.
- Paper/sandbox accounts: acts against the venue emulator in tests; real testnet/practice accounts in P2-T071.
- Recovery: when the engine heartbeat returns, the sidecar stops acting and the engine follows the restart-flat flow (P2-T074); `risk.deadman.ack` (C1) clears the alert.
- Footprint: 0.5 CPU / 256 MB; reaction measured `mt_deadman_reaction_seconds`.

## ToDo

- [ ] `packages/mt_risk/deadman/` service: heartbeat watcher, venue snapshot poller, action runner (cancel, reduce-only flatten)
- [ ] Minimal venue clients for cancel-all / reduce-only close (Binance spot + USD-M, Alpaca, OANDA, IG), reusing adapter REST code where possible
- [ ] Policy snapshot of `on_system_failure` per bot
- [ ] WORM audit + JetStream buffering; alerts; metrics
- [ ] Mock venue emulator container for tests (shared with P2-T075)
- [ ] Tests (see Verification)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: timer stages (5 s cancel, 10 s `on_system_failure`), per-policy actions, hold-and-earn exempt.
- Static/CI: no code path in `mt_risk.deadman` can place a non-reduce-only order (AST + unit test).
- Integration (mock venues): `docker kill engine` with open orders and positions → cancels within 5 s + 1 s, `flatten` bots flat within 10 s + 1 s.

### Scenarios
- Given the engine process is killed with 10 open mock-venue orders, when 5 s pass, then the sidecar cancels them all and alerts critical.
- Given a bot with `on_system_failure: cancel_orders_only`, when 10 s pass, then its position stays open with its resting stop and nothing else is sent.
- Given NATS is down when the engine dies, then the sidecar still acts on the missing heartbeat and buffers its audit rows.

### Stress / failure injection
- Engine heartbeat flapping (missing 4 s, back, missing 4 s): no false trigger at the 5 s threshold.
- Venue emulator returns 5xx on cancel-all: per-order cancel fallback with backoff; alert lists any order not confirmed cancelled.

## Acceptance criteria

- [ ] Engine death covered: cancel at 5 s, `on_system_failure` at 10 s (defaults from policy)
- [ ] The sidecar can only cancel and flatten (asserted in CI)
- [ ] Actions audited (WORM) and alerted
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite)

## Exceptions & edge cases

- Sidecar and engine both down (host down): only layer 3 protects (venue timers + resting stops, P2-T073).
- Sidecar's own keys revoked/invalid: it alerts at startup and the engine shows the dead-man tile red (it does not block trading by itself; you decide).
- Stale position snapshot: flatten uses a fresh venue query before sending; never closes more than the venue reports.

## Cardinal rules (do NOT)

- Do NOT give the sidecar any ability to open or increase positions, or any key beyond its own trade-only deadman keys.
- Do NOT share the engine's keys or connections with the sidecar.
- Do NOT hard-code the 5 s / 10 s timers.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2/§6: `deadman` container and subjects as built.
- `docs/16-configuration-and-safety-model.md` §3.1: confirm layer-2 behaviour as built (no value change).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.36 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T072-deadman-sidecar-layer-2`
- PR title: `P2-T072: Dead-man layer 2: external deadman sidecar with its own keys and venue connections`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T072` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.36: R2.56, R2.18)
