---
id: P5-T020
kind: task
title: On-chain cost gate: gas windows, budgets and allow/wait/reject verdicts
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T019, P5-T012]
requirements: [R5.04]
roadmap_todos: [T5.21]
modules: [M22, M16, M11]
dashboards: [D18, D12]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T020-costgate-policies-budgets
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T020 · On-chain cost gate: gas windows, budgets and allow/wait/reject verdicts

## Goal / expected outcome

`gate(action) → allow | wait | reject` applies the policies (benefit must exceed all-in cost by a margin; gas window below the 7-day 30th-percentile base fee unless the deadline is < 48 h; per-module daily gas budgets (alert at 80%, stop at 100%)) and logs every verdict with its numbers; the signer refuses any intent without an `allow` verdict.

## Context & references

- Roadmap: [R5.04](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.21 · D18 cost-gate widget ([D18](../../../docs/ui/dashboards/D18-wallets-treasury.md))
- [13 §7 policies](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Defaults ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13); decision P5-B001): margin 2× all-in cost; gas window = base fee below its 7-day 30th percentile unless the deadline is < 48 h; daily gas budgets airdrops A$20/day and DEX trading A$50/day, alert at 80%, stop at 100%. All read from the limits store (P5-T012), none hard-coded
- Library: `mt_onchain.costgate` (decision P5-B002)

## Requirements

- Inputs: action type, expected benefit (claim value at current price × (1 − haircut), or EV from P5-T040), deadline, module (`airdrop`, `sweep`, `revoke`, later `treasury`).
- Rule: allow iff benefit ≥ margin × all-in cost (margin default 2×, configurable) and budget available and (base fee ≤ 7-day p30 or deadline < 48 h); wait if only the window fails; reject otherwise.
- Defensive actions (revoke flagged approval, kill-switch sweep to the vault) bypass the benefit test, the window and the 100% budget stop (protective actions never wait), but are still logged and budget-counted.
- Daily gas budget per module (defaults airdrops A$20/day, DEX trading A$50/day): alert at 80%, `reject` (`budget_exhausted`) at 100%; usage in `ops.gas_budget_usage`.
- `wait` verdicts re-evaluated every 15 min until deadline − 48 h, then window ignored.
- API: `POST /treasury/costgate/preview` (C0) and `/wallets/costgate/quotes` for D18.

## ToDo

- [ ] Implement `packages/mt_onchain/costgate/policy.py`, `budget.py` and the re-evaluation scheduler (Prefect or service loop).
- [ ] Persist verdicts with inputs; publish `costgate.quote`.
- [ ] Signer integration: intent carries quote id; signer verifies verdict = allow and freshness ≤ 60 s.
- [ ] Endpoints + tests; doc sync.

## Verification

### Tests
- Unit: decision table (benefit/cost/budget/window/deadline) → expected verdict.
- Unit: defensive actions bypass the benefit test but not logging.
- Integration: signer refuses an intent with a stale (> 60 s) or `wait` quote.

### Scenarios
- Given base fee above the 7-day p30 and deadline in 5 days, when a claim is gated, then `wait`; at deadline − 47 h, then `allow` if economic.
- Given the airdrop module spent its daily gas budget, when another claim arrives, then `reject` (`budget_exhausted`) and a task is created.

### Stress / failure injection
- Base-fee spike replay (historic data) over a week: verdicts flip to wait and back without oscillation (hysteresis 5%).

## Acceptance criteria

- [ ] Verdicts logged with all numbers
- [ ] Gas windows and budgets enforced
- [ ] Signer requires a fresh allow verdict
- [ ] D18 shows last quotes and blocked moves with reasons

## Exceptions & edge cases

- Price feed for benefit stale (> 24 h CoinGecko cache): treat benefit as unknown → `reject` for autonomous paths.

## Cardinal rules (do NOT)

- Do NOT let defensive bypasses apply to anything except revoke and sweep-to-vault intents.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §7: margin and hysteresis defaults.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.21 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T020-costgate-policies-budgets`
- PR title: `P5-T020: On-chain cost gate: gas windows, budgets and allow/wait/reject verdicts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (margin, gas window and gas budgets as 16 §2.7 defaults from the limits store; 80% alert / 100% stop; `mt_onchain.costgate`)
