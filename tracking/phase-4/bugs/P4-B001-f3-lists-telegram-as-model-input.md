---
id: P4-B001
kind: gap
title: 02 F3 lists Telegram as an input to the text → decision-model chain
phase: 4
type: DOC
status: done
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.03, R4.06]
roadmap_todos: []
modules: [M2, M21]
dashboards: []
branch: p4/P4-B001-f3-lists-telegram-as-model-input
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §8 F3 (also §3.2 ingest-text row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P4-B001 · 02 F3 lists Telegram as an input to the text → decision-model chain

## Goal / expected outcome

Flow F3 makes clear that Telegram never enters the nlp/decision-model chain: Telegram has its own branch (regex → postures → code/policy), and F3 starts with a provenance gate.

## Context & references

- Found in: [02 §8 F3](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 1 'A feed (RSS / Telegram / Discord / Bluesky / GDELT) arrives' → step 3 relevance gate/FinBERT/TEI
- Contradicts: [R4.03](../../../docs/roadmap/phase-4-intel.md#3-requirements) · [12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements) · [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext) (no model ever sees Telegram text)
- Related tasks: P4-T025, P4-T019, P4-T050.

## Requirements

- **Steps to reproduce:** read 02 §8 F3 step 1–3.
- **Expected:** F3 step 0 = provenance gate; Telegram excluded; a separate 'F3b Telegram → postures' flow (Telethon/Bot API/RSS-Bridge → regex extractors → `text.tg_mention`/`text.tg_posture` → `posture.tg.*` → code/policy consumers).
- **Actual:** Telegram is listed as an F3 input flowing into the relevance gate, FinBERT and TEI.
- **Impact:** S2 — an implementer following F3 would breach Telegram API ToS §1.5 and the phase exit criterion 3.
- **Suggested fix:** edit F3 as above; in §3.2 note 'Telegram: postures only' on the ingest-text row.

## ToDo

- [x] Decision recorded: 02 F3 split; Telegram → regex extractor → postures → code/policy only; every other source → model chain (17 §A P4-B001)
- [x] Docs carry it: 02 §8 F3 ('every source except Telegram', provenance gate first) and new F3b 'Telegram → postures'; 02 §3.2 ingest-text row 'Telegram: postures only'; 12 §4–5
- [x] Implementation owned by tasks P4-T025 (gate, nlp never subscribes to Telegram), P4-T019 (F3b postures), P4-T050 (gate test)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given a developer reads only 02 F3, then they would not wire Telegram into nlp.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] 02 F3 no longer lists Telegram as a model-chain input; F3b exists (checked in 02 §8, 2026-10-22)
- [x] Root cause noted: F3 was written before the postures-only rule was applied to the flow list

## Exceptions & edge cases

- P4 tasks already implement the correct behaviour (P4-T025 never subscribes `raw.text.telegram*`).

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §8 F3 + new F3b; §3.2 ingest-text note

## Branch & PR

- Branch: `p4/P4-B001-f3-lists-telegram-as-model-input`
- PR title: `P4-B001: fix 02 F3 lists Telegram as an input to the text → decision-model chain`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B001` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P4-B001); docs checked: 02 §8 F3 + F3b, 02 §3.2 ingest-text row, 12 §4–5; implementation owned by P4-T025, P4-T019, P4-T050, P4-T057; root cause: F3 predated the postures-only rule in 12 §4
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P4-B001); docs updated: 02 §8 F3 + new F3b, 02 §3.2 ingest-text row, 12 §4-5; implementation owned by P4-T025, P4-T019, P4-T050, P4-T057
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
