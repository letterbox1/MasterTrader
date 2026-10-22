---
id: P2-T071
kind: task
title: Testnet/practice end-to-end with your trade-only keys
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T001, P2-T057, P2-T045, P2-T056, P2-T072, P2-T073]
requirements: [R2.30, R2.N3, R2.31]
roadmap_todos: [T2.72]
modules: [M12, M11]
dashboards: [D05, D06]
tools: [uv, docker, sops]
mcp: []
env: [BINANCE_TESTNET_TRADE_KEY, BINANCE_TESTNET_TRADE_SECRET, BINANCE_TESTNET_DEADMAN_KEY, BINANCE_TESTNET_DEADMAN_SECRET, ALPACA_PAPER_KEY_ID, ALPACA_PAPER_SECRET_KEY, OANDA_PRACTICE_TOKEN, OANDA_PRACTICE_ACCOUNT_ID, IG_DEMO_API_KEY, IG_DEMO_USERNAME, IG_DEMO_PASSWORD]
services: [binance-testnet, alpaca-paper, oanda-practice, ig-demo, nats, postgres]
branch: p2/P2-T071-verify-testnet-e2e-with-your-keys
pr: ""
doc_sync: [docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T071 · Testnet/practice end-to-end with your trade-only keys

## Goal / expected outcome

With your trade-only, IP-locked, no-withdrawal testnet/practice keys from P2-T001, the keyless-built engine is proven live: one order per venue passes M11, fills (or rests and cancels), lands in `audit.order`/`audit.fill` and reconciles; the key audit passes on every real key; the conformance suite and the STP audit pass against the real endpoints; and the kill and dead-man drills pass once on each venue (the 'safety drills on the bot's venue' gate). This is the late keyed check of the 'build first, keys last' split of T2.25.

## Context & references

- Roadmap: [R2.30, R2.N3, R2.31](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.72 (split from T2.25, which keeps the keyless build)
- Decisions: [17 §E 'build first, keys last'](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) · [16 §3.1 dead-man layers](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) · [16 §2.4 safety-drills gate](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) · [07 §3 keys](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [17 §D P2-B006](../../../docs/17-decisions-register.md#d-other-decisions) (netting brokers `stp: n/a (netting)`)
- Inputs: your keys (P2-T001, USER); key audit tool (P2-T045); conformance suite with `--live` (P2-T057); `mt audit stp` (P2-T056); `deadman` sidecar (P2-T072); venue timers + resting stops (P2-T073).
- Unblocks: HITL bots on testnet/practice accounts (P2-T066).

## Requirements

- Runs on the host runner only (never a hosted CI runner); secrets are decrypted from the sops file into tmpfs for the engine/deadman containers; the `env` names above are what the run reads; values never appear in logs or this file.
- Key audit (`mt keys audit`) on every P2 key incl. the separate `deadman` keys: trade-only, withdrawals disabled, IP-restricted, one key per mode/account, age recorded.
- Per venue (Binance spot/USD-M testnet, Alpaca paper, OANDA practice, IG demo): one limit order rests then cancels, one small marketable order fills; each passes M11 (decision recorded), carries an explicit STP field or `n/a_netting`, a `{bot}-{engine_epoch}-{seq}` client ID, lands in `audit.order`/`audit.fill`, and the P1 reconciliation matches (positions exact, balances within tolerance, 16 §2.9).
- Conformance suite `--live` green on all four venues (or documented venue limitation).
- STP audit over the live window: 0 orders on STP-capable venues without STP; netting venues `n/a_netting`; one induced self-match on Binance testnet recorded as non-fills.
- Safety drills per venue: kill → all cancels sent < 1 s; `deadman` sidecar cancels at 5 s and applies `on_system_failure` at 10 s when the engine is stopped; venue cancel-after timer observed where supported; resting venue stop present on every open position.

## ToDo

- [ ] Confirm P2-T001 is done and the keys are in the sops file (names only in this log)
- [ ] Run `mt keys audit` on all P2 keys; record the masked results
- [ ] Run the per-venue order round trip and reconciliation; record audit IDs
- [ ] Run the conformance suite with `--live` on the host runner
- [ ] Run `mt audit stp --since <window>` incl. one induced self-match on Binance testnet
- [ ] Run the kill + dead-man drill once per venue; record timings
- [ ] Replace cassettes/fixtures where the live behaviour differs (no secrets in fixtures)
- [ ] Record results (numbers, run IDs) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The live runs above (evidence: audit IDs, recon report IDs, drill timings, masked key-audit table).

### Scenarios
- Given your OANDA practice credentials, when the engine sends a small marketable order through M11, then it fills, `audit.order` shows `stp_mode = n/a_netting` and the recon job matches the position.
- Given a key with withdrawals enabled (if found), when the audit runs, then that account is disabled, a critical alert names the venue/mode, and P2-T001 is reopened for you.
- Given the engine is stopped with an open testnet position, when 10 s pass, then the `deadman` sidecar has cancelled orders at 5 s and flattened at 10 s (default `flatten`).

### Stress / failure injection
- Disconnect the host network for 30 s mid-order on Binance testnet: orders become `unknown`, the venue cancel-after timer (if supported) cancels resting orders, and reconciliation on reconnect shows no duplicate.

## Acceptance criteria

- [ ] One order per venue passed M11, filled or cancelled, audited and reconciled
- [ ] Key audit green on every key incl. `deadman` keys (masked table recorded)
- [ ] Conformance `--live` and STP audit green (or limitations documented)
- [ ] Kill and dead-man drills pass on every venue

## Exceptions & edge cases

- A venue's testnet is down or reset: record it, retry later; don't mark this done on partial venues without a written limitation.
- IG demo has no sub-accounts: separate demo logins per mode (P2-T001 exception).
- No exit node yet (P7): keys are locked to the host's current public IP; the egress check (P1-T071) verifies that IP/country.

## Cardinal rules (do NOT)

- Do NOT use live (real-money) accounts or keys.
- Do NOT run this on a hosted CI runner or store keys in CI secrets.
- Do NOT print key material; masked metadata only.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` M12: venue capability matrix confirmed live.
- `docs/07-security-notes.md` §3: key-audit results summary (masked) and the deadman keys.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.72 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T071-verify-testnet-e2e-with-your-keys`
- PR title: `P2-T071: Testnet/practice end-to-end with your trade-only keys`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T071` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.72: R2.30, R2.N3, R2.31)
