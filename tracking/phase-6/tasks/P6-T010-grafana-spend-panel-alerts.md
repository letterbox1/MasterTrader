---
id: P6-T010
kind: task
title: Grafana LLM spend panel and budget alerts
phase: 6
type: OPS
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T009, P0-T045, P1-T045]
requirements: [R6.07]
roadmap_todos: [T6.41]
modules: [M17, M21]
dashboards: [D10]
tools: [git, docker]
mcp: []
env: []
services: [grafana, prometheus, alertmanager, ntfy]
branch: p6/P6-T010-grafana-spend-panel-alerts
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T010 · Grafana LLM spend panel and budget alerts

## Goal / expected outcome

A provisioned Grafana dashboard shows LLM spend by role vs budget, month-to-date vs cap, fallbacks and latency, with alerts at 80% and 100% to Telegram + ntfy.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.41
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) (spend panel in Grafana) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (spend goes to Grafana) · [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs)
- Cross-phase: P0-T045 (Grafana provisioning), P1-T045 (alert fan-out to Telegram/ntfy/email)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (budgets the panel compares against; read from settings, never hard-coded)
- Depends on (this phase): P6-T009

## Requirements

- Dashboard JSON provisioned from git (`ops/grafana/dashboards/llm-spend.json`).
- Panels: spend by role (today), MTD vs cap, fallback rate, error rate, p95 latency per model, audit drift (gateway requests − audit rows).
- Alerts: role ≥ 80% / 100% of daily budget; MTD ≥ 80% / 100% of monthly cap; audit drift > 0 for 15 min.

## ToDo

- [ ] Create dashboard + alert rules as code.
- [ ] Wire contact points (Telegram, ntfy).
- [ ] Test with synthetic metrics.
- [ ] Docs.

## Verification

### Tests
- Provisioning test: dashboard loads with no missing datasource.
- Alert rule unit test via Grafana's rule test / synthetic series.

### Scenarios
- Given `explain` spend hits 80%, then one Telegram + ntfy alert fires and resolves next day.

### Stress / failure injection
- n/a: dashboards only; load covered by P6-T053.

## Acceptance criteria

- [ ] Dashboard provisioned from git.
- [ ] Synthetic 80%/100% alerts delivered to both channels.

## Exceptions & edge cases

- Prometheus down: alert on absent metrics (`absent()`) rather than silence.

## Cardinal rules (do NOT)

- Do NOT put API keys or prompt text in metric labels.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` §7: link the dashboard.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.41 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T010-grafana-spend-panel-alerts`
- PR title: `P6-T010: Grafana LLM spend panel and budget alerts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase deps P0-T045/P1-T045; budgets from 16 §2.10 settings; run fields)
