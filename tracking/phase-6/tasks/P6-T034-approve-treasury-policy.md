---
id: P6-T034
kind: task
title: Approve the treasury policy and protocol allow-list (C3); decide on HLP
phase: 6
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P6-T033]
requirements: [R6.20, R6.21, R6.22]
roadmap_todos: [T6.03]
modules: [M22]
dashboards: [D18]
branch: p6/P6-T034-approve-treasury-policy
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

# P6-T034 · Approve the treasury policy and protocol allow-list (C3); decide on HLP

## Goal / expected outcome

You have reviewed and approved (C3) the first treasury policy and the protocol allow-list, and decided whether HLP is allowed (only if Hyperliquid is approved for you).

## Context & references

- Roadmap: [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.22](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.03
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) · [13 §5](../../../docs/13-wallets-treasury-and-onchain.md#5-treasury) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (HLP ≤ 10% of stables, P1 capped)
- UI: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) `/wallets/treasury`
- Unblocks: P6-T038 earn execution, P6-T060 verification
- Depends on (this phase): P6-T033

## Requirements

- Decide reserve % (20–40%), floats per sleeve, per-protocol (≤ 20%), per-chain and per-stablecoin caps.
- Choose the initial allow-list (e.g. JitoSOL/mSOL/stETH, core Aave/Spark/Kamino markets, Pendle PTs) and which entries may auto-move (stablecoin lending only).
- HLP: yes only if the venue registry says Hyperliquid is `allowed` for your residency; cap ≤ 10% of stables.

## ToDo

- [ ] Open D18 → Treasury policy; review the seeded draft.
- [ ] Edit values; submit `treasury.policy.update` and `treasury.allow_list.add` for each protocol.
- [ ] Approve each C3 prompt in Telegram with your TOTP; wait out the cool-down.
- [ ] Confirm the active policy version in D18 and note it (version number only) in the progress log.

## Verification

### Tests
- n/a: human approval; enforcement tested in P6-T060.

### Scenarios
- Given you approve the policy, when the cool-down ends, then D18 shows the new version as active and M11 uses it.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] Active policy version recorded.
- [ ] Allow-list approved; HLP decision recorded.

## Exceptions & edge cases

- You can tighten any time (C1); loosening later repeats C3.

## Cardinal rules (do NOT)

- Do NOT approve third-party curator vaults (Stream Finance-style risk) onto the allow-list.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4: note that the allow-list is user-approved (no values).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.03 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T034-approve-treasury-policy`
- PR title: `P6-T034: Approve the treasury policy and protocol allow-list (C3); decide on HLP`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
