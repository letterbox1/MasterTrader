---
id: P7-T051
kind: task
title: MT5/cTrader adapter paper parity vs MasterTradingBot outputs
phase: 7
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T038, P7-T036, P7-T037]
requirements: [R7.10]
roadmap_todos: [T7.62]
modules: [M12, M0]
dashboards: [D03, D05]
branch: p7/P7-T051-verify-mt5-ctrader-paper-parity
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T051 · MT5/cTrader adapter paper parity vs MasterTradingBot outputs

## Goal / expected outcome

Over a 2-week paper window on the FP Markets demo account, ported strategies running through MasterTrader's adapter produce the same signals and materially the same orders as MasterTradingBot running side by side, so the adapter can be trusted with money.

## Context & references

- Roadmap: [R7.10 · ToDo T7.62](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (none touches live money until tested in paper) · Roadmap R7.10 'Verified by: paper parity'
- Cross-phase: P2 T2.67 (golden files match).
- Related: P7-T036/T037 (whichever route is chosen; the other is cancelled), P7-T038

## Requirements

- Window: ≥ 10 trading days covering at least one weekly open/close.
- Signals: 100% match on bar-close signals (same timestamps, direction).
- Orders: same side and instrument; size within 1 lot step (sizing differs by design only if documented in the manifest); entry price difference ≤ 1× median spread.
- Every mismatch explained (latency, sizing rule change) or filed as a bug.
- Parity report attached to the progress log; required before any FP Markets bot goes live.

## ToDo

- [ ] Run MasterTradingBot and the MasterTrader bot in parallel on demo accounts.
- [ ] Collect signals/orders; write `tools/parity/mtb_parity.py` comparison.
- [ ] Produce and attach the parity report.
- [ ] File bugs for unexplained mismatches.

## Verification

### Tests
- Comparison script unit tests with fixture logs.

### Scenarios
- Given a weekend gap, then both systems handle the Monday open identically (or the difference is explained).

### Stress / failure injection
- Bridge/adapter restart mid-window: no missed or duplicate signals afterwards.

## Acceptance criteria

- [ ] Signal parity 100%; order parity within the stated tolerances; mismatches explained.
- [ ] Parity report recorded.

## Exceptions & edge cases

- Route not chosen (MT5 or cTrader): run parity only on the chosen route; record that the other adapter task was cancelled.

## Cardinal rules (do NOT)

- Do NOT run this on a live FP Markets account.
- Do NOT change MasterTradingBot behaviour to force parity.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: parity result.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.62 when this item is done.

## Branch & PR

- Branch: `p7/P7-T051-verify-mt5-ctrader-paper-parity`
- PR title: `P7-T051: MT5/cTrader adapter paper parity vs MasterTradingBot outputs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T051` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
