---
id: P2-B006
kind: gap
title: STP rule undefined for venues with no STP parameter (Alpaca, OANDA, IG, IBKR)
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.31]
roadmap_todos: []
modules: [M12]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B006-stp-venues-without-parameter
pr: ""
doc_sync: [docs/12-policy-and-compliance.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B006 · STP rule undefined for venues with no STP parameter (Alpaca, OANDA, IG, IBKR)

## Goal / expected outcome

12 §3 says what 'STP sent explicitly on every order' means where a venue has no STP field.

## Context & references

- [12 §3 STP table](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Affects P2-T022, P2-T024–T026, P2-T056.

## Requirements

- **Steps to reproduce:** 12 §3 lists STP parameters only for OKX, Binance, Kraken, BTC Markets; R2.31 requires explicit STP on every order and Phase 2 builds Alpaca/OANDA/IG adapters.
- **Expected:** A documented engine-side self-cross guard for venues without native STP, recorded as `stp_mode=engine_guard`.
- **Actual:** Requirement can't be met literally on those venues; behaviour unspecified.
- **Suggested fix:** Add rows for Alpaca/OANDA/IG/IBKR: 'no native STP → engine self-cross guard (block an order that would cross own resting order on the same account)'. Implemented in P2-T022.
- **Impact:** S3: STP audit (P2-T056) would fail or be fudged.

## ToDo

- [x] Decision recorded: netting brokers (OANDA, IG, Alpaca, IBKR) have no STP field → registry `stp: n/a (netting)`; one strategy per account/sub-account where netting would merge bots
- [x] Docs agree: 12 §2/§3
- [x] Tasks updated: engine-guard design replaced by the netting rule (P2-T022, adapters, P2-T036 bot creation, P2-T056 audit)

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given an OANDA order crossing own resting order, when submitted, then the engine guard rejects it.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (12 §2 registry table (STP row) and §3 STP table (netting-broker row `stp: n/a (netting)`))
- [x] Affected tasks reference the decision (P2-T022, P2-T024, P2-T025, P2-T026, P2-T036, P2-T056)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §3: new rows.

## Branch & PR

- Branch: `p2/P2-B006-stp-venues-without-parameter`
- PR title: `P2-B006: define STP for venues without an STP parameter`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B006); docs carry it (12 §2 registry table (STP row) and §3 STP table (netting-broker row `stp: n/a (netting)`)); implementation owned by P2-T022, P2-T024, P2-T025, P2-T026, P2-T036, P2-T056)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B006)); docs updated: 12 §2 registry table (STP row) and §3 STP table (netting-broker row `stp: n/a (netting)`); implementation owned by P2-T022, P2-T024, P2-T025, P2-T026, P2-T036, P2-T056
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
