---
id: P4-T057
kind: task
title: End-to-end F3 scenarios: feed → document → tier B → KV → D08 per source
phase: 4
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T030, P4-T031, P4-T044, P4-T046, P4-T020, P4-T021, P4-T022, P4-T023, P4-T012, P4-T013, P4-T014, P4-T015]
requirements: [R4.06, R4.01, R4.04, R4.05, R4.13]
roadmap_todos: []
modules: [M2, M9, M21]
dashboards: [D08, D01, D02]
tools: [uv, git, docker, pnpm]
mcp: []
env: []
services: [postgres, nats, rss-bridge, decision-svc, tei-embed]
branch: p4/P4-T057-verify-f3-e2e-scenarios
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
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

# P4-T057 · End-to-end F3 scenarios: feed → document → tier B → KV → D08 per source

## Goal / expected outcome

A scenario suite runs flow F3 end to end on the Compose stack for each source family (RSS, RSS-Bridge, GDELT, EDGAR, central bank, Discord, Bluesky, Mastodon, Farcaster) with recorded fixtures: item fetched → deduped → gated → linked → scored → stored → chunked → `text.doc.new` → `dec.tierb.*` → KV `tierb_scores` → visible in D08 within 5 s — plus the Telegram branch (F3b) ending in `text.telegram_posture` / `posture.telegram.*` only. Everything runs on recorded fixtures; the live checks are P4-T067/P4-T068.

## Context & references

- Roadmap: [R4.06, R4.01, R4.04, R4.05, R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Flow: [02 F3](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D08 acceptance](../../../docs/ui/dashboards/D08-intel.md)

## Requirements

- Per-source ingest test (roadmap 'Ingest tests' for R4.04/R4.05) included.
- Timing assertion: ingest → visible in D08 p95 ≤ 5 s on the test stack.
- Approximate-timestamp fixture shows '≈' in UI.
- Duplicate wire story shows '+N similar'.

## ToDo

- [ ] Fixture servers for each source family.
- [ ] Scenario runner + Playwright assertions.
- [ ] CI nightly job + report artifact.

## Verification

### Tests
- The scenario suite.

### Scenarios
- Given an EDGAR 8-K fixture, then its chunks have the `{ticker} 8-K {period} Item x.xx` header and it is retrievable via `/rag/search`.
- Given a Discord crosspost fixture, then the source server name shows in the card.

### Stress / failure injection
- n/a here; see P4-T058.

## Acceptance criteria

- [ ] All source families pass; p95 ≤ 5 s ingest → D08
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Sources disabled by terms/checks are reported as 'skipped (disabled)' not failures.

## Cardinal rules (do NOT)

- Do NOT hit live third-party endpoints in CI; use fixtures.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §8 F3: link the scenario suite
- `docs/roadmap/phase-4-intel.md`: note the item in §7 risks / progress

## Branch & PR

- Branch: `p4/P4-T057-verify-f3-e2e-scenarios`
- PR title: `P4-T057: End-to-end F3 scenarios: feed → document → tier B → KV → D08 per source`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T057` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (F3/F3b split (17 §A P4-B001); fixtures only, live checks in P4-T067/T068)
