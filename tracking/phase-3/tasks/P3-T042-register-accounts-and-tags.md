---
id: P3-T042
kind: task
title: Register your accounts and tag each investment or trading
phase: 3
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P3-T012]
requirements: [R3.04]
roadmap_todos: [T3.04]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T042-register-accounts-and-tags
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T042 · Register your accounts and tag each investment or trading

## Goal / expected outcome

Every exchange/broker account, sub-account and on-chain address you own is in the registry with role and a tax tag (`investment` or `trading`), so internal transfers are recognised and capital vs revenue segregation works from day one.

## Context & references

- Roadmap: [R3.04, T3.04](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 goals §6–7](../../../docs/09-journal-and-tax.md#goals) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Mechanism: P3-T012 (seed file + `wallet.register`/`wallet.tag` commands)

## Requirements

- Edit `config/journal/accounts.yaml` on the host (masked account ids, public addresses only; **no keys, no seed phrases**).
- For each entry: venue/chain, masked account id or public address, provider label, role, custody, mode (paper/live), tag `investment` or `trading`, effective_from.
- Run the loader: `python -m mt_journal.registry.seed config/journal/accounts.yaml` (it issues C1 commands through `mt_api`; confirm each in the UI/CLI prompt).
- Ask the agent (via a TAX_QUESTION) if any account mixes both purposes.

## ToDo

- [ ] List all accounts/addresses (include paper/testnet ones used by P2)
- [ ] Fill the seed file; run the loader; confirm the C1 prompts
- [ ] Check D14 Events: no `unknown_account` quarantine items remain
- [ ] Commit the seed file only if it contains no personal identifiers beyond masked ids (otherwise keep it host-only and git-ignored)

## Verification

### Tests

- Confirmation: registry query lists every account; quarantine count for `unknown_account` = 0.

### Scenarios

- Given a withdrawal from Binance to your Ledger, when both are registered, then the journal shows an internal transfer, not a disposal.

### Stress / failure injection

- n/a

## Acceptance criteria

- [ ] Every account used by the P2 paper clock is registered and tagged
- [ ] No `unknown_account` quarantine items

## Exceptions & edge cases

- Unsure about a tag → tag `trading` (conservative for segregation) and raise a TAX_QUESTION; the tag history is effective-dated so it can change later.

## Cardinal rules (do NOT)

- Do NOT put API keys, seed phrases or full account numbers in the seed file.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.04 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T042-register-accounts-and-tags` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T042: Register your accounts and tag each investment or trading`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
