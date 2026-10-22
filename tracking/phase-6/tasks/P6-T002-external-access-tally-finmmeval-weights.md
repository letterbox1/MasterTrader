---
id: P6-T002
kind: task
title: Get the Tally key and FinMMEval data access
phase: 6
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R6.12, R6.23]
roadmap_todos: []
modules: [M21, M22]
dashboards: [D10]
tools: [sops]
mcp: []
env: []
services: [tally, finmmeval]
branch: p6/P6-T002-external-access-tally-finmmeval-weights
pr: ""
doc_sync: [docs/research/decision-models-system-one.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T002 · Get the Tally key and FinMMEval data access

## Goal / expected outcome

The free external accesses only you can obtain are in place: a **Tally** free API key (DAO monitor) in the sops file, and access to the **CLEF-2026 FinMMEval Buy/Hold/Sell** data under its terms. Model-licence checks (Laya, Clef-flash, Kev-4B/9B) are agent work in P6-T068 ((U) facts are verified by agents, [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)).

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (Snapshot keyless, Tally free key) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) bake-off · [research: decision models](../../../docs/research/decision-models-system-one.md)
- Licences and the Kev (U) check: P6-T068 (agent, T6.72; owns P6-B003)
- Unblocks: P6-T059 (FinMMEval part of the bake-off review), P6-T070 (live Tally check). P6-T040 is built keyless against recorded Snapshot/Tally fixtures.

## Requirements

- Tally: free account; API key stored in the sops file outside the repo as `TALLY_API_KEY`.
- FinMMEval: register for / download the CLEF-2026 FinMMEval Buy/Hold/Sell task data; record its licence and whether private research use is allowed.
- Model weights and licences are not part of this item (P6-T068).

## ToDo

- [ ] Create a Tally account → Settings → API → create key; `sops ~/.config/mastertrader/secrets.enc.yaml` → add `TALLY_API_KEY`.
- [ ] Follow the FinMMEval task page (arXiv 2602.10886) to obtain the Buy/Hold/Sell data; save it under `data/external/finmmeval/` on the host (git-ignored) and write its licence text to `data/external/finmmeval/LICENCE.txt`.
- [ ] Note here when both are done (or that you declined either), so P6-T059 and P6-T070 know what to run.

## Verification

### Tests
- n/a: human action; P6-T027/P6-T029 smoke-test the results.

### Scenarios
- Given the Tally key is in sops, when P6-T070 runs the live check, then the Tally client authenticates without a key in env files or git.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] Tally key present in sops (verified by `sops -d` key listing, value not printed).
- [ ] FinMMEval data on the host with its licence file, or a written note that access was refused.
- [ ] Any decline recorded, so the dependants skip that part.

## Exceptions & edge cases

- If FinMMEval access is refused, the bake-off runs on our data only and the report says so.
- Never accept paid tiers for any of these.

## Cardinal rules (do NOT)

- Do NOT pay for any access or use a hosted paid decision model (Jev, Microsoft-Decision-1 are excluded).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/research/decision-models-system-one.md`: FinMMEval access terms (Kev and the licences are recorded by P6-T068).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T002-external-access-tally-finmmeval-weights`
- PR title: `P6-T002: Get the Tally key and FinMMEval data access`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Kev/licence (U) check moved to agent task P6-T068 per 17 §E; Tally key as TALLY_API_KEY in the sops file outside the repo; feeds live check P6-T070 and P6-T059)
