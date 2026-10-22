---
id: P6-T038
kind: task
title: Hold-and-earn execution through M11, the cost gate and the signer
phase: 6
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T033, P6-T036, P6-T037, P5-T013, P5-T016, P5-T020, P5-T026, P2-T017]
requirements: [R6.20, R6.24]
roadmap_todos: [T6.28]
modules: [M22, M11, M12, M16]
dashboards: [D18]
tools: [git, uv, python>=3.12, docker, anvil, solana-test-validator]
mcp: []
env: []
services: [signer, anvil, postgres, nats]
branch: p6/P6-T038-earn-execution-path
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T038 · Hold-and-earn execution through M11, the cost gate and the signer

## Goal / expected outcome

`treasury.earn.enter` / `treasury.earn.exit` and approved proposals execute as `treasury.intent` → M11 policy check → on-chain cost gate (allow/wait/reject, logged) → signer (hot tier only) or an approval task (warm tier); depeg and exploit monitors trigger auto-reduce/withdraw; positions, rewards and journal events are recorded.

## Context & references

- Roadmap: [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (automation column per type; warm actions need approval) · [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) (gate) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) (depeg > 50 bps auto-reduce; exploit auto-withdraw if allow-listed for auto) · [13 §2](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) (intents only) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`treasury.intent`/`result`/`depeg`) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (C2)
- UI: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) (cost gate result before confirmation; kill freezes entries, exits stay at C2)
- Cross-phase: P5-T013 (signer core; intents only from the policy service, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) P5-B003), P5-T016 (simulation), P5-T020 (`mt_onchain.costgate`, P5-B002), P5-T026 (depeg/exploit monitors), P2-T017 (M11)
- Decisions: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P5-B008 vault/warm watch-only; P5-B009 automated depeg reduce only once the treasury exists; P5-B007 kill freezes new treasury/earn moves) · defaults [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)
- Exit: [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 4
- Depends on (this phase): P6-T033, P6-T036, P6-T037

## Requirements

- Intent builder per protocol type (lending deposit/withdraw, LST stake/unstake, PT buy/redeem, HLP deposit/withdraw with 4-day lock awareness) using pinned, allow-listed contract addresses/IDLs.
- M11: policy caps, reserve band, kill switch, venue registry, per-tx and 24h caps; deny by default.
- Cost gate (`mt_onchain.costgate`): expected benefit (net yield × hold) vs all-in cost × margin (default 2×, 16 §2.7); `wait` honours gas windows (7-day 30th percentile unless deadline < 48 h).
- Signing only via the policy service → signer (hot tier, simulation mandatory). Vault and warm are watch-only: the system may prepare an unsigned transaction (QR/WalletConnect) plus a D13 task for you to sign in your own wallet; never sign from the UI.
- Monitors: depeg beyond the threshold (default 50 bps, 16 §2.7) → auto-reduce exposure in that stablecoin (automated reduce starts here, with the treasury; before P6 it's alert + task only; exits are protective, never wait for approval); exploit/oracle/TVL drop → auto-withdraw if `auto_ok`, else urgent task.
- `treasury.position` updates, rewards ledger, journal events (staking/lending income classification), `/treasury`, `/treasury/earn`, WS `treasury`.

## ToDo

- [ ] Intent builders + protocol adapters (Aave/Spark, Kamino, Jito/Marinade, Lido, Pendle, HLP).
- [ ] M11 treasury checks.
- [ ] Cost gate integration + gas windows.
- [ ] Monitor handlers (depeg/exploit) with protective exits.
- [ ] Positions, rewards ledger, journal events, API + WS.
- [ ] Paper/fork mode: Anvil fork and Solana local validator for tests.
- [ ] Tests; docs.

## Verification

### Tests
- Integration (Anvil fork): Aave USDC deposit/withdraw intent passes M11 + gate + signer simulation; journal event written.
- Unit: gate decisions (allow/wait/reject) for fixture costs; HLP lock handling.
- Monitor tests: injected depeg → exit intent bypasses approval but still passes M11 hard checks.

### Scenarios
- Given an uneconomic $50 deposit with $12 round-trip gas, then the gate rejects with numbers shown (P6-T060).
- Given kill switch ON, then `earn.enter` is refused and `earn.exit` is allowed at C2.
- Given a warm-wallet proposal, then no transaction is signed and a D13 task appears with steps.

### Stress / failure injection
- Signer unavailable during a depeg: exit retried with backoff; urgent alert after 2 failures; no duplicate exits (idempotent intent ids).
- RPC failover mid-transaction: status reconciled from chain before retry.

## Acceptance criteria

- [ ] Every move passes M11 + cost gate (audit shows both).
- [ ] Depeg auto-reduce works on fork.
- [ ] No signing path for warm/vault.

## Exceptions & edge cases

- Gas spike → `wait` with expiry; protective exits use priority fees within budget.
- Partial fills / reverts recorded; Flashbots Protect on L1 (no fee on revert).

## Cardinal rules (do NOT)

- Do NOT sign anything outside the signer, and never from warm/vault keys.
- Do NOT bypass the cost gate for non-protective moves.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4/§6/§7: execution path and monitor actions.
- `docs/02-v1-architecture.md` §6/§7: `treasury.*` payloads and `/treasury/earn`.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T038-earn-execution-path`
- PR title: `P6-T038: Hold-and-earn execution through M11, the cost gate and the signer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (signing via policy service, vault/warm watch-only, depeg reduce only from the treasury, cost-gate 2× (17 §B, 16 §2.7); fork/testnet only, no keys; cross-phase deps P5-T013/T016/T020/T026/P2-T017; run fields)
