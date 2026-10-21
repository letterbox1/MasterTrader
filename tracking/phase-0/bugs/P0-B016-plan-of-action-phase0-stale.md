---
id: P0-B016
kind: gap
title: 04 plan of action Phase 0 is stale (Ollama, daily hash chain, missing Caddy/LiteLLM/TEI)
phase: 0
type: DOC
status: ready
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.02, R0.07]
roadmap_todos: [T0.41, T0.23]
modules: []
dashboards: []
branch: p0/P0-B016-plan-of-action-phase0-stale
pr: ""
doc_sync: [docs/04-plan-of-action.md]
doc_sync_status: n/a
found_in: docs/04-plan-of-action.md Phase 0
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B016 · 04 plan of action Phase 0 is stale (Ollama, daily hash chain, missing Caddy/LiteLLM/TEI)

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Update 04 Phase 0 bullets to match R0.02/R0.07 or replace them with a link to the phase doc.

## Context & references

- Found in: `docs/04-plan-of-action.md Phase 0`
- Related: P0-T020, P0-T029
- [04 do-this-week](../../../docs/04-plan-of-action.md#️-do-this-week-regardless-of-phase)

## Requirements

- **Steps to reproduce:** Compare 04 Phase 0 with the roadmap phase doc and 15 §2.
- **Expected:** 04 summarises the roadmap without contradicting it.
- **Actual:** 04 lists Ollama in compose and 'append-only audit roles + daily hash chain' (pre-WORM design: no per-row chain, external seals, offline owner); omits Caddy and mt_api/web shell details.
- **Impact:** Low: readers of 04 get an outdated design.
- **Suggested fix:** Update 04 Phase 0 bullets to match R0.02/R0.07 or replace them with a link to the phase doc.

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

- `docs/04-plan-of-action.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B016-plan-of-action-phase0-stale`
- PR title: `P0-B016: fix 04 plan of action Phase 0 is stale (Ollama, daily hash chain, missing Caddy/LiteLLM/TEI)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B016` run

## Progress log

- 2026-10-21 00:00 · planner · opened
