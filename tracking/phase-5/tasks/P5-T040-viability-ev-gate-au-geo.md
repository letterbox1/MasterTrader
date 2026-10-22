---
id: P5-T040
kind: task
title: Viability score with AU geo/KYC exclusion and EV gate
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T037]
requirements: [R5.14]
roadmap_todos: [T5.27]
modules: [M4]
dashboards: [D12]
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p5/P5-T040-viability-ev-gate-au-geo
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T040 · Viability score with AU geo/KYC exclusion and EV gate

## Goal / expected outcome

Each risk-passed opportunity gets a viability score (opportunity strength, cost to take part, fit incl. **AU geo/KYC exclusion** and sybil-filter strictness and current eligibility) and an expected value `EV = P(launch)·E[allocation]·E[price at unlock]·(1 − haircut) − gas − fees − capital_lockup_cost − minutes·time_value`; only EV > 0 reaches the digest as a task, with inputs shown.

## Context & references

- Roadmap: [R5.14](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.27 · USER settings P5-T007
- [08 viability](../../../docs/08-airdrops-and-token-launches.md#viability-score) · [08 EV gate](../../../docs/08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) · [D12 acceptance 2](../../../docs/ui/dashboards/D12-airdrops.md) (AU restrictions visible before any task)
- Hurdle: default 5% p.a. on capital locked (AUD cash-rate proxy), configurable ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13); decision P5-B012); gas costs from the cost gate (P5-T019)

## Requirements

- Strength: funding (investors, round size from CryptoRank), TVL/user trend, confirmed vs rumoured token/points, comparable-airdrop EV table (versioned).
- Cost: gas (cost-gate estimate), capital needed, minutes per task, deadline proximity.
- Fit: sybil-filter strictness, **geo/KYC: AU excluded → viability 0 and stage `excluded_geo`** (shown in D12, no task), eligibility of the public address vs stated criteria.
- EV inputs persisted with ranges (low/base/high); `capital_lockup_cost = capital × days × hurdle/365`; the hurdle and time value come from settings (P5-T007; default 5% p.a.), never hard-coded.
- Gate: EV(base) > 0 after risk pass → task-eligible; EV ≤ 0 → watch with reason; user can override (C1) from D12.

## ToDo

- [ ] Implement `packages/mt_airdrop/score/viability.py` and `ev.py` with config `config/airdrop_ev.yaml`.
- [ ] Geo/KYC parser: terms-page keywords + CryptoRank/launchpad restricted-country fields; unknown → flagged.
- [ ] Write `opportunity_score` rows with breakdown; tests; doc sync.

## Verification

### Tests
- Unit: EV formula golden examples (incl. negative EV from time cost).
- Unit: AU listed in restricted countries → `excluded_geo`, no task.
- Property: increasing gas or minutes never increases EV.

### Scenarios
- Given a points programme needing 90 minutes at A$1/min with E[value] A$60, then EV < 0 and it stays in watch with the reason.
- Given geo restrictions are unknown, then a task may be created but shows "AU eligibility unverified" first.

### Stress / failure injection
- n/a: pure functions over scored opportunities (≤ seconds per batch)

## Acceptance criteria

- [ ] Viability breakdown and EV with inputs stored and shown
- [ ] AU exclusion enforced before task creation
- [ ] EV ≤ 0 never reaches the digest as a task

## Exceptions & edge cases

- Missing price for E[price at unlock]: use comparable table low case; mark `ev_uncertain`.

## Cardinal rules (do NOT)

- Do NOT create tasks that require VPNs or misrepresenting residency (SPEC NN11).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: EV defaults and comparable table location.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.27 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T040-viability-ev-gate-au-geo`
- PR title: `P5-T040: Viability score with AU geo/KYC exclusion and EV gate`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (EV hurdle default 5% p.a. from settings per 16 §2.7/P5-B012)
