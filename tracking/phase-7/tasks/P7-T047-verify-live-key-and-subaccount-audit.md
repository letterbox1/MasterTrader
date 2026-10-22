---
id: P7-T047
kind: task
title: Live key audit: trade-only, no withdrawals, IP-locked to the egress IP, one key per sub-account
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T032, P7-T007, P7-T008, P7-T031, P7-T066]
requirements: [R7.04, R7.14]
roadmap_todos: [T7.65, T7.40]
modules: [M12, M17]
dashboards: [D16, D05]
tools: [git, uv, docker, sops]
mcp: []
env: [MT_LIVE_TRADE_KEY, MT_LIVE_TRADE_SECRET, MT_LIVE_DEADMAN_KEY, MT_LIVE_DEADMAN_SECRET, MT_LIVE_RECON_KEY, MT_LIVE_RECON_SECRET]
services: [live venue sub-accounts (P7-T006/T007), egress exit node (P7-T065/T066)]
branch: p7/P7-T047-verify-live-key-and-subaccount-audit
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

# P7-T047 · Live key audit: trade-only, no withdrawals, IP-locked to the egress IP, one key per sub-account

## Goal / expected outcome

A recorded key audit (T7.65, after P7-T007 and P7-T065) shows every live key is trade-only, withdrawals disabled, IP-locked to the exit node's static IP, one engine key per sub-account; each mandate has its own sub-account and secrets in the live engine config; STP prevents self-matching across sub-accounts; and Travel Rule addresses are registered. This is the keys-last check for the keyless builds P7-T031/T032. The `env` names are the first live sub-account's keys as exported from the sops file (`live.<venue>.<subaccount>.*`) for the audit run.

## Context & references

- Roadmap: [R7.04, R7.14 · ToDo T7.65, T7.40](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (only the exit-node IP allow-listed) · [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (Travel Rule) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (STP, no self-matching) · Roadmap R7.04 'Verified by: key audit'
- Related: P7-T032, P7-T007, P7-T008, P7-T031, P7-T065/P7-T066 (exit node and tunnel)

## Requirements

- Add the real live sub-account entries to the engine config (P7-T031 schema; secret names only) and run the key audit: `pass` for every live key (P7-T032), one engine key per sub-account (plus the `deadman` and recon keys, 16 §3.1).
- Each key's allow-list equals exactly the exit node's static IP (venue introspection or attestation); a request from a non-allow-listed IP (e.g. the home IP outside the tunnel) with a **read-only** recon key is rejected by the venue (proves the IP lock), and the same request through the tunnel succeeds; never probe with a trade key.
- Container inspection: only `engine` and `deadman` hold trade-only keys; only `monitor` holds recon keys; all three use the egress namespace.
- STP: two opposing small paper/testnet orders from two sub-accounts never self-match (STP cancel recorded as non-fill).
- Venue rows list whitelisted addresses and dates.

## ToDo

- [ ] Add the live sub-account config entries; run the key audit; attach result.
- [ ] Run the IP-lock probe with a recon key (outside and through the tunnel); attach result.
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
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.65, T7.40 when this item is done.

## Branch & PR

- Branch: `p7/P7-T047-verify-live-key-and-subaccount-audit`
- PR title: `P7-T047: Live key audit: trade-only, no withdrawals, IP-locked to the egress IP, one key per sub-account`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T047` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T7.65 live key audit: allow-list = exit-node IP (16 §3.2/17 §A P7-B004), deadman keys (16 §3.1); carries the live env names; deps P7-T066)
