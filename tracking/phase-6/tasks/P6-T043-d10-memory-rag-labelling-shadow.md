---
id: P6-T043
kind: task
title: D10 Memory, RAG, Labelling queue and Shadow-disagreement views
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T012, P6-T019, P6-T025, P4-T032, P0-T049]
requirements: [R6.40, R6.13, R6.04]
roadmap_todos: [T6.29]
modules: [M15, M9, M21]
dashboards: [D10]
tools: [git, pnpm, node>=20, playwright]
mcp: []
env: []
services: [mt-api]
branch: p6/P6-T043-d10-memory-rag-labelling-shadow
pr: ""
doc_sync: [docs/ui/dashboards/D10-models-memory.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T043 · D10 Memory, RAG, Labelling queue and Shadow-disagreement views

## Goal / expected outcome

D10 shows Hindsight banks (counts, recent, PIT search, delete C1), the RAG playground (hybrid results, scores, `as_of`), the **Labelling queue** tab (fast keyboard/touch labelling via `models.label.add`, C0) and per-question shadow disagreement.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.29
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Memory/RAG tabs and CryptoTrader additions · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B004: labels endpoint + D10 Labelling queue tab; D10's route list now includes it)
- Cross-phase: P4-T032 (RAG retrieval for the playground), P0-T049 (component library)
- Depends on (this phase): P6-T012, P6-T019, P6-T025

## Requirements

- Memory: bank list, search with `as_of` option (filters on `observed_at`/`ingested_at`, P6-T012), delete (C1, audited).
- RAG: query → vector/keyword/RRF/reranked scores, chunk source, `as_of` filter, index stats.
- Labelling queue: one item at a time, state preview (truncated, provenance), options as large buttons, keyboard shortcuts, skip, undo (new superseding label), daily progress (target ~15 min/day).
- Shadow: per-question disagreement rate (7d/30d), drill-down to disagreements (→ queue).
- Telegram-derived content never displayed as model input previews (not present by construction).

## ToDo

- [ ] Tabs + components.
- [ ] Labelling UX incl. phone layout (swipe/tap).
- [ ] Playwright + viewport matrix.
- [ ] Docs.

## Verification

### Tests
- Playwright: label 5 items → 5 `models.label.add` commands; undo creates a superseding row.
- Viewport matrix.

### Scenarios
- Given an abstention item on a 390×844 phone, then options are thumb-reachable and labelling works one-handed.
- Given a memory search with as_of in the past, then later memories don't show.

### Stress / failure injection
- Queue of 2,000 items: next-item latency p95 < 200 ms.

## Acceptance criteria

- [ ] Labelling queue usable on phone and desktop.
- [ ] Viewport matrix green.

## Exceptions & edge cases

- Hindsight down: Memory tab shows unavailable; labelling still works.

## Cardinal rules (do NOT)

- Do NOT show model (shadow) answers as default selections in the labelling UI (anchoring).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D10-models-memory.md`: mark the Labelling queue tab implemented (already in the route list).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.29 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T043-d10-memory-rag-labelling-shadow`
- PR title: `P6-T043: D10 Memory, RAG, Labelling queue and Shadow-disagreement views`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (labels endpoint + D10 queue tab per 17 §D P6-B004; PIT memory search per 17 §A; deps P4-T032/P0-T049; run fields)
