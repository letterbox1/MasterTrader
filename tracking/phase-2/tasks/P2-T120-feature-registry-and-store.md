---
id: P2-T120
kind: task
title: mt_features registry, versioning and batch/incremental parity
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T103]
requirements: [R2.46]
roadmap_todos: [T2.29]
modules: [M6]
dashboards: [D04]
branch: p2/P2-T120-feature-registry-and-store
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T120 · mt_features registry, versioning and batch/incremental parity

## Goal / expected outcome

A versioned feature registry (`features.def`) with one definition per feature that computes identically in batch (lab, point-in-time) and incrementally (engine), stores values in `features.value` and publishes `feat.{name}.{symbol}`.

## Context & references

- Roadmap: [R2.46](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.29
- [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features) (versioned features) · [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M6 owns `features.value`, `features.def`; publishes `feat.*`) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Consumers: lab (P2-T104/T105), tier A (P2-T125/T128), templates (part A T2.21), MTB library (P2-T130)

## Requirements

- `features.def`: name, version (semver), inputs (bar spec / tick / L2), params, warm-up bars, code_sha, owner, licence; immutable once published — changes create a new version.
- `Feature` protocol with `batch(df) -> Series` and `update(state, event) -> value`; the parity harness asserts |batch − incremental| ≤ 1e-9 on fixtures.
- Batch values computed through `pit(as_of)` datasets; stored in `features.value` (hypertable: feature_id, version, instrument_id, event_time, ingest_time, value) only for features marked `materialise=true`.
- Engine-side incremental values published on `feat.{name}.{symbol}` (msgspec) with ≤ 1 ms compute per update for TA-style features.
- Provenance: features inherit the most restrictive `train_ok`/`model_input_ok` of their inputs.

## ToDo

- [ ] Migration for `features.def`, `features.value` (Timescale hypertable)
- [ ] Implement `packages/mt_features/{registry,base,store,publish}.py`
- [ ] Implement parity harness `mt_features.testing.assert_parity`
- [ ] Provenance propagation
- [ ] Tests + doc

## Verification

### Tests
- Unit: registry refuses re-publishing a changed definition under the same version.
- Property: parity harness passes for a moving-average feature on random series (hypothesis).
- Integration: materialised feature written and read back via `pit`.

### Scenarios
- Given a feature computed from a Telegram-derived input (P4+), then its `model_input_ok=false` propagates and tier A refuses it.
- Given an engine restart, then incremental state rebuilds from the declared warm-up bars before publishing.

### Stress / failure injection
- Incremental update of 50 features × 20 symbols at 1-s bars: p99 compute < 1 ms per update on one core.

## Acceptance criteria

- [ ] Registry, store and publish path working
- [ ] Parity harness used by all later feature sets
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Warm-up not satisfied: publish `None` with `warming_up=true`, never a partial value.
- Feature version deprecated: still readable for reproduction; not selectable for new strategies.

## Cardinal rules (do NOT)

- Do NOT compute research features from raw tables; use `pit`.
- Do NOT change a published feature version in place.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M6: registry/versioning contract.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.29 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T120-feature-registry-and-store`
- PR title: `P2-T120: mt_features registry, versioning and batch/incremental parity`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T120` run

## Progress log

- 2026-10-21 00:00 · planner · created
