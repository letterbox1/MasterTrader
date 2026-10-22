---
id: P5-T021
kind: task
title: Wallet registry with proof of control, register/tag commands
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P5-T011, P5-T012, P5-T067, P3-T012]
requirements: [R5.05, R5.01, R5.25]
roadmap_todos: [T5.22]
modules: [M22, M18]
dashboards: [D18]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T021-wallet-registry-proof-of-control
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/09-journal-and-tax.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T021 · Wallet registry with proof of control, register/tag commands

## Goal / expected outcome

`wallet.register` (C1) and `wallet.tag` (C1) maintain `ops.wallets` — address, chain, provider label, role/custody tier, `investment`/`trading` tag — with a proof-of-control step, and system-created signer wallets register themselves; the journal and indexer read ownership only from here.

## Context & references

- Roadmap: [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.22 · USER item P5-T005
- [13 §3 step 1](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · [09 goals 6–7](../../../docs/09-journal-and-tax.md)
- P3 `ops.wallets` (P3-T012) is the base, extended additively (decision P5-B015, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); proof of control per R5.25 / P5-B016 is verified by P5-T067 (the system never signs)

## Requirements

- Proof of control (R5.25): the `wallet.register` preview returns the one-time challenge from P5-T067; confirm submits your wallet-app signature (EIP-4361-style text / Solana `signMessage`) or waits for the self-transfer; the system only verifies and never signs. There is no unproven registration: without proof the row stays `pending` and is excluded from autonomous paths and sweep destinations.
- Signer-created wallets auto-register with `proof_method=signer_owned`.
- Ownership changes (role/tag) append audit rows; tag changes affect only future journal classifications unless a correction is requested.
- Address normalisation (EIP-55 checksum; base58 Solana) and duplicate detection across chains.

## ToDo

- [ ] Implement command handlers in `packages/mt_treasury/registry/` and queries `/wallets`, `/wallets/{id}`.
- [ ] Call the P5-T067 proof verifier from `wallet.register` (preview → challenge; confirm → verify) and feed it `wallet.*.transfer` events for self-transfers.
- [ ] Hook signer `key_create` → auto-register.
- [ ] Emit `journal` registry-changed event so M18 re-tags internal transfers going forward.
- [ ] Tests; doc sync.

## Verification

### Tests
- Integration: `wallet.register` with a valid challenge signature → `verified`; with an invalid one → `rejected` (verifier unit tests live in P5-T067).
- Integration: self-transfer proof completes when the indexer sees the exact amount/memo.
- Unit: duplicate address on the same chain rejected.

### Scenarios
- Given an address registered with a wrong tag, when the user re-tags it, then a new audit row is written and the journal flags past events for review instead of rewriting them.
- Given a proof self-transfer never arrives within 24 h, then status `unverified` and a reminder task.

### Stress / failure injection
- n/a: low-volume admin path (indexer load covered in P5-T022)

## Acceptance criteria

- [ ] Register/tag commands live at C1
- [ ] Registration requires proof via P5-T067 (wallet-app signature or self-transfer); signer wallets `signer_owned`; exchange accounts `exchange_api`
- [ ] Signer wallets auto-registered
- [ ] Journal sees ownership changes

## Exceptions & edge cases

- Exchange accounts (from P3) have no address proof: proof = read-only API key works.

## Cardinal rules (do NOT)

- Do NOT ask the user to connect a wallet to the web UI or sign typed data; message signing happens on the user's own device only.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: proof-of-control methods.
- `docs/09-journal-and-tax.md`: registry is `ops.wallets`.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T021-wallet-registry-proof-of-control`
- PR title: `P5-T021: Wallet registry with proof of control, register/tag commands`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (proof of control per R5.25/P5-B016 via P5-T067, manual_attested dropped; extends P3 `ops.wallets` per P5-B015)
