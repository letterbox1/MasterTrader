---
id: P3-T012
kind: task
title: Account and wallet registry with investment and trading tags
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005]
requirements: [R3.04]
roadmap_todos: [T3.22]
modules: [M18, M22]
dashboards: [D15]
branch: p3/P3-T012-account-wallet-registry-tags
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T012 · Account and wallet registry with investment and trading tags

## Goal / expected outcome

One registry lists every account and address you own (exchange/broker accounts and sub-accounts, on-chain addresses) with role, provider, custody and a per-account `investment` or `trading` tax tag (effective-dated), exposed through `wallet.register` / `wallet.tag` (C1) and a seed-file loader, so the journal can tell internal transfers from disposals and segregate capital from revenue activity.

## Context & references

- Roadmap: [R3.04, T3.22](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 goals §6–7](../../../docs/09-journal-and-tax.md#goals) · [13 §3 unified wallet view](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) (`ops.wallets` fields) · commands in [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`wallet.register` C1, `wallet.tag` C1)
- Boundary: P5 T5.22 `wallet-indexer` reads and extends this registry (aggregation, approvals); P3 owns the table and tags
- Gaps: P3-B003 (table naming `ops.wallets` vs `treasury.wallet`), P3-B011 (no P3 UI surface for the registry)

## Requirements

- Table `ops.wallets` (as in 13 §3 and R5.05): `wallet_id`, kind (`exchange_account` | `broker_account` | `onchain_address`), venue/chain, address or masked account id, provider label, role (vault/warm/hot/identity/burner/governance/trading), custody (custodial/self), `mode` (paper/live), `owner = self`.
- Tax tag history `journal.account_tag` (WORM, effective-dated): `wallet_id`, `tag` ∈ {investment, trading}, `effective_from` (taxpayer-local date), reason; current tag = latest effective row ≤ event date.
- Commands: `wallet.register` (C1), `wallet.tag` (C1) via `mt_api` with audit; tag change mid-FY allowed but shows a D15 warning (agent question).
- Seed loader: `config/journal/accounts.yaml` (no secrets, account numbers masked to last 4) → issues `wallet.register`/`wallet.tag` commands through `mt_api` (never direct SQL).
- Every journal event resolves `account_id` → registry; unknown account → event quarantined with `unknown_account`.

## ToDo

- [ ] Migration for `ops.wallets` (if not created by P0) and `journal.account_tag`
- [ ] Command handlers in `packages/mt_api/commands/wallet.py` (C1 level) + validation
- [ ] `mt_journal.registry` lookup service with effective-dated tag resolution
- [ ] Seed loader CLI `python -m mt_journal.registry.seed config/journal/accounts.yaml`
- [ ] Tests; docs

## Verification

### Tests

- Unit: tag resolution on boundary dates (tag effective 2027-01-15 applies to events with local date ≥ 2027-01-15).
- Integration: `wallet.register` via mt_api writes `audit.command` and the registry row; C1 confirm enforced.
- Unit: unknown account → quarantine.

### Scenarios

- Given an exchange sub-account tagged `trading` and a cold address tagged `investment`, when BTC moves from one to the other, then P3-T018 marks it internal (not a disposal) and the lots keep their acquisition dates but now sit under the `investment` tag.
- Given a tag change mid-FY, when D15 opens, then a warning explains both tags apply to different parts of the year.

### Stress / failure injection

- n/a: low-volume config path (load test not meaningful)

## Acceptance criteria

- [ ] Registry + tag history live; commands audited at C1
- [ ] Every journalled event has a resolvable `account_id`
- [ ] Seed file loads idempotently
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Shared custody (exchange omnibus deposit address) → registry stores the account, not the omnibus address.
- An address later found not to be yours → new registry row with `owner = not_self` superseding; past internal-transfer matches are re-evaluated as corrections.

## Cardinal rules (do NOT)

- Do NOT put full account numbers, keys or seed phrases in the seed file.
- Do NOT treat a tag as a tax ruling; it's a segregation input for the agent.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: note that the registry lands in P3 and the tax tag is effective-dated in `journal.account_tag`.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.22 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T012-account-wallet-registry-tags`
- PR title: `P3-T012: Account and wallet registry with investment and trading tags`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
