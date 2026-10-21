---
id: P6-T048
kind: task
title: Optional: account credibility scoring and shill-burst posture
phase: 6
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T003]
requirements: [R6.31]
roadmap_todos: [T6.30]
modules: [M23, M6]
dashboards: [D13, D12]
branch: p6/P6-T048-credibility-shill-burst
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

# P6-T048 · Optional: account credibility scoring and shill-burst posture

## Goal / expected outcome

Accounts you follow get credibility scores from past calls vs outcomes, and a shill-burst posture (mentions vs on-chain unique-buyer growth) becomes a dump-risk feature for strategies and airdrop vetting; Telegram contributes counts only.

## Context & references

- Roadmap: [R6.31](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.30
- Optional: only if P6-T003 recorded `yes`; otherwise cancel this item.
- Spec: [13 §8](../../../docs/13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social) (credibility, shill-burst) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (Telegram counts only)
- Cross-phase: P4 social ingest, P5 wallet/on-chain data
- Depends on (this phase): P6-T003

## Requirements

- Credibility: extract calls (ticker + direction) from allowed platforms (X if ever enabled, Bluesky, Discord, Farcaster) → settle vs outcomes → Bayesian hit-rate score per account; feature `credibility.{account}`.
- Shill-burst: ratio of mention velocity (all platforms; Telegram as counts) to unique-buyer growth; spikes from new/low-follower accounts without buyers → posture `shill_burst=true`.
- Features published via `feat.*` with provenance; usable in airdrop vetting and strategies.

## ToDo

- [ ] Call extractor (non-Telegram text) + settlement.
- [ ] Shill-burst posture job.
- [ ] Features + D12/D13 display.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: posture on synthetic mention/buyer series.
- Provenance: Telegram text never enters the extractor (counts only).

### Scenarios
- Given 500 mentions from 3-day-old accounts and flat unique buyers, then `shill_burst=true` for that token.

### Stress / failure injection
- n/a: batch features.

## Acceptance criteria

- [ ] Posture and credibility features available with provenance.

## Exceptions & edge cases

- Sparse call history → credibility prior only (flagged).

## Cardinal rules (do NOT)

- Do NOT use Telegram text; counts only.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §8: feature definitions.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.30 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T048-credibility-shill-burst`
- PR title: `P6-T048: Optional: account credibility scoring and shill-burst posture`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
