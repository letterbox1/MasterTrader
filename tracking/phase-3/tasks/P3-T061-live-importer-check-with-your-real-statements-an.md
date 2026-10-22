---
id: P3-T061
kind: task
title: Live importer check with your real statements and read-only practice keys
phase: 3
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T003, P3-T014, P3-T015, P3-T016, P3-T021, P1-T002]
requirements: [R3.01, R3.05]
roadmap_todos: [T3.20, T3.23]
modules: [M18]
dashboards: [D14, D15]
tools: [git, uv, docker]
mcp: []
env: [BINANCE_TESTNET_READONLY_KEY, BINANCE_TESTNET_READONLY_SECRET, BYBIT_TESTNET_READONLY_KEY, BYBIT_TESTNET_READONLY_SECRET, OANDA_PRACTICE_TOKEN, IG_DEMO_API_KEY]
services: [postgres, journal, Binance testnet, Bybit testnet, OANDA practice, IG demo]
branch: p3/P3-T061-live-importer-check-with-your-real-statements-an
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T061 · Live importer check with your real statements and read-only practice keys

## Goal / expected outcome

The importers built against recorded and sample files (P3-T014/T015/T016/T021) are proven on real inputs: your exported historical statements (P3-T003) import into opening lots that reconcile to each statement's closing positions, and the ccxt-ledger and OANDA/IG adapters pull live from testnet/practice accounts with read-only keys. This is the "keys last" check; no build task needs these inputs.

## Context & references

- Roadmap: [R3.01, R3.05, T3.20, T3.23](../../../docs/roadmap/phase-3-journal-and-tax.md) · inputs from USER T3.03 (P3-T003)
- Build first, keys last: [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) · [planning brief](../../briefs/PLANNING_BRIEF.md)
- Cross-phase prerequisite (depends_on): P1-T002 (read-only keys on practice and testnet accounts, stored in the sops file)
- Related: P3-T003 (your exports), P3-T021 (opening lots import), P3-T014/T015/T016 (adapters), P3-T042 (accounts registered)

## Requirements

- Statements: run the `historical` import over `/srv/mastertrader/journal/inbox/` (P3-T003 drop); every file parses (or is quarantined with a reason); per account computed holdings at statement end = closing positions (qty exact; cash within the configured tolerance, [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)); import report stored with file hashes; gaps flagged `cost_base_estimated`.
- Live ledgers: one scheduled `journal-ccxt-ledger` run per configured testnet account and one OANDA/IG pull with the read-only keys named in `env`; at least one funding payment (perp testnet) and one financing event (practice CFD) journalled with AUD/USD/native values.
- IBKR Flex Web Service: only if you created `IBKR_FLEX_TOKEN` in P3-T003 (optional; otherwise file import only).
- Any parser drift found here becomes a bug against the adapter (`--found-in P3-T061`), and the scrubbed real sample is added to that adapter's golden files (no personal data).

## ToDo

- [ ] Confirm the inbox drop is complete (P3-T003 progress log) and accounts are registered (P3-T042)
- [ ] Run the historical import; review the import report; resolve or acknowledge each mismatch
- [ ] Run the live ledger and practice pulls; check D14 shows the events
- [ ] Record results (counts, mismatches, file hashes; no personal data) in the progress log; file bugs for drift

## Verification

### Tests
- Import report: zero unparsed rows (or quarantined with reason); reconciliation per account `ok` or acknowledged.
- Live pulls: events present with `source = ccxt_ledger` / `broker_stmt`; no duplicates against fill events.

### Scenarios
- Given a lot bought years ago in your IBKR statement, when imported, then D15 Lots shows its original acquisition date and cost base.
- Given a missing year in your exports, when imported, then affected lots are `cost_base_estimated` with a D15 warning.

### Stress / failure injection
- Re-run the full import → no new rows (idempotent).

## Acceptance criteria

- [ ] Every account with statements reconciles or has an acknowledged mismatch
- [ ] Live ledger and practice pulls journalled with three currencies
- [ ] No keys, statements or personal data in git, logs or chat

## Exceptions & edge cases

- A venue whose read-only key isn't scope-limited (OANDA/IG practice tokens) is used for reads only; noted in the progress log.
- Real statement contains a format variant the samples lacked → quarantine + bug, never a partial import.

## Cardinal rules (do NOT)

- Do NOT commit statements, keys or scrubbed-but-identifiable data; scrub before adding golden files.
- Do NOT use keys with trade or withdrawal permission for these reads.
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20, T3.23 once every item mapped to them is done.

## Branch & PR

- Branch: `p3/P3-T061-live-importer-check-with-your-real-statements-an`
- PR title: `P3-T061: Live importer check with your real statements and read-only practice keys`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T061` run

## Progress log

- 2026-10-22 00:00 · aligner · created (build first, keys last: live checks split out of P3-T014/T015/T016/T021)
