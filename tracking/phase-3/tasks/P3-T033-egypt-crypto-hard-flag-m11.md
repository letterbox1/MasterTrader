---
id: P3-T033
kind: task
title: Egypt crypto hard flag wired to the risk manager
phase: 3
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T031]
requirements: [R3.09]
roadmap_todos: [T3.26]
modules: [M18, M11]
dashboards: [D15, D06]
branch: p3/P3-T033-egypt-crypto-hard-flag-m11
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T033 · Egypt crypto hard flag wired to the risk manager

## Goal / expected outcome

While the residency timeline says Egypt, M11 blocks every crypto order, bot/strategy in autonomous or HITL mode on crypto, and any crypto mandate, and D15 shows a red compliance flag on any crypto activity; leaving Egypt never auto-unblocks without the C3 path.

## Context & references

- Roadmap: [R3.09, T3.26](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 key findings: Egypt](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · [12 §2 venue registry per residency](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · D15 rules (Egypt red flag) [D15](../../../docs/ui/dashboards/D15-tax.md)
- Cross-phase: P2 T2.22 (M11 venue registry check per residency), P5 mandates (consumers of the same flag)
- Gap: P3-B007 (no NATS/contract defined; C-level for loosening)

## Requirements

- Contract (proposed, document in 02 §6): NATS KV `compliance_state` key `residency` = {country, since, flags:[crypto_prohibited]}; `journal` writes it on every residency change; M11 reads it in pre-trade checks (in-process cache, p99 < 1 ms budget unaffected).
- M11 rule: asset class crypto (spot, perp, token) + flag `crypto_prohibited` → reject with reason `residency_EG_crypto_prohibited`; protective exits (reduce-only closes) still allowed.
- Residency change that **removes** the flag is a loosening → applied only after C3 (Telegram approve + TOTP + cool-down) through `mt_api`.
- Startup: if KV is missing, M11 reads the latest `journal.residency_period` via API; if both unavailable → fail-closed for crypto (default-deny).

## ToDo

- [ ] Write KV publisher in `mt_journal/residency/compliance.py`
- [ ] Add the M11 check in `packages/mt_risk/checks/residency.py` + reason code
- [ ] C3 classification for flag removal in the command layer
- [ ] Tests; docs

## Verification

### Tests

- Unit (M11): crypto order with EG flag → rejected; reduce-only close → allowed.
- Integration: add EG residency → KV updated → paper crypto order rejected within 5 s.
- Unit: removing EG requires C3 (C1 attempt refused).

### Scenarios

- Given residency EG from a date, when a bot tries a crypto entry, then M11 rejects it and D06 shows the reason.
- Given the KV store is unavailable at engine start, when a crypto order arrives, then it's denied (fail-closed).

### Stress / failure injection

- Pre-trade latency benchmark with the extra check: p99 still < 1 ms (P2 SLO).

## Acceptance criteria

- [ ] Crypto blocked while EG is active (tests)
- [ ] Protective exits never blocked
- [ ] Unblocking needs C3
- [ ] Latency SLO unchanged
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Future-dated residency → flag activates at the local start date (scheduled KV update).

## Cardinal rules (do NOT)

- Do NOT block protective exits.
- Do NOT let a residency edit loosen risk without C3.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6: add KV `compliance_state`.
- `docs/03-build-spec.md` M11: residency compliance check.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.26 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T033-egypt-crypto-hard-flag-m11`
- PR title: `P3-T033: Egypt crypto hard flag wired to the risk manager`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
