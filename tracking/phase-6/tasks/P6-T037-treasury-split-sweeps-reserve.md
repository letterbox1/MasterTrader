---
id: P6-T037
kind: task
title: Treasury split, daily profit sweeps, concentration limits and the reserve
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T033, P5-T028, P5-T022, P3-T018]
requirements: [R6.22, R6.24]
roadmap_todos: [T6.28]
modules: [M22, M18]
dashboards: [D18]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, prefect, nats]
branch: p6/P6-T037-treasury-split-sweeps-reserve
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T037 · Treasury split, daily profit sweeps, concentration limits and the reserve

## Goal / expected outcome

A daily treasury job keeps working floats per sleeve, sweeps realised profit above the floats into stablecoins and on to the vault address, enforces stablecoin-issuer concentration limits, and holds the **20–40% reserve**, with every move as an intent through M11 and the cost gate.

## Context & references

- Roadmap: [R6.22](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §5](../../../docs/13-wallets-treasury-and-onchain.md#5-treasury) (floats, daily sweep, concentration, 20–40% reserve) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) (concentration per protocol/chain/stablecoin/venue) · [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) (vault watch-only)
- Cross-phase: P5-T028 (sweep scheduler, kill sweep/freeze), P5-T022 (wallet view), P3-T018 (internal-transfer matcher: transfers are never disposals); M11 via P2-T017
- Decisions: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P6-B008 venue cap one value; P5-B008 vault/warm watch-only) · defaults [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown), [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)
- Depends on (this phase): P6-T033

## Requirements

- Daily Prefect flow (after EOD reconciliation): compute realised profit per sleeve from the journal; amount above float → sweep proposal.
- Sweep path: venue/hot → stables → vault address (allow-listed destination only); exchange withdrawals are **manual tasks** (keys have withdrawals disabled).
- Concentration: per stablecoin-issuer cap (default ≤ 50% of stables in any one issuer, a setting proposed for 16 §2.7) and the venue cap read from the L1 risk policy (default ≤ 25% of total equity per venue, 16 §2.1; one value everywhere); breaches → rebalance proposal + alert.
- Reserve check: reserve % of portfolio in stables/AUD kept within band; below min → stop new earn entries and propose top-up.
- Internal transfers tagged in the journal (never disposals).

## ToDo

- [ ] `mt_treasury.sweeps` flow + proposals.
- [ ] Concentration + reserve monitors publishing `treasury.*` events.
- [ ] Journal tagging integration.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: profit-above-float calc; concentration breach detection; reserve band logic.
- Integration: fixture day → expected sweep proposals and tasks.

### Scenarios
- Given sleeve A realised +$800 above its float, then a sweep proposal exists and, for an exchange balance, a manual withdrawal task appears in D13.
- Given USDT is 70% of stables, then a concentration alert and rebalance proposal are created.
- Given the reserve falls to 18%, then earn entries are blocked until restored.

### Stress / failure injection
- Run the flow over 90 days of fixture fills; proposals deterministic and journal tags complete.

## Acceptance criteria

- [ ] Daily flow live in paper mode with proposals visible in D18.
- [ ] Reserve and concentration monitors alert correctly.

## Exceptions & edge cases

- Recon mismatch open → sweeps paused.
- Kill switch ON → sweeps of hot balances follow P5 kill behaviour; treasury entries frozen.

## Cardinal rules (do NOT)

- Do NOT enable withdrawals on exchange keys to automate sweeps.
- Do NOT sweep to any non-allow-listed address.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §5: issuer cap default and sweep path.
- `docs/16-configuration-and-safety-model.md` §2.7: add the stablecoin-issuer cap default.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T037-treasury-split-sweeps-reserve`
- PR title: `P6-T037: Treasury split, daily profit sweeps, concentration limits and the reserve`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (venue cap from L1 risk policy 25% (17 §B P6-B008); issuer cap as a setting; cross-phase deps P5-T028/P5-T022/P3-T018; run fields)
