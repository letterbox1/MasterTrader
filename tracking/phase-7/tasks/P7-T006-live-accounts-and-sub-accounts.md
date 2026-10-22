---
id: P7-T006
kind: task
title: Open or verify live accounts and create sub-accounts per mandate
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T003]
requirements: [R7.04]
roadmap_todos: [T7.02]
modules: [M12, M11]
dashboards: [D05, D06]
tools: []
mcp: []
env: []
services: [venue live accounts (KYC)]
branch: p7/P7-T006-live-accounts-and-sub-accounts
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

# P7-T006 · Open or verify live accounts and create sub-accounts per mandate

## Goal / expected outcome

At each `allowed` target venue you hold one KYC'd live account and a separate **sub-account per mandate** (`hitl` and `autonomous` mandates kept apart from each other and from paper), each funded later only with that mandate's capital.

## Context & references

- Roadmap: [R7.04 · ToDo T7.02](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (separate keys and sub-accounts for paper, `hitl` and `autonomous` mandates) · modes per bot [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) · [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (Travel Rule, never misstate wholesale status) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (no self-matching across sub-accounts)
- Related: P7-T003 (venue must be `allowed`), P7-T007 (keys), P7-T008 (withdrawal addresses), P7-T031 (engine config per sub-account)

## Requirements

- One KYC identity per venue; **no** second KYC accounts; declare **retail** status (never wholesale).
- Sub-accounts named `mt-<sleeve>-<mode>` (e.g. `mt-trend-hitl`, `mt-trend-autonomous`), one per mandate; record venue, sub-account id and mandate on the venue row (no credentials).
- Sub-account-level STP set where the venue supports it (OKX `acctStpMode`), and self-trade across sub-accounts prevented (12 §3).
- Unblocks P7-T007 and P7-T031.

## ToDo

- [ ] For each target venue, complete or verify KYC as a retail client in your own name and country.
- [ ] Create the sub-accounts listed by the planner for the first sleeves (start with one sleeve; every bot starts live in `hitl`, R7.08).
- [ ] Enable venue-side 2FA and withdrawal whitelist-only roles where offered (Independent Reserve-style).
- [ ] Record sub-account ids against the mandate in D05 → Venues (ids are not secrets; keys are).
- [ ] Confirm with the agent so P7-T007 can start.

## Verification

### Tests
- n/a (user action); P7-T047 audits the resulting key/sub-account set.

### Scenarios
- Given two sub-accounts on one venue, when two sleeves' orders could cross, then STP cancels and the engine records non-fills (verified in P7-T047).

### Stress / failure injection
- n/a: account setup.

## Acceptance criteria

- [ ] Every target venue has a verified live account in your name, retail status.
- [ ] One sub-account per mandate exists and is recorded on the venue row.
- [ ] No venue has more than one KYC account for you.

## Exceptions & edge cases

- Venue lacks sub-accounts: use a separate venue for the auto mandate or keep its bots in `hitl` there; never a second KYC account.
- KYC asks for wholesale status: decline.

## Cardinal rules (do NOT)

- Do NOT claim wholesale status (ASIC fined Binance AU A$10m for misclassification).
- Do NOT fund any sub-account yet (P7-T057 does that after the gate report).
- Do NOT open multiple KYC accounts, use VPNs/proxies, or self-match across sub-accounts (12 §3).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/07-security-notes.md` §3: note the sub-account naming convention.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.02 when this item is done.

## Branch & PR

- Branch: `p7/P7-T006-live-accounts-and-sub-accounts`
- PR title: `P7-T006: Open or verify live accounts and create sub-accounts per mandate`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T006` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (modes paper/hitl/autonomous per 17 §B; fields)
