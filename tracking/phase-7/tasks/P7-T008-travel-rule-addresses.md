---
id: P7-T008
kind: task
title: Pre-register withdrawal addresses with proof of control (Travel Rule)
phase: 7
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T006, P3-T012]
requirements: [R7.04]
roadmap_todos: [T7.03]
modules: [M22]
dashboards: [D18, D06]
tools: []
mcp: []
env: []
services: [venue withdrawal whitelist settings]
branch: p7/P7-T008-travel-rule-addresses
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T008 · Pre-register withdrawal addresses with proof of control (Travel Rule)

## Goal / expected outcome

Every AU venue you trade on has your own vault/warm withdrawal addresses pre-registered with proof of control and whitelist-only withdrawals, so manual transfers out (done outside the system) and the kill-switch sweep destination are ready.

## Context & references

- Roadmap: [R7.04 · ToDo T7.03](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (Travel Rule at zero threshold since 1 Jul 2026; pre-register with proof of control; pre-fund inventory) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (transfers out are manual, outside the system)
- Cross-phase: P3-T012 creates `ops.wallets` (one registry, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)) and is a `depends_on`; P5-T001/P5-T005 (hardware vault/warm wallets, full registration) extend it but are **not** required: register the addresses you already own in `ops.wallets` (P7 doesn't wait for P5, [17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions)).
- Related: P7-T022 (flatten to stables keeps funds on venue; transfers stay manual)

## Requirements

- Only addresses registered in `ops.wallets` with role `vault` or `warm` may be whitelisted.
- Whitelist-only withdrawal mode enabled on each venue where available; new-address cool-down left at the venue default or longer.
- Record on the venue row: whitelisted address labels (not keys/seeds), date registered.

## ToDo

- [ ] For each live venue: add your vault and warm addresses to the withdrawal whitelist; complete the venue's proof-of-control step (signed message or micro-deposit).
- [ ] Enable whitelist-only withdrawals; confirm the API keys still have no withdrawal scope (P7-T007).
- [ ] Record address labels and dates on the venue row in D06.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given a whitelist is enforced, when anyone tries to add a new address, then the venue's cool-down and email confirmation apply (venue-side control).

### Stress / failure injection
- n/a: account setup.

## Acceptance criteria

- [ ] Each live venue has whitelist-only withdrawals to your registered vault/warm addresses.
- [ ] Venue rows list the address labels and registration dates.

## Exceptions & edge cases

- Venue lacks whitelists: keep balances at the micro-live minimum and note the gap on the venue row.
- Residency move: Travel Rule obligations change; re-run with the new jurisdiction's rules.

## Cardinal rules (do NOT)

- Do NOT give any system key withdrawal rights to make sweeps 'automatic'.
- Do NOT paste seed phrases or private keys anywhere.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §1: note that addresses are pre-registered per live venue (dates only).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.03 when this item is done.

## Branch & PR

- Branch: `p7/P7-T008-travel-rule-addresses`
- PR title: `P7-T008: Pre-register withdrawal addresses with proof of control (Travel Rule)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T008` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (dep on P3-T012 ops.wallets instead of P5 per 17 §B/§D P7-B011; fields)
