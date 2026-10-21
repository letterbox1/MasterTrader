---
id: P3-T003
kind: task
title: Export historical broker and exchange statements for opening balances
phase: 3
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R3.01, R3.05]
roadmap_todos: [T3.03]
modules: [M18]
dashboards: []
branch: p3/P3-T003-export-historical-statements
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

# P3-T003 · Export historical broker and exchange statements for opening balances

## Goal / expected outcome

Every historical statement you already have (IBKR Flex, OANDA, IG, exchanges, any wallets) is exported in machine-readable form and dropped into the journal inbox, so P3-T021 can build opening balances and opening lots with their original acquisition dates and cost bases.

## Context & references

- Roadmap: [R3.01, R3.05, T3.03](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Formats used by the adapters: P3-T015 (IBKR Flex XML), P3-T016 (OANDA v20 transactions / IG history CSV), P3-T014 (ccxt ledgers), P3-T021 (opening lots)
- Security: [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) — statements are tax-sensitive and encrypted at column level (P3-T007)

## Requirements

- Coverage: from the acquisition date of the **oldest still-open position** (anything older matters for cost base and the 12-month discount) and at least the current FY from 1 July 2026.
- IBKR: Flex Query → Activity, XML, include Trades, Cash Transactions, Transfers, Corporate Actions, Open Positions with `openDateTime` and cost basis; one file per year.
- OANDA: transaction history export (CSV/JSON) per account; IG: transaction + trade history CSV per account.
- Exchanges: full trade, deposit/withdrawal, funding and fee history CSVs per account (Binance, Kraken, Independent Reserve, BTC Markets, etc. as used).
- Files go to the host inbox `/srv/mastertrader/journal/inbox/<venue>/<account>/` (bind-mounted read-only into `journal`), **never into git**; the inbox dir is git-ignored and on the encrypted disk.
- Any API token you create for automated retrieval (e.g. IBKR Flex Web Service token) goes **only** into the sops secrets file as `IBKR_FLEX_TOKEN` (read-only).

## ToDo

- [ ] List every account you've held since your oldest open lot (venue, account id suffix, currency)
- [ ] Export statements per the formats above; name files `<venue>_<account>_<from>_<to>.<ext>`
- [ ] Copy them into the inbox paths on the host (scp over Tailscale); confirm checksums
- [ ] If using the IBKR Flex Web Service: create a read-only Flex token + query ids; add them to the sops file (`sops secrets/journal.enc.yaml`)
- [ ] Note any gaps (closed accounts, lost records) in the progress log so P3-T021 can flag those lots as `cost_base_estimated`
- [ ] Tell the agent (comment here) when the drop is complete

## Verification

### Tests

- Confirmation is P3-T021's import report: every file parsed, opening lots per asset listed, zero unparsed rows.

### Scenarios

- Given a statement for a closed account, when P3-T021 imports it, then its lots appear as fully disposed history and nothing stays open.
- Given a missing year, when imported, then the affected lots carry `cost_base_estimated = true` and a D15 warning.

### Stress / failure injection

- n/a: one-off export

## Acceptance criteria

- [ ] Every account listed has at least one statement file in the inbox
- [ ] Gaps documented in the progress log
- [ ] No statement file or token in git (`git status` clean; gitleaks passes)

## Exceptions & edge cases

- Venue no longer offers exports → use emailed annual statements; P3-T021 accepts a manual opening-lot CSV (template in its task).
- Old exchange gone (e.g. collapsed) → record as a loss/theft candidate question for the agent.

## Cardinal rules (do NOT)

- Do NOT commit statements or tokens; do NOT paste them into chat.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.03 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T003-export-historical-statements` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T003: Export historical broker and exchange statements for opening balances`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
