---
id: P0-T062
kind: task
title: Create your login and enrol TOTP when you first open the app
phase: 0
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T050]
requirements: [R0.08]
roadmap_todos: [T0.12]
modules: [mt-api, supabase-auth]
dashboards: []
tools: []
mcp: []
env: []
services: [mt-web, supabase-auth]
branch: p0/P0-T062-set-password-enrol-totp
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T062 · Create your login and enrol TOTP when you first open the app

## Goal / expected outcome

You own the only login on the workstation stack: a strong password and a TOTP factor in Supabase Auth ([18 §4.6](../../../docs/18-platform-and-deployment.md#46-auth)), ideally with a second TOTP device enrolled as a backup. About two minutes, done whenever you first open the app. Automated tests use a seeded test account, so no agent task waits on this; it's needed for the exit demo (P0-T064), for C3 actions and before live money.

## Context & references

- [Roadmap P0 T0.12](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §4.6 auth](../../../docs/18-platform-and-deployment.md#46-auth) · [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api)
- [ui §3.6 sessions](../../../docs/ui/README.md#36-permissions--sessions)
- Implementation: P0-T033 (`mtctl auth create-owner`), P0-T050 (screens)
- Depends on: P0-T050 (brings in P0-T033 and P0-T070)
- Unblocks: exit criterion 2 demo (P0-T064)

## Requirements

- On the workstation, the agent (or you) runs `mtctl auth create-owner --email <you>`; it prints a one-time set-password link valid 30 min to the local console only.
- Password ≥ 14 chars from your password manager generator; TOTP in an authenticator app (or YubiKey OATH) on a device you keep; optionally a second TOTP factor on another device as the backup (Supabase Auth has no recovery codes of its own).
- Done on the workstation at `https://localhost/` (or over Tailscale if you set it up, P0-T003).

## ToDo

- [ ] Open the set-password link from `mtctl auth create-owner`; set the password.
- [ ] Scan the QR; enter the current code to confirm (`aal2`).
- [ ] Optionally enrol a second TOTP device as a backup.
- [ ] Log out and log in again with password + TOTP.
- [ ] Log 'done' (no values) here.

## Verification

### Tests
- Confirmation: D16 Security shows TOTP enrolled and your session at `aal2`; `audit.auth_event` has the enrolment and `login_success` rows.

### Scenarios
- Given you lose your phone, then the backup TOTP device logs you in; with none, `mtctl auth reset-mfa` on the workstation (audited) lets you re-enrol.

### Stress / failure injection
- n/a: one-time user action.

## Acceptance criteria

- [ ] Password set and TOTP enrolled on the workstation stack
- [ ] Backup factor enrolled, or 'no backup device' logged
- [ ] Second login with TOTP succeeded

## Exceptions & edge cases

- Set-password link expired: re-run `mtctl auth create-owner` (it re-issues the link for the same user).
- At the shift to Supabase cloud (P7-T073), the account moves with the data or is re-created the same way.

## Cardinal rules (do NOT)

- Do NOT screenshot the QR or store the TOTP secret anywhere except the authenticator.
- Do NOT share the set-password link or codes in chat.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- None.
- `docs/roadmap/phase-0-foundations.md`: tick T0.12 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T062-set-password-enrol-totp`
- PR title: `P0-T062: Create your login and enrol TOTP`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (deps trimmed and production host added; run fields added)
- 2026-11-19: Workstation-first (17 §G): login is Supabase Auth (password + TOTP). Done whenever you first open the app on the workstation (about 2 minutes); automated tests use a test account, so no agent task waits on this. Required before C3 actions and before live money.
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (body rewritten for Supabase Auth: owner link from `mtctl auth create-owner`, TOTP + optional backup factor, on the workstation; no setup token, recovery codes or Tailscale precondition)
