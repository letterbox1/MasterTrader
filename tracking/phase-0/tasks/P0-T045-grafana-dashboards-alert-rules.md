---
id: P0-T045
kind: task
title: Provision Grafana dashboards and baseline alert rules
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T023, P0-T018]
requirements: [R0.10]
roadmap_todos: [T0.46]
modules: [M17]
dashboards: [D16]
tools: [docker, promtool, amtool]
mcp: []
env: []
services: [grafana, prometheus, loki, alertmanager]
branch: p0/P0-T045-grafana-dashboards-alert-rules
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T045 · Provision Grafana dashboards and baseline alert rules

## Goal / expected outcome

Grafana shows, from provisioning files in git, dashboards for host, Postgres, NATS, containers, backups/WORM and LLM spend, plus a Loki logs explorer with `trace_id` links; Alertmanager routes baseline alerts to your Telegram (email/ntfy join in P1).

## Context & references

- [Roadmap P0 R0.10](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.46](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response) (alert list)
- [Roadmap P0 §6 exit criteria](../../../docs/roadmap/phase-0-foundations.md#6-exit-criteria-demo) (1: Grafana shows host/DB/NATS health and logs in Loki)
- Depends on: P0-T023, P0-T018. Build first, keys last: the Telegram receiver is tested against a mocked Bot API; the real alert receipt is checked in the soak (P0-T063, after P0-T002).

## Requirements

- Dashboards (JSON in `infra/grafana/dashboards/`, uid-stable): `mt-host` (CPU, RAM, disk per volume, NVMe/HDD, temps, chrony offset, GPU if any), `mt-postgres` (connections, TPS, locks, replication/WAL, bloat), `mt-nats` (JetStream streams/KV, slow consumers), `mt-containers` (cAdvisor: CPU/mem/restarts per service), `mt-backups-worm` (backup age, WAL lag, restore test, seal/verify status), `mt-llm` (spend per role, fallbacks).
- Logs: Loki data source with derived field `trace_id` → link to Explore; dashboard variables `service`, `level`.
- Alert rules (Prometheus rules files): service down > 2 min; disk > 80 %; backup last success > 26 h; WAL lag > 15 min; restore test > 35 days; `mt_audit_verify_status == 0` or KV `audit.integrity` ≠ `ok` (critical); WORM write buffer > 80 % of its bound ([16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)) (critical); seal anchor failed; key age > its `rotate_days` (default 90 days, 16 §2.3; `key_age.prom`); chrony offset > 100 ms; host SSH login (Loki rule on journald `sshd` Accepted); auth lockout.
- Alertmanager: route `severity=critical` and `warning` to Telegram (`telegram_configs` with bot token + chat id from tmpfs); inhibition rules. This direct route is the P0 interim: P1 (R1.14) moves delivery to the single fan-out (Alertmanager → webhook → `alert.*` consumer → Telegram/ntfy/email, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B007).
- Spend panel per 03 §7 against the monthly cap setting (default US$40, [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)).

## ToDo

- [ ] Write datasource + dashboard provisioning and the six dashboards.
- [ ] Write Prometheus/Loki alert rules and Alertmanager config.
- [ ] Send a test alert end to end to the mocked Bot API (CI); the real receipt is logged in P0-T063.
- [ ] Snapshot screenshots of each dashboard for the PR.

## Verification

### Tests
- Lint: `promtool check rules`, `amtool check-config`, dashboard JSON schema check in CI.
- Integration: fire a synthetic alert (`amtool alert add`) → Telegram API mock receives it (CI); the real receipt is logged in P0-T063.

### Scenarios
- Given Postgres stops, then `service down` fires within ~2 min and resolves after restart.
- Given someone logs in via SSH, then a warning alert arrives (07 §9 'login to the host').

### Stress / failure injection
- Alert storm: 50 synthetic alerts → grouping keeps Telegram messages ≤ 5 per minute (well under Bot API 30 msg/s).

## Acceptance criteria

- [ ] Six dashboards provisioned from git
- [ ] Logs searchable in Loki with trace_id links
- [ ] Alert rules + Telegram route working (test alert received by the mocked Bot API)
- [ ] Rule/config lint in CI
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Telegram unreachable: Alertmanager retries; the second channel (ntfy) arrives in P1 — until then alerts also show in D16.

## Cardinal rules (do NOT)

- Do NOT hand-edit dashboards in the UI without exporting to git.
- Do NOT include secrets in dashboard JSON or alert annotations.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §9: list which alerts are live as of P0 and their channel.
- `docs/roadmap/phase-0-foundations.md`: tick T0.46 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T045-grafana-dashboards-alert-rules`
- PR title: `P0-T045: Provision Grafana dashboards and baseline alert rules`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless: mocked Bot API, real receipt in P0-T063; integrity/buffer alerts; thresholds from 16 defaults; interim direct route until the P1 fan-out (17 §D P1-B007); run fields added)
