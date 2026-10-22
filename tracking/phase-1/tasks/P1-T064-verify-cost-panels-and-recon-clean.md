---
id: P1-T064
kind: task
title: Verify cost panels populate and reconciliation runs clean
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T039, P1-T040, P1-T048, P1-T073, P1-T074]
requirements: [R1.11, R1.12]
roadmap_todos: [T1.28, T1.29]
modules: [M16]
dashboards: [D07, D02]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres, mt-api, grafana]
branch: p1/P1-T064-verify-cost-panels-and-recon-clean
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T064 · Verify cost panels populate and reconciliation runs clean

## Goal / expected outcome

Exit criterion 2 is evidenced: spread, funding and swap panels in D07/D02/Grafana are populated for every universe instrument, and 24 h of reconciliation on all practice accounts shows zero unexplained mismatches.

## Context & references

- Roadmap: requirements [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.28](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.29](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Exit criterion 2 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo)) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous)
- Depends on (this phase): P1-T039, P1-T040, P1-T048, P1-T073, P1-T074
- Uses the live runs proven in P1-T073 (cost collectors) and P1-T074 (reconciliation); the stack holds the keys via its sops mounts

## Requirements

- Checklist script over the universe: spread heatmap has ≥ 1 week of hour-of-week data (or all hours observed so far), fee tier present, funding (perps) and financing (FX/CFD) present
- Recon: 24 h at the default cadence (positions/open orders every 60 s, balances every 5 min, one EOD run; [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)) with status `matched` per venue (or every mismatch explained by a logged manual action)
- Report under `reports/verify/P1-T064/`

## ToDo

- [ ] Write the checklist script
- [ ] Collect 24 h of recon results and screenshots
- [ ] Store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Checklist script exits non-zero on any missing panel data

### Scenarios

- Given a manual test trade on the OANDA practice account, when recon runs, then the mismatch is detected, explained in the report, and the next baseline is clean

### Stress / failure injection

- n/a: evidence collection

## Acceptance criteria

- [ ] All panels populated; recon clean for 24 h; report stored
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- IBKR not used: listed as "not used" with `ibkr.enabled: false` (P1-T070)

## Cardinal rules (do NOT)

- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.28, T1.29 once every task traced to it in PHASE.md is done; note P1-T064 next to it.
- `docs/03-build-spec.md` §M16: link the evidence report

## Branch & PR

- Branch: `p1/P1-T064-verify-cost-panels-and-recon-clean`
- PR title: `P1-T064: Verify cost panels populate and reconciliation runs clean`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T064` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (recon cadence per 16 §2.9; depends on live checks P1-T073/P1-T074 instead of the USER key task)
