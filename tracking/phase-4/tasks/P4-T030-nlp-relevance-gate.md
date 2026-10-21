---
id: P4-T030
kind: task
title: nlp relevance gate via SemIf with per-source caps and hit-rate tracking
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T027, P4-T029]
requirements: [R4.06, R4.12]
roadmap_todos: [T4.23, T4.28]
modules: [M2, M21]
dashboards: [D08]
branch: p4/P4-T030-nlp-relevance-gate
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T030 · nlp relevance gate via SemIf with per-source caps and hit-rate tracking

## Goal / expected outcome

The `nlp` pipeline asks `relevance{yes,no}` ("is this about a tradable instrument or macro event in my universe?") before FinBERT/embeddings, keeps only documents above the gate threshold for scoring and RAG, enforces per-source caps, and tracks each source's **relevance hit-rate** for D08 Sources and source tuning.

## Context & references

- Roadmap: [R4.06, R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDos [T4.23, T4.28](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Risk 'Source volume overwhelms the relevance gate'
- Design: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (SemIf replaces the planned LLM gate) · [06 §2 processing chain](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)
- Related: P4-T048 (threshold calibration), P4-T053 (precision/recall).

## Requirements

- Stage order: provenance gate → dedupe → **relevance gate** → linking (already done) → FinBERT → embeddings → store (irrelevant docs stored headline-only with `relevance` score, no embedding).
- Initial threshold 0.5 on P(yes); replaced by the calibrated value from P4-T048.
- Cheap pre-filter: docs with zero linked entities and no watchlist keyword skip SemIf and get `relevance=0` (saves load).
- Per-source caps (docs/hour, default 200) with overflow stored headline-only and counted; mute honoured.
- Hit-rate per source = relevant / ingested over 7 days, exposed on `text.source` and `/data/feeds?kind=text`.
- When decision-svc is degraded: fall back to the keyword/entity pre-filter only, flag docs `relevance_fallback=true`.

## ToDo

- [ ] Gate stage + pre-filter.
- [ ] Caps + overflow accounting.
- [ ] Hit-rate aggregation job.
- [ ] Fallback mode.
- [ ] Tests.

## Verification

### Tests
- Unit: pre-filter routing.
- Unit: cap overflow → headline-only.
- Integration: gate decision persisted on the doc and visible on `text.doc.new`.

### Scenarios
- Given a source floods 2,000 items/hour, then 200 are gated and the rest stored headline-only with a D08 warning.
- Given decision-svc is down, then the keyword fallback is used and flagged.

### Stress / failure injection
- Covered by P4-T058 (source flood + decision-svc down).

## Acceptance criteria

- [ ] Gate active; hit-rate visible per source
- [ ] Fallback mode tested
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Postgres down (02 §9.3): consumers pause and resume from the JetStream durable cursor; no item lost or duplicated.

## Cardinal rules (do NOT)

- Do NOT drop documents silently; irrelevant ones are kept headline-only for audit and hit-rate.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 processing chain: gate = SemIf, caps, fallback
- `docs/roadmap/phase-4-intel.md`: tick T4.23, T4.28 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T030-nlp-relevance-gate`
- PR title: `P4-T030: nlp relevance gate via SemIf with per-source caps and hit-rate tracking`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
