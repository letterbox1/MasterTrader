---
id: P6-B009
kind: gap
title: Crowd-sim: MiroFish needs Zep Cloud (no local fallback), open CORS and a default secret — conflicts with self-hosted/free/no-telemetry
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.32]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B009-mirofish-zep-cloud-conflict
pr: ""
doc_sync: [docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M14; docs/research/mirofish.md
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B009 · Crowd-sim: MiroFish needs Zep Cloud (no local fallback), open CORS and a default secret — conflicts with self-hosted/free/no-telemetry

## Goal / expected outcome

The docs agree and are specific enough to build from: M14 states the allowed path: clean-room on CAMEL-AI OASIS (Apache-2.0) with a local LLM and our memory, isolated; MiroFish reference only.

## Context & references

- Found in: docs/03-build-spec.md M14; docs/research/mirofish.md
- [03 M14](../../../docs/03-build-spec.md#m14-crowd-simulation-optional) · [research: MiroFish](../../../docs/research/mirofish.md)
- Affects: P6-T050

## Requirements

- **Steps to reproduce:** read docs/03-build-spec.md M14; docs/research/mirofish.md and compare it with the cross-referenced sections listed under Context.
- **Expected:** M14 states the allowed path: clean-room on CAMEL-AI OASIS (Apache-2.0) with a local LLM and our memory, isolated; MiroFish reference only.
- **Actual:** 03 M14 and R6.32 say 'MiroFish/OASIS crowd-sim'; the research notes show MiroFish requires Zep Cloud, has CORS *, a default SECRET_KEY and no auth, and is AGPL.
- **Suggested fix:** Amend 03 M14 accordingly; P6-T050 follows the clean-room path.
- **Impact:** Could pull a cloud dependency and an insecure service into the stack (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P6-B009): MiroFish/OASIS only with a local memory backend and hardened config; no Zep Cloud; otherwise M14 is skipped
- [x] Owning docs carry it: 03 M14; roadmap R6.32 and T6.30; 04 Phase 6 optional bullet
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T050 (crowd-sim, optional), P6-T003 (your decision)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (03 M14; roadmap R6.32 and T6.30; 04 Phase 6 optional bullet)
- [x] Affected tasks consistent with it (P6-T050 (crowd-sim, optional), P6-T003 (your decision))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT run MiroFish with Zep Cloud.
- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/03-build-spec.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B009-mirofish-zep-cloud-conflict`
- PR title: `P6-B009: Crowd-sim: MiroFish needs Zep Cloud (no local fallback), open CORS and a default secret — conflicts with self-hosted/free/no-telemetry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P6-B009: MiroFish/OASIS only with a local memory backend and hardened config; no Zep Cloud; otherwise M14 is skipped. Docs now carry it: 03 M14; roadmap R6.32 and T6.30; 04 Phase 6 optional bullet. Implementation owned by P6-T050 (crowd-sim, optional), P6-T003 (your decision). Root cause: MiroFish's default stack depends on Zep Cloud and ships an insecure default config.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P6-B009); docs updated: 03 M14, roadmap R6.32/T6.30, 04 Phase 6 optional bullet; implementation owned by P6-T050, P6-T003
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
