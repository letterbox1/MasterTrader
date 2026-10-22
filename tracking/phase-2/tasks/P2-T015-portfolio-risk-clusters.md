---
id: P2-T015
kind: task
title: "Portfolio-level risk: correlation clusters, concentration, VaR/ES"
phase: 2
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T014]
requirements: [R2.11]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
tools: [uv]
mcp: []
env: []
services: [nats]
branch: p2/P2-T015-portfolio-risk-clusters
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T015 · Portfolio-level risk: correlation clusters, concentration, VaR/ES

## Goal / expected outcome

The portfolio policy level works: exposure per correlated cluster (USD, crypto beta, etc.), concentration limits and a daily VaR/ES estimate are computed and checked pre-trade, and exposed to the D06 breakdown.

## Context & references

- Roadmap: [R2.11](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [03 M11 portfolio level](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [D06 Exposure breakdown](../../../docs/ui/dashboards/D06-risk.md)
- Data: bars via `pit(as_of)` (P1). The D06 Stress tab is a placeholder in P2 (R2.57, P2-T043); the historical shock replay and `risk.stress.run` are built in P7 (R7.16, T7.27).
- Defaults: cluster caps, concentration and the VaR confidence/horizon are L1 settings with documented defaults; venue concentration ≤ 25% of total equity is evaluated in P2-T012 ([16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).

## Requirements

- Clusters from policy (`clusters: {usd: [...], crypto_beta: [...]}`) plus rolling 90d correlation clustering as an advisory view.
- Pre-trade: post-trade cluster exposure ≤ cluster cap; single-instrument concentration ≤ cap.
- VaR/ES: historical simulation, default 1-day, 99% (L1 settings, editable), recomputed every 5 min off the order path and cached in KV; pre-trade uses the cached marginal estimate (no heavy compute in the check).
- `/risk/state?breakdown=1` returns by asset class, currency, venue, strategy, cluster + VaR/ES.

## ToDo

- [ ] `packages/mt_risk/portfolio.py` (cluster exposure, concentration, VaR/ES job)
- [ ] Prefect/engine timer for the 5-min recompute
- [ ] Breakdown endpoint fields
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: cluster cap rejection.
- Unit: VaR on a known return series equals the textbook quantile.
- Integration: breakdown endpoint returns all dimensions.

### Scenarios
- Given USD cluster cap 50% of equity, when an EURUSD short pushes USD long exposure to 55%, then reject `cluster_cap:usd`.

### Stress / failure injection
- VaR job over 200 instruments × 2 years daily returns < 2 s; pre-trade lookup unaffected (p99 < 1 ms holds).

## Acceptance criteria

- [ ] Cluster and concentration checks in the gate
- [ ] VaR/ES cached and shown via API
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Insufficient history for VaR: show 'n/a' and do not block trading on VaR alone (cluster caps still apply).

## Cardinal rules (do NOT)

- Do NOT run VaR computation inside the pre-trade check.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M11: VaR method and cadence.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T015-portfolio-risk-clusters`
- PR title: `P2-T015: Portfolio-level risk: correlation clusters, concentration, VaR/ES`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (stress tab placeholder (R2.57) and P7 replay noted; caps as L1 settings)
