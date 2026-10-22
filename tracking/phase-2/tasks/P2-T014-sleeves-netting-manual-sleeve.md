---
id: P2-T014
kind: task
title: Sleeves, per-asset netting and the manual sleeve
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T012]
requirements: [R2.13]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T014-sleeves-netting-manual-sleeve
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

# P2-T014 · Sleeves, per-asset netting and the manual sleeve

## Goal / expected outcome

Capital is split into sleeves, each with its own capital, risk budget, limits and kill switch; exposure is netted per asset across sleeves against a total per-asset cap; manual tickets use a dedicated `manual` sleeve with its own limits and journal tag.

## Context & references

- Roadmap: [R2.13](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5 sleeves](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §3 allocation table](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §4 manual tickets = manual sleeve](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- UI: [D06 Sleeves widget](../../../docs/ui/dashboards/D06-risk.md) · D05 manual ticket (Part B UI)
- Decisions: sleeves are the **L3** layer ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); two-stage sleeve drawdown 10% halve / 15% halt and `risk.sleeve.restart` (C3) ([16 §2.1, §2.3](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); sleeve names come from your policy, not a fixed list ([17 §D P2-B004](../../../docs/17-decisions-register.md#d-other-decisions), D06 Sleeves row).
- Related: P2-T049 (you choose sleeves), P2-T012 (drawdown evaluators), P2-T069 (layer merge).

## Requirements

- `Sleeve(id, name, capital, risk_budget_pct, limits, drawdown_stages{derisk_pct=10, halt_pct=15}, exit_rule, kill_state, peak_equity)` as L3 config (values are 16 defaults, editable; stage 1 < stage 2 validated at save); sleeve names and count come from your policy (example: 14 §3 list + `manual`); every bot belongs to exactly one sleeve. The bot's mode is set per bot (P2-T037), not per sleeve.
- Netting: per asset (e.g. BTC across spot, perp, different venues), net exposure = Σ sleeves signed delta-equivalent; total per-asset cap enforced on the **post-trade net**; gross also tracked.
- A trade that reduces net exposure but breaches its own sleeve limit is still rejected (sleeve isolation first).
- Per-sleeve kill switch independent of the global one; sleeve DD/halt states from P2-T012.
- `manual` sleeve always exists (created by migration), with its own limits; manual orders tagged `sleeve=manual` for the journal (P3).
- Equity per sleeve marked from fills + marks on the 16 §2.1 drawdown basis (AUD, realised + unrealised, deposits/withdrawals adjusted, vault and hold-and-earn excluded); running peak for the two drawdown stages; peak resets only after a review lock ends or by a C3 reset.
- A halted sleeve restarts only via `risk.sleeve.restart` (C3, P2-T012/P2-T019).

## ToDo

- [ ] `packages/mt_risk/sleeves.py` + netting module `netting.py`
- [ ] Migration: `risk.sleeve` config in policy doc + seed `manual`
- [ ] Per-sleeve kill hooks into P2-T031
- [ ] Golden tests incl. multi-venue netting
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Golden: two sleeves long/short same asset → net within cap passes; a third trade pushing net over the cap rejected.
- Unit: sleeve-A halt doesn't block sleeve-B.
- Unit: manual sleeve orders carry the tag and obey manual limits.

### Scenarios
- Given trend sleeve long 0.5 BTC and carry sleeve short 0.5 BTC perp, when trend adds 0.3 BTC, then net 0.3 BTC is checked against the per-asset cap.
- Given the memecoin sleeve hits its 15% stage-2 drawdown and halts, when the trend sleeve submits, then trend proceeds normally; restarting memecoin asks for C3.

### Stress / failure injection
- Property test: random sequences of fills across 5 sleeves × 20 assets; net exposure equals recomputation; cap never exceeded post-trade.

## Acceptance criteria

- [ ] Sleeves with independent limits + kill
- [ ] Per-asset netting across sleeves enforced
- [ ] `manual` sleeve seeded and tested
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Asset mapping ambiguity (BTC vs WBTC vs BTC perp): explicit `asset_map` in policy; unmapped instrument → reject with `asset_unmapped`.
- FX/CFD notional in non-base currency: convert with latest FX; FX stale → hold.

## Cardinal rules (do NOT)

- Do NOT let one sleeve's capital fund another's breach.
- Do NOT treat manual orders as exempt from M11.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5: document the netting formula.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T014-sleeves-netting-manual-sleeve`
- PR title: `P2-T014: Sleeves, per-asset netting and the manual sleeve`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (sleeves are L3 with two-stage drawdowns, names from policy, restart C3, drawdown basis; mode per bot)
