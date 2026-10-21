---
id: P6-T004
kind: task
title: Signal v2 schema with provenance and decision-run WORM tables
phase: 6
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.01]
roadmap_todos: [T6.20]
modules: [M8, M17]
dashboards: [D09]
branch: p6/P6-T004-signal-schema-decision-tables
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T004 · Signal v2 schema with provenance and decision-run WORM tables

## Goal / expected outcome

A versioned `Signal` schema in `mt_core.schemas` (msgspec) with mandatory provenance, plus WORM tables `audit.decision_run` and `audit.signal`, so every agent output is structured, sourced and point-in-time.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) · [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M8 owns `audit.decision_run`, `audit.signal`; publishes `sig.agent.*`) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`sig.{source}.{strategy}`) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (agents' only output is a structured Signal)
- UI fields: [D09](../../../docs/ui/dashboards/D09-agents.md) (direction, conviction, horizon, provenance count, risk outcome) · [ui components](../../../docs/ui/components.md) `ProvenanceList`
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · tests [15 §2.4](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- Gap: P6-B014 (Signal fields not specified in any doc)
- Cross-phase: P0 T0.21 (`mt_core.Signal` v1), P0 R0.07 (WORM machinery)

## Requirements

- `Signal` v2 fields: `signal_id` (UUIDv7), `source` (agent|strategy|tierb), `instrument_id`, `direction` (long|short|flat), `probability` (0–1), `conviction` (low|med|high), `horizon` (ISO-8601 duration), `as_of`, `event_time`, `ingest_time`, `rationale_summary`, `provenance[]` (kind: document|bar|filing|memory|tool, id, as_of, hash), `run_id`, `model_ids[]`, `prompt_versions[]`, `schema_version`.
- Validation: any numeric claim in `rationale_summary` must map to a provenance entry, else `unsourced_numbers=true` (flagged in D09).
- `audit.decision_run`: run_id, subject, trigger (scheduled|event|manual|anomaly), stages JSON, models, tokens, cost, latency, status, settlement_due_at; `audit.signal`: one row per Signal. Both WORM (INSERT/SELECT only, hash-chained); settlement is a new row referencing `run_id`.
- NATS subject `sig.agent.{strategy|adhoc}` carries the Signal; payload versioned.
- Backwards compatible with P0 `Signal` v1 consumers (adapter).

## ToDo

- [ ] Add `Signal` v2 + `Provenance` structs in `packages/mt_core/mt_core/schemas/signal.py`, with a v1→v2 adapter.
- [ ] Alembic migration for `audit.decision_run`, `audit.signal` (+ `audit.decision_settlement` for P6-T013) on the WORM owner role with hash-chain triggers.
- [ ] Writer helpers in `mt_obs.audit` (`write_decision_run`, `write_signal`).
- [ ] Unsourced-number detector (regex for numbers/percentages in rationale vs provenance values).
- [ ] Register `sig.agent.*` subject schema in `mt_core.schemas` registry.
- [ ] Tests (below); update docs.

## Verification

### Tests
- Unit: schema round-trip, v1→v2 adapter, unsourced-number detector (golden rationale strings).
- Integration: insert Signal → row hash chained; UPDATE/DELETE/TRUNCATE by app role fails (15 §2.4).
- Property: any Signal with `direction != flat` requires ≥ 1 provenance entry.

### Scenarios
- Given a rationale citing "RSI 72" with a bar provenance, when validated, then `unsourced_numbers=false`.
- Given a rationale citing "EPS +12%" with no filing provenance, when validated, then the flag is set and D09 shows it.
- Given an app role tries `UPDATE audit.signal`, then the trigger rejects it.

### Stress / failure injection
- Insert 10k signals; hash-chain insert p99 stays within the WORM SLO and `audit.verify` passes.

## Acceptance criteria

- [ ] Schema, migrations and writers merged with tests green.
- [ ] `audit.verify` covers the new tables.
- [ ] CI green (lint, types, tests, `pit` check).

## Exceptions & edge cases

- Restart mid-insert: chain resumes from last committed `row_hash`.
- Clock: `as_of`/`event_time` are UTC; reject Signals with `event_time` in the future (> 5 s skew).

## Cardinal rules (do NOT)

- Do NOT let a Signal carry an order; agents output Signals only, orders come from strategies via M11.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M8: link the Signal v2 field list.
- `docs/02-v1-architecture.md` §5.3/§6: `audit.decision_settlement`, `sig.agent.*` payload version.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T004-signal-schema-decision-tables`
- PR title: `P6-T004: Signal v2 schema with provenance and decision-run WORM tables`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
