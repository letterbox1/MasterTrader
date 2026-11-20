---
id: P1-T003
kind: task
title: Before go-live: install ntfy on your phone and subscribe over Tailscale
phase: 1
type: USER
status: backlog
priority: low
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
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T003 · Before go-live: install ntfy on your phone and subscribe over Tailscale

## Goal / expected outcome

Your phone receives pushes from the self-hosted ntfy server on a private topic over Tailscale. This is a **pre-go-live** step: Tailscale is optional until go-live ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)), so no agent task waits on it. The alert path itself is proven on the workstation in P1-T060 (Telegram + ntfy + email if on); this task adds the phone as an ntfy subscriber before live money, and its result feeds the P7 preflight / go-live pack (P7-T070).

## Context & references

- Roadmap: requirements [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.03](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Alerts: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (Telegram + email + ntfy as the second independent channel)
- ntfy server is deployed by P1-T044 (auth on; localhost on the workstation, plus a Tailscale listener once your tailnet exists); iOS push goes via ntfy's upstream relay, which carries only a message ID ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B006)
- Email: the destination address, the SMTP app password (or turning email off) are all in P1-T068
- Schedule: any time before go-live; nothing in Phases 1–6 depends on it. Workstation-first: ntfy is reachable on localhost until Tailscale exists ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode), [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path))
- Depends on (this phase): P1-T044
- Cross-phase prerequisites (depends_on): P0-T003 (your tailnet, T0.03; optional until go-live)

## Requirements

- Install the ntfy app (Android or iOS) and the Tailscale app on the phone; the phone must be on your tailnet to reach the server
- Subscribe to the private topic (the agent tells you the topic name; you read the `phone` read token yourself with `sops -d ~/.config/mastertrader/secrets.sops.env`, key `MT_NTFY_PHONE_TOKEN`)

## ToDo

- [ ] Install Tailscale and ntfy on the phone; log in to Tailscale
- [ ] Add the server URL `https://ntfy.<tailnet-name>.ts.net` (the Tailscale route P1-T044 enables once your tailnet exists) and subscribe to the topic with the access token
- [ ] Send yourself a test with the agent's `mt-alerts test --channel ntfy` and confirm it arrives
- [ ] Tell the agent "phone ntfy confirmed" (it records the result for the P7 preflight)

## Verification

### Tests

- Agent check: `mt-alerts test --channel ntfy` reports delivered and you confirm receipt on the phone

### Scenarios

- Given the phone is off the tailnet, when a test alert is sent, then ntfy caches it and delivers when the phone reconnects (Android); on iOS the upstream relay wakes the app with a message ID only and the app fetches the content over Tailscale; record the behaviour in the progress log

### Stress / failure injection

- n/a: device setup

## Acceptance criteria

- [ ] A test push arrived on your phone over Tailscale
- [ ] Battery optimisation is disabled for ntfy (Android) so pushes are not delayed

## Exceptions & edge cases

- If the phone changes, repeat the subscription; the token can be rotated in sops without changing the topic

## Cardinal rules (do NOT)

- Do NOT use the public ntfy.sh server for alerts carrying instrument or account details
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.03 once every task traced to it in PHASE.md is done; note P1-T003 next to it.
- `docs/07-security-notes.md` §9: note the ntfy topic setup (no secrets) and the phone requirements (before go-live)

## Branch & PR

- Branch: `p1/P1-T003-ntfy-app-and-email`
- PR title: `P1-T003: Before go-live: install ntfy on your phone and subscribe over Tailscale`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (ntfy iOS via upstream relay (P1-B006); email address confirm or off, SMTP password moved to P1-T068 (P1-B005); sops path; dep P0-T003)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (workstation-first: Tailscale optional until go-live, so this is a pre-go-live USER step that no agent task waits on; P1-T060 now verifies ntfy on the workstation and no longer depends on it; email address moved to P1-T068; result feeds the P7 preflight / go-live pack)
