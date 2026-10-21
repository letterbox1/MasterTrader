---
id: P6-T052
kind: task
title: Verify every LLM call is audited and agents never run per tick
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T005, P6-T008, P6-T013, P6-T015]
requirements: [R6.02, R6.03]
roadmap_todos: []
modules: [M8, M17]
dashboards: [D09, D10]
branch: p6/P6-T052-verify-llm-audit-scheduler
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T052 · Verify every LLM call is audited and agents never run per tick

## Goal / expected outcome

Evidence that (a) every gateway call over a 48 h window has exactly one `audit.llm_call` row with model, hashes, text, tokens, cost and latency; (b) no agent run is triggered by ticks; (c) tool outputs are cached per (instrument, as_of); (d) new WORM tables pass the 15 §2.4 suite.

## Context & references

- Roadmap: [R6.02](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.03](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Roadmap: R6.02 verified by 'Scheduler tests', R6.03 by 'Audit check' · [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) · [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [15 §2.4](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- Gap: P6-B001 (no roadmap VERIFY ToDo for these)
- Depends on (this phase): P6-T005, P6-T008, P6-T013, P6-T015

## Requirements

- Reconcile LiteLLM request log count vs `audit.llm_call` (by call_id) for 48 h of normal operation: zero missing, zero duplicates.
- Field completeness: no NULL model/prompt_hash/tokens/cost/latency.
- Tick storm test: 1M `md.*` messages → zero runs.
- Cache hit-rate report for repeated (instrument, as_of) tool calls.
- WORM suite on `audit.llm_call`, `audit.decision_run`, `audit.signal`, `audit.decision_settlement`, `audit.anomaly`, `models.label`, treasury change rows.

## ToDo

- [ ] Write the reconciliation script `tools/verify/llm_audit_recon.py`.
- [ ] Run the tick-storm test in the staging compose profile.
- [ ] Run the WORM suite.
- [ ] Attach results to the progress log.

## Verification

### Tests
- Reconciliation script unit test on fixtures.
- WORM suite (15 §2.4).

### Scenarios
- Given 48 h of runs, when reconciled, then counts match exactly.
- Given a direct `UPDATE audit.llm_call` as app role, then it fails.

### Stress / failure injection
- Tick storm 1M messages at max rate; agents CPU unaffected; zero runs.

## Acceptance criteria

- [ ] Recon: 0 missing / 0 duplicates.
- [ ] Tick storm: 0 runs.
- [ ] WORM suite green for all new tables.

## Exceptions & edge cases

- Gateway restarts during the window are fine if buffered rows land.

## Cardinal rules (do NOT)

- Do NOT exclude failed calls from the reconciliation.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M17: link the reconciliation check.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T052-verify-llm-audit-scheduler`
- PR title: `P6-T052: Verify every LLM call is audited and agents never run per tick`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
