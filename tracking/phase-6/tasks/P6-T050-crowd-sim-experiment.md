---
id: P6-T050
kind: task
title: Optional: crowd-simulation experiment (OASIS, local, research only)
phase: 6
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T003]
requirements: [R6.32]
roadmap_todos: [T6.30]
modules: [M14]
dashboards: []
tools: [git, docker, uv]
mcp: []
env: []
services: [llm-local]
branch: p6/P6-T050-crowd-sim-experiment
pr: ""
doc_sync: [docs/03-build-spec.md, docs/research/mirofish.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T050 · Optional: crowd-simulation experiment (OASIS, local, research only)

## Goal / expected outcome

A walled-off crowd-sim experiment (clean-room on CAMEL-AI OASIS with a local LLM and our own memory, not MiroFish's Zep Cloud) produces scenario narratives for a few events, evaluated as a candidate feature only, with written experiment notes.

## Context & references

- Roadmap: [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.30
- Optional: only if P6-T003 recorded `yes`; otherwise cancel this item.
- Spec: [03 M14](../../../docs/03-build-spec.md#m14-crowd-simulation-optional) (candidate feature only) · [research: MiroFish](../../../docs/research/mirofish.md) (AGPL, Zep Cloud mandatory, no auth, CORS *, default secret, non-deterministic)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B009: MiroFish/OASIS only with a local memory backend and a hardened config (auth on, no default secrets, no open CORS); no Zep Cloud; otherwise M14 is skipped) · [03 M14](../../../docs/03-build-spec.md#m14-crowd-simulation-optional)
- Depends on (this phase): P6-T003

## Requirements

- Isolated `crowdsim` service on its own network, no DB/signer route, no inbound; local LLM via gateway role `strategy-gen` or a dedicated budget.
- Seeded, recorded runs; ≤ 40 rounds; outputs to `research.crowdsim_run` only.
- Evaluation: does the narrative score add information vs existing features on post-cutoff events? Report IC with CI.
- No path to strategies unless a later gated feature promotion.
- Allowed paths only: (a) MiroFish with its memory swapped to a local backend (our Postgres/Hindsight) and the hardened config, or (b) clean-room OASIS (Apache-2.0). If neither runs locally, M14 is skipped: record it and cancel this item.

## ToDo

- [ ] Clean-room OASIS runner (Apache-2.0) + local LLM.
- [ ] Experiment on ≥ 5 historical post-cutoff events.
- [ ] Experiment notes in `notebooks/` + MLflow.
- [ ] Docs.

## Verification

### Tests
- Smoke: one seeded run completes offline.
- Isolation: network policy test.

### Scenarios
- Given a CPI surprise event, then the sim produces a narrative and a crowd-reaction score logged with the seed.

### Stress / failure injection
- Token budget cap reached → run stops cleanly.

## Acceptance criteria

- [ ] Experiment notes with a keep/drop recommendation.

## Exceptions & edge cases

- Non-determinism: report variance across ≥ 3 seeds.

## Cardinal rules (do NOT)

- Do NOT use Zep Cloud or any hosted service; do NOT expose the service.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M14: clean-room note.
- `docs/research/mirofish.md`: outcome.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.30 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T050-crowd-sim-experiment`
- PR title: `P6-T050: Optional: crowd-simulation experiment (OASIS, local, research only)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (M14 local-memory-backend/hardened-config rule, else skipped (17 §D P6-B009); run fields)
