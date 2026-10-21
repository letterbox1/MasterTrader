---
id: P6-T017
kind: task
title: Post-training-cutoff evaluation gate for LLM strategies
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T016, P6-T005]
requirements: [R6.06]
roadmap_todos: [T6.23]
modules: [M7, M0, M21]
dashboards: [D10]
branch: p6/P6-T017-post-cutoff-evaluation-gate
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T017 · Post-training-cutoff evaluation gate for LLM strategies

## Goal / expected outcome

The lab enforces gate §8 item 4: any strategy whose inputs include an LLM (M8 Signals, tier-B models trained on LLM labels) is evaluated only on data after the **latest training cutoff** of every model in its chain, plus an embargo; otherwise promotion is refused.

## Context & references

- Roadmap: [R6.06](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.23
- Spec: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 4 · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design)
- Cross-phase: P2 R2.42 validation harness, R2.06 lifecycle gates
- Related: P6-T005 (`training_cutoff` in `models.registry`)
- Depends on (this phase): P6-T016, P6-T005

## Requirements

- Model lineage resolver: strategy manifest → Signal sources → `model_ids` → `models.registry.training_cutoff` (gateway models) and `training_data_end` (own tier-B heads).
- Gate: evaluation window start ≥ max(cutoffs) + embargo (default 30 days); report the usable OOS length; fail if < configured minimum (default 90 days).
- Unknown cutoff → gate fails closed with reason `unknown_cutoff`.
- For LLM strategies, historical Signals must be generated with `pit(as_of)` tools at each historical date (no future context) or replayed from the live record.
- Gate result written to the strategy's validation record and shown in D03/D10.

## ToDo

- [ ] Lineage resolver in `mt_lab.gates.llm_cutoff`.
- [ ] Gate wiring into the P2 gate runner.
- [ ] Seed cutoffs for configured gateway models (from provider docs; marked (U) if unverified).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: lineage with nested models; max cutoff; unknown cutoff fails closed.
- Integration: an LLM-signal strategy with a window starting before cutoff is rejected; after cutoff+embargo is accepted.

### Scenarios
- Given Claude model cutoff 2026-xx and a backtest from 2025-01, then the gate rejects with the usable window shown.
- Given a tier-B head trained on data to 2027-03-01, then its strategies evaluate only from 2027-03-31.

### Stress / failure injection
- n/a: deterministic gate logic; covered by unit/integration tests.

## Acceptance criteria

- [ ] Gate enforced for every strategy whose lineage includes an LLM.
- [ ] Unknown cutoff can't pass.

## Exceptions & edge cases

- Model upgraded mid-paper period: the paper clock restarts for gate purposes (logged).

## Cardinal rules (do NOT)

- Do NOT hand-enter a cutoff to make a gate pass; cutoff edits are audited and need a source.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` §8: embargo + minimum OOS defaults.
- `docs/14-strategy-evidence-and-validation.md` §6: LLM cutoff gate.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.23 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T017-post-cutoff-evaluation-gate`
- PR title: `P6-T017: Post-training-cutoff evaluation gate for LLM strategies`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
