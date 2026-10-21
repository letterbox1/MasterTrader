---
id: P6-T055
kind: task
title: PIT test: memory recall in a backtest never returns later episodes
phase: 6
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T012, P6-T013]
requirements: [R6.04]
roadmap_todos: [T6.63]
modules: [M9, M7]
dashboards: [D10]
branch: p6/P6-T055-verify-pit-memory-recall
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T055 · PIT test: memory recall in a backtest never returns later episodes

## Goal / expected outcome

A backtest that replays agent decisions across a year with memory recall enabled proves that no recalled memory (including consolidated/derived ones and reflections) was created after the backtest's `as_of`.

## Context & references

- Roadmap: [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.63
- Roadmap: R6.04 'PIT recall test' · [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) NN1
- Gap: P6-B016
- Depends on (this phase): P6-T012, P6-T013

## Requirements

- Seed Hindsight with dated episodes, settlements and reflections over 12 months, plus consolidated observations spanning periods.
- Run a walk-forward replay with recall at each step; assert every returned memory has `created_at ≤ as_of` and all source memories ≤ as_of.
- Also test `/memory/search?as_of=` and D10 search.

## ToDo

- [ ] Fixture generator.
- [ ] Replay test `tests/pit/test_memory_recall_pit.py`.
- [ ] Add to the CI `pit` suite.
- [ ] Record results.

## Verification

### Tests
- The PIT test above (CI).

### Scenarios
- Given a reflection written 2027-03-10 about a February trade, when replaying 2027-03-01, then it is not recalled.

### Stress / failure injection
- 10k memories, 250 replay steps: zero violations; runtime < 10 min.

## Acceptance criteria

- [ ] Zero PIT violations.
- [ ] Test in CI `pit` suite.

## Exceptions & edge cases

- If Hindsight can't filter natively, the post-filter in P6-T012 must be the code path tested.

## Cardinal rules (do NOT)

- Do NOT relax the filter to 'same day'.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §1: PIT test reference.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.63 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T055-verify-pit-memory-recall`
- PR title: `P6-T055: PIT test: memory recall in a backtest never returns later episodes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T055` run

## Progress log

- 2026-10-21 00:00 · planner · created
