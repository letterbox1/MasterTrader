---
id: P2-T027
kind: task
title: Epoch-based idempotent client order IDs and restart reconciliation
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P1-T041, P1-T042]
requirements: [R2.32]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T027-epoch-client-ids-reconcile
pr: ""
doc_sync: [docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T027 · Epoch-based idempotent client order IDs and restart reconciliation

## Goal / expected outcome

Client order IDs follow the decided format **`{bot}-{engine_epoch}-{seq}`**, with a **signal hash stored separately** for idempotency so a restarted engine can't resubmit the same signal, and the engine reconciles open orders and positions from every venue before it resumes trading after any start.

## Context & references

- Roadmap: [R2.32](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M12 idempotent IDs](../../../docs/03-build-spec.md#m12-execution--mt_engine) · [07 §6 IDs derived from signal ID](../../../docs/07-security-notes.md#6-application-controls)
- Degraded modes: [02 §9.3 venue disconnect](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Decision: [17 §D P2-B007](../../../docs/17-decisions-register.md#d-other-decisions) (client order ID = `{bot}-{engine_epoch}-{seq}`; a signal hash is stored separately for idempotency) · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) · defaults [16 §2.9 reconciliation](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)
- Cross-phase (`depends_on`): P1 reconciliation jobs and report parsers (P1-T041 crypto testnets, P1-T042 practice brokers, T1.29).
- Related: P2-T055 restart-duplicate test; P2-T074 restart-flat flow (bots paused, residue flattened/cancelled per policy) runs after this reconciliation.

## Requirements

- `ops.engine_epoch` (monotonic int incremented on every engine boot, persisted before any submit).
- Client order ID = `{bot}-{engine_epoch}-{seq}`: `bot` is the bot's short code (manual tickets use `manual`), `engine_epoch` the boot counter, `seq` a per-epoch monotonic counter persisted before submit.
- **Signal hash** = hash(signal id, leg) for strategy orders, or the command idempotency key for manual orders, stored separately in the **intent ledger** (`ops.intent_ledger`, insert-only, maps signal hash → client order IDs). Before submit, the engine checks the ledger across all epochs; a hit → no resubmit, attach to the existing order.
- Venue field length/charset limits handled per adapter (IG ≤ 30 chars, Binance ≤ 36, OANDA ≤ 128): bot short codes sized so the full ID fits every venue; a too-long ID is a config error at bot creation, never truncated silently.
- Startup: state `RECONCILING` blocks new entries; pulls open orders, fills since last checkpoint and positions from each venue (Nautilus reconciliation on); matches by client id; unknown venue orders → incident + optional cancel (policy); missing local orders → imported with `origin=reconciled`; then `READY`.
- Reconciliation timeout per venue (default 30 s) → venue stays `unconfirmed` (positions shown 'unconfirmed') and new orders there are held.

## ToDo

- [ ] Epoch + ledger tables and service
- [ ] ID generator per adapter constraints
- [ ] Startup reconciliation orchestrator + state publication `strat.status`/`risk.event`
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: IDs match `{bot}-{engine_epoch}-{seq}`; the same signal hash in a later epoch is blocked by the ledger; different legs → different signal hashes; every venue length limit respected.
- Integration (sandbox): kill -9 the engine after submit before ack; restart → reconciles, no second submit.
- Unit: unknown venue order triggers incident.

### Scenarios
- Given the engine crashed after sending an order, when it restarts, then it finds the order by client id at the venue and resumes managing it without resubmitting.
- Given a venue is down at startup, when the engine boots, then other venues become READY and that venue's positions show 'unconfirmed'.

### Stress / failure injection
- Chaos loop: 50 random crashes during a 30-min sandbox session; zero duplicate client ids at the venue; every order accounted for.

## Acceptance criteria

- [ ] No duplicate orders across 50 crash cycles
- [ ] Trading resumes only after reconciliation
- [ ] Epoch persisted before first submit
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Postgres down at boot: engine refuses to start trading (can't read ledger) → default-deny.
- Clock jumps: epoch is a counter, not a timestamp.

## Cardinal rules (do NOT)

- Do NOT resubmit an intent without checking ledger + venue status.
- Do NOT auto-close unknown venue positions without policy permission.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/03-build-spec.md` M12 + `docs/07-security-notes.md` §6: confirm the `{bot}-{engine_epoch}-{seq}` format and the signal-hash ledger as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T027-epoch-client-ids-reconcile`
- PR title: `P2-T027: Epoch-based idempotent client order IDs and restart reconciliation`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (client order ID {bot}-{engine_epoch}-{seq} + separate signal hash (17 §D P2-B007), recon defaults 16 §2.9, restart-flat handoff to P2-T074)
