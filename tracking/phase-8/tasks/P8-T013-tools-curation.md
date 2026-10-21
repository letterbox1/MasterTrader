---
id: P8-T013
kind: task
title: "Curation tool group: watchlist, airdrop URLs, task actions"
phase: 8
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T006, P8-T007]
requirements: [R8.03]
roadmap_todos: [T8.20]
modules: [M19, M4, M2, M20]
dashboards: [D13, D12, D17]
branch: p8/P8-T013-tools-curation
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T013 · Curation tool group: watchlist, airdrop URLs, task actions

## Goal / expected outcome

Claude can add watchlist items and airdrop URLs and mark tasks (done/skip/snooze/never). Everything goes through the existing P4/P5 pipelines and vetting; nothing in this group claims, signs or posts.

## Context & references

- Roadmap: [R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Curation row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2 Intel, Airdrops, Tasks groups](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D13](../../../docs/ui/dashboards/D13-tasks-curation.md)
- Cross-phase: P5 R5.20–R5.22 / T5.30 (task queue), R5.10–R5.13 (airdrop discovery + risk scoring); P4 watchlist.

## Requirements

- Tools (group `curation`, enabled): `intel_watchlist_update` → `intel.watchlist.update` (C1); `airdrop_add_url` → `airdrop.add_url` (C1: https only, ≤ 2,048 chars; the URL goes through the normal blocklist + risk-scoring pipeline and the result returns the score status, never a claim); `task_done`, `task_skip`, `task_snooze`, `task_never` (C0, "marking a task"); reads `get_tasks`, `get_community` (guarded), `get_airdrops`.
- Disabled by default: `intel.source.add`, `intel.source.mute` (new sources must satisfy 12 §4), `social.draft.approve` (opens a web intent from your account; posting stays your action), `airdrop.rescore`, `airdrop.reject`.
- Never (per P8-T004): `airdrop.claim.execute`, `airdrop.mandate.*`, `wallet.*`.
- Task ids must exist; a stale id → 404 problem.

## ToDo

- [ ] Add the registry entries and regenerate the snapshot.
- [ ] Integration tests against P5 fixtures.
- [ ] Update docs.

## Verification

### Tests
- Integration: `airdrop_add_url` with a blocklisted domain → stored as rejected with reasons; a clean URL → queued for scoring.
- Integration: `task_done` updates the queue and WS `tasks`; D13 reflects it.
- Unit: URL validation (scheme, length, IDN homograph flagged).

### Scenarios
- Given Claude finds an airdrop page in a news article, when it calls `airdrop_add_url`, then the URL is vetted like any other and never auto-claimed without a mandate.
- Given a `JOIN_DISCORD` task, when Claude marks it done, then the bot later verifies posts arrive (F10).

### Stress / failure injection
- n/a: low-volume C0/C1 actions; covered by the generic rate limit (P8-T005).

## Acceptance criteria

- [ ] Curation tools work end to end; nothing claims, signs or posts
- [ ] Disabled/never items refused server-side
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Curation service down: commands return 503; nothing is queued in `mt_mcp`.
- Duplicate URL: deduped by the P5 normaliser; the result says "already known".

## Cardinal rules (do NOT)

- Do NOT expose claim execution, mandates or posting through this group.
- Do NOT add scraping sources that break platform terms.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/03-build-spec.md` M20: curation tool list.
- `docs/ui/dashboards/D17-mcp-console.md`: Curation group.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T013-tools-curation`
- PR title: `P8-T013: Curation tool group: watchlist, airdrop URLs, task actions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
