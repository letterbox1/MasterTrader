---
id: P0-B016
kind: gap
title: 04 plan of action Phase 0 is stale (Ollama, daily hash chain, missing Caddy/LiteLLM/TEI)
phase: 0
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B016-plan-of-action-phase0-stale
pr: ""
doc_sync: [docs/04-plan-of-action.md]
doc_sync_status: done
found_in: docs/04-plan-of-action.md Phase 0
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision taken: 17 §D P0-B016 (ratified in 17 §E)
- [x] Docs updated so they agree: 04 Phase 0 (no Ollama; WORM layer with offline `worm_owner`, per-row chain, external seal; Caddy; `mt_api` + web shell; `llm-local`; two TEI containers; docker-proxy)
- [x] Affected P0 task files reference the resolution: P0-T020, P0-T029
- [x] Regression check owned: doc check: 04 Phase 0 matches the roadmap phase doc

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B016 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: n/a (doc only)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B016; docs checked: 04 Phase 0 (no Ollama; WORM layer with offline `worm_owner`, per-row chain, external seal; Caddy; `mt_api` + web shell; `llm-local`; two TEI containers; docker-proxy). Root cause: 04 summarised an earlier design and wasn't refreshed after 15 §2. Implementation owned by n/a (doc only).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B016); docs updated: 04 Phase 0 (no Ollama; WORM layer with offline `worm_owner`, per-row chain, external seal; Caddy; `mt_api` + web shell; `llm-local`; two TEI containers; docker-proxy); implementation owned by n/a (doc only)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
