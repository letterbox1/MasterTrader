---
id: P5-T062
kind: task
title: Stress and failure injection: RPC quotas, signer/Anvil/Postgres down, restarts mid-claim
phase: 5
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T018, P5-T022, P5-T028, P5-T044, P5-T030]
requirements: [R5.02, R5.04, R5.05, R5.N2]
roadmap_todos: []
modules: [M22, M4, M19]
dashboards: [D07, D18]
tools: [uv, docker, toxiproxy]
mcp: []
env: []
services: [postgres, nats, anvil]
branch: p5/P5-T062-verify-stress-failure-injection
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T062 · Stress and failure injection: RPC quotas, signer/Anvil/Postgres down, restarts mid-claim

## Goal / expected outcome

A chaos suite proves P5 degrades safely: every on-chain path fails **closed** (no signature) when its prerequisites are missing, read paths degrade with visible staleness, and nothing duplicates after restarts — covering the 02 §9.3 degraded modes for the new services.

## Context & references

- Roadmap: R5.02, R5.04, R5.05, R5.N2 · [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Risk table: [§7](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) (simulation is a sanity check; free RPC limits)

## Requirements

- Faults: RPC provider 429/5xx/timeouts (each provider, then all); Anvil down; Helius down; OpenBao sealed; Postgres down 2 min; NATS restart; signer crash after sign/before broadcast; airdrop-exec restart mid-queue; clock skew 2 s; Telegram API down; GoPlus/RugCheck down.
- Expectations: no signature without a ledger row or while the limits are unconfirmed (`limits_unconfirmed`); claims → CLAIM_MANUAL or retry within deadline; indexer marks stale (D18 amber); quotas never exceeded; tasks still visible in UI when Telegram is down; risk `incomplete` blocks autonomy.
- Load: 3× normal discovery volume for 1 h with quotas enforced; 50 concurrent claims across 3 wallets.
- Report with per-fault outcome table.

## ToDo

- [ ] Write `tests/chaos/p5/` using toxiproxy (pinned) and compose service stops.
- [ ] Run on staging compose; produce the outcome table; file bugs for failures.
- [ ] Add any newly discovered degraded mode to 02 §9.3.

## Verification

### Tests
- Chaos suite (≥ 12 fault cases) + load run.

### Scenarios
- Given Postgres is down when a claim is ready, then the signer refuses (ledger unavailable) and the claim retries after recovery without duplicates.
- Given all EVM RPC providers fail, then cost gate returns `wait`, no claim is signed, D07 shows the outage.

### Stress / failure injection
- This item is the stress/failure-injection item for P5 (see Requirements).

## Acceptance criteria

- [ ] Every fault case has the expected safe outcome
- [ ] No duplicate claims/sweeps after any restart
- [ ] Outcome table recorded; bugs filed for failures

## Exceptions & edge cases

- Faults overlapping (Postgres + NATS): system remains frozen for signing until both recover.

## Cardinal rules (do NOT)

- Do NOT run chaos against mainnet funds or live venues.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.3: add rows for signer/indexer/airdrop-exec degraded modes.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick the related exit criterion when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T062-verify-stress-failure-injection`
- PR title: `P5-T062: Stress and failure injection: RPC quotas, signer/Anvil/Postgres down, restarts mid-claim`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (signing-disabled state added to the fail-closed expectations)
