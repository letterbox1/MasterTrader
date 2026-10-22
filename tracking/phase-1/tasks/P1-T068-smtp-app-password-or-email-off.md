---
id: P1-T068
kind: task
title: Create an SMTP app password for email alerts, or turn email off
phase: 1
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R1.14]
roadmap_todos: [T1.05]
modules: [M17]
dashboards: [D16]
tools: [sops]
mcp: []
env: []
services: [smtp-provider]
branch: p1/P1-T068-smtp-app-password-or-email-off
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T068 · Create an SMTP app password for email alerts, or turn email off

## Goal / expected outcome

Either the email alert channel has working SMTP credentials from **your own mail provider** (an app password, never your main password) in the secrets file, or email alerts are switched off and Telegram + ntfy carry every alert. Either way the alert path test (P1-T060) knows which channels to prove.

## Context & references

- Roadmap: requirement [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B005 (your mail provider's SMTP with an app password, or email off)
- Security: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (email via your provider's SMTP over TLS; app password in the secrets file) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops file lives outside the repo, e.g. `~/.config/mastertrader/`)
- Consumer: the `alert.*` fan-out (P1-T045) and the alert path test (P1-T060)
- Related: P1-T003 (ntfy app + confirm the destination address)

## Requirements

- Decide: **email on** or **email off**. Off is a valid choice; Telegram + ntfy remain ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions)).
- If on:
  - At your mail provider, turn on 2-step verification if it is required, then create an **app password** named `MasterTrader alerts` (Gmail: Google Account → Security → App passwords; Fastmail: Settings → Privacy & Security → App passwords; iCloud: appleid.apple.com → App-Specific Passwords; others: the provider's "app password" page).
  - Note the provider's SMTP host and port (TLS: 465 implicit or 587 STARTTLS) and the sender address.
  - Add to the sops file (run `sops ~/.config/mastertrader/secrets.sops.yaml`), keys `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_APP_PASSWORD`, `ALERT_EMAIL_FROM`, `ALERT_EMAIL_TO`. Values go **only** into that file, never into chat, issues, git or the item file.
- If off: set `alerts.email.enabled: false` in `config/alerts.yaml` (or tell the agent "email off"); this is a routing change you make yourself, and turning a channel off later is a loosening of alert routing (C3 via the break-glass CLI until Telegram C3 lands in P2).
- Rotation: the secrets file records the creation date; revoke the app password at the provider if you suspect a leak.

## ToDo

- [ ] Decide email on or off and tell the agent (no values)
- [ ] If on: create the app password at your mail provider and note SMTP host/port and sender
- [ ] If on: add the six `SMTP_*` / `ALERT_EMAIL_*` entries to the sops file
- [ ] If on: run `uv run mt-alerts test --channel email` (after P1-T045) and confirm the message arrived (check spam once and allow the sender)
- [ ] Record "email on, delivered" or "email off" in the progress log

## Verification

### Tests

- Agent check (email on): `mt-alerts test --channel email` reports `delivered` and you confirm receipt; the notifier log shows TLS and no credential text
- Agent check (email off): `mt-alerts test --all` reports email as `disabled`, not `failed`

### Scenarios

- Given email is on, when a critical test alert fires, then it arrives by email as well as Telegram and ntfy
- Given the app password is revoked at the provider, when an alert fires, then the email channel fails, `alert.warning.channel_down` names email, and Telegram + ntfy still deliver
- Given email is off, when the alert path test runs, then it proves Telegram and ntfy only and records email as off

### Stress / failure injection

- n/a: account setup; channel failure is covered by P1-T045 and P1-T060

## Acceptance criteria

- [ ] Email is either on with a delivered test message, or explicitly off in `config/alerts.yaml`
- [ ] No SMTP credential appears anywhere except the sops file (gitleaks clean)

## Exceptions & edge cases

- Providers without app passwords (or with OAuth-only SMTP): choose email off, or use another mailbox you own that supports app passwords
- Provider rate limits on SMTP: the notifier batches to ≤ 1 msg/s per channel, so normal alert volume stays well inside them

## Cardinal rules (do NOT)

- Do NOT use your main mailbox password; app password only
- Do NOT paste the app password into chat, issues, logs, commits or this file; it goes only into the sops file outside the repo ([07 §2](../../../docs/07-security-notes.md#2-secrets))
- Do NOT use a paid transactional email service; your own provider's SMTP or email off ([03 §1](../../../docs/03-build-spec.md#1-ground-rules))

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.05; note P1-T068 next to it.
- `docs/07-security-notes.md` §9: note whether email is on (provider type only, no values).

## Branch & PR

- Branch: `p1/P1-T068-smtp-app-password-or-email-off` (only if `config/alerts.yaml` changes)
- PR title: `P1-T068: Create an SMTP app password for email alerts, or turn email off`
- PR checklist: no secrets in diff · task file ticked · `./kanban done P1-T068` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.05 (docs/16–17 alignment)
