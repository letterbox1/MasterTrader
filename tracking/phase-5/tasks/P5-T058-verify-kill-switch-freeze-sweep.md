---
id: P5-T058
kind: task
title: Kill switch drill: auto-claims frozen and hot balances swept
phase: 5
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T028, P5-T044, P5-T065]
requirements: [R5.N2, R5.07]
roadmap_todos: [T5.64]
modules: [M22, M4, M11]
dashboards: [D12, D18]
tools: [uv, anvil, solana-test-validator]
mcp: []
env: []
services: [telegram, anvil, sepolia-rpc]
branch: p5/P5-T058-verify-kill-switch-freeze-sweep
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T058 · Kill switch drill: auto-claims frozen and hot balances swept

## Goal / expected outcome

A drill (testnet or Anvil with real signer) shows: `/kill` from Telegram freezes `airdrop-exec` within 1 s (queued claims cancelled, none signed after the kill timestamp), treasury moves are frozen, protective revokes still work, and hot trading balances above the gas reserve sweep to the vault address (default on, P5-B007); turning kill OFF needs C3 and does not auto-resume claims.

## Context & references

- Roadmap: ToDo T5.64 → [R5.N2](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) ("Drill"), R5.07 ("Sweep test")
- [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [14 §5 rung 6](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · P2 kill drill (T2.61)

## Requirements

- Setup: testnet keys created in the drill's own setup (faucet funds, C3 approved by you; no real money), signing enabled with the limits confirmed in P5-T065; 5 queued claims, 1 in simulation, balances on the hot, identity and burner test wallets.
- Assertions: freeze latency < 1 s (ledger/exec_log timestamps); 0 signatures for claims after kill; hot-wallet sweep txs confirmed to the vault (identity/burner frozen, not kill-swept); D12/D18 red banners; Telegram summary.
- Kill OFF via C3; claims remain paused until re-armed explicitly.

## ToDo

- [ ] Write the drill script `tests/drills/kill_freeze_sweep.py` (also runnable on Anvil in CI).
- [ ] Run once on testnet with you triggering `/kill` from your phone; record timings.
- [ ] File bugs for any miss.

## Verification

### Tests
- Drill script with timing assertions (CI on Anvil; manual on testnet).

### Scenarios
- Given kill ON during a gas spike, then sweeps still go out (defensive bypass) and are budget-logged.
- Given `kill_sweep_enabled = false` (your setting), when kill turns ON, then claims freeze, no sweep runs, and the Telegram summary says so.

### Stress / failure injection
- Trigger kill while RPC latency is 2 s and one provider is down: freeze still < 1 s; sweeps retry via fallback.

## Acceptance criteria

- [ ] Freeze < 1 s with zero post-kill claim signatures
- [ ] Hot balances swept to the vault
- [ ] Kill OFF requires C3; no auto-resume

## Exceptions & edge cases

- NATS down at kill time: Telegram `/kill` fallback path (P2) still reaches the signer's fail-closed rule.

## Cardinal rules (do NOT)

- Do NOT pre-stage the drill in a way that hides latency (no warm caches beyond normal).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking T5.64.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.64 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T058-verify-kill-switch-freeze-sweep`
- PR title: `P5-T058: Kill switch drill: auto-claims frozen and hot balances swept`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (kill sweeps hot trading balances to the vault per P5-B007, configurable; testnet keys in setup instead of P5-T004 real funds; needs P5-T065)
