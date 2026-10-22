---
id: P7-T026
kind: task
title: Unconfirmed position state after disconnects and recon-gated resume
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T025, P2-T027, P2-T074]
requirements: [R7.09]
roadmap_todos: [T7.23]
modules: [M12, M11, M16]
dashboards: [D05, D01]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T026-unconfirmed-positions-after-disconnect
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D05-execution.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T026 · Unconfirmed position state after disconnects and recon-gated resume

## Goal / expected outcome

After any venue disconnect, engine restart or order in unknown state, affected positions and orders are marked `unconfirmed`, new entries on that account are blocked, and trading resumes only after a clean reconciliation; emergency flatten via the kill switch still works.

## Context & references

- Roadmap: [R7.09 · ToDo T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) (venue disconnect: reconnect with backoff, orders flagged unknown → reconcile; positions 'unconfirmed') · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) (open orders reconciled before trading resumes) · [D05](../../../docs/ui/dashboards/D05-execution.md) (unconfirmed hatched; close needs recon unless emergency flatten)
- Cross-phase: P2-T027 (`depends_on`: epoch client order IDs `{bot}-{engine_epoch}-{seq}` and restart reconciliation, [17 §D P2-B007](../../../docs/17-decisions-register.md#d-other-decisions)) · P2-T074 (`depends_on`: clean restart, flat, bots paused) · restart flat with bots paused [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch).
- Related: P7-T025, P7-T029 (auto-downgrade on unconfirmed), P7-T050

## Requirements

- Triggers: WS/REST disconnect > 5 s, engine start, order ack timeout (> 10 s), venue error 5xx on submit, exit-node tunnel down (P7-T066). Timings are settings.
- State: `confirmation = unconfirmed` on positions/orders of the account; M11 rejects new entries for that account (reason `account_unconfirmed`); protective exits and resting broker-side stops remain.
- Exit: a recon run with zero unexplained breaks on that account flips state to `confirmed` and publishes `recon.{account}`; after a disconnect `hitl` bots resume automatically and autonomous bots stay downgraded (P7-T029); after an engine restart every bot stays **paused** until you resume it (C1) or it has `auto_resume_after_crash: true` (16 §3.1).
- UI: hatched rows + 'unconfirmed' chip (ui README states table); D01 safety tile shows count.
- Emergency flatten via kill switch bypasses the confirmation gate (but still passes M11 protective path).

## ToDo

- [ ] Account confirmation state in `mt_engine` (KV `account_state`).
- [ ] M11 pre-trade check `account_confirmed`.
- [ ] Recon-triggered confirmation on clean run.
- [ ] D05/D01 UI states.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: drop venue WS for 10 s → state unconfirmed; entries rejected; reconnect + clean recon → confirmed.
- Integration: engine crash mid-order → restart → open orders fetched from venue, no duplicate submits (epoch ids), positions confirmed only after recon.
- Unit: kill switch flatten allowed while unconfirmed.

### Scenarios
- Given an order times out with no ack, then it is `unknown`, the account is unconfirmed, and recon finds it filled → journal gets the fill, account confirmed.
- Given unconfirmed for > 24 h with an unexplained break, then P7-T027 halts everything.

### Stress / failure injection
- Flap the venue connection 20 times in 5 min: no duplicate orders, no stuck state; backoff caps at 60 s.

## Acceptance criteria

- [ ] Unconfirmed state blocks new entries and is cleared only by a clean recon.
- [ ] No duplicates across restarts.
- [ ] CI green.

## Exceptions & edge cases

- Partial fills during disconnect: recon imports them before confirmation.
- Postgres down while unconfirmed: engine keeps state in memory; journal buffered (02 §9.3).

## Cardinal rules (do NOT)

- Do NOT clear `unconfirmed` manually without a recon run.
- Do NOT block protective exits or kill-switch flattening.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.3: triggers and exit condition for unconfirmed.
- `docs/ui/dashboards/D05-execution.md`: unconfirmed behaviour.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.23 when this item is done.

## Branch & PR

- Branch: `p7/P7-T026-unconfirmed-positions-after-disconnect`
- PR title: `P7-T026: Unconfirmed position state after disconnects and recon-gated resume`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (restart flat/paused per 16 §3.1; tunnel-down trigger; dep P2-T027)
