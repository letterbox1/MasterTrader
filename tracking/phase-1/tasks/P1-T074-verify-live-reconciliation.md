---
id: P1-T074
kind: task
title: Live reconciliation on practice and testnet accounts
phase: 1
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T009, P1-T002, P1-T041, P1-T042]
requirements: [R1.12]
roadmap_todos: [T1.67]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker, sops]
mcp: []
env: [BINANCE_TESTNET_READ_KEY, BINANCE_TESTNET_READ_SECRET, BYBIT_TESTNET_READ_KEY, BYBIT_TESTNET_READ_SECRET, OANDA_PRACTICE_TOKEN, OANDA_PRACTICE_ACCOUNT_ID, IG_DEMO_API_KEY, IG_DEMO_USERNAME, IG_DEMO_PASSWORD, ALPACA_PAPER_KEY_ID, ALPACA_PAPER_SECRET_KEY]
services: [nats, postgres, binance-testnet, bybit-testnet, oanda-practice, ig-demo, alpaca-paper]
branch: p1/P1-T074-verify-live-reconciliation
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T074 · Live reconciliation on practice and testnet accounts

## Goal / expected outcome

With your keys loaded, reconciliation runs against every practice/testnet venue you use at the default cadence (positions and open orders every 60 s, balances every 5 min, full EOD Sydney) and comes back clean; then a deliberately seeded mismatch raises an incident in `audit.recon`, publishes `recon.{venue}` as `unexplained`, and alerts. This is the live half of T1.29 (the build was keyless, against recorded fixtures).

## Context & references

- Roadmap: requirement [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.67](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) (split from T1.29)
- Defaults: [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation) (60 s / 5 min / EOD; positions exact, balances within 0.01% or dust; unexplained after 24 h halts everything) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) reconciliation
- Keys: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B008 (practice/paper accounts use normal credentials; read-only keys where offered)
- IBKR: only when you use it; then P1-T070's `ib-gateway` must be up with `IBKR_PAPER_USERNAME`/`IBKR_PAPER_PASSWORD` in the sops file (not listed in `env` because IBKR is optional)
- Cross-phase prerequisite: P0-T009 (the accounts)
- Depends on (this phase): P1-T002 (credentials), P1-T041 and P1-T042 (keyless recon framework and adapters)
- Run with `sops exec-env ~/.config/mastertrader/secrets.sops.yaml 'make verify-live-recon'`

## Requirements

- Clean run: ≥ 2 h at the default cadence on every configured venue (Binance testnet, Bybit testnet, OANDA practice, IG demo, Alpaca paper; IBKR paper if enabled) with status `matched` on every cycle and one forced EOD run (`data.recon.run --full`)
- Seeded mismatch, per venue class: you (or the agent, with your go-ahead) make a tiny manual change on the practice/testnet account through the **venue's own UI** (e.g. a 1-unit OANDA practice trade, a testnet transfer between spot and futures wallets); the next cycle reports an `unexplained` mismatch row in `audit.recon`, `recon.{venue}` shows it, and `alert.warning.recon` reaches the notifier; you acknowledge and a new baseline row is appended (no edits)
- GET-only allow-list proven live: a deliberate write attempt from the adapter raises before any network call (log shows zero outbound write requests)
- Report under `reports/verify/P1-T074/`: per venue cycles run, matched/unexplained counts, cadence observed, seeded mismatch timeline (change → detection → alert), no credentials or account numbers

## ToDo

- [ ] Run `./kanban preflight P1-T074`; block on a missing key and point at P1-T002
- [ ] Start recon with secrets loaded; run ≥ 2 h clean and one full EOD run
- [ ] Seed one mismatch per venue class via the venue UI and record detection and alert times
- [ ] Acknowledge each mismatch and confirm the clean baseline afterwards
- [ ] Store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box

## Verification

### Tests

- `make verify-live-recon` (pytest marker `live`, outside normal CI) asserts cadence, statuses and WORM rows (`audit.recon` passes its hash-chain check after the run)

### Scenarios

- Given a clean account, when 2 h of cycles run, then every cycle is `matched` and positions/open-order cycles are 60 s apart (± 5 s), balances 5 min
- Given a 1-unit practice trade made in the OANDA web UI, when the next 60 s cycle runs, then an `unexplained` position mismatch is recorded and alerted within one cycle
- Given a testnet balance reset by the venue, when recon runs, then it is flagged `venue_reset` per the runbook, not a silent baseline change

### Stress / failure injection

- Block one venue's host for 10 min mid-run: that venue shows `unreachable` (not mismatch), others continue, and it recovers on the next cycle without a retry storm

## Acceptance criteria

- [ ] Clean recon on every configured practice/testnet venue (IBKR clean or recorded as not used)
- [ ] Each seeded mismatch detected within one cycle, written to `audit.recon`, alerted, and re-baselined by a new row
- [ ] Report stored; no credentials anywhere in it

## Exceptions & edge cases

- In P1 there are no fills or journal events yet, so every mismatch is `unexplained`; the 24 h "halts everything" rule is enforced by M11 from P2 and is only reported here
- Testnet maintenance windows: rerun the affected hour rather than counting it as a failure

## Cardinal rules (do NOT)

- Do NOT place orders from the system; seeded changes are made by hand in the venue's own UI, on practice/testnet accounts only
- Do NOT use live (real-money) accounts or keys; no live money before the P7 gates
- Do NOT UPDATE or DELETE `audit.recon` rows; acknowledgements and new baselines are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many))
- Do NOT print, log or commit credentials ([07 §2](../../../docs/07-security-notes.md#2-secrets))
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get green

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.67; note P1-T074 next to it.
- `docs/03-build-spec.md` M16: note any venue whose API forces a slower cadence than the defaults.

## Branch & PR

- Branch: `p1/P1-T074-verify-live-reconciliation`
- PR title: `P1-T074: Live reconciliation on practice and testnet accounts`
- PR checklist: report stored · no secrets in diff · docs synced · task file ticked · `./kanban done P1-T074` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.67 (docs/16–17 alignment: live reconciliation split from T1.29)
