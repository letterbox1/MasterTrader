---
id: P6-T060
kind: task
title: Treasury: cost gate blocks uneconomic moves; depeg auto-reduce; caps and reserve hold
phase: 6
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T038, P6-T036, P6-T037, P6-T034, P6-T039, P6-T040]
requirements: [R6.21, R6.22, R6.23, R6.24, R6.20]
roadmap_todos: [T6.64]
modules: [M22, M11]
dashboards: [D18]
branch: p6/P6-T060-verify-treasury-gates-depeg-caps
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

# P6-T060 · Treasury: cost gate blocks uneconomic moves; depeg auto-reduce; caps and reserve hold

## Goal / expected outcome

On forks/testnets: an uneconomic move is rejected by the cost gate with numbers logged; a simulated depeg > 50 bps auto-reduces; per-protocol (≤ 20%), per-chain, per-stablecoin, HLP and venue caps and the 20–40% reserve can't be breached; treasury loosening needs C3; kill switch freezes entries.

## Context & references

- Roadmap: [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.22](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.64
- Roadmap: R6.20 'Policy tests', R6.21 'Allocator tests', R6.22 'Sweep test', R6.23 'Model review', R6.24 'Gate tests' · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) · [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Exit: [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 4
- Depends on (this phase): P6-T038, P6-T036, P6-T037, P6-T034, P6-T039, P6-T040

## Requirements

- Scenarios on Anvil mainnet fork and Solana local validator with recorded fee data.
- Each block/allow decision has its numbers in the log/audit.
- Node/validator model and DAO monitor reviewed (R6.23) with a short note.

## ToDo

- [ ] Scenario suite `tests/treasury/`.
- [ ] Run on fork; capture evidence.
- [ ] Model review note for R6.23.
- [ ] Record results.

## Verification

### Tests
- Treasury scenario suite in CI (fork-based, recorded RPC).

### Scenarios
- Given a $50 deposit with $12 all-in round trip, then gate=reject with numbers.
- Given USDC trades at 0.9940 (60 bps), then exposure in USDC is reduced automatically and the banner shows in D18.
- Given an allocation that would put 25% in one protocol, then M11 denies it.
- Given the reserve would drop to 18%, then the move is denied.
- Given kill ON, then `earn.enter` denied, `earn.exit` allowed (C2).
- Given a C1 attempt to raise a cap, then rejected (C3 needed).

### Stress / failure injection
- Gas spike ×10 during allocation: proposals switch to `wait`; protective exits still proceed within the gas budget.

## Acceptance criteria

- [ ] All scenarios pass with logged numbers.
- [ ] R6.23 review note recorded.

## Exceptions & edge cases

- Fork RPC unavailable: use recorded fixtures; note in results.

## Cardinal rules (do NOT)

- Do NOT run these scenarios with real funds.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §6–7: verified behaviours.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.64 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T060-verify-treasury-gates-depeg-caps`
- PR title: `P6-T060: Treasury: cost gate blocks uneconomic moves; depeg auto-reduce; caps and reserve hold`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
