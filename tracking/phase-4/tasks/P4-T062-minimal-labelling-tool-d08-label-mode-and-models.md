---
id: P4-T062
kind: task
title: Minimal labelling tool (D08 Label mode) and models.label.add command
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T028, P4-T030, P4-T043, P4-T044]
requirements: [R4.16, R4.12]
roadmap_todos: [T4.31]
modules: [M21, M2]
dashboards: [D08, D10]
tools: [uv, pnpm, node>=20, git]
mcp: []
env: []
services: [postgres, mt-api]
branch: p4/P4-T062-minimal-labelling-tool-d08-label-mode-and-models
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T062 · Minimal labelling tool (D08 Label mode) and models.label.add command

## Goal / expected outcome

You can label a stratified sample of ~200 documents relevant/irrelevant (plus optional direction/event type) in a **Label mode** on the D08 Feed, each label stored through the `models.label.add` command (C0) as an insert-only `models.label` row. Your labels (P4-T049) then calibrate the SemIf gate (P4-T048) and measure it (P4-T053). D10's full labelling queue reuses the same table and command in P6.

## Context & references

- Roadmap: [R4.16](../../../docs/roadmap/phase-4-intel.md#3-requirements) (minimal labelling tool + `models.label.add`, verified by a label flow test) · [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.31](../../../docs/roadmap/phase-4-intel.md#4-todo-sets); used by T4.04 (P4-T049)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B007): add `models.label.add` and a minimal labelling tool in P4
- UI: [D08 Label mode (Phase 4)](../../../docs/ui/dashboards/D08-intel.md) (`models.label.add`, C0; Telegram content is never offered) · [D10 Labelling queue](../../../docs/ui/dashboards/D10-models-memory.md) (P6, reuses the labels)
- API: [02 §7.2 Agents & models](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (`models.label.add` C0) · `/models/labels` query ([02 §7.1](../../../docs/02-v1-architecture.md#7-api-contract-mt_api))
- Labels rule: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design): labels come from outcomes or you, **never** from shadow-model outputs
- Related: P4-T028 (`models` tables), P4-T030 (gate scores for stratifying), P4-T043 (API router), P4-T044 (D08 document sheet), P4-T048, P4-T049, P4-T053, P4-T059 (viewport matrix includes Label mode).

## Requirements

- `models.label` (insert-only): id, subject (doc id), question id + version, label, optional direction/event type, `source` (`user` | `outcome`), batch id, labelled_at; the latest row per (subject, question) wins, older rows stay.
- Sampler: a batch of ~200 docs (configurable) stratified by source kind and by SemIf P(yes) decile; excludes Telegram (never sampled) and every `model_input_ok = false` row via the P4-T025 guard; the model score is hidden in Label mode.
- Command `models.label.add` (C0) through the `mt_api` command bus, audited in `audit.command`; query `/models/labels` (by batch, question, source) and `/models/labels/batches`.
- Label mode at `/intel?label=batch-<id>`: keyboard 1 / 0 / s (skip) on desktop, large buttons on phones; progress counter; resumable across sessions.
- Non-functional: label submit p95 < 200 ms; works at every DESIGN §6.8 tier; no shadow/teacher output can be written as a label (`source` limited to `user` from this UI).

## ToDo

- [ ] Migration for `models.label` (table only; schema from P0) + insert-only privileges
- [ ] Sampler + batch creation command/CLI (`mt_models.labels.sample`), guard applied
- [ ] `models.label.add` handler (C0) + `/models/labels` queries in `mt_api` (OpenAPI updated)
- [ ] D08 Label mode UI (keyboard + phone buttons, hidden scores, progress, resume)
- [ ] Post the batch link to your Telegram when a batch is ready (via the alert path)
- [ ] Tests (below), including the label flow test for R4.16
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: sampler never includes Telegram or `model_input_ok = false` rows (forged flags included).
- Unit: `models.label.add` rejects `source` other than `user` from the UI path; changing a label inserts a new row (old kept).
- API: command audited in `audit.command`; `/models/labels` filters and pagination.
- Playwright (label flow test, R4.16): label 5 docs by keyboard and 5 by phone buttons; reload resumes at the next unlabelled doc.

### Scenarios
- Given you change your mind on a document, when you relabel it, then a new row is inserted and the latest one counts.
- Given a batch has a doc that later becomes `model_input_ok = false` (terms change), then it's dropped from the batch and from calibration.
- Given you skip more than 20 docs, then a top-up batch from the same strata can be created.

### Stress / failure injection
- n/a: small human-labelling volume; 1,000-row label table queried in < 50 ms is enough (asserted in the API test).

## Acceptance criteria

- [ ] A ~200-doc batch can be created and labelled end to end on desktop and phone
- [ ] Labels stored insert-only via `models.label.add` (C0), audited
- [ ] Telegram and flagged rows never offered (test)
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix + axe)

## Exceptions & edge cases

- Paywalled/headline-only documents: label on the headline or skip.
- Postgres down: Label mode shows read-only with a banner; nothing is queued client-side.

## Cardinal rules (do NOT)

- Do NOT use shadow-model or teacher outputs as labels.
- Do NOT show the model's score in Label mode.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: mark Label mode implemented
- `docs/02-v1-architecture.md`: §7.1/§7.2: confirm `/models/labels` and `models.label.add` (C0) as built
- `docs/roadmap/phase-4-intel.md`: tick T4.31

## Branch & PR

- Branch: `p4/P4-T062-minimal-labelling-tool-d08-label-mode-and-models`
- PR title: `P4-T062: Minimal labelling tool (D08 Label mode) and models.label.add command`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T062` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R4.16 / T4.31 per 17 §D P4-B007; split out of P4-T048)
