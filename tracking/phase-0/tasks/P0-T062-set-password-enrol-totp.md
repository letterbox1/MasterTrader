---
id: P0-T062
kind: task
title: Set your login password and enrol TOTP on first boot
phase: 0
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T050, P0-T019]
requirements: [R0.08]
roadmap_todos: [T0.12]
modules: [mt_api]
dashboards: []
tools: []
mcp: []
env: []
services: [mt-api, tailscale]
branch: p0/P0-T062-set-password-enrol-totp
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T062 · Set your login password and enrol TOTP on first boot

## Goal / expected outcome

You own the only login: a strong password and a TOTP enrolment on your authenticator, with recovery codes stored safely — done on the real host over Tailscale.

## Context & references

- [Roadmap P0 T0.12](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api)
- [ui §3.6 sessions](../../../docs/ui/README.md#36-permissions--sessions)
- Implementation: P0-T033, P0-T050
- Depends on: P0-T050 (brings in P0-T033), P0-T019 (the production host)
- Unblocks: exit criterion 2 demo (P0-T064)

## Requirements

- Do it on the production host stack (not a test instance), over Tailscale, from your laptop.
- Password ≥ 14 chars from your password manager generator; TOTP in an authenticator app (or YubiKey OATH) on a device you keep; 10 recovery codes stored in the password manager.
- Setup token: read it on the host with `docker compose logs mt-api | grep SETUP_TOKEN` within 30 min of first start (re-start mt-api to get a new one if it expired).

## ToDo

- [ ] Open `https://<host>.<tailnet>.ts.net/` → redirected to Setup.
- [ ] Paste the setup token; set the password.
- [ ] Scan the QR; enter the current code to confirm.
- [ ] Save the recovery codes in your password manager; confirm 'saved'.
- [ ] Log out and log in again with password + TOTP.
- [ ] Log 'done' (no values) here.

## Verification

### Tests
- Confirmation: D16 Security shows `TOTP: enrolled` and your session; `audit.auth_event` has `setup_completed` and `login_success`.

### Scenarios
- Given you lose your phone, then a recovery code logs you in and forces re-enrolment.

### Stress / failure injection
- n/a: one-time user action.

## Acceptance criteria

- [ ] Password set and TOTP enrolled on the production stack
- [ ] Recovery codes stored in the password manager
- [ ] Second login with TOTP succeeded

## Exceptions & edge cases

- Setup token expired: restart mt-api and use the new token.

## Cardinal rules (do NOT)

- Do NOT screenshot the QR or store the TOTP secret anywhere except the authenticator.
- Do NOT share the setup token or codes in chat.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- None.
- `docs/roadmap/phase-0-foundations.md`: tick T0.12 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T062-set-password-enrol-totp`
- PR title: `P0-T062: Set your login password and enrol TOTP on first boot`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (deps trimmed and production host added; run fields added)
