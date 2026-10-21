---
id: P2-B006
kind: gap
title: STP rule undefined for venues with no STP parameter (Alpaca, OANDA, IG, IBKR)
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B006-stp-venues-without-parameter
pr: ""
doc_sync: [docs/12-policy-and-compliance.md]
doc_sync_status: n/a
found_in: docs/12-policy-and-compliance.md §3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given an OANDA order crossing own resting order, when submitted, then the engine guard rejects it.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

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
