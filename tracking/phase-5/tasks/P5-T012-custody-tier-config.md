---
id: P5-T012
kind: task
title: Custody tier model and config (limits, floats, destinations)
phase: 5
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009]
requirements: [R5.01, R5.07]
roadmap_todos: [T5.20, T5.24]
modules: [M22]
dashboards: [D18]
branch: p5/P5-T012-custody-tier-config
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T012 · Custody tier model and config (limits, floats, destinations)

## Goal / expected outcome

`mt_treasury.custody` defines the six custody tiers with their limits and allowed operations, loaded from a versioned `config/custody.yaml`; vault and warm are watch-only; changes that loosen limits require C3. Signer, sweeps and UI read limits only from here.

## Context & references

- Roadmap: [R5.01](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.07 · ToDos T5.20, T5.24
- Tiers: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) (vault, Hyperliquid master if approved, warm, hot, airdrop identity per chain, burner)
- Numeric defaults gap → P5-B001; Hyperliquid approval status → 12 §1
- Risk change control (tighten instantly, loosen C3): P2 R2.19

## Requirements

- Per tier: `signing` ∈ none(watch-only)/manual_device/signer_auto; `per_tx_cap` and `rolling_24h_cap` (in USD and AUD), `float`, `daily_gas_budget`, `allowed_ops` (claim, revoke, sweep_out, genuine_use), `sweep_destination` (vault address id).
- Vault/warm/HL master: `signing=none` in the system; any intent naming them is refused.
- Identity: max one per chain (enforced); burner: refill-to-float only, never receives sweeps-in except refills.
- Config versioned in `risk.change`-style audit; tighten = C1 immediate, loosen = C3; hard ceilings in a file no API can write (mirrors P2).
- Defaults ship conservative placeholders marked `UNSET_REQUIRES_USER` that block signing until P5-T004 sets them.

## ToDo

- [ ] Write `packages/mt_treasury/custody/model.py` (pydantic/msgspec) and loader for `config/custody.yaml`.
- [ ] Implement tighten/loosen diff classification and wire to the `mt_api` C1/C3 flow.
- [ ] Expose `GET /wallets/custody` for D18 (tiers, limits, usage).
- [ ] Unit + property tests; update 13 §1 with the config file reference.

## Verification

### Tests
- Unit: loosening `per_tx_cap` classified C3; tightening applied immediately.
- Property: for any config, vault/warm tiers never have `signing=signer_auto`.
- Unit: two identity wallets on one chain → validation error.

### Scenarios
- Given caps are `UNSET_REQUIRES_USER`, when the signer is asked to sign, then it refuses with `custody_unset`.
- Given a hard ceiling of A$X per tx, when a C3 change asks for more, then it is rejected outright.

### Stress / failure injection
- n/a: configuration model (signer enforcement is stressed in P5-T013/T062)

## Acceptance criteria

- [ ] Six tiers modelled with limits and allowed ops
- [ ] Loosen = C3 enforced
- [ ] Watch-only tiers cannot sign
- [ ] Signing blocked until user sets limits

## Exceptions & edge cases

- HL master tier present but disabled unless the venue registry marks Hyperliquid allowed.
- Config file missing/corrupt at start → services start in `frozen` (no signing) and alert.

## Cardinal rules (do NOT)

- Do NOT hard-code caps in signer or executor code; read them from custody config.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §1: reference `config/custody.yaml` and the chosen defaults (after P5-B001).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20, T5.24 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T012-custody-tier-config`
- PR title: `P5-T012: Custody tier model and config (limits, floats, destinations)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
