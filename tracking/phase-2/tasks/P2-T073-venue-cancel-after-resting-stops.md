---
id: P2-T073
kind: task
title: "Dead-man layer 3: venue cancel-after timers and resting venue stops at entry"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P2-T028, P2-T023, P2-T024, P2-T025, P2-T026]
requirements: [R2.56]
roadmap_todos: [T2.36]
modules: [M12, M11]
dashboards: [D06, D05]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T073-venue-cancel-after-resting-stops
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T073 · Dead-man layer 3: venue cancel-after timers and resting venue stops at entry

## Goal / expected outcome

When our whole host or its internet is down, the venue protects us: where a venue supports **cancel-on-disconnect / countdown timers**, the engine arms and refreshes them (default refresh every 15 s, 60 s timeout), and **every position carries a resting stop-loss order at the venue, placed at entry**, so a dead system leaves no unprotected exposure.

## Context & references

- Roadmap: [R2.56](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.36
- Decisions: [16 §3.1 layer 3](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) (e.g. Kraken `CancelAllOrdersAfter`, OKX cancel-all-after, Binance USDⓈ-M `countdownCancelAll`; others (U); refreshed every 15 s with a 60 s timeout; resting stop at entry for every position) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (tunnel down → fail-flat via venue timers + resting stops)
- Research rule: (U) facts are verified before the build that relies on them ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)).
- Related: P2-T028 (exit plan fixed at entry), P2-T024–T026 (adapters), P2-T072 (layer 2), P2-T075 (drill), P2-T071 (live check).
- Build first, keys last: built against cassettes and the venue emulator; observed live in P2-T071.

## Requirements

- **Capability matrix** per venue/product in the venue registry: `cancel_after` (`countdown` | `on_disconnect` | `none`), `resting_stop` (`native` | `bracket/OTO` | `none`), each with a source link and verification date; unverified entries are marked (U) and verified from official API docs before enabling.
- **Timers:** for venues with `cancel_after`, arm on connect and refresh every 15 s with a 60 s timeout (L2 settings); refresh failures alert; disarm only on a clean planned shutdown after open orders are handled.
- **Resting stops:** every entry intent's exit-plan stop (P2-T028) is placed at the venue as a native stop or as a bracket/OTO leg in the same request where supported; if the stop can't be placed, the position is closed immediately (or the entry is rejected for venues with `resting_stop: none`, unless the bot explicitly accepts `no_venue_stop` for paper only). Stops are re-placed after modifications and reconciled on restart.
- The RiskGate rejects entries on a live-capable account with `resting_stop: none` unless allowed by policy (`allow_no_venue_stop`, default false; loosening C3).
- Status published per venue (`timer_armed`, last refresh, stops covered/total) for D06 dead-man tile and D05 venues tab.

## ToDo

- [ ] Verify from official docs each venue's cancel-after/countdown and stop-order support (Binance spot vs USD-M, Alpaca, OANDA, IG, Bybit testnet); record in the registry with sources (U → verified)
- [ ] `packages/mt_engine/venue_safety.py`: timer arm/refresh loop per supported venue; status metrics
- [ ] Resting-stop placement at entry (native/bracket/OTO) in each adapter; immediate close if placement fails
- [ ] RiskGate rule for `resting_stop: none` accounts; policy flag `allow_no_venue_stop`
- [ ] Reconcile stops on restart (P2-T027/P2-T074)
- [ ] Tests (cassettes + venue emulator)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: refresh scheduler (15 s / 60 s); stop placement request per venue type.
- Integration (emulator): disconnect the engine from the emulator for 65 s → the emulator's countdown cancels resting orders; positions keep their resting stops.
- Integration (cassettes): entry on each adapter produces the stop/bracket payload; failed stop placement → immediate close.

### Scenarios
- Given an open position on a venue with a native stop, when the host loses internet, then the resting stop remains at the venue and fires if price crosses it.
- Given a venue with `cancel_after: countdown`, when refreshes stop, then open orders are cancelled by the venue after 60 s.
- Given a venue with `resting_stop: none`, when a hitl bot submits an entry on that account, then it is rejected `no_venue_stop` (default policy).

### Stress / failure injection
- Timer refresh endpoint returning errors for 2 minutes: alerts fire; behaviour falls back to the venue's timeout; no false cancel of the timer during normal operation.

## Acceptance criteria

- [ ] Capability matrix verified with sources (no unverified (U) entry enabled)
- [ ] Timers armed and refreshed where supported
- [ ] Every position opened by the engine has a resting venue stop (or a recorded paper-only exception)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite)

## Exceptions & edge cases

- Netting brokers: one stop per net position; a second strategy on the same account is already refused (P2-T022).
- Gaps through the stop: the stop is a market order at the venue; losses can exceed it (documented).
- Venues that cancel all orders incl. stops on disconnect: record it; stops must be placed as position-attached (OTO/bracket) where available, else the account is flagged.

## Cardinal rules (do NOT)

- Do NOT open a position without a resting venue stop where the venue supports one.
- Do NOT rely on unverified (U) venue features in code paths that protect money.
- Do NOT hard-code the 15 s / 60 s timer values.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: registry columns `cancel_after` and `resting_stop` with sources.
- `docs/16-configuration-and-safety-model.md` §3.1: replace the (U) examples with the verified list.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.36 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T073-venue-cancel-after-resting-stops`
- PR title: `P2-T073: Dead-man layer 3: venue cancel-after timers and resting venue stops at entry`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T073` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.36: R2.56)
