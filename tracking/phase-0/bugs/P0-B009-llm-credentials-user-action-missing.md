---
id: P0-B009
kind: gap
title: Roadmap USER list lacks obtaining LLM API credentials
phase: 0
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.09]
roadmap_todos: [T0.45]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B009-llm-credentials-user-action-missing
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md §4 A
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B009 · Roadmap USER list lacks obtaining LLM API credentials

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Add a T0.13-style USER ToDo to the roadmap (tracked here as P0-T007).

## Context & references

- Found in: `docs/roadmap/phase-0-foundations.md §4 A`
- Related: P0-T007, P0-T042

## Requirements

- **Steps to reproduce:** R0.09 needs Claude and your custom endpoint; check §4 A for a USER item to obtain them.
- **Expected:** A USER ToDo: Anthropic API key with spend limit + custom endpoint URL/key + per-role budgets.
- **Actual:** Missing; only data keys (T0.10) are listed.
- **Impact:** LiteLLM smoke calls (R0.09 verification) block on an unplanned user action.
- **Suggested fix:** Add a T0.13-style USER ToDo to the roadmap (tracked here as P0-T007).

## ToDo

- [x] Decision taken: 17 §D P0-B009 (ratified in 17 §E)
- [x] Docs updated so they agree: roadmap P0 §4 A: USER ToDo T0.13 (Anthropic + custom-endpoint keys into the secrets file); roadmap README user-action register; 07 §2 'What goes in it'
- [x] Affected P0 task files reference the resolution: P0-T007, P0-T042, P0-T068
- [x] Regression check owned: P0-T068 depends on P0-T007

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B009 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T007 (USER), P0-T068 (live smoke)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/phase-0-foundations.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B009-llm-credentials-user-action-missing`
- PR title: `P0-B009: fix roadmap USER list lacks obtaining LLM API credentials`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B009` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B009; docs checked: roadmap P0 §4 A: USER ToDo T0.13 (Anthropic + custom-endpoint keys into the secrets file); roadmap README user-action register; 07 §2 'What goes in it'. Root cause: the USER list covered data keys but not LLM keys. Implementation owned by P0-T007 (USER), P0-T068 (live smoke).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B009); docs updated: roadmap P0 §4 A: USER ToDo T0.13 (Anthropic + custom-endpoint keys into the secrets file); roadmap README user-action register; 07 §2 'What goes in it'; implementation owned by P0-T007 (USER), P0-T068 (live smoke)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
