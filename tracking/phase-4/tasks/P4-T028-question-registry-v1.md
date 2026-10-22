---
id: P4-T028
kind: task
title: Tier B question registry v1, models schema and decision audit
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T029, P0-T030]
requirements: [R4.12]
roadmap_todos: [T4.28]
modules: [M21]
dashboards: [D10]
tools: [uv, git]
mcp: []
env: []
services: [postgres]
branch: p4/P4-T028-question-registry-v1
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
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

# P4-T028 · Tier B question registry v1, models schema and decision audit

## Goal / expected outcome

`mt_models` has a versioned question registry (`models.question`), a stage-1 model registry entry type, and the WORM `audit.tierb_decision` table; v1 questions are defined: `relevance{yes,no}`, `news_direction{bull,bear,neutral}`, `event_type{guidance_cut,M&A,hack,listing,regulation,macro_release,cb_policy,other}`, `veto{yes,no}`, plus first flags `regime_hint{trend,range,crisis}`.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.28](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (typed, versioned questions; ~320-token state budget; binary/low-option only) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Architecture: [02 §4 M21 row](../../../docs/02-v1-architecture.md#4-logical-components) (`models.registry`, `models.question`, `audit.tierb_decision`)
- Decision: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P4-B006): all 13 schemas incl. `models` and `rag` are created in P0 (P0-T024); this task only adds tables. Cross-phase `depends_on`: P0-T024 (schemas), P0-T029/P0-T030 (WORM triggers and hash chain for `audit.tierb_decision`).
- UI: [D10 Decision questions](../../../docs/ui/dashboards/D10-models-memory.md) (full UI in P6).

## Requirements

- `models.question`: id, version, type (choice/score/yes-no), options[], prompt template, state builder ref, state token budget (default 320), threshold(s), status (draft/active/retired); a new version is a new row. Threshold defaults come from [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (auto-decide at ≥ 0.75 precision, direct veto only at ≥ 0.90 precision, ECE ≤ 0.05), configurable per question.
- `audit.tierb_decision` (WORM, hash-chained): decision id, question id+version, subject (doc id / instrument), probabilities, model revision, `prompt_hash`, backend, latency, abstained bool.
- State builders produce compact structured state (title, first 2 paragraphs, tickers, source, time) within budget; **refuse** Telegram/`model_input_ok=false` subjects via the P4-T025 guard.
- Endpoints (via P4-T043): `/models/questions`, `/models/tierb/decisions`; command `models.question.update` (C1).

## ToDo

- [ ] Alembic migrations for `models.registry`, `models.question` and `audit.tierb_decision` (tables only; schemas exist from P0; WORM triggers from P0-T029/T030). `models.label` is added by P4-T062.
- [ ] Question YAMLs in `config/models/questions/*.yaml` + loader.
- [ ] State builders + token-budget enforcer (tokenizer of the pinned model).
- [ ] Tests.

## Verification

### Tests
- Unit: state builder never exceeds 320 tokens on a long 10-K section.
- WORM: UPDATE/DELETE on `audit.tierb_decision` fails.
- Unit: question version bump creates a new row; old decisions keep their version.

### Scenarios
- Given a question template changes, then `prompt_hash` changes and decisions are attributable to the exact version.
- Given a Telegram doc id as subject, then the state builder refuses (guard).

### Stress / failure injection
- n/a: schema/registry work; throughput covered in P4-T029.

## Acceptance criteria

- [ ] v1 questions registered and loadable
- [ ] WORM + budget tests pass
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- The `models` schema exists from P0 (17 §B); migrations only add tables and fail loudly if the schema is missing.

## Cardinal rules (do NOT)

- Do NOT allow open-ended/generative questions in the registry.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3: list question registry v1
- `docs/03-build-spec.md`: M21: stage 1 question set
- `docs/roadmap/phase-4-intel.md`: tick T4.28 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T028-question-registry-v1`
- PR title: `P4-T028: Tier B question registry v1, models schema and decision audit`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (schemas created in P0 per 17 §B (P4-B006); tier-B threshold defaults linked to 16 §2.10; explicit P0 depends_on)
