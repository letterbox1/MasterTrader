---
id: P0-B009
kind: gap
title: Roadmap USER list lacks obtaining LLM API credentials
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B009-llm-credentials-user-action-missing
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md §4 A
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

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
