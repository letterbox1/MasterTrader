---
id: P5-T041
kind: task
title: Decision engine: reject / task / watch / auto-claim with fresh-launch default-reject
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T040, P5-T038, P5-T029]
requirements: [R5.15, R5.17, R5.14]
roadmap_todos: [T5.27]
modules: [M4, M19]
dashboards: [D12, D13]
branch: p5/P5-T041-decision-engine-fresh-launch-reject
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T041 · Decision engine: reject / task / watch / auto-claim with fresh-launch default-reject

## Goal / expected outcome

A deterministic decision engine turns risk, corroboration, viability/EV, eligibility and mandate coverage into exactly one of **reject** (with reasons), **user task** (typed, with steps), **watch** or **auto-claim** (only if an active mandate covers it), writes a `decision` row with the full trail, and default-rejects fresh launches (< 24 h, unverified, or no locked liquidity).

## Context & references

- Roadmap: [R5.15](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.17, R5.14 · ToDo T5.27
- [02 F8](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [08 autonomous](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) · [08 fresh launches](../../../docs/08-airdrops-and-token-launches.md#fresh-launches--memecoins)
- Never-automated guard P5-T042; tasks via P5-T029

## Requirements

- Order: hard fail → reject; fresh launch → reject (`fresh_launch`) unless routed to the P7 memecoin template (not in P5); corroboration < 2 → watch; EV ≤ 0 → watch; AU excluded → reject-for-you (`excluded_geo`); otherwise task or auto-claim.
- Auto-claim candidate only if all hold: claim contract verified and referenced by ≥ 2 official sources; function on an active mandate's allow-list; no approvals/permits/EIP-712, `msg.value = 0`; public-address eligibility proven (Merkle proof/claim contract); burner run clean when required; caps and cost gate pass (checked at execution).
- Task mapping: social → JOIN_DISCORD/FOLLOW_X/QUEST; claims needing signatures or borderline risk → CLAIM_MANUAL; ICO/IDO → ICO_REVIEW (always a user task); protocol use → ONCHAIN_ACTION_MANUAL or GENUINE_USE.
- Decision row: inputs snapshot (score versions), outcome, reasons, policy version; re-decide on rescore (`airdrop.rescore`).
- Publishes `airdrop.decision`.

## ToDo

- [ ] Implement `packages/mt_airdrop/decide/engine.py` with a rules table and versioning.
- [ ] Task generator per type with step templates and verified links.
- [ ] `airdrop.reject` (C1) and `airdrop.rescore` (C0) handlers.
- [ ] Decision-table tests; doc sync.

## Verification

### Tests
- Unit: decision table covering every branch (≥ 25 cases) incl. ties and missing data.
- Unit: ICO/IDO always becomes ICO_REVIEW, never auto.
- Integration: an opportunity with active mandate but `incomplete` risk → CLAIM_MANUAL.

### Scenarios
- Given a token launched 3 h ago with no LP lock, then reject `fresh_launch` with reasons.
- Given an eligible Merkle claim with mandate coverage and ≥ 2 official sources, then auto-claim is queued for the executor (P5-T044).

### Stress / failure injection
- Re-decide 5,000 opportunities after a weights change < 2 min; no duplicate tasks (idempotency).

## Acceptance criteria

- [ ] Exactly one outcome per opportunity with a full trail
- [ ] Fresh launches default-rejected
- [ ] Auto-claim only with mandate coverage and all conditions
- [ ] Every reject has reasons

## Exceptions & edge cases

- Mandate expires between decision and execution: executor re-checks and downgrades to CLAIM_MANUAL.

## Cardinal rules (do NOT)

- Do NOT auto-claim anything the never-automated list covers (P5-T042).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: decision table.
- `docs/02-v1-architecture.md` F8: precise branch order.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.27 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T041-decision-engine-fresh-launch-reject`
- PR title: `P5-T041: Decision engine: reject / task / watch / auto-claim with fresh-launch default-reject`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
