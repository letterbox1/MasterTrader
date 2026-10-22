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
depends_on: [P0-T016, P0-T030, P0-T031]
requirements: [R6.01]
roadmap_todos: [T6.20]
modules: [M8, M17]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p6/P6-T004-signal-schema-decision-tables
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T004 · Signal v2 schema with provenance and decision-run WORM tables

## Goal / expected outcome

A versioned `Signal` schema in `mt_core.schemas` (msgspec) with mandatory provenance, plus WORM tables `audit.decision_run` and `audit.signal`, so every agent output is structured, sourced and point-in-time.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) · [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M8 owns `audit.decision_run`, `audit.signal`; publishes `sig.agent.*`) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`sig.{source}.{strategy}`) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (agents' only output is a structured Signal)
- UI fields: [D09](../../../docs/ui/dashboards/D09-agents.md) (direction, conviction, horizon, provenance count, risk outcome) · [ui components](../../../docs/ui/components.md) `ProvenanceList`
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · tests [15 §2.4](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B014: `Signal` fields defined in 03 M8)
- Cross-phase: P0-T016 (`mt_core.Signal` v1), P0-T030/P0-T031 (hash-chain trigger, WORM audit helper). `audit.decision_run` and `audit.signal` are new here (canonical names, 02 §5.1, 17 §B)

## Requirements

- `Signal` v2 fields are exactly the 03 M8 list (17 §D, P6-B014): `id` (UUIDv7), `ts` (when it was produced: the earliest time a consumer may see it), `as_of` (data cut-off), `instrument`, `horizon` (ISO-8601 duration), `direction` (long|short|flat), `edge` (expected return over the horizon after costs, bps), `confidence` (calibrated probability 0–1), `rationale_summary`, `sources[]` (kind: document|bar|filing|memory|tool, id, as_of, hash), `model_versions[]` / `prompt_versions[]`, `run_id`. Optional extras only: `source` (agent|strategy|tierb), `conviction` (D09 display), `schema_version`.
- Validation: any numeric claim in `rationale_summary` must map to a `sources[]` entry, else `unsourced_numbers=true` (flagged in D09).
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
- Property: any Signal with `direction != flat` requires ≥ 1 `sources[]` entry.

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
- Clock: `as_of`/`ts` are UTC; reject Signals with `ts` in the future (> 5 s skew) or `as_of` > `ts`.

## Cardinal rules (do NOT)

- Do NOT let a Signal carry an order; agents output Signals only, orders come from strategies via M11.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M8: link the implemented schema (the field list is already there).
- `docs/02-v1-architecture.md` §5.3/§6: `audit.decision_settlement`, `sig.agent.*` payload version.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T004-signal-schema-decision-tables`
- PR title: `P6-T004: Signal v2 schema with provenance and decision-run WORM tables`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Signal fields = 03 M8 list per 17 §D P6-B014; canonical audit names; cross-phase deps P0-T016/T030/T031; run fields)
