---
id: P7-T007
kind: task
title: Create live trade-only, IP-locked, no-withdrawal keys per sub-account
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T006]
requirements: [R7.04]
roadmap_todos: [T7.03]
modules: [M12]
dashboards: [D16, D05]
branch: p7/P7-T007-live-trade-only-keys
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T007 · Create live trade-only, IP-locked, no-withdrawal keys per sub-account

## Goal / expected outcome

Each live sub-account has its own API key with trade-only scope, withdrawals disabled, and an IP allow-list containing only the static egress IP(s) of the host (and the MT5 VPS if used); the keys are stored only in the sops secrets file.

## Context & references

- Roadmap: [R7.04 · ToDo T7.03](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops/age, 90-day rotation, key creation date recorded) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (key model per venue)
- Related: P7-T006, P7-T031 (engine reads keys per sub-account), P7-T032/T047 (key audit), gap P7-B004 (4G failover changes egress IP)

## Requirements

- Scopes: read + trade only. **No** withdrawal, transfer, sub-account management or margin-loan scopes.
- IP allow-list: the host's static egress IP; if 4G failover is used, the failover path must egress from the same static IP (see P7-B004) — never widen to 0.0.0.0/0.
- Secrets file entries: `live.<venue>.<subaccount>.{api_key,api_secret,passphrase,created_at}`; `created_at` drives the 90-day rotation alert.
- One key per sub-account; per-container least privilege (only `engine` and `monitor` read-only key get them).

## ToDo

- [ ] For each sub-account: create an API key with trade + read scopes only; untick every withdrawal/transfer scope.
- [ ] Set the IP allow-list to the host's static egress IP (and the VPS IP for FP Markets if relevant).
- [ ] Edit the sops file on the host (`sops secrets/live.enc.yaml`) and add the key fields plus `created_at`; never paste them anywhere else.
- [ ] Create a separate **read-only** key per venue for reconciliation (`live.<venue>.recon.*`).
- [ ] Run the key audit (P7-T032) from D16 → Keys → 'Audit live keys' and fix anything it flags.
- [ ] Note the key creation date on the D16 keys metadata view.

## Verification

### Tests
- n/a (user action); P7-T032/P7-T047 test scopes and IP locks against the venue APIs where exposed.

### Scenarios
- Given a key with withdrawal scope, when the key audit runs, then it fails with 'withdrawal scope present' and the engine refuses to start that sub-account.
- Given the request comes from a non-allow-listed IP, when the venue rejects it, then the audit records 'IP lock confirmed'.

### Stress / failure injection
- n/a: key creation.

## Acceptance criteria

- [ ] Key audit passes for every live sub-account (trade-only, IP-locked, withdrawals disabled).
- [ ] Keys exist only in the sops file; `gitleaks` clean.
- [ ] Each key has a `created_at` within the last 90 days.

## Exceptions & edge cases

- Venue cannot IP-lock: mark the venue `read_only` for live until it can (07 §3).
- Key leaked: follow the 'keys leaked' runbook (revoke at venue, rotate, check withdrawals).

## Cardinal rules (do NOT)

- Do NOT paste keys into chat, Telegram, issues or `.env` files in git.
- Do NOT enable withdrawal or transfer scopes on any key.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/07-security-notes.md` §2–3: document the `live.*` secrets layout (names only).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.03 when this item is done.

## Branch & PR

- Branch: `p7/P7-T007-live-trade-only-keys`
- PR title: `P7-T007: Create live trade-only, IP-locked, no-withdrawal keys per sub-account`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T007` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
