---
id: P1-T060
kind: task
title: Verify the alert path on Telegram, ntfy and email (if on)
phase: 1
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T003, P1-T045, P1-T054, P1-T068, P0-T002]
requirements: [R1.14]
roadmap_todos: [T1.64]
modules: [M17]
dashboards: [D16]
tools: [git, uv, docker, sops]
mcp: []
env: [TELEGRAM_BOT_TOKEN, TELEGRAM_ALERT_CHAT_ID, NTFY_NOTIFIER_TOKEN]
services: [telegram, ntfy, nats, grafana, alertmanager]
branch: p1/P1-T060-verify-alert-path-three-channels
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
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

# P1-T060 · Verify the alert path on Telegram, ntfy and email (if on)

## Goal / expected outcome

Test alerts from both entry points (NATS `alert.*` and Grafana alerts via the webhook) reach Telegram, ntfy and (if on) email on your devices, channel failures fail over correctly, and delivery latency is recorded.

## Context & references

- Roadmap: requirements [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.64](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.64 · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) · exit criterion 3 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Depends on (this phase): P1-T003, P1-T045, P1-T054, P1-T068
- This is the live, keyed half of the alert path: it needs your Telegram bot (P0-T002), the ntfy app (P1-T003) and the SMTP app password or email off (P1-T068); network paths per [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) (P1-B020)
- Run with `sops exec-env ~/.config/mastertrader/secrets.sops.yaml 'make verify-alerts'`; if email is on, the `SMTP_*`/`ALERT_EMAIL_*` names from P1-T068 must also be present
- Cross-phase prerequisites (depends_on): P0-T002 (Telegram bot, your T0.06)

## Requirements

- Send `alert.critical.test` and trigger a Grafana test rule; confirm receipt on every enabled channel (you confirm on the phone and inbox)
- Kill each enabled channel in turn (block Telegram API egress, stop ntfy, break SMTP if on) and confirm the others deliver plus `channel_down`
- Record end-to-end latency per channel (publish → provider accepted; and your observed receipt time)
- Report under `reports/verify/P1-T060/`

## ToDo

- [ ] Run the tests with you watching the phone and inbox
- [ ] Write the report with latencies and failover results
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Scripted part: `mt-alerts test --all` and channel-kill toggles in `tests/e2e/alerts_failover.py`

### Scenarios

- Given ntfy is down, when a critical alert fires, then Telegram and email deliver and a `channel_down` warning names ntfy

### Stress / failure injection

- Fault: each channel removed in turn (3 runs); storm test reuse from P1-T045

## Acceptance criteria

- [ ] Telegram, ntfy and (if on) email received both test alerts; failover works for each enabled channel; latencies recorded
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Phone off-tailnet: record ntfy behaviour (Android: cached and delivered on reconnect; iOS: relay wake-up with message ID only, content fetched over Tailscale)

## Cardinal rules (do NOT)

- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.64 once every task traced to it in PHASE.md is done; note P1-T060 next to it.
- `docs/07-security-notes.md` §9: record measured latencies and failover behaviour

## Branch & PR

- Branch: `p1/P1-T060-verify-alert-path-three-channels`
- PR title: `P1-T060: Verify the alert path on Telegram, ntfy and email (if on)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (email optional (P1-B005); one fan-out; live keyed check with env names; deps P1-T068, P0-T002)
