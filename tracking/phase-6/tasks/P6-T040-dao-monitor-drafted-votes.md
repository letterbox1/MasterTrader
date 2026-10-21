---
id: P6-T040
kind: task
title: DAO proposal monitor with drafted votes
phase: 6
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T002]
requirements: [R6.23]
roadmap_todos: [T6.28]
modules: [M22, M19]
dashboards: [D18, D13]
branch: p6/P6-T040-dao-monitor-drafted-votes
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

# P6-T040 · DAO proposal monitor with drafted votes

## Goal / expected outcome

Snapshot (GraphQL, keyless 100 req/min) and Tally (free key) are polled for proposals in protocols we hold; those changing parameters, oracles or treasuries raise alerts and a drafted vote task for your confirmation from the per-DAO governance key.

## Context & references

- Roadmap: [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (DAO monitoring, votes drafted for your confirmation, dedicated governance key, one wallet per DAO)
- Cross-phase: P5 R5.20 task queue
- Depends on (this phase): P6-T002

## Requirements

- Holdings-driven watch list (from `treasury.position` + wallet view).
- Classifier for proposal impact (parameter/oracle/treasury/other) — rules first; tier-B question optional (non-Telegram text only).
- Alert + `DAO_VOTE` task with summary, impact on our positions, drafted choice + rationale; you confirm; signing only via the governance wallet flow (no auto-sign).
- Respect limits: Snapshot ≤ 100 req/min; Tally free key quota tracked.

## ToDo

- [ ] Snapshot + Tally clients with quota tracker.
- [ ] Impact classifier.
- [ ] Task creation + digest entry.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: parsers on recorded responses; impact rules.
- Integration: new oracle-change proposal → one task.

### Scenarios
- Given Aave proposes an oracle change for a market we hold, then an urgent task with a drafted vote appears.

### Stress / failure injection
- Snapshot rate-limit responses: backoff keeps under 100 req/min.

## Acceptance criteria

- [ ] Monitor live for held protocols; tasks created for impactful proposals.

## Exceptions & edge cases

- Governance wallet not registered → task says so; no vote path.

## Cardinal rules (do NOT)

- Do NOT auto-vote or sign governance transactions.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4: impact rules.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T040-dao-monitor-drafted-votes`
- PR title: `P6-T040: DAO proposal monitor with drafted votes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
