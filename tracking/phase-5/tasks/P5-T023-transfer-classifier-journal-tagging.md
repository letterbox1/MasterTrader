---
id: P5-T023
kind: task
title: Transfer classifier: internal tagging, airdrop receipts and approval events into M18
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T022]
requirements: [R5.05, R5.18]
roadmap_todos: [T5.22]
modules: [M22, M18]
dashboards: [D18, D14]
branch: p5/P5-T023-transfer-classifier-journal-tagging
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T023 · Transfer classifier: internal tagging, airdrop receipts and approval events into M18

## Goal / expected outcome

Every on-chain transfer touching a registered wallet is classified (internal between own wallets, external in/out, airdrop receipt, staking reward, fee/gas, swap leg, approval/revoke) and emitted to the journal (M18) as append-only events; internal moves are **never disposals** and link both wallet rows.

## Context & references

- Roadmap: R5.05 (transfer classifier → M18), R5.18 · ToDo T5.22
- [09 goals](../../../docs/09-journal-and-tax.md) (internal transfers never disposals) · P3 ingestion (R3.01, on-chain stub)
- D18 internal transfers widget ([D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) acceptance 2)

## Requirements

- Sources: EVM Transfer/Approval logs (Blockscout/RPC `eth_getLogs` per address), native transfers via traces where available; Solana parsed transactions (Helius).
- Rules: both sides registered → `internal`; inbound from a known claim contract/Merkle distributor → `airdrop_receipt` (linked to opportunity/campaign); Approval logs → `ops.wallet_approval` + `wallet.*.approval`; nonce changes → `ops.nonce_account` + `wallet.*.nonce_authority`.
- Unknown inbound tokens from unknown senders → `unsolicited` (possible address-poisoning/dust); never auto-interacted with.
- Journal events carry native/USD/AUD with FX source (P3 FX service), tx hash, block time as `event_time`.
- Idempotent on (chain, tx hash, log index).

## ToDo

- [ ] Implement `packages/mt_treasury/indexer/classifier.py` and rule table.
- [ ] Emit `wallet.{chain}.{address}.transfer` and journal events through the P3 ingestion API.
- [ ] Address-poisoning detection (lookalike addresses sending zero-value transfers) → warning badge.
- [ ] Tests with fixtures; doc sync.

## Verification

### Tests
- Unit: rule table golden tests (internal, airdrop receipt, unsolicited, approval, swap leg).
- Integration: replaying the same block range twice yields no duplicate journal events.
- Property: sum of classified flows per wallet equals the balance delta over the window.

### Scenarios
- Given a sweep from hot to vault, when classified, then `internal` with both wallet links and no CGT event.
- Given a zero-value transfer from a lookalike address, then `unsolicited` + poisoning warning and the address is never added to any allow-list.

### Stress / failure injection
- Backfill 90 days for 20 wallets within RPC quotas (chunked); resumable after interruption.

## Acceptance criteria

- [ ] All transfer classes emitted to M18
- [ ] Internal never a disposal
- [ ] Idempotent replay
- [ ] Approvals and nonce events feed monitors

## Exceptions & edge cases

- Reorgs: events < N confirmations marked provisional; journal receives them only after finality depth (EVM 12 blocks / Solana finalized).

## Cardinal rules (do NOT)

- Do NOT rewrite journal events on reclassification; append corrections.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md`: on-chain ingestion now live (classification table).
- `docs/13-wallets-treasury-and-onchain.md` §3: classifier rules.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T023-transfer-classifier-journal-tagging`
- PR title: `P5-T023: Transfer classifier: internal tagging, airdrop receipts and approval events into M18`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
