---
id: P4-T050
kind: task
title: Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)
phase: 4
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T019, P4-T025, P4-T027, P4-T029, P4-T030, P4-T032]
requirements: [R4.03, R4.02]
roadmap_todos: [T4.60]
modules: [M2, M9, M21]
dashboards: [D08]
branch: p4/P4-T050-verify-telegram-text-gate
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T050 · Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)

## Goal / expected outcome

An automated end-to-end test suite, run in CI and as part of the exit demo, proves that a Telegram message (with a unique canary string) produces postures but **never** appears in FinBERT inputs, TEI requests, decision-svc prompts, `rag.doc_chunk`, `text.document`, agent context builders, any training-set export, NATS payloads outside the Telegram ingest process, logs or API responses.

## Context & references

- Roadmap: [R4.03](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.60](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 3
- Policy: [12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements) · [10 §4.3 operating rules](../../../docs/10-memory-rag-and-models.md#43-design)
- Related: P4-T025 guard, P4-T019 postures.

## Requirements

- Canary: inject synthetic Telegram messages via a fake Telethon/Bot API source containing `MT-CANARY-<uuid>` + a valid EVM address.
- Probes: request spies on FinBERT runner, TEI client, decision-svc client, LiteLLM client, RAG writer; DB scan (`text.*`, `rag.*`, `models.*`, `audit.*`) for the canary; NATS tap on `>`; Loki query for the canary; API crawl of `/intel/*` and `/rag/search?q=<canary>`.
- Training-set exporters (`mt_lab`/`mt_models` dataset builders) run with Telegram rows present → zero Telegram rows exported.
- Forged-flag case: a Telegram row with `model_input_ok=true` forced in a test DB is still refused by every boundary.
- Positive control: the canary address **does** appear in `text.tg_mention` and postures.

## ToDo

- [ ] Write `tests/e2e/test_telegram_gate.py` + fixtures.
- [ ] Add NATS tap + Loki query helpers.
- [ ] Wire into CI (nightly + on PRs touching `mt_data/text`, `mt_features/text`, `mt_memory`, `mt_models`).
- [ ] Report artifact (JSON + markdown summary) saved for the exit demo.

## Verification

### Tests
- The suite itself (all probes above).
- Mutation check: temporarily removing the guard decorator in a test branch makes the suite fail (proves sensitivity).

### Scenarios
- Given a Telegram message mentioning `$ETH` and an address, then postures update and every probe reports zero canary hits.
- Given a developer adds a new model client without the guard, then the provenance lint (P4-T025) and this suite fail.

### Stress / failure injection
- Run with 10k canary messages: zero leaks; posture counts exact.

## Acceptance criteria

- [ ] Suite green in CI with zero canary hits outside allowed tables
- [ ] Mutation check proves the suite catches a removed guard
- [ ] Report saved for the exit demo
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Allowed locations: in-memory extractor only; `text.tg_mention` stores the extracted address, never the canary text.

## Cardinal rules (do NOT)

- Do NOT mark this suite flaky/skip; failures block merges.
- Do NOT use real Telegram content in fixtures.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: §5: reference the gate test as the enforcement proof
- `docs/roadmap/phase-4-intel.md`: tick T4.60 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T050-verify-telegram-text-gate`
- PR title: `P4-T050: Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
