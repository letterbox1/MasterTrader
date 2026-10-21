---
id: P6-T018
kind: task
title: Question registry v2, ~320-token state builder and per-question thresholds
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.13]
roadmap_todos: [T6.26]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T018-question-registry-v2-state-budget
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T018 · Question registry v2, ~320-token state builder and per-question thresholds

## Goal / expected outcome

The tier-B question registry (from P4) is extended so every question is binary/low-option, has a **~320-token state budget**, per-question abstention and veto thresholds, versioning via `models.question.update`, the social-battery questions, and refuses Telegram rows at the boundary.

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.26
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) operating rules (state budget, per-question thresholds, social battery, Telegram refusal) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`models.question.update` C1, new version)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Decision questions tab
- Cross-phase: P4 R4.12 (registry v1, SemIf), P4 R4.03 (Telegram gate)

## Requirements

- `models.question` v2 columns: `options` (≤ 5; binary preferred), `state_budget_tokens` (default 320), `state_template` id, `abstain_threshold`, `veto_threshold` (null unless a veto question), `target_precision`, `serving_model_id`, `version`, `status`.
- State builder: compact structured state (JSON fields, numeric features, ≤ N short text spans) rendered and **tokenizer-counted** for the serving model; over budget → deterministic truncation by field priority, never raw documents.
- Boundary check: any input row with `model_input_ok=false` (Telegram, Birdeye, Etherscan…) raises `ProvenanceRefused` before tokenisation; counter per question.
- Social battery questions (X/Bluesky/Discord/Farcaster text only): `organic`, `bot_like`, `scam_language`, `narrative`, `stance`, `conviction`.
- Edits create a new version (old rows immutable); decisions log `question_version`.

## ToDo

- [ ] Migration for registry v2 columns + seed the social battery questions.
- [ ] State builder + tokenizer counting per model family (Qwen3 tokenizer).
- [ ] Provenance boundary guard in `decision-svc` request path.
- [ ] `models.question.update` command handler (C1) with versioning.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: budget truncation deterministic; option-count validator; version bump on edit.
- Property: rendered state never exceeds budget for random inputs.
- Integration: a Telegram-sourced row is refused at `models.tierb.ask` and in the `text.doc.new` path.

### Scenarios
- Given a 3,000-token filing excerpt, when building state for `event_type`, then the state is ≤ 320 tokens with the highest-priority fields kept.
- Given an edit to `veto` options, then a new version is created and old decisions keep their version.
- Given a Bluesky post, then the social battery returns six scores; given a Telegram message, then the request is refused.

### Stress / failure injection
- 10k state builds/s on CPU (budget check is not the bottleneck); p99 < 2 ms per build.

## Acceptance criteria

- [ ] All questions in registry v2 have budgets and thresholds.
- [ ] Telegram refusal test green.
- [ ] Social battery questions registered.

## Exceptions & edge cases

- Tokenizer mismatch after model swap → registry flags questions needing re-validation.

## Cardinal rules (do NOT)

- Do NOT feed raw documents to tier B; state only.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: state template format.
- `docs/02-v1-architecture.md` §5.3: `question` columns.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.26 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T018-question-registry-v2-state-budget`
- PR title: `P6-T018: Question registry v2, ~320-token state builder and per-question thresholds`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
