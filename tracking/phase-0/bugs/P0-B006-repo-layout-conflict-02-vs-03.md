---
id: P0-B006
kind: gap
title: Repository layout conflicts between 02 §11 and 03 §3
phase: 0
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.01]
roadmap_todos: [T0.20]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B006-repo-layout-conflict-02-vs-03
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §3 vs docs/02-v1-architecture.md §11
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B006 · Repository layout conflicts between 02 §11 and 03 §3

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Follow 02 §11 (newer, matches 02 §10 React SPA); update 03 §3 and M15 wording ('mt_ui: Telegram bot; web app in apps/web').

## Context & references

- Found in: `docs/03-build-spec.md §3 vs docs/02-v1-architecture.md §11`
- Related: P0-T014, P0-T047
- [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout)
- [02 §11 repo layout](../../../docs/02-v1-architecture.md#11-repository-layout)
- [03 M15](../../../docs/03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api)

## Requirements

- **Steps to reproduce:** Compare the two trees.
- **Expected:** One layout.
- **Actual:** 03 §3: `docker-compose.yml` at root, migrations inside `mt_store`, `mt_ui` = 'FastAPI web UI + Telegram bot', no `apps/`, `infra/`. 02 §11: `infra/docker-compose.yml`, root `migrations/`, `apps/web/` React app, `mt_ui` = Telegram only.
- **Impact:** The monorepo skeleton task must guess; the web stack choice (FastAPI-rendered vs React SPA) is ambiguous in 03.
- **Suggested fix:** Follow 02 §11 (newer, matches 02 §10 React SPA); update 03 §3 and M15 wording ('mt_ui: Telegram bot; web app in apps/web').

## ToDo

- [x] Decision taken: 17 §B P0-B006 (ratified in 17 §E)
- [x] Docs updated so they agree: 03 §3 (canonical layout with `apps/web/`, `infra/`, `migrations/`, `mt_ui` = Telegram bot); 02 §11 now points to 03 §3
- [x] Affected P0 task files reference the resolution: P0-T014, P0-T047
- [x] Regression check owned: P0-T014 skeleton follows 03 §3

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §B P0-B006 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T014
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/03-build-spec.md`: reconcile as described.
- `docs/02-v1-architecture.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B006-repo-layout-conflict-02-vs-03`
- PR title: `P0-B006: fix repository layout conflicts between 02 §11 and 03 §3`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B006` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B006; docs checked: 03 §3 (canonical layout with `apps/web/`, `infra/`, `migrations/`, `mt_ui` = Telegram bot); 02 §11 now points to 03 §3. Root cause: 02 §11 was written after 03 §3 and never back-ported. Implementation owned by P0-T014.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B006); docs updated: 03 §3 (canonical layout with `apps/web/`, `infra/`, `migrations/`, `mt_ui` = Telegram bot); 02 §11 now points to 03 §3; implementation owned by P0-T014
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
