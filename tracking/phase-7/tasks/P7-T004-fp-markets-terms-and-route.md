---
id: P7-T004
kind: task
title: FP Markets: read algo/scalping/hedging clauses and choose MT5 or cTrader
phase: 7
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.10, R7.13]
roadmap_todos: [T7.08]
modules: [M12]
dashboards: [D06]
branch: p7/P7-T004-fp-markets-terms-and-route
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/12-policy-and-compliance.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T004 · FP Markets: read algo/scalping/hedging clauses and choose MT5 or cTrader

## Goal / expected outcome

You know whether FP Markets' AU client agreement permits algorithmic trading, scalping and hedging for your MasterTradingBot strategies, and you have chosen the execution route (MT5 on a Windows VPS, cTrader Open API, or both).

## Context & references

- Roadmap: [R7.10, R7.13 · ToDo T7.08](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (execution stays on FP Markets; MT5 primary, cTrader Linux route; open items) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (FP Markets row: clauses (U)) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15)
- Related: P7-T005 (VPS, MT5 route), P7-T034/T036 (MT5 bridge + adapter), P7-T037 (cTrader adapter) — cancel the adapter task for the route you don't choose.

## Requirements

- Record: algo trading allowed (Y/N/conditions), scalping restrictions (minimum hold time, if any), hedging allowed, EA/API restrictions, server name in your client area (decides LD4 vs NY4 VPS location), whether FIX is available to retail, cTrader Open API rate limits.
- Choose route: `mt5`, `ctrader` or `both`; write the choice and reason on the `PRO_ADVICE`/`VENUE_CHECK` task.
- If any clause forbids a strategy style, that MasterTradingBot strategy is excluded from the port (P7-T038).

## ToDo

- [ ] Download the current FP Markets AU client agreement and PDS from the client area.
- [ ] Read the clauses on algorithmic trading, scalping, hedging, EAs/APIs; note the clause numbers.
- [ ] Note your MT5 server name (client area) and whether a cTrader account is available on your login.
- [ ] Record the findings and the route choice on the FP Markets task in D13; update the FP Markets venue row in D06 (tightening immediate).
- [ ] Tell the planner which adapter task (P7-T036 or P7-T037) to cancel, if any.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given the agreement forbids holds under 2 minutes, then scalper strategies with shorter holds are excluded from the port and the parity test.

### Stress / failure injection
- n/a: document review.

## Acceptance criteria

- [ ] FP Markets task records each clause finding with clause numbers.
- [ ] Route choice recorded; the unchosen adapter task is cancelled or kept with a reason.

## Exceptions & edge cases

- Clauses ambiguous: treat as forbidden until FP Markets confirms in writing.
- Server moves (LD4 ↔ NY4): re-site the VPS (P7-T005).

## Cardinal rules (do NOT)

- Do NOT run any MasterTradingBot strategy live that the agreement forbids.
- Do NOT share your FP Markets password in any task text.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT open multiple KYC accounts, use VPNs/proxies, or self-match across sub-accounts (12 §3).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: close the open items (clauses, FIX, cTrader limits).
- `docs/12-policy-and-compliance.md` §2: FP Markets row loses its (U).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.08 when this item is done.

## Branch & PR

- Branch: `p7/P7-T004-fp-markets-terms-and-route`
- PR title: `P7-T004: FP Markets: read algo/scalping/hedging clauses and choose MT5 or cTrader`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T004` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
