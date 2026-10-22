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
depends_on: [P0-T009]
requirements: [R1.12, R1.11]
roadmap_todos: [T1.02]
modules: [M16]
dashboards: [D07]
tools: [sops]
mcp: []
env: []
services: [binance-testnet, bybit-testnet, oanda-practice, ig-demo, alpaca-paper, ibkr-paper]
branch: p1/P1-T002-read-only-recon-keys
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
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

# P1-T002 · Create read-only keys on practice and testnet accounts

## Goal / expected outcome

Read-only API keys exist on the Binance and Bybit testnets (IP-allow-listed); the OANDA practice, IG demo, Alpaca paper and (if you use it) IBKR paper credentials are confirmed (normal credentials, no money at risk); all of them sit in the sops secrets file outside the repo, so the late live checks can run: P1-T073 (connectors and fee tiers) and P1-T074 (reconciliation). The builds never need them.

## Context & references

- Roadmap: requirements [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Security: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (scopes, IP allow-list, sub-accounts) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (secrets)
- Accounts were opened in P0 (T0.09: OANDA practice, IG demo, Alpaca paper, IBKR paper, Binance + Bybit testnets)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B008 (practice/paper accounts use their normal credentials; read-only keys where the testnet offers them; live accounts later use read-only keys where offered, otherwise trade-only)
- Cross-phase prerequisites (depends_on): P0-T009 (practice/testnet accounts, your T0.09)

## Requirements

- Binance testnet and Bybit testnet: create API keys with **read only** permission, IP-allow-listed to the host's current public IP (the static exit node replaces it in P7, [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)), no trading, no withdrawals; that IP also becomes `expected_ips` for the egress check (P1-T071)
- OANDA practice: generate a personal access token on the practice account (fxTrade Practice → Manage API Access); normal credentials, no money at risk
- IG demo: API key + demo username/password (normal credentials)
- Alpaca paper: paper key ID/secret; IBKR paper (only if you use IBKR): paper username/password for the `ib-gateway` login (P1-T070); no live-account credentials
- Every value goes into the sops file **outside the repo** (`sops ~/.config/mastertrader/secrets.sops.yaml`, [07 §2](../../../docs/07-security-notes.md#2-secrets)) under these names: `BINANCE_TESTNET_READ_KEY`, `BINANCE_TESTNET_READ_SECRET`, `BYBIT_TESTNET_READ_KEY`, `BYBIT_TESTNET_READ_SECRET`, `OANDA_PRACTICE_TOKEN`, `OANDA_PRACTICE_ACCOUNT_ID`, `IG_DEMO_API_KEY`, `IG_DEMO_USERNAME`, `IG_DEMO_PASSWORD`, `ALPACA_PAPER_KEY_ID`, `ALPACA_PAPER_SECRET_KEY`, and if used `IBKR_PAPER_USERNAME`, `IBKR_PAPER_PASSWORD`; record each key's creation date (rotation alert at 90 days, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)). **Never** chat, issues, git or this file
- The agent's GET-only client allow-list stays as a second safeguard for the full-scope practice credentials (P1-T041/T042)

## ToDo

- [ ] For each testnet/practice venue, create the narrowest key available and turn on its IP allow-list
- [ ] Run `sops ~/.config/mastertrader/secrets.sops.yaml` and add the values under the names above, with creation dates
- [ ] Tell the agent which venues are done (names only, no values)
- [ ] Run `./kanban preflight P1-T073 P1-T074` and confirm no key name is reported missing
- [ ] Record in the progress log which venues use read-only keys (Binance/Bybit testnets) and which use normal practice credentials

## Verification

### Tests

- Agent check: `./kanban preflight P1-T073 P1-T074` passes; authentication itself is proven in P1-T073/P1-T074 (never by showing values)

### Scenarios

- Given a Binance testnet read-only key, when the recon job calls a private order endpoint, then the venue rejects it and the client never sent it (GET-only allow-list)
- Given a missing secret, when recon starts, then it reports `credentials_missing` for that venue in D07 and does not crash the others

### Stress / failure injection

- n/a: account setup

## Acceptance criteria

- [ ] Every practice/testnet venue used in P1 has credentials in the sops file (verified by preflight, not by showing values)
- [ ] Binance and Bybit testnet keys are read-only and IP-locked

## Exceptions & edge cases

- If a venue's testnet key expires (Binance testnet keys are periodically reset), recon flags `auth_failed` and you regenerate it
- IBKR paper needs the `ib-gateway` container (P1-T070); skip IBKR entirely if you don't use it

## Cardinal rules (do NOT)

- Do NOT create keys on live (real-money) accounts for this task
- Do NOT enable withdrawal or transfer permissions on any key
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.02 once every task traced to it in PHASE.md is done; note P1-T002 next to it.
- `docs/07-security-notes.md` §3: note which venues only offer full-scope practice tokens and how the client compensates

## Branch & PR

- Branch: `p1/P1-T002-read-only-recon-keys`
- PR title: `P1-T002: Create read-only keys on practice and testnet accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T1.02 reworded: read-only keys on Binance/Bybit testnets, normal credentials for practice/paper (P1-B008); sops file outside repo with key names; live use moved to P1-T073/P1-T074; dep P0-T009)
