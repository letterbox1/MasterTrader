---
id: P1-T054
kind: task
title: Provision Grafana boards and alert rules for data, costs and quotas
phase: 1
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T006, P1-T030, P1-T040, P1-T045, P0-T045]
requirements: [R1.10, R1.11, R1.08, R1.14]
roadmap_todos: [T1.42]
modules: [M17, M16]
dashboards: [D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [grafana, prometheus, alertmanager]
branch: p1/P1-T054-grafana-boards-and-alert-rules
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

# P1-T054 · Provision Grafana boards and alert rules for data, costs and quotas

## Goal / expected outcome

Provisioned Grafana dashboards show live prices by timeframe, spreads/funding/swaps, DQ incidents and SLOs, quota usage and storage, and Grafana Alerting rules route through the notifier to all channels.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.42](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M15](../../../docs/03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api) (Grafana: markets, costs, DQ) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (metrics → Prometheus, Grafana alerts) · exit criterion 1 "Grafana and D02 show live prices at every timeframe" ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Depends on (this phase): P1-T006, P1-T030, P1-T040, P1-T045
- Cross-phase prerequisites (depends_on): P0-T045 (Grafana provisioning and baseline alert rules)

## Requirements

- Dashboards as code in `infra/grafana/dashboards/`: Markets (price by timeframe 1s … 1W from Timescale bars via the Postgres datasource), Costs (spread heatmap, funding, financing), DQ (status counts, incidents, data age and the stale reaction SLO, divergence, skew), Quotas, Storage, UI lag
- Alert rules (thresholds are configurable defaults): stale reaction SLO breach (> 250 ms p99), quota ≥ 80%, disk thresholds, recon unexplained mismatch, channel down, chrony offset, batch failure, egress mismatch; contact point = Alertmanager webhook → the `alert.*` consumer (P1-T045), the only route
- Dashboards load in < 3 s for 24 h ranges

## ToDo

- [ ] Build dashboards (JSON, provisioned) and alert rules (provisioned)
- [ ] Screenshot test of provisioning in CI (Grafana container renders without errors)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Integration: Grafana container loads all dashboards with no datasource errors; alert rule evaluation on test data fires to a fake webhook

### Scenarios

- Given a quota at 85%, when the rule evaluates, then one alert reaches Telegram and ntfy through the notifier (dedupe applies)

### Stress / failure injection

- n/a: dashboards; query cost checked by the 3 s load target

## Acceptance criteria

- [ ] All boards provisioned from code; alert rules reach the notifier
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Datasource down: panels show errors, not empty "no data" that looks healthy

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.42 once every task traced to it in PHASE.md is done; note P1-T054 next to it.
- `docs/03-build-spec.md` §M15: list Grafana boards provisioned

## Branch & PR

- Branch: `p1/P1-T054-grafana-boards-and-alert-rules`
- PR title: `P1-T054: Provision Grafana boards and alert rules for data, costs and quotas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (1W boards, data-age SLO rule, single webhook route (P1-B007); P0 provisioning dep)
