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
depends_on: [P7-T006, P7-T065]
requirements: [R7.04, R7.14]
roadmap_todos: [T7.03, T7.11]
modules: [M12]
dashboards: [D16, D05]
tools: []
mcp: []
env: []
services: [venue API key pages, egress exit-node VM (P7-T065)]
branch: p7/P7-T007-live-trade-only-keys
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T007 · Create live trade-only, IP-locked, no-withdrawal keys per sub-account

## Goal / expected outcome

Each live sub-account has its own API key with trade-only scope, withdrawals disabled, and an IP allow-list containing only the static IP of the Sydney exit node (P7-T065; for FP Markets the MT5 VPS's own IP if used); the keys are stored only in the sops secrets file.

## Context & references

- Roadmap: [R7.04 · ToDo T7.03](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops/age, 90-day rotation, key creation date recorded) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (key model per venue)
- Related: P7-T006, P7-T065 (exit-node VM and its static IP), P7-T066 (tunnel), P7-T031 (engine config per sub-account), P7-T032/T047 (key audit, T7.65) · design [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys), decision [17 §A P7-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · rotation every 90 days [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · `deadman` sidecar's own keys [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)

## Requirements

- Scopes: read + trade only. **No** withdrawal, transfer, sub-account management or margin-loan scopes.
- IP allow-list: **only** the exit node's static IP (16 §3.2); broadband and 4G both tunnel to it, so failover never needs another IP. Never widen to 0.0.0.0/0 or add the home/4G IP.
- Secrets file entries: `live.<venue>.<subaccount>.{api_key,api_secret,passphrase,created_at}`; `created_at` drives the 90-day rotation alert.
- Per sub-account: one engine trade key, the `deadman` sidecar's own trade-only key (16 §3.1, `live.<venue>.<subaccount>.deadman.*`) and one read-only recon key; per-container least privilege (`engine` and `deadman` get their trade-only keys, `monitor` only the read-only key).

## ToDo

- [ ] For each sub-account: create an API key with trade + read scopes only; untick every withdrawal/transfer scope.
- [ ] Set the IP allow-list to the exit node's static IP from P7-T065 only (and the VPS IP for FP Markets if relevant); this is T7.11's 'allow-list its IP on every live key' step.
- [ ] Edit the sops file on the host (`sops secrets/live.enc.yaml`) and add the key fields plus `created_at`; never paste them anywhere else.
- [ ] Create the `deadman` sidecar's own trade-only key per sub-account and a separate **read-only** key per venue for reconciliation (`live.<venue>.recon.*`), all allow-listed to the same exit-node IP.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (allow-list only the exit-node static IP per 16 §3.2/17 §A P7-B004; deadman sidecar keys per 16 §3.1; dep P7-T065; T7.11)
