---
id: P2-T009
kind: task
title: "Strategy templates batch 2: evidence-catalogue and special types"
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T008]
requirements: [R2.02, R2.03]
roadmap_todos: [T2.21]
modules: [M0]
dashboards: [D03]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T009-templates-evidence-catalogue
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T009 · Strategy templates batch 2: evidence-catalogue and special types

## Goal / expected outcome

Templates for grid/DCA, pairs/stat-arb, event-driven, ML-signal, funding carry (regime-gated), cross-sectional momentum, token-unlock positioning and memecoin momentum (paper-only) exist with parameter schemas; the deterministic rule-based template slot is registered for Part B's MasterTradingBot libraries.

## Context & references

- Roadmap: [R2.02, R2.03](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.21
- Spec: [14 §3 catalogue](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §4 regime filters](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe)
- Policy: [12 §2 venue registry: carry needs perps](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- Part B: deterministic rule-based template (T2.31) and ML-signal model loading (tier A, T2.30) plug into the slots defined here.

## Requirements

- Funding carry: long spot / short perp same venue, only when trailing 7-day annualised funding > fees + buffer (start 8%), hedged 1×; flagged `requires: perps`; while perps are `blocked` for AU retail it runs on paper only where the product is marked `paper_ok` ([12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry), 17 §D P2-B008).
- Memecoin momentum: enter 5–60 min after launch (never first slot), rug filter hook, time stops, partial profits, never average down; manifest flag `paper_only: true` enforced by the lifecycle mode ceiling; the memecoin gate profile needs ≥ 300 paper trades (16 §2.4).
- Cross-sectional momentum: top-20 liquid, survivorship-free universe input (dynamic selection rule).
- Token-unlock: short into large team cliffs, needs a perp (paper-only under current registry).
- Event-driven: entry windows keyed on `cal.*`/`evt.*` events (blackout-aware: 15 min before to 15 min after high-importance events for `event_sensitive` bots by default, 16 §2.8; calendars land in P4, so P2 uses manual event lists).
- ML-signal: consumes a tier-A model id from the MLflow registry via an interface (`ModelSignalProvider`).
- Grid/DCA and pairs/stat-arb (P3 evidence) with explicit inventory caps.

## ToDo

- [ ] Implement the 8 templates + schemas
- [ ] Register `deterministic_rule_based` template slot (manifest + interface only)
- [ ] Enforce `paper_only` in the lifecycle (P2-T007 hook)
- [ ] Template smoke backtests on fixtures
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Template tests: valid manifest + backtest completes for each (D03 acceptance 1).
- Unit: carry entry blocked when trailing funding < fees + 8%.
- Unit: memecoin template refuses averaging down and entries < 5 min after launch.
- Unit: promotion of a `paper_only` template beyond `paper` refused.

### Scenarios
- Given funding drops below the threshold, when the carry strategy holds a position, then it emits an exit intent (exit plan) and no new entry.
- Given the venue registry marks perps `blocked` + `paper_ok`, when a carry bot in `hitl` mode tries a testnet order, then M11 rejects it, while the same bot in `paper` mode continues; without `paper_ok`, paper is rejected too.

### Stress / failure injection
- Nightly: run all batch-2 templates over 1 year of fixture data; no exceptions.

## Acceptance criteria

- [ ] 8 templates + rule-based slot registered
- [ ] Paper-only enforcement tested
- [ ] Regime gates tested
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Funding data missing (DQ degraded): carry holds, no new entries.
- Dynamic universe empty: strategy idles, logs reason.

## Cardinal rules (do NOT)

- Do NOT let memecoin or unlock templates leave paper in this phase.
- Do NOT read Telegram text as a signal input; postures only (P4).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- No Telegram text in any model, RAG index or training set (12 §4–5).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §3: mark which catalogue rows have templates.
- `docs/03-build-spec.md` M0: template list as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.21 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T009-templates-evidence-catalogue`
- PR title: `P2-T009: Strategy templates batch 2: evidence-catalogue and special types`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper_ok rule for blocked perps, memecoin ≥ 300 trades gate, blackout defaults)
