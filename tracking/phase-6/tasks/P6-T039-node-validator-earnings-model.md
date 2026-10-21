---
id: P6-T039
kind: task
title: Node/validator net-earnings model
phase: 6
type: BUILD
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.23]
roadmap_todos: [T6.28]
modules: [M22]
dashboards: [D18]
branch: p6/P6-T039-node-validator-earnings-model
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T039 · Node/validator net-earnings model

## Goal / expected outcome

A monthly model computes `net = rewards + MEV fees + commission − infra − ops time − E[slash] − opportunity cost` per candidate node/validator, recommends start only if positive under conservative inputs, and flags retirement after two negative months.

## Context & references

- Roadmap: [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (formula, start only if positive, retire after two negative months, operations checklist; Solana validators: avoid)

## Requirements

- Inputs: candidate list (ETH solo 32 ETH, Lido CSM bond 2.4 → 1.3 ETH, Rocket Pool Saturn I 4 ETH, DVT, light/testnet nodes), reward/MEV estimates, infra cost, ops hours × your hourly value, slashing probability × penalty, opportunity cost vs allocator best yield.
- Conservative mode (lower rewards, higher costs) drives the recommendation.
- Monthly report in D18 with history; two consecutive negative months → retire task.
- No automation of validator start/stop; ops checklist shown (slashing-protection backups, one key per machine, withdrawal to vault/warm, client diversity, missed-duty alerts, hard-fork schedule).

## ToDo

- [ ] Model + report generator.
- [ ] Monthly Prefect job.
- [ ] Retire-task creation.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: formula golden cases; conservative mode is never more optimistic than base.
- Two-negative-months rule test.

### Scenarios
- Given a Solana validator candidate, then the model shows the ~290 SOL/yr admission cost and recommends avoid.

### Stress / failure injection
- n/a: monthly batch.

## Acceptance criteria

- [ ] Monthly report visible; retirement rule tested.

## Exceptions & edge cases

- Missing reward data → no recommendation.

## Cardinal rules (do NOT)

- Do NOT run any validator/node container from this task; model only.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4: model inputs.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T039-node-validator-earnings-model`
- PR title: `P6-T039: Node/validator net-earnings model`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
