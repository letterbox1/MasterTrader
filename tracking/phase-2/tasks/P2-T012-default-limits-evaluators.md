---
id: P2-T012
kind: task
title: Default hard-limits pack and limit evaluators
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010]
requirements: [R2.14, R2.13]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T012-default-limits-evaluators
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T012 · Default hard-limits pack and limit evaluators

## Goal / expected outcome

The default limits of [16 §2.1–§2.3](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (mirrored in 14 §5) ship as install defaults in the layered policy (P2-T010) and each has an evaluator with the specified on-breach action, including the **two-stage sleeve and system drawdowns** on the 16 §2.1 drawdown basis, with live usage tracked in `risk.limit_state` and NATS KV `risk_state`.

## Context & references

- Roadmap: [R2.14](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5 default hard limits](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §4 per-trade risk, leverage](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [03 M11 global limits](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Decisions: [17 §A P2-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (two-stage drawdowns) · [17 §C P2-B003](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (collar, deadlines, cost blow-out) · [16 §2.3 `risk.sleeve.restart` C3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)
- Related: P2-T048 (you review the prefilled defaults), P2-T069 (strictest-wins merge feeds the evaluators), P2-T070 (inline data age, decision deadline, integrity and egress checks), P2-T018 (ladder).

## Requirements

- Defaults (16 §2.1, all configurable, none hard-coded): risk/trade 1% of sleeve equity [0.1–2%] → reject (memecoin 0.25–0.5% of total equity); max position 10% of sleeve (memecoin 2%) → reject; daily loss 3% of sleeve → sleeve halts until the next day (**Sydney time**); open positions 10 per sleeve → reject new entries; leverage 1× until you approve more (loosening = C3), crypto derivatives ≤ 2× (L0 ceiling) → reject; venue concentration ≤ **25%** of total equity per venue [10–30%] → block new exposure there; price collar 2% crypto majors / 0.5% FX majors / 1% ETFs from the last trade → reject; API/RPC errors 5 in 60 s → pause **that venue's** orders 10 min; cost blow-out realised ÷ modelled > 1.5× over the last 20 fills → **pause the bot** + alert.
- **Sleeve drawdown, two stages** (L3): stage 1 at 10% below the sleeve peak → halve new position sizes; stage 2 at 15% → halt the sleeve (cancel orders, close per the sleeve's exit rule, alert); restart only via `risk.sleeve.restart` (**C3**). Save-time rule: stage 1 < stage 2.
- **System drawdown, two stages** (L1): stage 1 at 10% below the portfolio peak → no new entries anywhere (exits and protective orders continue; restart C3); stage 2 at 25% → flatten to stablecoins/AUD + 30-day review lock; a second stage-2 event ends the trading programme (state `programme_ended`, critical alert + USER task; capital to hold-and-earn happens manually until P6).
- **Drawdown basis** (16 §2.1): trading equity in AUD, marked to market (realised + unrealised), excluding the vault and hold-and-earn, adjusted for your deposits and withdrawals, measured from its running peak; the peak resets only after a review lock ends or by a C3 reset. Sleeve stages use the sleeve's own equity on the same basis.
- Data age, decision deadline, WORM integrity and egress are checked inline by P2-T070 (not here).
- Global (03 M11): max gross/net exposure, max open orders, order-rate limit, trading hours/blackouts.
- Each evaluator returns `(pass|reject|hold|halt, rule_id, observed, limit)`; breaches emit `risk.event` and update `risk.limit_state` (warn at 80%).
- State is incremental (O(1) per order/fill), rebuilt from fills on restart.
- Every number lives in the layered policy as a default from 16 (with its link), none hard-coded in evaluators.

## ToDo

- [ ] Install defaults mirroring 16 §2.1–§2.3 (data in the policy store, P2-T010), each with its 16 section link
- [ ] Drawdown-basis equity tracker (trading equity, deposits/withdrawals adjusted, running peak, C3 peak reset) + two-stage sleeve and system evaluators
- [ ] `risk.sleeve.restart` command (C3) wired through P2-T019; `programme_ended` state after the second system stage-2 event
- [ ] Evaluators in `packages/mt_risk/limits/` (one module per limit)
- [ ] `risk.limit_state` table (latest per scope, not WORM) + KV publication
- [ ] State rebuild from `audit.fill` on restart
- [ ] Golden tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Golden: table of (state, intent) → expected decision for every limit at below/at/above threshold.
- Unit: daily-loss halt resets at the next day boundary only.
- Unit: sleeve stage-2 halt requires `risk.sleeve.restart` (C3: Telegram + TOTP + cool-down), logged; system stage 1 restart is C3 too.
- Golden: sleeve at −9.9% → full size; −10% → new sizes halved; −15% → halt. System at −10% → entries rejected anywhere, exits pass; −25% → flatten + 30-day lock.
- Unit: drawdown basis ignores a deposit/withdrawal (no fake drawdown) and excludes vault and hold-and-earn balances.
- Unit: cost blow-out pauses only the affected bot; API errors pause only that venue.
- Unit: API-error counter sliding window (5 in 60 s) and 10-min pause timer.

### Scenarios
- Given a sleeve at −3.1% today, when a new entry arrives, then reject `daily_loss` and the sleeve shows halted until 00:00 Sydney time.
- Given a sleeve 12% below its peak, when a new entry arrives, then its size is halved and the sleeve keeps trading (stage 1, not a halt).
- Given system drawdown hits 10%, when any new entry arrives, then it is rejected `system_drawdown_stage1` everywhere, exits and protective stops still pass, alert critical; restart is C3.

### Stress / failure injection
- Replay 100k fills + 1M intents through evaluators; state matches a from-scratch recompute; per-check p99 < 50 µs.

## Acceptance criteria

- [ ] Every 14 §5 row has an evaluator, a default and a golden case
- [ ] Breach actions match the table
- [ ] State rebuild verified
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Price missing for exposure calc (stale feed): treat as stale → hold, never assume zero.
- Restart during a halt: halt state persists (rebuilt from `risk.event`).

## Cardinal rules (do NOT)

- Do NOT hard-code limit numbers in evaluator code.
- Do NOT let a halt auto-clear except where 16 §2.1 says so (daily loss at the next Sydney day; venue API pause after 10 min); sleeve and system restarts are C3.
- Do NOT block exits or protective orders in any drawdown stage.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5 and `docs/16-configuration-and-safety-model.md` §2.1: link the install-defaults module as the code source of the table (values unchanged).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T012-default-limits-evaluators`
- PR title: `P2-T012: Default hard-limits pack and limit evaluators`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (defaults from 16 §2.1–§2.3, two-stage sleeve (10/15) and system (10/25 + lock) drawdowns on the 16 drawdown basis, risk.sleeve.restart C3, venue cap 25%, Sydney day, cost blow-out pauses the bot)
