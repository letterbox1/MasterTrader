---
id: P6-T064
kind: task
title: Degraded-mode drill for the AI layer and treasury
phase: 6
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T024, P6-T009, P6-T012, P6-T038, P6-T015]
requirements: [R6.07, R6.11, R6.04, R6.24]
roadmap_todos: []
modules: [M8, M9, M21, M22, M10]
dashboards: [D09, D10, D18]
tools: [docker, uv, nvidia-smi]
mcp: []
env: []
services: [litellm, llm-local, hindsight, decision-svc, postgres, gpu]
branch: p6/P6-T064-verify-degraded-modes-drill
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T064 · Degraded-mode drill for the AI layer and treasury

## Goal / expected outcome

A chaos drill shows each P6 component degrades as 02 §9.3 says: gateway/budget exhausted → local models + badge; GPU unavailable → tier B on CPU or disabled, tier A unaffected; Hindsight down → debate runs without memory; Postgres down → audit buffered; kill switch → treasury entries frozen, exits available.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Spec: [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)
- Depends on (this phase): P6-T024, P6-T009, P6-T012, P6-T038, P6-T015

## Requirements

- Fault injections: stop `litellm`; exhaust budgets; remove GPU (`nvidia-smi` disable / container device removal); stop `hindsight`; stop `tei`; pause Postgres 60 s; kill `agents` mid-run; kill switch ON.
- For each: expected system + UI behaviour, observed behaviour, recovery time.
- No data loss in `audit.llm_call` and `audit.tierb_decision` (buffer replay).

## ToDo

- [ ] Write the drill runbook `docs/runbooks/ai-layer-degraded-drill.md`.
- [ ] Execute on the host in paper mode.
- [ ] Record results table in the progress log; file bugs for deviations.

## Verification

### Tests
- Automated subset in CI compose (gateway down, Hindsight down).

### Scenarios
- Given the GPU disappears, then tier-A p99 stays < 50 µs and D10 shows tier B degraded.
- Given Postgres pauses for 60 s, then LLM audit rows buffer and all land after recovery.

### Stress / failure injection
- All of the above in sequence within 30 min; system returns to green without manual DB edits.

## Acceptance criteria

- [ ] Every injected fault matches 02 §9.3.
- [ ] Zero audit loss.
- [ ] Runbook committed.

## Exceptions & edge cases

- A deviation is a bug item (S2 if it risks money/data, else S3).

## Cardinal rules (do NOT)

- Do NOT run the drill with live money or live keys.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.3: add tier-B/memory/treasury rows if missing.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T064-verify-degraded-modes-drill`
- PR title: `P6-T064: Degraded-mode drill for the AI layer and treasury`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T064` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; local fallback runs keyless on P0 llm-local; budgets per 16 §2.10)
