---
id: P1-T003
kind: task
title: Install ntfy on your phone and confirm the alert email address
phase: 1
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P1-T044, P0-T003]
requirements: [R1.14]
roadmap_todos: [T1.03]
modules: [M17]
dashboards: []
tools: []
mcp: []
env: []
services: [ntfy, tailscale]
branch: p1/P1-T003-ntfy-app-and-email
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

# P1-T003 · Install ntfy on your phone and confirm the alert email address

## Goal / expected outcome

Your phone receives pushes from the self-hosted ntfy server on a private topic, and the email address for alerts is confirmed, so the alert path test (P1-T060) can prove all three channels.

## Context & references

- Roadmap: requirements [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.03](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Alerts: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (Telegram + email + ntfy as the second independent channel)
- ntfy server is deployed by P1-T044 (auth on, Tailscale only); iOS push goes via ntfy's upstream relay, which carries only a message ID ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B006)
- Email: you confirm the address here; the SMTP app password (or turning email off) is P1-T068
- Depends on (this phase): P1-T044
- Cross-phase prerequisites (depends_on): P0-T003 (your tailnet, T0.03)

## Requirements

- Install the ntfy app (Android or iOS) and the Tailscale app on the phone; the phone must be on your tailnet to reach the server
- Subscribe to the private topic (the agent tells you the topic name; you read the `phone` read token yourself with `sops -d ~/.config/mastertrader/secrets.sops.yaml`, key `NTFY_PHONE_TOKEN`)
- Confirm the destination email address for alerts (sops key `ALERT_EMAIL_TO`) and that it accepts mail from the sender set in P1-T068, or confirm email is off

## ToDo

- [ ] Install Tailscale and ntfy on the phone; log in to Tailscale
- [ ] Add the server URL `https://ntfy.<tailnet-name>.ts.net` (from P1-T044) and subscribe to the topic with the access token
- [ ] Send yourself a test with the agent's `uv run mt-alerts test --channel ntfy` and confirm it arrives
- [ ] Confirm the email address (sops key `ALERT_EMAIL_TO`) and allow the sender in your mail client, or confirm email is off (P1-T068)
- [ ] Tell the agent "ntfy confirmed; email on/off"

## Verification

### Tests

- Agent check: `mt-alerts test --channel ntfy` (and `--channel email` if on) report delivered and you confirm receipt

### Scenarios

- Given the phone is off the tailnet, when a test alert is sent, then ntfy caches it and delivers when the phone reconnects (Android); on iOS the upstream relay wakes the app with a message ID only and the app fetches the content over Tailscale; P1-T060 records the behaviour

### Stress / failure injection

- n/a: device setup

## Acceptance criteria

- [ ] A test push arrived on your phone, and a test email arrived (or email is recorded as off)
- [ ] Battery optimisation is disabled for ntfy (Android) so pushes are not delayed

## Exceptions & edge cases

- If the phone changes, repeat the subscription; the token can be rotated in sops without changing the topic

## Cardinal rules (do NOT)

- Do NOT use the public ntfy.sh server for alerts carrying instrument or account details
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.03 once every task traced to it in PHASE.md is done; note P1-T003 next to it.
- `docs/07-security-notes.md` §9: note the ntfy topic setup (no secrets) and the phone requirements

## Branch & PR

- Branch: `p1/P1-T003-ntfy-app-and-email`
- PR title: `P1-T003: Install ntfy on your phone and confirm the alert email address`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (ntfy iOS via upstream relay (P1-B006); email address confirm or off, SMTP password moved to P1-T068 (P1-B005); sops path; dep P0-T003)
