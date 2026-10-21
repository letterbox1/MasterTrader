---
id: P6-B009
kind: gap
title: Crowd-sim: MiroFish needs Zep Cloud (no local fallback), open CORS and a default secret — conflicts with self-hosted/free/no-telemetry
phase: 6
type: DOC
status: backlog
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
branch: p6/P6-B009-mirofish-zep-cloud-conflict
pr: ""
doc_sync: [docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M14; docs/research/mirofish.md
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Propose the M14 wording.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] M14 names the clean-room path.
- [ ] Root cause noted in the progress log.

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
