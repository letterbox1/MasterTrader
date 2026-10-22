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
depends_on: [P3-T012, P3-T056]
requirements: [R3.04, R3.17]
roadmap_todos: [T3.04]
modules: [M18]
dashboards: [D15]
tools: []
mcp: []
env: []
services: [your venue accounts and wallets]
branch: p3/P3-T042-register-accounts-and-tags
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T042 · Register your accounts and tag each investment or trading

## Goal / expected outcome

Every exchange/broker account, sub-account and on-chain address you own is in the registry with role and a tax tag (`investment` or `trading`), so internal transfers are recognised and capital vs revenue segregation works from day one.

## Context & references

- Roadmap: [R3.04, T3.04](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 goals §6–7](../../../docs/09-journal-and-tax.md#goals) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Mechanism: the Accounts page in D16 Settings (P3-T056) or the seed file loaded through it; both issue `wallet.register`/`wallet.tag` (C1) from P3-T012 · decision [17 §D P3-B011](../../../docs/17-decisions-register.md#d-other-decisions)

## Requirements

- Use **D16 → Settings → Accounts** (P3-T056) to register each entry, or fill `config/journal/accounts.yaml` on the host and load it from that page (masked account ids, public addresses only; **no keys, no seed phrases**).
- For each entry: venue/chain, masked account id or public address, provider label, role, custody, mode (paper/live), tag `investment` or `trading`, effective_from.
- Each registration and tag is a C1 command through `mt_api`; confirm each in the UI prompt (the CLI loader `python -m mt_journal.registry.seed` remains as a fallback).
- Ask the agent (via a TAX_QUESTION) if any account mixes both purposes.

## ToDo

- [ ] List all accounts/addresses (include paper/testnet ones used by P2)
- [ ] Register and tag them on the Accounts page (or load the seed file there); confirm the C1 prompts
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (registration now on the D16 Accounts page (P3-T056, R3.17, P3-B011); services filled)
