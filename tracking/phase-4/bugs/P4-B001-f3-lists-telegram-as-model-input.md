---
id: P4-B001
kind: gap
title: 02 F3 lists Telegram as an input to the text → decision-model chain
phase: 4
type: DOC
status: backlog
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
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §8 F3 (also §3.2 ingest-text row)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
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

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given a developer reads only 02 F3, then they would not wire Telegram into nlp.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

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
