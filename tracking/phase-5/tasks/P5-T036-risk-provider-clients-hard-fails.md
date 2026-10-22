---
id: P5-T036
kind: task
title: Risk providers (GoPlus, Honeypot.is, RugCheck) and hard-fail rules
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T035, P5-T031]
requirements: [R5.13]
roadmap_todos: [T5.26]
modules: [M4]
dashboards: [D12]
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p5/P5-T036-risk-provider-clients-hard-fails
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

# P5-T036 · Risk providers (GoPlus, Honeypot.is, RugCheck) and hard-fail rules

## Goal / expected outcome

Provider clients for **GoPlus** (EVM primary + approval/phishing checks), **Honeypot.is** (EVM sell simulation) and **RugCheck.xyz** (Solana primary) feed `token_risk_report`, and the hard-fail rules (blocklisted domain/contract/deployer, honeypot or failed sell simulation, approval-granting off-chain signature required, claim domain ≠ official domain, unverified contract for autonomous paths, blacklist link) set risk = 100 = reject with reasons.

## Context & references

- Roadmap: [R5.13](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.26
- [08 risk score hard fails](../../../docs/08-airdrops-and-token-launches.md#risk-score-0100-any-hard-fail--100--reject) · [research risk sources](../../../docs/research/airdrops-rugpull-discord.md) · [12 §4 GoPlus/RugCheck](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)

## Requirements

- GoPlus limits: 150K CU/month, 30K/day, 150/min; one key, cache per token (24 h), no proxies. Built and tested on recorded fixtures without the key; the live keyed run is P5-T068 (key from P0-T010).
- Honeypot.is and RugCheck read endpoints free (limits unverified): conservative 30/min each with backoff.
- Raw provider reports stored (collapsed in D12) with provenance; normalised flags mapped to our feature names.
- Hard-fail evaluation is deterministic, ordered, and every fail carries a human-readable reason and source.
- Provider unavailable ≠ pass: missing primary report → `incomplete` → autonomous paths blocked; task/watch only.

## ToDo

- [ ] Implement `packages/mt_airdrop/risk/providers/` (goplus.py, honeypot_is.py, rugcheck.py) with quota registration.
- [ ] Implement `risk/hard_fail.py` rule set with reason codes.
- [ ] Fixture tests incl. known honeypot and known clean tokens; doc sync.

## Verification

### Tests
- Unit: each hard-fail rule fires on its fixture and not on a clean fixture.
- Unit: GoPlus response mapping for honeypot/mintable/balance-changeable/tax-modifiable flags.
- Integration: missing RugCheck report for a Solana token → `incomplete`, decision engine cannot auto-claim.

### Scenarios
- Given Honeypot.is reports sell failure, then risk = 100 with reason "sell simulation failed (Honeypot.is)" and the opportunity is rejected.
- Given the claim site needs an EIP-712 Permit to claim, then hard fail "approval-granting signature required".

### Stress / failure injection
- GoPlus at 140/min sustained for 30 min: client stays under 150/min; burst queue drains in priority order.

## Acceptance criteria

- [ ] Three provider clients live within quotas
- [ ] All 08 hard fails implemented with reasons
- [ ] Missing reports block autonomy

## Exceptions & edge cases

- Provider returns contradictory flags: take the riskier; record both.

## Cardinal rules (do NOT)

- Do NOT treat "no data" from a provider as a pass.
- Do NOT bulk-mine provider data or use proxies to exceed limits.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: hard-fail reason codes.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.26 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T036-risk-provider-clients-hard-fails`
- PR title: `P5-T036: Risk providers (GoPlus, Honeypot.is, RugCheck) and hard-fail rules`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless fixtures, live run in P5-T068)
