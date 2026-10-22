---
id: P5-T042
kind: task
title: Never-automated policy guard enforced server-side at every layer
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T011, P5-T014, P5-T015]
requirements: [R5.16, R5.15]
roadmap_todos: [T5.27, T5.28]
modules: [M4, M19, M22, M15]
dashboards: [D12, D13, D18]
tools: [uv]
mcp: []
env: []
services: []
branch: p5/P5-T042-never-automated-policy-guard
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/07-security-notes.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T042 · Never-automated policy guard enforced server-side at every layer

## Goal / expected outcome

One shared policy module (`mt_core.policy.never_automated`) encodes the **never automated** list and is enforced in four places — `mt_api` command layer, decision engine/task generator, claim executor and signer — so permits, SIWE on unknown domains, approvals, buying/bridging into launches, connecting wallets, sybil patterns, social actions, captchas, KYC and drainer patterns can never execute automatically, whatever the caller.

## Context & references

- Roadmap: [R5.16](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.15 · ToDos T5.27, T5.28 · tests P5-T053
- [08 never automated](../../../docs/08-airdrops-and-token-launches.md#never-automated) · [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims) · [D12 rules](../../../docs/ui/dashboards/D12-airdrops.md) · [D18 never offered](../../../docs/ui/dashboards/D18-wallets-treasury.md)

## Requirements

- Policy items (IDs NA-01…NA-14): main/cold wallet actions; LLM-visible keys; Permit/Permit2/EIP-712/`personal_sign` of arbitrary payloads; SIWE on unknown domains; approvals/`setApprovalForAll` (except signer-built sized approvals); buying/swapping/bridging into new launches (ICO/IDO); connecting a wallet to any site/eligibility checker; multiple wallets per campaign/sybil; any social action; captcha solving; Discord self-bots; KYC/launchpad registration; claim-fee payments to an EOA; simulation showing a non-gas outflow.
- Enforcement points: command registry denylist + argument checks; task generator never emits automated variants; executor pre-check; signer hard blocks (P5-T014/T015) reference the same IDs.
- Sybil guard: one identity wallet per chain per campaign; a second wallet in the same campaign → refuse (`NA-09`).
- Every refusal is audited with the NA ID and surfaced in D12/D13 as a reason.
- UI never renders controls for these actions (checked by Playwright in P5-T048–T050).

## ToDo

- [ ] Implement the policy module with IDs and a `check(action) → allow | refuse(NA-xx)` API.
- [ ] Wire into mt_api middleware, decision engine, executor and signer.
- [ ] Campaign-wallet uniqueness constraint in `campaign_record`.
- [ ] Tests per NA ID at every enforcement point; doc sync.

## Verification

### Tests
- Unit: one test per NA ID per enforcement point (matrix ≥ 14 × 4).
- Integration: a crafted mt_api call bypassing the UI to request a permit signature → refused with NA ID and audited.
- Integration: assigning a second wallet to an existing campaign → refused NA-09.

### Scenarios
- Given an opportunity whose only claim path is "connect wallet on site", then the outcome is CLAIM_MANUAL with the standing warning, never auto.
- Given a mandate creation request listing `approve` as a function, then creation is rejected (NA-05) before C3.

### Stress / failure injection
- Mutation test: remove any single enforcement point in a test build → at least one other layer still refuses every NA scenario (defence in depth).

## Acceptance criteria

- [ ] All 14 NA items enforced at all applicable layers
- [ ] Refusals audited with IDs
- [ ] No UI control for any NA action
- [ ] Defence-in-depth mutation test passes

## Exceptions & edge cases

- Ambiguous classification (e.g. unknown selector that might approve): refuse by default.
- Proof of control (P5-T067) only verifies a signature you made in your own wallet app; the system never requests or produces one, so NA-03 still holds.

## Cardinal rules (do NOT)

- Do NOT add configuration flags that disable any NA item.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: NA IDs next to the list.
- `docs/07-security-notes.md` §4: reference the shared policy module.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.27, T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T042-never-automated-policy-guard`
- PR title: `P5-T042: Never-automated policy guard enforced server-side at every layer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; proof-of-control is verify-only, consistent with NA-03)
