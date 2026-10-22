---
id: P2-T070
kind: task
title: "Inline pre-trade safety-state checks: data age, audit.integrity, egress status, decision deadline"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010, P1-T030, P1-T071, P0-T038]
requirements: [R2.58, R2.16]
roadmap_todos: [T2.39]
modules: [M11]
dashboards: [D06]
tools: [uv]
mcp: []
env: []
services: [nats]
branch: p2/P2-T070-inline-safety-state-checks
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T070 · Inline pre-trade safety-state checks: data age, audit.integrity, egress status, decision deadline

## Goal / expected outcome

`mt_risk.checks.safety_state` runs **inline on every order** inside the RiskGate and rejects the order (the ladder holds) when: the data it acts on is older than the bot's threshold; the WORM integrity status says so; the egress check is failing; or the decision is past its deadline. No order can act on stale data or an untrusted record whatever the monitors' timing.

## Context & references

- Roadmap: [R2.58](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.39 · verified by P2-T076 (T2.71)
- Decisions: [16 §2.2 data freshness](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) (data age = now on the host monotonic clock − our receive time; 2 s fast / 60 s slow; session-aware; inline order-time check) · [16 §2.11 WORM integrity](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity) (`block_new_entries` default; `alert_only`, `halt_all`) · [16 §3.2 egress check](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) · [16 §2.3 decision deadlines](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [17 §A P0-B001, P1-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Spec: [03 M11 pre-trade checks](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [02 F2 step 4](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase (`depends_on`): DQ monitor publishing per-stream receive times / `feed_status` (P1-T030, R1.10); egress IP/country check publishing `egress.status` (P1-T071, T1.33, R1.16); `audit.verify`, the integrity incident path, KV `audit.integrity` and the `mt_risk.integrity_gate` hook point (P0-T038, T0.23/T0.27, R0.07/R0.12); this task calls that hook inline on every order. Unit tests use a fake KV with the documented values.
- Related: P2-T017 (RiskGate wires this check after the venue/mode checks), P2-T018 (a failing check holds the ladder, rung 3 for the scope), P2-T069 (per-bot thresholds from the merged layers), P2-T059 (degraded-mode e2e).

## Requirements

- **Data age:** for each instrument stream the bot uses, `age = monotonic_now − last_receive_monotonic` (our receive time, never the exchange timestamp; skew tracked separately by P1). Threshold per bot from its stale class (defaults **2 s fast / 60 s slow**, L4 setting capped by L1). Session-aware: a closed session is `closed`, not stale (entries rejected `session_closed` by the venue/session rule, not as stale). Older than threshold → reject `data_stale` + ladder hold.
- **WORM integrity:** read NATS KV `audit.integrity` (`ok` | mismatch with action `alert_only` | `block_new_entries` | `halt_all`). `block_new_entries` (default) → reject entries `integrity_block`, exits and protective orders pass; `halt_all` → reject every new order (resting venue stops and kill cancels are unaffected); `alert_only` → pass with a warning on the decision. Missing/unknown KV state → default-deny entries.
- **Egress:** read `egress.status` (`ok` | `mismatch` | `unknown`, with age). `mismatch`, or status older than its freshness bound (default 2 min), → reject new orders `egress_block` + alert; protective exits are still attempted (the venue may refuse them; resting venue stops protect). Before the P7 exit node exists, R1.16 checks the configured registered IP/country.
- **Decision deadline:** `now − signal_ts` > the bot's deadline (defaults scalping 1 s · intraday 10 s · swing 5 min · position 1 h) → drop the decision, reject `decision_late` (never act late). Protective exits are exempt.
- Each rejection carries `observed` vs `threshold` and the source state version; publishes `risk.event` and feeds P2-T018 so the ladder holds for the affected scope.
- In-memory state only (KV watchers), no I/O on the order path; adds ≤ 20 µs p99 to the gate.
- `/risk/state` exposes current integrity and egress status and per-feed ages (D06 risk-state tile).
- All thresholds are settings with 16 defaults; none hard-coded.

## ToDo

- [ ] `packages/mt_risk/checks/safety_state.py` with the four checks and reason codes
- [ ] KV watchers/caches for `audit.integrity`, `egress.status` and per-stream receive times (monotonic), with staleness of the status itself tracked
- [ ] Per-bot thresholds from the merged policy (stale class, decision deadline)
- [ ] Ladder hook (rung 3 hold for the scope) and `risk.event` publication
- [ ] `/risk/state` fields for D06
- [ ] Unit tests + microbenchmark
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: data age boundaries per stale class (1.999 s pass / 2.001 s reject for fast); closed session not stale.
- Unit: integrity states × order kinds (entry, exit, protective) → expected decision for `ok`, `alert_only`, `block_new_entries`, `halt_all`, unknown.
- Unit: egress `ok` / `mismatch` / stale status; decision deadline per horizon class.
- Microbenchmark: the four checks add ≤ 20 µs p99.

### Scenarios
- Given a fast bot whose BTC feed was last received 2.5 s ago, when it submits an entry, then it is rejected `data_stale` and the ladder holds for that bot.
- Given `audit.integrity = block_new_entries`, when a bot submits an exit, then it passes; an entry is rejected `integrity_block`.
- Given `egress.status = mismatch`, when any new entry arrives, then it is rejected `egress_block` and an alert fires.
- Given a swing bot's signal from 6 minutes ago, when the intent arrives, then it is dropped `decision_late`.

### Stress / failure injection
- Flap `egress.status` and `audit.integrity` every 100 ms for 1 min under 1k intents/s: every decision matches the state version current at check time; no order slips through a blocking state.
- Kill the KV watcher: state turns unknown and entries are default-denied within 1 s.

## Acceptance criteria

- [ ] All four checks run inline on every order with reason codes and observed vs threshold
- [ ] A failing check rejects the order and holds the ladder
- [ ] ≤ 20 µs p99 added to the gate
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite)

## Exceptions & edge cases

- Clock: only the host monotonic clock (chrony-synced host) is used for ages; a monotonic jump is impossible, a wall-clock step doesn't affect ages.
- Backtests: integrity and egress are treated as `ok` and recorded so; data age uses the simulated clock (P2-T105).
- Protective exits under `halt_all`: not sent; resting venue stops and the dead-man layers protect positions.

## Cardinal rules (do NOT)

- Do NOT measure data age from the exchange's timestamp.
- Do NOT let a missing or unknown state pass an entry (default-deny).
- Do NOT add I/O to the order path.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` M11: reason codes for the safety-state checks.
- `docs/02-v1-architecture.md` F2: check order as built (egress status checked from Phase 1 (P1-T071) and inline in M11 from P2; 02 F2 updated, P2-B019).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.39 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T070-inline-safety-state-checks`
- PR title: `P2-T070: Inline pre-trade safety-state checks: data age, audit.integrity, egress status, decision deadline`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T070` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.39: R2.58, R2.16)
