---
id: P1-T060
kind: task
title: Verify the alert path on Telegram, ntfy and email (if on) from the workstation
phase: 1
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T045, P1-T054, P1-T068, P0-T002]
requirements: [R1.14]
roadmap_todos: [T1.64]
modules: [M17]
dashboards: [D16]
tools: [git, cargo, docker, sops]
mcp: []
env: [TELEGRAM_BOT_TOKEN, TELEGRAM_ALERTS_CHAT_ID, MT_NTFY_PUBLISHER_TOKEN]
services: [telegram, ntfy, nats, grafana, alertmanager]
branch: p1/P1-T060-verify-alert-path-three-channels
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T060 · Verify the alert path on Telegram, ntfy and email (if on) from the workstation

## Goal / expected outcome

Test alerts from both entry points (NATS `alert.*` and Grafana alerts via the webhook) reach Telegram (your chat), ntfy (a subscriber on the workstation: the ntfy web app on localhost or `ntfy subscribe`) and (if on) email, channel failures fail over correctly, and delivery latency is recorded.

## Context & references

- Roadmap: requirements [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.64](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.64 · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) · exit criterion 3 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Depends on (this phase): P1-T045, P1-T054, P1-T068
- This is the live, keyed half of the alert path: it needs your Telegram bot (P0-T002) and the SMTP app password or email off (P1-T068); network paths per [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) (P1-B020)
- Workstation first ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)): ntfy is checked with a subscriber on the workstation; the phone subscription over Tailscale is the pre-go-live USER step P1-T003, which this task no longer waits for
- Run with `sops exec-env ~/.config/mastertrader/secrets.sops.env 'just verify-alerts'`; if email is on, the `SMTP_*`/`ALERT_EMAIL_*` names from P1-T068 must also be present
- Cross-phase prerequisites (depends_on): P0-T002 (Telegram bot, your T0.06)

## Requirements

- Send `alert.critical.test` and trigger a Grafana test rule; confirm receipt on every enabled channel (Telegram chat, the workstation ntfy subscriber, and the inbox if email is on)
- Kill each enabled channel in turn (block Telegram API egress, stop ntfy, break SMTP if on) and confirm the others deliver plus `channel_down`
- Record end-to-end latency per channel (publish → provider accepted; and your observed receipt time)
- Report under `reports/verify/P1-T060/`

## ToDo

- [ ] Run the tests (`cargo test -p mt-e2e --test alerts_failover -- --ignored`) with a workstation ntfy subscriber; you confirm the Telegram message and, if on, the email
- [ ] Write the report with latencies and failover results
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Scripted part: `mt-alerts test --all` and channel-kill toggles in the `alerts_failover` test of the Rust e2e crate (`tests/e2e`, package `mt-e2e`)

### Scenarios

- Given ntfy is down, when a critical alert fires, then Telegram and email deliver and a `channel_down` warning names ntfy

### Stress / failure injection

- Fault: each channel removed in turn (3 runs); storm test reuse from P1-T045

## Acceptance criteria

- [ ] Telegram, ntfy and (if on) email received both test alerts; failover works for each enabled channel; latencies recorded
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Phone delivery (Android cache-and-deliver, iOS relay wake-up with message ID only) is recorded in P1-T003 before go-live, not here

## Cardinal rules (do NOT)

- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.64 once every task traced to it in PHASE.md is done; note P1-T060 next to it.
- `docs/07-security-notes.md` §9: record measured latencies and failover behaviour

## Branch & PR

- Branch: `p1/P1-T060-verify-alert-path-three-channels`
- PR title: `P1-T060: Verify the alert path on Telegram, ntfy and email (if on) from the workstation`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (email optional (P1-B005); one fan-out; live keyed check with env names; deps P1-T068, P0-T002)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (verifies Telegram + ntfy (workstation subscriber) + email if on; removed the dependency on P1-T003 (phone ntfy over Tailscale is now a pre-go-live USER step); kept P0-T002 and P1-T068 (credentials); tools cargo+uv)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Python e2e harness → Rust integration tests in the `mt-e2e` crate (`tests/e2e`) with the same cases; tools drop uv)
