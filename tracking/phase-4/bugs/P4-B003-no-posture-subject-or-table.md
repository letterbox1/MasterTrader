---
id: P4-B003
kind: gap
title: No NATS subject, table or consumer rule for Telegram postures
phase: 4
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.02, R4.03]
roadmap_todos: []
modules: [M2, M6]
dashboards: []
branch: p4/P4-B003-no-posture-subject-or-table
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/12-policy-and-compliance.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §4 (M2 row) and §6 (subject taxonomy); docs/12-policy-and-compliance.md §4
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B003 · No NATS subject, table or consumer rule for Telegram postures

## Goal / expected outcome

02 names where postures live and who may consume them, and 12 §4 states explicitly that postures are not M6 features for tier A/B models.

## Context & references

- Found in: [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M2 owns only `text.document`, `text.source`) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (no posture subject)
- Policy tension: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) bans 'any Telegram-derived feature in a model input' yet allows postures 'used by code/policy only'
- Related: P4-T010, P4-T019, P4-T040.

## Requirements

- **Steps to reproduce:** search 02 §4/§6 for a posture table or subject — none.
- **Expected:** tables `text.tg_mention`, `text.tg_posture` (`model_input_ok=false`, `train_ok=false`), subject `posture.tg.{subject}`, KV `tg_posture`, and a consumer allow-list (P5 airdrop rules, D08, brief) excluding M6 model features, tier A/B, agents, RAG.
- **Actual:** unspecified; M6 could pick postures up as a 'sentiment' input and tier A would then be a model trained on Telegram-derived data.
- **Impact:** S3 — ambiguity that risks a policy breach.
- **Suggested fix:** add the names above to 02 §4/§6 and one sentence to 12 §4 and 03 M6.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given M6 sentiment pipelines are built from 03 M6 alone, then postures could be ingested as features — P4-T040 excludes them explicitly.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- P5 deterministic airdrop rules may consume postures (code/policy).

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §4 M2 row and §6 subject table
- `docs/12-policy-and-compliance.md`: §4 consumer rule
- `docs/03-build-spec.md`: M6: postures excluded

## Branch & PR

- Branch: `p4/P4-B003-no-posture-subject-or-table`
- PR title: `P4-B003: fix no NATS subject, table or consumer rule for Telegram postures`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B003` run

## Progress log

- 2026-10-21 00:00 · planner · opened
