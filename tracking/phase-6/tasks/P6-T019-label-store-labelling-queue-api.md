---
id: P6-T019
kind: task
title: Label store with provenance and the labelling-queue API
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T018, P4-T062]
requirements: [R6.13]
roadmap_todos: [T6.26]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, prefect, mt-api]
branch: p6/P6-T019-label-store-labelling-queue-api
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/ui/dashboards/D10-models-memory.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T019 · Label store with provenance and the labelling-queue API

## Goal / expected outcome

Training labels come **only from outcomes or from you**: a `models.label` store whose `label_source` can't be `shadow`/`model`, a sampler that fills the D10 labelling queue (abstentions, teacher disagreements, high-value calls), and the `models.label.add` command (C0).

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.26
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (labels from outcomes or you, never shadow outputs) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (`train_ok`)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Additions (labelling queue, `models.label.add` C0)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B004: labels endpoint/command and the D10 queue tab; now in 02 §7.1–7.2 and D10)
- Cross-phase: P4-T062 (`models.label` table, `models.label.add` C0, D08 Label mode)
- Depends on (this phase): P6-T018

## Requirements

- `models.label` already exists from P4 (P4-T062: insert-only, source `user` | `outcome`). Extend it additively (decision ref, labeller, note, queue item ref, a DB CHECK on the source column if P4 didn't add one); never re-create it. Corrections are new rows superseding old.
- `models.shadow_check` lives in a separate table; there is no code path or FK that writes a shadow output into `models.label` (enforced by role grants: shadow writer has no INSERT on `models.label`).
- Queue sampler (Prefect hourly): abstentions, shadow disagreements, high-value calls (by notional/EV), stratified per question; target ~15 min/day of items (default 40/day); excludes rows with `train_ok=false`.
- API: add `GET /models/labels/queue` and extend `GET /models/labels` (`?question=`); reuse the P4 `models.label.add` command (C0, audited, idempotent), adding the queue item reference.
- Outcome labels written by the settlement-driven job (P6-T020) with `label_source=outcome`.

## ToDo

- [ ] Additive migration (`models.label` columns, `models.label_queue`, role grants).
- [ ] Sampler flow and queue API.
- [ ] `models.label.add` handler; Telegram inline quick-label optional (C0).
- [ ] Tests; docs (02 §7 already lists the command and endpoints; document the queue payload).

## Verification

### Tests
- Unit: sampler stratification and daily cap.
- DB: INSERT into `models.label` with `label_source='shadow'` fails; shadow writer role lacks grant.
- API: label add is idempotent and audited.

### Scenarios
- Given a tier-B abstention on `news_direction`, then it appears in the queue within an hour.
- Given you label it `bear`, then a `user` label row exists and the item leaves the queue.
- Given a queue item whose document has `train_ok=false`, then it is never sampled.

### Stress / failure injection
- Queue with 50k candidates: sampler runs < 60 s; API p95 < 200 ms.

## Acceptance criteria

- [ ] No path writes shadow outputs as labels (DB + code tests).
- [ ] Queue API serves D10.
- [ ] Queue endpoint payload documented in 02 §7.1.

## Exceptions & edge cases

- Conflicting user and outcome labels: both kept; training uses the documented precedence (user > outcome for text questions; outcome for direction questions).

## Cardinal rules (do NOT)

- Do NOT ever create labels from shadow-model or other-model outputs.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: label precedence.
- `docs/02-v1-architecture.md` §7.1/§7.2: labels endpoint and `models.label.add`.
- `docs/ui/dashboards/D10-models-memory.md`: queue sampling rules.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.26 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T019-label-store-labelling-queue-api`
- PR title: `P6-T019: Label store with provenance and the labelling-queue API`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (extends P4 models.label/models.label.add (P4-T062) instead of re-creating; labels endpoint + D10 queue tab per 17 §D P6-B004; run fields)
