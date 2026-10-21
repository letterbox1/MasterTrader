---
id: P5-T044
kind: task
title: Claim executor (airdrop-exec): mandate → cost gate → simulation → signer → journal
phase: 5
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T043, P5-T016, P5-T020, P5-T041, P5-T042]
requirements: [R5.15, R5.N2, R5.18]
roadmap_todos: [T5.28]
modules: [M4, M22, M18]
dashboards: [D12]
branch: p5/P5-T044-claim-executor-airdrop-exec
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T044 · Claim executor (airdrop-exec): mandate → cost gate → simulation → signer → journal

## Goal / expected outcome

The `airdrop-exec` service executes queued auto-claims end to end: re-check mandate, kill switch, never-automated policy and eligibility → cost-gate verdict → signer intent (which simulates) → broadcast (Flashbots Protect on Ethereum L1 where applicable) → confirmation → `exec_log` row and a claim-result event that the records task (P5-T046) journals; anything that fails a check becomes a `CLAIM_MANUAL` task with the reason. Manual `airdrop.claim.execute` (C2) uses the same path.

## Context & references

- Roadmap: [R5.15](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.N2 · ToDo T5.28 · scenario P5-T056
- [02 F8](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [08 autonomous 2](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) · [13 §7 DEX/RPC](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) · [D12 path/history](../../../docs/ui/dashboards/D12-airdrops.md)

## Requirements

- Pre-checks at execution time (not just at decision time): mandate active and covering (contract, selector); kill OFF; wallet not frozen; NA policy pass; eligibility still true (`isClaimed` false); risk report < 24 h old and no hard fail.
- Cost gate `allow` (≤ 60 s old); signer returns simulation digest and signed tx; broadcast via RPC pool (Flashbots Protect for Ethereum L1, no fee on reverts); wait for finality (EVM 12 blocks / Solana finalized).
- Records: `exec_log` (WORM) with mandate id, quote id, simulation digest, ledger ref, tx hash; publish `airdrop.claim.result` (consumed by P5-T046, which writes the income journal event); Telegram instant notice "auto-claim executed" with links.
- Idempotency: one claim per (opportunity, wallet); restart-safe (resume from exec_log state; never double-broadcast).
- Kill ON: stop accepting work within 1 s; in-flight before signing → cancelled; after broadcast → tracked to completion.
- Throughput: sequential per wallet (nonce safety); max claims/day from mandate.

## ToDo

- [ ] Implement `packages/mt_airdrop/exec/` service: queue consumer, pre-check pipeline, signer client (mTLS/socket), broadcaster, confirmation tracker.
- [ ] `airdrop.claim.execute` (C2) handler with simulation preview shown before confirm.
- [ ] Compose service `airdrop-exec` on `core` + `signer` networks with digest.
- [ ] Integration tests on Anvil and local Solana validator; doc sync.

## Verification

### Tests
- Integration (Anvil fork): eligible Merkle claim → exec_log row + `airdrop.claim.result`; second run is a no-op (idempotent).
- Integration: mandate revoked between queue and execution → CLAIM_MANUAL task, no signer call.
- Integration: crash after signing before broadcast → on restart, re-check `isClaimed`/nonce and resume without duplicate.

### Scenarios
- Given an auto-claim whose simulation shows an extra USDC outflow, then the signer refuses and a CLAIM_MANUAL task with "simulation outflow" is created.
- Given kill ON during a confirmation wait, then the tracker still records the result; no new claims start.

### Stress / failure injection
- 50 queued claims across 3 wallets with RPC latency 1–3 s and 10% RPC errors: no duplicates, per-wallet nonces correct, all outcomes recorded.

## Acceptance criteria

- [ ] End-to-end claim path with all pre-checks at execution time
- [ ] exec_log row, `airdrop.claim.result` event and notification for every claim
- [ ] Idempotent and restart-safe
- [ ] Kill freezes within 1 s

## Exceptions & edge cases

- Gas spike after quote: quote stale → re-gate; `wait` defers within deadline.
- Claim contract upgraded since mandate: refuse (implementation pin) → task.

## Cardinal rules (do NOT)

- Do NOT broadcast any transaction the signer did not sign after its own simulation.
- Do NOT retry a refused intent with modified parameters to get around a check.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: executor pre-check list.
- `docs/02-v1-architecture.md` F8: execution-time re-checks.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T044-claim-executor-airdrop-exec`
- PR title: `P5-T044: Claim executor (airdrop-exec): mandate → cost gate → simulation → signer → journal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
