---
id: P6-T002
kind: task
title: Get the Tally key, FinMMEval data access and confirm bake-off model licences
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
branch: p6/P6-T002-external-access-tally-finmmeval-weights
pr: ""
doc_sync: [docs/research/decision-models-system-one.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T002 · Get the Tally key, FinMMEval data access and confirm bake-off model licences

## Goal / expected outcome

The free external accesses only you can obtain are in place: a **Tally** free API key (DAO monitor), access to the **CLEF-2026 FinMMEval Buy/Hold/Sell** data under its terms, and a yes/no on each bake-off contender's weights licence (Laya, Clef-flash, **Kev-4B/9B**).

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (Snapshot keyless, Tally free key) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) bake-off · [research: decision models](../../../docs/research/decision-models-system-one.md)
- Gap: P6-B003 (Kev source/licence unspecified)
- Unblocks: P6-T027 (contender containers), P6-T029 (bake-off harness), P6-T040 (DAO monitor)

## Requirements

- Tally: free account, API key stored in sops (`tally.api_key`).
- FinMMEval: register for / download the CLEF-2026 FinMMEval Buy/Hold/Sell task data; record its licence and whether private research use is allowed.
- Weights: confirm each contender is free to self-host (Apache-2.0/MIT or equivalent); Kev must have a named source and licence or it is excluded from the bake-off.

## ToDo

- [ ] Create a Tally account → Settings → API → create key; `sops secrets/mt.enc.yaml` → add `tally.api_key`.
- [ ] Follow the FinMMEval task page (arXiv 2602.10886) to obtain the Buy/Hold/Sell data; save it under `data/external/finmmeval/` on the host (git-ignored) and write its licence text to `data/external/finmmeval/LICENCE.txt`.
- [ ] For Laya (`NandhaKishorM/laya`), Clef-flash (Cloudflare weights) and Kev-4B/9B: note repo URL, licence and size in the progress log; mark Kev 'excluded' if no free self-hostable source exists.
- [ ] Comment on P6-B003 with what you found.

## Verification

### Tests
- n/a: human action; P6-T027/P6-T029 smoke-test the results.

### Scenarios
- Given the Tally key is in sops, when P6-T040 starts, then the Tally client authenticates without a key in env files or git.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] Tally key present in sops (verified by `sops -d` key listing, value not printed).
- [ ] FinMMEval data on the host with its licence file, or a written note that access was refused.
- [ ] Licence decision recorded for Laya, Clef-flash and Kev.

## Exceptions & edge cases

- If FinMMEval access is refused, the bake-off runs on our data only and the report says so.
- Never accept paid tiers for any of these.

## Cardinal rules (do NOT)

- Do NOT pay for any access or use a hosted paid decision model (Jev, Microsoft-Decision-1 are excluded).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/research/decision-models-system-one.md`: add Kev's source/licence (or exclusion) and FinMMEval access terms.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T002-external-access-tally-finmmeval-weights`
- PR title: `P6-T002: Get the Tally key, FinMMEval data access and confirm bake-off model licences`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
