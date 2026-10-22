---
id: P4-T025
kind: task
title: Provenance gate library and nlp entry point
phase: 4
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T008, P1-T030]
requirements: [R4.03, R4.06]
roadmap_todos: [T4.23]
modules: [M2, M9, M21]
dashboards: [D08]
tools: [uv, git, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p4/P4-T025-provenance-gate
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
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

# P4-T025 · Provenance gate library and nlp entry point

## Goal / expected outcome

One shared guard, `mt_store.provenance.require_model_input(rows)` (and `require_train_ok`), is the **first** step of the `nlp` service and is called at every model boundary (FinBERT, TEI embeddings, SemIf/tier B question boundary, RAG indexer and retriever, agent context builder). Rows with `model_input_ok = false`, and every row whose source kind is `telegram`, are refused and audited as a WORM `audit.dq_event` row of kind `provenance_refusal` (canonical audit names, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)).

## Context & references

- Roadmap: [R4.03, R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.23](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (inference paths refuse `model_input_ok=false`; training refuses `train_ok=false`) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements)
- Flow: [02 F3](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (provenance checked first) · operating rules [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design)
- Decision: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B001): F3 starts with a provenance gate and excludes Telegram; Telegram has its own branch F3b → postures ([02 §8](../../../docs/02-v1-architecture.md#8-end-to-end-flows)).
- Cross-phase: P1-T030 (`audit.dq_event` WORM table) is a `depends_on` entry.
- Verified end-to-end by P4-T050.

## Requirements

- Guard is a pure function + decorator `@model_input` for any callable that sends data to a model; raises/filters and emits an `audit.dq_event` row (`kind = provenance_refusal`; WORM insert) with row id, source, boundary name.
- Double check: flag check **and** source-kind check (`telegram` refused even if a flag were mis-set).
- The `nlp` consumer of `raw.text.>` drops `raw.text.telegram*` subjects at subscribe level (never subscribes), never subscribes to `posture.telegram.>`, and applies the guard to everything else.
- Static check (CI): any call into `transformers`, TEI client, decision-svc client, LiteLLM client or RAG writer outside a `@model_input`-guarded function fails the build (AST lint rule in `tools/lint/provenance_lint.py`).
- Overhead < 50 µs per row.

## ToDo

- [ ] Implement `mt_store.provenance` guard, decorator and refusal audit writer (`audit.dq_event`, kind `provenance_refusal`).
- [ ] AST lint rule + CI wiring.
- [ ] `nlp` service skeleton (`mt_features.text.service`): durable consumer on `raw.text.>` excluding Telegram, guard first, then stage pipeline hooks (P4-T026/T027/T030).
- [ ] Document the boundaries list in `packages/mt_store/provenance/README.md`.

## Verification

### Tests
- Unit: rows with each flag combination; telegram source with forged `model_input_ok=true` still refused.
- Lint test: a fixture module calling the TEI client unguarded fails the lint.
- Integration: `raw.text.telegram` message published by a test producer is never consumed by `nlp`.

### Scenarios
- Given Finnhub rows flagged `model_input_ok=false`, then they are stored and displayed but skip FinBERT/embeddings/tier B with one refusal audit row each.
- Given the audit table is unavailable, then the guard still refuses (fail closed) and buffers the audit insert.

### Stress / failure injection
- 1M guard calls: p99 < 50 µs; refusal audit inserts batched without blocking the pipeline.

## Acceptance criteria

- [ ] Guard + lint in CI; all known model boundaries decorated
- [ ] Telegram never consumed by `nlp` (test)
- [ ] Refusals audited in `audit.dq_event` (WORM)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Display paths (D08) are not model boundaries and may show `display_ok` rows; Telegram text is still never displayed (postures only).

## Cardinal rules (do NOT)

- Do NOT add an override flag or bypass parameter to the guard.
- Do NOT update refusal audit rows.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: §5: name the guard and its boundaries
- `docs/02-v1-architecture.md`: §8 F3: provenance gate as step 0
- `docs/roadmap/phase-4-intel.md`: tick T4.23 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T025-provenance-gate`
- PR title: `P4-T025: Provenance gate library and nlp entry point`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (refusals audited in canonical audit.dq_event (17 §B); F3 provenance-first per 17 §A P4-B001; added P4-T008 and P1-T030 dependencies)
