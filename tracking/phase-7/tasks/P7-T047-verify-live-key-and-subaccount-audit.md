---
id: P7-T047
kind: task
title: Verify live keys and sub-account isolation before funding
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T032, P7-T007, P7-T008, P7-T031]
requirements: [R7.04]
roadmap_todos: [T7.03, T7.40]
modules: [M12, M17]
dashboards: [D16, D05]
branch: p7/P7-T047-verify-live-key-and-subaccount-audit
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

# P7-T047 · Verify live keys and sub-account isolation before funding

## Goal / expected outcome

A recorded key audit shows every live key is trade-only, IP-locked and withdrawal-disabled, each mandate has its own sub-account and secrets, STP prevents self-matching across sub-accounts, and Travel Rule addresses are registered.

## Context & references

- Roadmap: [R7.04 · ToDo T7.03, T7.40](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (Travel Rule) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (STP, no self-matching) · Roadmap R7.04 'Verified by: key audit'
- Related: P7-T032, P7-T007, P7-T008, P7-T031

## Requirements

- Key audit result `pass` for every live key (P7-T032).
- A request from a non-allow-listed IP (e.g. a temporary cloud shell) with a **read-only** recon key is rejected by the venue (proves IP lock) — never with a trade key.
- Container inspection: only `engine` holds trade keys; only `monitor` holds recon keys.
- STP: two opposing small paper/testnet orders from two sub-accounts never self-match (STP cancel recorded as non-fill).
- Venue rows list whitelisted addresses and dates.

## ToDo

- [ ] Run the key audit; attach result.
- [ ] Run the IP-lock probe with a recon key; attach result.
- [ ] Inspect container env/mounts; attach redacted listing.
- [ ] Run the STP cross-sub-account test on testnet.
- [ ] Record everything in the progress log.

## Verification

### Tests
- Integration: STP cross-sub-account test; container secret-scope test (`docker inspect` assertions).

### Scenarios
- Given a key with withdrawal scope appears, then the audit fails and the engine refuses that sub-account.

### Stress / failure injection
- n/a: audit.

## Acceptance criteria

- [ ] All checks above pass and are recorded with redacted evidence.

## Exceptions & edge cases

- Venue without permission introspection: manual attestation present and < 90 days.

## Cardinal rules (do NOT)

- Do NOT run the IP-lock probe with a trade key.
- Do NOT include key material in evidence.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT open multiple KYC accounts, use VPNs/proxies, or self-match across sub-accounts (12 §3).

## Doc sync on completion

- `docs/07-security-notes.md` §3: audit evidence location.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.03, T7.40 when this item is done.

## Branch & PR

- Branch: `p7/P7-T047-verify-live-key-and-subaccount-audit`
- PR title: `P7-T047: Verify live keys and sub-account isolation before funding`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T047` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
