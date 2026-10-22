---
id: P5-T012
kind: task
title: Custody tiers and wallet/signer/gas limits config (signing disabled until you confirm)
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P2-T010, P2-T019]
requirements: [R5.01, R5.07, R5.24]
roadmap_todos: [T5.20, T5.24]
modules: [M22]
dashboards: [D18]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T012-custody-tier-config
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T012 · Custody tiers and wallet/signer/gas limits config (signing disabled until you confirm)

## Goal / expected outcome

`mt_treasury.custody` defines the six custody tiers with their allowed operations, and holds the wallet, signer and gas limits of [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) as **configurable defaults** in a versioned limits store (seeded from `config/custody.yaml`). Vault and warm are watch-only. `signing_enabled` starts **false**; only your first confirmation (P5-T065, C3) turns it on; later tightening is immediate and loosening is C3. Signer, sweeps, cost gate and UI read limits only from here.

## Context & references

- Roadmap: [R5.01](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.07 · ToDos T5.20, T5.24
- Tiers: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) (vault, Hyperliquid master if approved, warm, hot, airdrop identity per chain, burner)
- Defaults ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13); decision P5-B001, [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)): hot float ≤ A$500 per chain; identity ≤ A$300 per chain; burner ≤ A$50; signer A$250 per transaction and A$1,000 per rolling 24 h per wallet; gas budgets airdrops A$20/day and DEX trading A$50/day (alert 80%, stop 100%); cost-gate margin 2×; gas window 7-day p30 unless the deadline is < 48 h; EV hurdle 5% p.a.
- Watch-only: the system never holds vault/warm keys; it may only prepare unsigned transactions for you to sign in your own wallet (decision P5-B008, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); Hyperliquid approval status → 12 §1
- Kill sweep: from P5 the kill switch sweeps hot trading balances to the vault address (default on, configurable; decision P5-B007)
- Change control (tighten immediate, loosen C3 with the 15 min cool-down): P2-T019 on the P2-T010 policy store; layers and strictest-wins in [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)

## Requirements

- Per tier: `signing` ∈ none(watch-only)/manual_device/signer_auto; `per_tx_cap` and `rolling_24h_cap` (AUD, USD shown), `float`, `daily_gas_budget` per module (airdrops, DEX trading; sweeps and revokes count against the module that caused them), `allowed_ops` (claim, revoke, sweep_out, genuine_use), `sweep_destination` (vault address id). Global: cost-gate margin, gas-window percentile and deadline, EV hurdle, `kill_sweep_enabled` (default true).
- Vault/warm/HL master: `signing=none` in the system; any intent naming them is refused.
- Identity: max one per chain (enforced); burner: refill-to-float only, never receives sweeps-in except refills.
- Limits versioned as new rows (WORM history) through `risk.policy.update`; tighten = C1 immediate, loosen = C3; L0 hard ceilings (e.g. max per-transaction signer value) come from the hard-ceilings section of the bot strategy settings and can't be exceeded ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance), [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)); save-time validation rejects inconsistent sets (per-tx cap > 24 h cap, negative floats).
- Defaults ship as the 16 §2.7 values and only prefill the D18 form; `signing_enabled = false` until you confirm them (P5-T065). While false the signer refuses every intent with `limits_unconfirmed` (protective sweeps/revokes are offered as manual steps).

## ToDo

- [ ] Write `packages/mt_treasury/custody/model.py` (msgspec) and the seed loader for `config/custody.yaml` (16 §2.7 defaults, no secrets).
- [ ] Implement tighten/loosen diff classification and the first-confirmation (C3) flow that sets `signing_enabled`, wired to the P2 change-control service.
- [ ] Expose `GET /wallets/custody` for D18 (tiers, limits, usage).
- [ ] Unit + property tests; update 13 §1 with the config file reference.

## Verification

### Tests
- Unit: loosening `per_tx_cap` classified C3; tightening applied immediately.
- Property: for any config, vault/warm tiers never have `signing=signer_auto`.
- Unit: two identity wallets on one chain → validation error.

### Scenarios
- Given the limits are unconfirmed (`signing_enabled = false`), when the signer is asked to sign, then it refuses with `limits_unconfirmed`.
- Given a hard ceiling of A$X per tx, when a C3 change asks for more, then it is rejected outright.

### Stress / failure injection
- n/a: configuration model (signer enforcement is stressed in P5-T013/T062)

## Acceptance criteria

- [ ] Six tiers modelled with limits and allowed ops
- [ ] Loosen = C3 enforced
- [ ] Watch-only tiers cannot sign
- [ ] Signing blocked until you confirm the limits (P5-T065)
- [ ] No limit hard-coded: every number comes from the limits store with its 16 §2.7 default

## Exceptions & edge cases

- HL master tier present but disabled unless the venue registry marks Hyperliquid allowed.
- Config file missing/corrupt at start → services start in `frozen` (no signing) and alert.

## Cardinal rules (do NOT)

- Do NOT hard-code caps in signer or executor code; read them from custody config.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §1: reference the limits store and the `config/custody.yaml` seed (the defaults stay in 16 §2.7).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20, T5.24 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T012-custody-tier-config`
- PR title: `P5-T012: Custody tiers and wallet/signer/gas limits config (signing disabled until you confirm)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (16 §2.7 defaults as configuration; signing disabled until P5-T065 confirms; L0 from strategy settings per 17 §E; kill sweep default on; P2 change-control deps)
