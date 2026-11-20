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
depends_on: [P3-T005, P0-T024, P0-T034, P0-T035]
requirements: [R3.04]
roadmap_todos: [T3.22]
modules: [M18, M22]
dashboards: [D15]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p3/P3-T012-account-wallet-registry-tags
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T012 · Account and wallet registry with investment and trading tags

## Goal / expected outcome

One registry lists every account and address you own (exchange/broker accounts and sub-accounts, on-chain addresses) with role, provider, custody and a per-account `investment` or `trading` tax tag (effective-dated), exposed through `wallet.register` / `wallet.tag` (C1) and a seed-file loader, so the journal can tell internal transfers from disposals and segregate capital from revenue activity.

## Context & references

- Roadmap: [R3.04, T3.22](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Platform: [18 §2](../../../docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary) (`mt-journal` Rust crate, `rust_decimal`; Python only for the ccxt ledger importer `mt_ledger_import`, [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)) · [09 architecture](../../../docs/09-journal-and-tax.md#architecture) · [18 §4](../../../docs/18-platform-and-deployment.md#4-database-supabase-postgres) (Supabase Postgres, `supabase/migrations/`, pgTAP)
- [09 goals §6–7](../../../docs/09-journal-and-tax.md#goals) · [13 §3 unified wallet view](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) (`ops.wallets` fields) · commands in [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`wallet.register` C1, `wallet.tag` C1)
- Boundary: P5 T5.22 `wallet-indexer` reads and extends this registry (aggregation, approvals); P3 owns the table and tags
- Decisions: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (one registry `ops.wallets`, created in P3, extended by the P5 wallet-indexer; P3-B003) and [17 §D P3-B011](../../../docs/17-decisions-register.md#d-other-decisions) (minimal Accounts page, built in P3-T056) · [02 §4](../../../docs/02-v1-architecture.md#4-logical-components)
- Cross-phase prerequisites (depends_on): P0-T024 (`ops` schema, roles), P0-T034 (command bus), P0-T035 (C-levels)

## Requirements

- Table `ops.wallets` (as in 13 §3 and R5.05): `wallet_id`, kind (`exchange_account` | `broker_account` | `onchain_address`), venue/chain, address or masked account id, provider label, role (vault/warm/hot/identity/burner/governance/trading), custody (custodial/self), `mode` (paper/live), `owner = self`.
- Tax tag history `journal.account_tag` (WORM, effective-dated): `wallet_id`, `tag` ∈ {investment, trading}, `effective_from` (taxpayer-local date), reason; current tag = latest effective row ≤ event date.
- Commands: `wallet.register` (C1), `wallet.tag` (C1) via `mt-api` with audit; tag change mid-FY allowed but shows a D15 warning (agent question).
- Seed loader (also used by the Accounts page upload, P3-T056): `config/journal/accounts.yaml` (no secrets, account numbers masked to last 4) → issues `wallet.register`/`wallet.tag` commands through `mt-api` (never direct SQL). The paper/testnet accounts are seeded by the agent from `config/journal/accounts.paper.yaml`, so recon and the paper run never wait for your real accounts (P3-T042).
- Every journal event resolves `account_id` → registry; unknown account → event quarantined with `unknown_account`.

## ToDo

- [ ] Migration creating `ops.wallets` (P3 owns it; P5 extends it additively) and `journal.account_tag`
- [ ] Command handlers in `crates/mt-api/src/commands/wallet.rs` (C1 level) + validation
- [ ] `mt_journal::registry` lookup service with effective-dated tag resolution
- [ ] Seed loader CLI `mt-journal registry seed config/journal/accounts.yaml` (issues the commands through `mt-api`)
- [ ] Repo seed `config/journal/accounts.paper.yaml`: the paper/testnet accounts the stack already uses (from the P2 venue config), tagged `trading`, loaded with source `seed`, idempotent, never overwriting your edits
- [ ] Tests; docs

## Verification

### Tests

- Unit: tag resolution on boundary dates (tag effective 2027-01-15 applies to events with local date ≥ 2027-01-15).
- Integration: `wallet.register` via mt-api writes `audit.command` and the registry row; C1 confirm enforced.
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
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`ops.wallets` created here per 17 §B (P3-B003); Accounts page split to P3-T056 (P3-B011); explicit P0 depends_on; tools/services filled)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (commands in `mt-api`; `mt-journal registry seed` CLI; agent-seeded paper/testnet accounts so recon never waits for P3-T042)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Python boundary named (`mt_ledger_import` only))
