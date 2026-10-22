---
id: P5-B015
kind: gap
title: Wallet registry ownership: P3 "account/wallet registry" vs 13 §3 `ops.wallets`; mandate/exec_log schema prefixes
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B015-wallet-registry-ownership-naming
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/09-journal-and-tax.md, docs/08-airdrops-and-token-launches.md]
doc_sync_status: done
found_in: "docs/13-wallets-treasury-and-onchain.md §3; docs/roadmap/phase-3-journal-and-tax.md R3.04; docs/08 §Data model"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §B P3-B003/P5-B015/P6-B005): one registry, `ops.wallets` (accounts and on-chain addresses), created in P3 and extended additively by the P5 wallet-indexer; no `treasury.wallet`; 08 data model uses schema prefixes
- [x] Docs carry it: 13 §3 step 1, 09 goal 6, 02 §5 (one wallet registry `ops.wallets`), phase-3 roadmap R3.04/T3.22, 08 data model (`curation.*` prefixes; wallets in `ops.wallets`), roadmap R5.05
- [x] P5 tasks aligned: P3-T012 (creates the table), P5-T009 (additive columns), P5-T021 (register/tag)

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

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
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P3-B003/P5-B015/P6-B005): one registry, `ops.wallets` (accounts and on-chain addresses), created in P3 and extended additively by the P5 wallet-indexer; no `treasury.wallet`; 08 data model uses schema prefixes. Docs checked: 13 §3 step 1, 09 goal 6, 02 §5 (one wallet registry `ops.wallets`), phase-3 roadmap R3.04/T3.22, 08 data model (`curation.*` prefixes; wallets in `ops.wallets`), roadmap R5.05. Implementation owned by P3-T012 (creates the table), P5-T009 (additive columns), P5-T021 (register/tag)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P3-B003/P5-B015/P6-B005); docs updated: 13 §3 step 1, 09 goal 6, 02 §5 (one wallet registry `ops.wallets`), phase-3 roadmap R3.04/T3.22, 08 data model (`curation.*` prefixes; wallets in `ops.wallets`), roadmap R5.05; implementation owned by P3-T012 (creates the table), P5-T009 (additive columns), P5-T021 (register/tag)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
