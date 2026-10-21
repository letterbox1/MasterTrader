---
id: P5-T028
kind: task
title: Sweep scheduler, burner refills and kill-switch sweep/freeze
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T013, P5-T020, P5-T022, P5-T012]
requirements: [R5.07, R5.N2]
roadmap_todos: [T5.24]
modules: [M22, M11, M4]
dashboards: [D18, D12]
branch: p5/P5-T028-sweeps-kill-switch-freeze
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T028 · Sweep scheduler, burner refills and kill-switch sweep/freeze

## Goal / expected outcome

A scheduler sweeps hot/burner/identity balances above their float to the **vault address** (allow-listed destination), refills burners to their fixed float, and on kill switch ON immediately freezes auto-claims and treasury moves while sweeping hot balances to the vault (14 §5 rung 6).

## Context & references

- Roadmap: [R5.07](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), [R5.N2](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.24 · drill P5-T058
- [13 §1 rules](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) · [14 §5 ladder rung 6](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Kill vs freeze semantics conflict → P5-B007

## Requirements

- Schedule: daily at 02:00 AEST plus event-driven after each claim; sweep amount = balance − float − gas reserve, only if ≥ min sweep value and the cost gate allows (defensive bypass only for kill sweeps).
- Destination: only the vault address registered with role `vault` and in the custody config allow-list; any other destination refused by the signer.
- Tokens: native + allow-listed tokens; claimed tokens subject to the disposal rule are swept after the disposal leg settles or after 24 h.
- Burner refill: from hot float to burner float only; never more.
- Kill ON (KV `kill`): airdrop-exec stops accepting new work within 1 s; queued claims cancelled with reason; kill sweep runs for hot/identity/burner; results in `ops.sweep_run` and a Telegram summary. Kill OFF is C3 and does not auto-resume claims until re-armed.
- `wallet.sweep` (C2) manual command from D12/D18.

## ToDo

- [ ] Implement `packages/mt_treasury/sweeps/` scheduler, planner (amounts, gas reserve), intent producer.
- [ ] Kill subscriber in airdrop-exec and sweeps; freeze flag consulted by executor and signer.
- [ ] `wallet.sweep` command handler; `ops.sweep_run` writes; Telegram summary.
- [ ] Tests on Anvil + local validator; doc sync.

## Verification

### Tests
- Integration (Anvil): hot wallet with float + 0.5 ETH → sweep sends 0.5 ETH − gas to the vault; ledger + `internal` journal event.
- Integration: kill ON → in-flight claim cancelled, new claim refused within 1 s, sweep executed.
- Unit: sweep planner never leaves balance below gas reserve; never targets non-vault.

### Scenarios
- Given the burner holds 3× its float after a refund, then the next sweep moves the excess to the vault.
- Given kill ON while gas is spiking, then kill sweeps still run (defensive bypass) and are budget-logged.

### Stress / failure injection
- Kill ON with 20 queued claims and RPC latency 2 s injected: freeze < 1 s, sweeps complete or retry with backoff, no claim signed after the kill timestamp (ledger check).

## Acceptance criteria

- [ ] Scheduled sweeps to vault working on EVM and Solana
- [ ] Burner refills capped at float
- [ ] Kill freezes claims < 1 s and sweeps hot balances
- [ ] No sweep to any non-vault destination possible

## Exceptions & edge cases

- Vault address not registered/verified → sweeps refuse and alert (never fall back to another address).
- Token with transfer tax/frozen account: sweep fails → task, no retry storm.

## Cardinal rules (do NOT)

- Do NOT allow any outflow from the vault (manual, offline-signed, outside the system).
- Do NOT make kill OFF resume claims automatically.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §1: sweep schedule and kill-sweep semantics.
- `docs/02-v1-architecture.md` F6: kill also sweeps hot balances.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.24 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T028-sweeps-kill-switch-freeze`
- PR title: `P5-T028: Sweep scheduler, burner refills and kill-switch sweep/freeze`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
