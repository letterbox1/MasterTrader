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
requirements: [R2.14]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T012-default-limits-evaluators
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T012 · Default hard-limits pack and limit evaluators

## Goal / expected outcome

The 14 §5 default limits ship as `packages/mt_risk/policy/defaults.yaml` and each has an evaluator with the specified on-breach action, with live usage tracked in `risk.limit_state` and NATS KV `risk_state`.

## Context & references

- Roadmap: [R2.14](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5 default hard limits](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §4 per-trade risk, leverage](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [03 M11 global limits](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Related: P2-B001 (drawdown de-risk vs halt), P2-B003 (unspecified numbers); P2-T048 sets your actual values.

## Requirements

- Defaults (per sleeve unless noted): risk/trade 1% → reject; max position 10% (memecoin 2%) → reject; daily loss 3% → sleeve halts until next day (UTC day boundary unless policy sets a session); drawdown from peak 15% sleeve / **10% whole system** → halt + alert + manual restart; open positions 10 → reject new entries; stale data 2 s fast / 60 s slow → hold; decision deadline per sleeve → drop decision; API/RPC errors 5 in 1 min → sleeve pauses 10 min; venue concentration 25–30% of capital → block new exposure there; leverage 1× until approved, then ≤ 2× on majors → reject.
- Global (03 M11): max gross/net exposure, max open orders, order-rate limit, trading hours/blackouts.
- Each evaluator returns `(pass|reject|hold|halt, rule_id, observed, limit)`; breaches emit `risk.event` and update `risk.limit_state` (warn at 80%).
- State is incremental (O(1) per order/fill), rebuilt from fills on restart.
- Every number lives in policy (user input), none hard-coded in evaluators.

## ToDo

- [ ] `defaults.yaml` mirroring 14 §5
- [ ] Evaluators in `packages/mt_risk/limits/` (one module per limit)
- [ ] `risk.limit_state` table (latest per scope, not WORM) + KV publication
- [ ] State rebuild from `audit.fill` on restart
- [ ] Golden tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Golden: table of (state, intent) → expected decision for every limit at below/at/above threshold.
- Unit: daily-loss halt resets at the next day boundary only.
- Unit: drawdown halt requires manual restart (`risk.sleeve.resume` C1, logged).
- Unit: API-error counter sliding window (5 in 60 s) and 10-min pause timer.

### Scenarios
- Given a sleeve at −3.1% today, when a new entry arrives, then reject `daily_loss` and the sleeve shows halted until 00:00 UTC.
- Given system drawdown hits 10%, when any new order arrives, then all sleeves halt, alert critical, and resuming needs a manual restart.

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
- Do NOT let a halt auto-clear except where 14 §5 says so (daily loss at next day; API pause after 10 min).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5: link `defaults.yaml` as the code source of the table.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T012-default-limits-evaluators`
- PR title: `P2-T012: Default hard-limits pack and limit evaluators`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
