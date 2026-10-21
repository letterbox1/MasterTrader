---
id: P0-B013
kind: gap
title: DESIGN §6.2 `tablet-landscape` query is missing from the §6.3 Tailwind config
phase: 0
type: DOC
status: ready
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.11, R0.N6]
roadmap_todos: [T0.26]
modules: []
dashboards: []
branch: p0/P0-B013-tailwind-tablet-landscape-screen-missing
pr: ""
doc_sync: [DESIGN.md]
doc_sync_status: n/a
found_in: DESIGN.md §6.3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B013 · DESIGN §6.2 `tablet-landscape` query is missing from the §6.3 Tailwind config

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Add `'tablet-landscape': { raw: '(orientation: landscape) and (min-width: 1024px) and (max-height: 820px)' }` to §6.3.

## Context & references

- Found in: `DESIGN.md §6.3`
- Related: P0-T047
- [DESIGN §6.3 Tailwind preset](../../../DESIGN.md#63-tailwind-configuration-use-in-every-implementation-and-mock-up)

## Requirements

- **Steps to reproduce:** Compare the raw queries in §6.2 (incl. `tablet-landscape`) with `screens` in §6.3.
- **Expected:** Every named raw query in §6.2 has a Tailwind screen in §6.3.
- **Actual:** `tablet-landscape` is absent from the config.
- **Impact:** Low: developers can't use the named variant; rules for short laptops get hand-written.
- **Suggested fix:** Add `'tablet-landscape': { raw: '(orientation: landscape) and (min-width: 1024px) and (max-height: 820px)' }` to §6.3.

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

- `DESIGN.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B013-tailwind-tablet-landscape-screen-missing`
- PR title: `P0-B013: fix dESIGN §6.2 `tablet-landscape` query is missing from the §6.3 Tailwind config`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B013` run

## Progress log

- 2026-10-21 00:00 · planner · opened
