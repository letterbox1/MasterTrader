---
id: P5-B015
kind: gap
title: Wallet registry ownership: P3 "account/wallet registry" vs 13 §3 `ops.wallets`; mandate/exec_log schema prefixes
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.05]
roadmap_todos: []
modules: [M22, M18]
dashboards: []
branch: p5/P5-B015-wallet-registry-ownership-naming
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/09-journal-and-tax.md, docs/08-airdrops-and-token-launches.md]
doc_sync_status: n/a
found_in: "docs/13-wallets-treasury-and-onchain.md §3; docs/roadmap/phase-3-journal-and-tax.md R3.04; docs/08 §Data model"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B015 · Wallet registry ownership: P3 "account/wallet registry" vs 13 §3 `ops.wallets`; mandate/exec_log schema prefixes

## Goal / expected outcome

Exactly one registry table (`ops.wallets`) owned by M22 and read by M18; table names in 08's data model carry schema prefixes matching 15 §2 (`curation.mandate`, `curation.exec_log`).

## Context & references

- P3 builds an account/wallet registry (R3.04, T3.22) without naming the table
- 13 §3 names `ops.wallets`; 08 lists `mandate`/`exec_log` without schema; 15 §2.1 uses `curation.mandate`
- Task P5-T009 extends or views the P3 table

## Requirements

- **Steps to reproduce:** Search the docs for the registry table name and owner.
- **Expected:** One name, one owner.
- **Actual:** Unnamed in P3/09, named in 13; schema prefixes inconsistent.
- **Suggested fix:** Name `ops.wallets` in 09 and the P3 roadmap note; add schema prefixes to 08's data model.
- **Impact:** S3: risk of two registries drifting.

## ToDo

- [ ] Agree the resolution with the user (or record the decision in the progress log)
- [ ] Edit the source docs listed under Doc sync so they agree
- [ ] Update the affected P5 task files if the numbers/names change

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Docs listed under Doc sync are consistent
- [ ] Affected P5 tasks reference the resolved value/name
- [ ] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution
- `docs/09-journal-and-tax.md`: align with the resolution
- `docs/08-airdrops-and-token-launches.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B015-wallet-registry-ownership-naming`
- PR title: `P5-B015: Wallet registry ownership: P3 "account/wallet registry" vs 13 §3 `ops.wallets`; mandate/exec_log schema prefixes`

## Progress log

- 2026-10-21 00:00 · planner · opened
