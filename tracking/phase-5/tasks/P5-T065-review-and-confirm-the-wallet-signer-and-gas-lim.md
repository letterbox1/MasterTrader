---
id: P5-T065
kind: task
title: Seed the wallet, signer and gas limits from 16 §2.7 (mainnet signing stays off until P5-T004)
phase: 5
type: BUILD
status: backlog
priority: critical
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T012, P5-T011]
requirements: [R5.24, R5.01, R5.04]
roadmap_todos: [T5.08]
modules: [M22]
dashboards: [D18]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p5/P5-T065-review-and-confirm-the-wallet-signer-and-gas-lim
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-T065 · Seed the wallet, signer and gas limits from 16 §2.7 (mainnet signing stays off until P5-T004)

## Goal / expected outcome

The limits store (P5-T012) holds the wallet, signer and gas limits of [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (floats, per-transaction and rolling 24 h caps, daily gas budgets, cost-gate margin, gas window, EV hurdle), seeded through `mt-api` with source `seed`. With the seed in place, testnet and Anvil work (P5-T056, P5-T058, CI) signs within these caps without waiting for you. **Mainnet signing stays disabled** (`signing_enabled = false`, refusals `limits_unconfirmed`) until you review and confirm the limits through C3 in P5-T004; you also see them once more in the go-live pack (P7-T070).

## Context & references

- Roadmap: [R5.24](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.08
- Defaults: [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (hot float ≤ A$500 per chain, identity ≤ A$300 per chain, burner ≤ A$50, signer A$250 per transaction and A$1,000 per rolling 24 h per wallet, gas budgets airdrops A$20/day and DEX trading A$50/day with alert at 80% and stop at 100%, cost-gate margin 2×, gas window 7-day p30 unless deadline < 48 h, EV hurdle 5% p.a.)
- Rule: "signing stays disabled until you confirm these numbers on first setup" ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13), [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers), [D18 rules](../../../docs/ui/dashboards/D18-wallets-treasury.md)); decision P5-B001 in [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved). The confirmation (C3) is now part of P5-T004, next to key creation; this task only seeds.
- Decision: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19): configurable values are seeded from the doc defaults by an agent; enabling signing still needs your approval (P5-T004).
- Change levels: tighten immediate, loosen C3 ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); C3 = Telegram approve + TOTP + 15 min cool-down ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl))
- Depends on: P5-T012 (`mt-treasury` custody model, limits store and seed loader), P5-T011 (`mt-api` commands)
- Unblocks: P5-T004 (you confirm and create keys), P5-T056 (testnet claim), P5-T058 (kill drill on testnet)

## Requirements

- Seed `config/custody.yaml` (16 §2.7 values, no secrets) into the limits store through `mt-api` with source `seed`, as a new version row (WORM history); idempotent; never overwrites a value you changed.
- The seed **never** sets mainnet `signing_enabled`; it stays false until your C3 confirmation in P5-T004.
- Testnet and Anvil chain ids (`network: testnet | local` in the chain registry) sign within the seeded caps without the mainnet confirmation: no real money is at stake ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)); every other signer check (kill switch, custody tier, allow-lists, caps, hard blocks, simulation) still applies.
- Each value carries `seed_source` (the 16 §2.7 row) so D18 and the go-live pack show where it came from.

## ToDo

- [ ] Run the P5-T012 seed loader through `mt-api` (`wallets.limits.seed`, source `seed`)
- [ ] Doc-parse test: every 16 §2.7 wallet/signer/gas row is present in `config/custody.yaml` with the same value
- [ ] Confirm D18 shows the seeded limits and the banner "Mainnet signing disabled until you confirm limits (P5-T004)"
- [ ] Tests (`cargo test -p mt-treasury`, `supabase test db`); progress log; `./kanban done P5-T065`

## Verification

### Tests
- Seeded values match 16 §2.7; re-running the seed changes nothing; a value you tightened keeps your value after a re-seed.
- After the seed, a mainnet test intent (P5-T013) is refused `limits_unconfirmed`; an Anvil intent within the caps is accepted.

### Scenarios
- Given the seed has run and you have not confirmed, when `airdrop-exec` asks to sign on mainnet, then the signer refuses with `limits_unconfirmed` and the claim becomes a `CLAIM_MANUAL` task.
- Given a seeded per-transaction cap above an L0 hard ceiling (misconfigured defaults file), when the seed runs, then it fails with the reason and nothing is written.

### Stress / failure injection
- n/a: seed data (signer enforcement is tested in P5-T013 and P5-T062)

## Acceptance criteria

- [ ] All 16 §2.7 wallet, signer and gas values seeded with source `seed` as a version row
- [ ] Mainnet `signing_enabled` still false after the seed; testnet/Anvil signing works within the seeded caps

## Exceptions & edge cases

- Kill switch ON: the seed still writes (it is a configuration change, not a signature); signing stays refused while kill is ON.
- If you never confirm in P5-T004, mainnet signing stays off: claims become `CLAIM_MANUAL` tasks and sweeps are listed as manual steps.

## Cardinal rules (do NOT)

- Do NOT set mainnet `signing_enabled` from a seed, a test or any agent path; only your C3 confirmation (P5-T004) does that.
- Do NOT apply loosening (enabling mainnet signing, higher caps, bigger gas budgets) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT hard-code numbers; they come from `config/custody.yaml` (16 §2.7 defaults).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §1: the limits are seeded from 16 §2.7; mainnet signing is enabled by your confirmation in P5-T004; testnet/Anvil sign within the seeded caps.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.08 when this lands.

## Branch & PR

- Branch: `p5/P5-T065-review-and-confirm-the-wallet-signer-and-gas-lim`
- PR title: `P5-T065: Seed the wallet, signer and gas limits from 16 §2.7 (mainnet signing stays off until P5-T004)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T065` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R5.24 / T5.08: signing disabled until you confirm the 16 §2.7 limits)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from a USER task to an agent seed task per 17 §G: limits seeded from 16 §2.7 through `mt-api` with source `seed`; your C3 confirmation that enables mainnet signing moved into P5-T004; testnet/Anvil sign within the seeded caps so P5-T056/P5-T058 don't wait on you; dropped deps P5-T050, P2-T035 (now on P5-T004); tools `cargo`, `supabase`; services `supabase-postgres`, `mt-api`)
