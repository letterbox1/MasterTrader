---
id: P2-T021
kind: task
title: mt_engine TradingNode wrapper, intent actor and order audit
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T003, P2-T017, P0-T031, P1-T004]
requirements: [R2.30, R2.10, R2.01]
roadmap_todos: [T2.25]
modules: [M12, M11, M0]
dashboards: [D05]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T021-engine-tradingnode-wrapper
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T021 · mt_engine TradingNode wrapper, intent actor and order audit

## Goal / expected outcome

The `engine` service runs a Nautilus `TradingNode` per environment (sandbox/paper, testnet/practice) that loads pinned strategy versions, installs the M11 `RiskGate`, accepts external intents from NATS (`ord.intent.*`), and writes every order, fill and position snapshot to the WORM audit tables while publishing `ord.*`, `fill.*`, `pos.*`.

## Context & references

- Roadmap: [R2.30, R2.10, R2.01](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) · Architecture: [02 §3.2 `engine` container](../../../docs/02-v1-architecture.md#32-containers) · [02 §4 M12 tables](../../../docs/02-v1-architecture.md#4-logical-components) · [02 §6 subjects](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Flow: [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Cross-phase (`depends_on`): WORM audit tables (P0-T031, T0.23); NATS JetStream streams (P1-T004). Market data `md.*` (P1) and recon jobs (P1 R1.12) are used at runtime; tests use recorded fixtures and the Nautilus sandbox venue.
- Decisions: [17 §D P2-B009](../../../docs/17-decisions-register.md#d-other-decisions) engine control subject `engine.cmd.*` · [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) canonical audit names (`audit.order`, `audit.fill`) · [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) write path (JetStream buffer 1 GB / 24 h, stop new entries above 80%).
- Build first, keys last: built and tested against the sandbox venue and recorded fixtures with no keys; the live testnet/practice run is P2-T071.
- Related: P2-T022 STP, P2-T023–T026 venues, P2-T027 IDs/reconcile, P2-T031 kill, P2-T033 modes.

## Requirements

- `packages/mt_engine/node.py`: builds `TradingNodeConfig` from `config/engine.<env>.yaml` (venues, accounts by mode, strategies by version id, cache/msgbus settings).
- `IntentActor`: subscribes `ord.intent.{source}` (manual, telegram, agent, bot) via a NATS bridge, validates schema, calls `RiskGate`, then submits; publishes `ord.risk.{decision}`.
- Strategy control: `strategy.start|pause|resume|stop`, mode, shadow runs and bot lifecycle reach the node through `engine.cmd.{command}` (02 §6) and update `strat.status.{strategy}` / `bot.{id}.status`.
- Audit writers: `audit.order` (intent, decision, client order id, venue id, STP mode, exit plan, trace_id, bot_id, sleeve), `audit.fill`, `audit.position_snapshot`; inserts never block the order path (async queue, bounded, spill to NATS JetStream when Postgres is down: bounded at 1 GB or 24 h by default; above 80% of the buffer new entries stop and exits continue; nothing is executed without a record, 16 §3.3).
- Publishes `fill.{venue}`, `pos.{account}` for journal (P3) and monitor (TCA).
- Heartbeat `sys.heartbeat.engine` every 1 s (P2-T032 library), watched by the in-engine watchdog (layer 1) and the external `deadman` sidecar (layer 2, P2-T072).
- Signal → order submitted p99 < 5 ms (excl. venue) budget: gate + submit path measured with OTel spans.

## ToDo

- [ ] Node builder + env configs (`config/engine.sandbox.yaml`, `engine.testnet.yaml`)
- [ ] NATS ↔ Nautilus msgbus bridge for intents/decisions/control
- [ ] Audit writer with bounded queue + JetStream spill
- [ ] Container entrypoint (`python -m mt_engine`)
- [ ] OTel spans `signal→intent→risk→submit`
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Integration (sandbox venue): example strategy → intent → gate → simulated fill → `audit.order` + `audit.fill` rows with matching ids and hash chain.
- Integration: `ord.intent.manual` path produces the same audit shape.
- Unit: control commands change strategy state and publish `strat.status`.

### Scenarios
- Given Postgres is stopped, when orders fill, then fills are buffered in JetStream and written in order once Postgres returns (no loss, no duplicate).
- Given a malformed intent on NATS, when received, then rejected `schema_invalid` and logged; node keeps running.

### Stress / failure injection
- 10k intents/min for 10 min in sandbox: no audit loss, queue never exceeds bound, p99 signal→submit recorded for P2/Part B latency work.

## Acceptance criteria

- [ ] Engine container runs the sandbox node from config; the testnet node config is validated against mock venues (live run in P2-T071)
- [ ] Every order/fill audited with trace_id
- [ ] External intents only enter via the gate
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue disconnect: orders flagged `unknown` until reconciled (P2-T027).
- JetStream buffer above 80%: stop accepting new entries (hold) and alert; exits still allowed.
- Unplanned restart: the node starts with every bot paused and flat (P2-T074).

## Cardinal rules (do NOT)

- Do NOT give mt_api, Telegram or agents a direct handle on Nautilus clients.
- Do NOT block the order path on audit writes.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/03-build-spec.md` M12 and `docs/02-v1-architecture.md` §6: control subject and audit fields as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T021-engine-tradingnode-wrapper`
- PR title: `P2-T021: mt_engine TradingNode wrapper, intent actor and order audit`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (engine.cmd.* control subject, canonical audit names, 16 §3.3 buffer bounds, deadman heartbeat consumer, keyless build)
