---
id: P5-T045
kind: task
title: Burner-first and identity flow, genuine-use tasks and disposal rule (manual-sale task until P7)
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T044, P5-T029, P5-T020]
requirements: [R5.17, R5.15]
roadmap_todos: [T5.28]
modules: [M4, M19, M22]
dashboards: [D12, D13]
tools: [uv, anvil]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T045-burner-first-identity-disposal-rule
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

# P5-T045 · Burner-first and identity flow, genuine-use tasks and disposal rule (manual-sale task until P7)

## Goal / expected outcome

New or untrusted dApp interactions always run first from a **burner** with minimal float; only after a clean burner run does a task move to the chain's **identity** wallet (one per chain), optionally as a `GENUINE_USE` task under a mandate with caps; on any claim the **disposal rule** (default sell 50%, configurable) creates a manual-sale `ONCHAIN_ACTION_MANUAL` USER task with the cost-gate numbers. Until live execution passes the P7 gates nothing is sold automatically; from P7 the sale becomes an order through M11.

## Context & references

- Roadmap: [R5.17](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.15 · ToDo T5.28 · USER P5-T007
- [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline) · [13 §1 rules](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) · [03 M4 genuine-use](../../../docs/03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop)
- Disposal before P7 (decision P5-B010, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer); 08 wallet discipline; 03 M4): a USER task (manual sale, worked in P5-T066); automated via M11 only once live execution passes the P7 gates

## Requirements

- Burner run: a burner-scoped mandate (tiny caps) for the specific contract/function; record `burner_run` result (simulation + on-chain effects, approvals created/revoked); clean = no unexpected outflows, approvals revoked, contract unchanged.
- Promotion: only after a clean burner run may the opportunity propose identity-wallet tasks; the identity wallet is never used for memecoin churn or unvetted contracts.
- `GENUINE_USE`: real, modest usage sized to genuine use (swap/stake/LP/vote) — no dust loops, volume farming or wash trading; every step is the user's click unless it is a plain claim.
- Disposal rule: after a claim finalises, compute sell qty = disposal % (setting, default 50%) × received and create one `ONCHAIN_ACTION_MANUAL` "manual sale" task (token, chain, wallet, quantity, suggested venue/route, cost-gate estimate, standing warnings, steps incl. `wallet.sweep` to the vault or an exchange you own) for you to do (P5-T066); the remainder is held under M22 rules. No `OrderIntent`, DEX swap or signer intent is created for disposal in P5; the automated M11 path belongs to P7.
- Per-campaign single-wallet constraint (NA-09).

## ToDo

- [ ] Implement `packages/mt_airdrop/flows/burner.py`, `identity.py`, `disposal.py`.
- [ ] Disposal task generator: quantity from the setting, cost-gate estimate from `mt_onchain.costgate` (P5-T020), task via the `TaskFactory` (P5-T029); journal link when you mark it Done (tx hash/order id).
- [ ] Task templates for GENUINE_USE and manual sell; tests; doc sync.

## Verification

### Tests
- Integration: burner run with a mock dApp that leaves an approval → not clean → no identity task; approval revoked.
- Integration: claim of a token listed on an allowed CEX → one manual-sale task for 50% with cost numbers; **no** OrderIntent reaches M11 and no signer intent is created (asserted).
- Unit: token with no known market → the manual-sale task is still created, marked "no known market".

### Scenarios
- Given a clean burner run on protocol P, then a GENUINE_USE task appears for the identity wallet with caps and steps.
- Given the disposal setting is 0%, when a claim finalises, then no disposal task is created and D12 shows "disposal: hold (0%)".

### Stress / failure injection
- n/a: per-claim flow (load covered by P5-T062)

## Acceptance criteria

- [ ] Burner-first enforced before identity tasks
- [ ] Disposal creates a manual-sale USER task; nothing is sold automatically before the P7 gates (test)
- [ ] No identity-wallet use for unvetted contracts

## Exceptions & edge cases

- Burner float insufficient for the run: refill via sweeps module (to float only), else task.

## Cardinal rules (do NOT)

- Do NOT create an automated sale (M11 order, DEX swap or signer intent) for disposal before the P7 gates pass (P5-B010).
- Do NOT propose dust loops or volume farming as genuine use.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: burner-clean criteria and disposal fallbacks.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T045-burner-first-identity-disposal-rule`
- PR title: `P5-T045: Burner-first and identity flow, genuine-use tasks and disposal rule (manual-sale task until P7)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (disposal = manual-sale USER task until the P7 gates per P5-B010; M11 order path removed from P5)
