---
id: P4-B003
kind: gap
title: No NATS subject, table or consumer rule for Telegram postures
phase: 4
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/02-v1-architecture.md §4 (M2 row) and §6 (subject taxonomy); docs/12-policy-and-compliance.md §4
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: table `text.telegram_posture`, subject `posture.telegram.*`, consumers M4/M11 rules only (17 §D)
- [x] Docs carry it: 02 §4 M2/M4/M11 rows, §4 rule 'consumed only by code/policy rules', §5.2 `text` tables, §6 subject row; 03 M2 (postures only) and 03 M6 ('Telegram is never a feature'); 12 §4 bans Telegram-derived features in models
- [x] Implementation owned by P4-T010 (tables), P4-T019 (publisher, consumer allow-list), P4-T040 (features exclude postures), P4-T043 (`/intel/postures`)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given M6 sentiment pipelines are built from 03 M6 alone, then postures could be ingested as features — P4-T040 excludes them explicitly.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Posture table, subject and consumer rule documented (checked in 02 §4/§5.2/§6 and 03 M2/M6, 2026-10-22)
- [x] Root cause noted: postures were allowed in 12 §4 but never given a home in 02

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B002/B003); docs checked: 02 §4/§5.2/§6, 03 M2 + M6, 12 §4; implementation owned by P4-T010, P4-T019, P4-T040, P4-T043, P4-T050; root cause: 12 §4 allowed postures without a named table/subject in 02
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B002/B003); docs updated: 02 §4/§5.2/§6 (text.telegram_posture, posture.telegram.*, consumers M4/M11 rules), 03 M2 + M6, 12 §4; implementation owned by P4-T010, P4-T019, P4-T040, P4-T043, P4-T050
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
