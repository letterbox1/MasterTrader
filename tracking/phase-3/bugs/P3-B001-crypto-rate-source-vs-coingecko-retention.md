---
id: P3-B001
kind: gap
title: Crypto rate source undefined and CoinGecko retention conflicts with 7-year journal
phase: 3
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.03]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B001-crypto-rate-source-vs-coingecko-retention
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Architecture (FX & price service)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B001 · Crypto rate source undefined and CoinGecko retention conflicts with 7-year journal

## Goal / expected outcome

The journal's crypto price source is a named, licence-compatible source whose values may be stored for ≥ 7 years.

## Context & references

- [09 architecture](../../../docs/09-journal-and-tax.md#architecture) says "reputable-exchange rate for crypto" without naming it
- [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules): CoinGecko cache ≤ 24 h, no long-lived archive
- [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view): wallet view prices from CoinGecko cached ≤ 24 h
- Affects: P3-T011, P3-T030, P3-T010

## Requirements

- **Steps to reproduce:** Read 09 FX/price service and 12 §4 CoinGecko row, then try to decide where a 2026 airdrop's AUD value comes from in 2032.
- **Expected:** One named source per asset class with retention ≥ 7 years and a fallback order.
- **Actual:** Unnamed; the obvious free aggregator (CoinGecko) forbids storage beyond 24 h, but tax values must be kept ≥ 7 years with their source.
- **Impact:** Wrong or unreproducible tax values; possible data-terms breach. (severity S2)
- **Suggested fix:** Add to 09: crypto prices come from our own recorded exchange bars (P1) with the venue preference in P3-T011; CoinGecko is display-only and never persisted to `journal.*`.

## ToDo

- [ ] Agree the venue preference list (AU venues first) and add it to 09 §Architecture
- [ ] Add a sentence to 13 §3 that wallet-view prices are display-only
- [ ] Update the affected task files (P3-T011, P3-T030, P3-T010) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T011, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Decision recorded in the owning doc
- [ ] Affected tasks consistent with it
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/09-journal-and-tax.md`: record the decision.
- `docs/13-wallets-treasury-and-onchain.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B001-crypto-rate-source-vs-coingecko-retention`
- PR title: `P3-B001: Crypto rate source undefined and CoinGecko retention conflicts with 7-year journal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B001` run

## Progress log

- 2026-10-21 00:00 · planner · opened
