---
id: P5-T056
kind: task
title: Testnet claim scenario: simulation +tokens −gas, mandate respected, journal entry
phase: 5
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T044, P5-T046, P5-T048, P5-T065, P5-T017]
requirements: [R5.15, R5.18, R5.02]
roadmap_todos: [T5.61]
modules: [M4, M22, M18]
dashboards: [D12]
tools: [uv, forge, anvil, solana, solana-test-validator]
mcp: []
env: []
services: [sepolia-rpc, solana-devnet, telegram]
branch: p5/P5-T056-verify-testnet-claim-scenario
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

# P5-T056 · Testnet claim scenario: simulation +tokens −gas, mandate respected, journal entry

## Goal / expected outcome

On a public testnet (Sepolia for EVM, Solana devnet), a test Merkle distributor airdrop is discovered (via `/add`), vetted, decided as auto-claim under your testnet mandate, simulated ("+tokens to me, −gas" only), signed, broadcast and journalled — with D12 showing mandate, simulation, tx and journal links. This is exit criterion 2 (auto-claim part).

## Context & references

- Roadmap: ToDo T5.61 → R5.15, R5.18 · exit criterion 2 ([§6](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md))
- [02 F8](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D12 acceptance 1](../../../docs/ui/dashboards/D12-airdrops.md) · testnet keys and the testnet mandate are created in this task's setup (faucet funds only, no real money) with you approving the C3 steps; the mainnet mandates of P5-T006 are not needed (build first, keys last, [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22))

## Requirements

- Setup: the signer's testnet profile creates the testnet identity wallets (Sepolia, Solana devnet) via `key_create` (C3, you approve in Telegram), funded from public faucets only; signing uses the limits you confirmed in P5-T065; you approve the testnet mandate (`airdrop.mandate.create`, C3) for the test distributor. Claims run from the identity wallet, never the hot trading wallet (P5-B017).
- Deploy test fixtures: an OpenZeppelin MerkleDistributor (EVM) and an SPL Merkle distributor (Solana) with your identity wallets in the tree; host the proof JSON on a test domain registered as "official" in the fixture project.
- Run the full pipeline; assert the decision is auto-claim, simulation digest shows only token inflow + gas, mandate id recorded, journal event with classification and AUD value (testnet tokens priced at a fixture price, flagged test), and a manual-sale disposal task (never an automated sale; P5-B010).
- Negative variant: a second distributor that also pulls a test token → refused, CLAIM_MANUAL task.
- Evidence pack: exec_log rows, ledger rows, tx hashes, D12 screenshots in the progress log.

## ToDo

- [ ] Write deploy scripts under `tests/scenarios/testnet_claim/` and the testnet key/mandate setup (C3 steps approved by you).
- [ ] Run the scenario; capture evidence.
- [ ] Automate a repeatable version on Anvil/local validator for CI (same assertions).

## Verification

### Tests
- Scenario (testnet, manual-trigger) + CI replica on Anvil/local validator.

### Scenarios
- Given the testnet mandate is active, when the distributor goes live, then the claim executes within the cost-gate window and D12 shows all four links.
- Given the mandate is revoked, when the claim is retried, then it becomes CLAIM_MANUAL.

### Stress / failure injection
- Rerun the CI replica 10× — no duplicate claims, deterministic outcomes.

## Acceptance criteria

- [ ] Testnet claim executed with simulation proof, mandate and journal links
- [ ] Negative variant refused
- [ ] CI replica green

## Exceptions & edge cases

- Testnet RPC flakiness: retries allowed; never bypass simulation to finish the demo.

## Cardinal rules (do NOT)

- Do NOT use mainnet funds for this scenario.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking T5.61.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.61 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T056-verify-testnet-claim-scenario`
- PR title: `P5-T056: Testnet claim scenario: simulation +tokens −gas, mandate respected, journal entry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keys last: testnet keys and mandate created here instead of depending on P5-T006/real funds; signing needs P5-T065; manual disposal task asserted)
