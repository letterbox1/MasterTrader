---
id: P1-T002
kind: task
title: Create read-only keys on practice and testnet accounts
phase: 1
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R1.12, R1.11]
roadmap_todos: [T1.02]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T002-read-only-recon-keys
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T002 · Create read-only keys on practice and testnet accounts

## Goal / expected outcome

Read-only (or the narrowest available) API credentials exist for every practice/testnet account and sit in the sops secrets file, so reconciliation (P1-T041/T042) and fee-tier reads (P1-T038) can run.

## Context & references

- Roadmap: requirements [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Security: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (scopes, IP allow-list, sub-accounts) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (secrets)
- Accounts were opened in P0 (T0.09: OANDA practice, IG demo, Alpaca paper, IBKR paper, Binance + Bybit testnets)
- Known gap: OANDA/IG/Alpaca/IBKR paper have no true read-only key (P1-B008)

## Requirements

- Binance testnet and Bybit testnet: create API keys with **read only** permission, IP allow-listed to the server's egress IP, no trading, no withdrawals
- OANDA practice: generate a personal access token on the practice account (fxTrade Practice → Manage API Access); note it is not scope-limited
- IG demo: API key + demo username/password; note it is not scope-limited
- Alpaca paper: paper key ID/secret; IBKR paper: paper username for IB Gateway login (no live account credentials)
- Every value goes into the sops secrets file (`secrets/mastertrader.sops.yaml`, keys under `venues.<venue>.readonly.*`), **never** chat, issues or git

## ToDo

- [ ] For each testnet/practice venue, create the narrowest key available and turn on its IP allow-list
- [ ] Run `sops secrets/mastertrader.sops.yaml` and add the values under `venues.<venue>.readonly.*`
- [ ] Tell the agent which venues are done (names only, no values)
- [ ] Run `uv run mt-monitor recon --dry-run --venue <venue>` (after P1-T041) and confirm it authenticates
- [ ] Record in the progress log which venues have scope-limited keys and which don't

## Verification

### Tests

- Agent check: the recon dry-run authenticates and a test that tries a write call with these credentials is refused by the client allow-list (P1-T041)

### Scenarios

- Given a Binance testnet read-only key, when the recon job calls a private order endpoint, then the venue rejects it and the client never sent it (GET-only allow-list)
- Given a missing secret, when recon starts, then it reports `credentials_missing` for that venue in D07 and does not crash the others

### Stress / failure injection

- n/a: account setup

## Acceptance criteria

- [ ] Every practice/testnet venue used in P1 has credentials in the sops file (verified by the dry-run, not by showing values)
- [ ] Binance and Bybit testnet keys are read-only and IP-locked

## Exceptions & edge cases

- If a venue's testnet key expires (Binance testnet keys are periodically reset), recon flags `auth_failed` and you regenerate it
- IBKR paper requires IB Gateway with a login; see P1-B013 before relying on it

## Cardinal rules (do NOT)

- Do NOT create keys on live (real-money) accounts for this task
- Do NOT enable withdrawal or transfer permissions on any key
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use keys with withdrawal rights or without an IP allow-list; practice/testnet/paper only, no live money before the P7 gates.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.02 once every task traced to it in PHASE.md is done; note P1-T002 next to it.
- `docs/07-security-notes.md` §3: note which venues only offer full-scope practice tokens and how the client compensates

## Branch & PR

- Branch: `p1/P1-T002-read-only-recon-keys`
- PR title: `P1-T002: Create read-only keys on practice and testnet accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
