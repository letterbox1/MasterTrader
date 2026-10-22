---
id: P5-T068
kind: task
title: "Live read-only check with your keys: Helius, Alchemy, GoPlus and CryptoRank on registered addresses"
phase: 5
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T010, P5-T003, P5-T005, P5-T018, P5-T022, P5-T032, P5-T035, P5-T036]
requirements: [R5.05, R5.12, R5.13]
roadmap_todos: [T5.66]
modules: [M22, M4]
dashboards: [D18, D07]
tools: [uv, docker, sops]
mcp: []
env: [HELIUS_API_KEY, ALCHEMY_API_KEY, GOPLUS_API_KEY, CRYPTORANK_API_KEY]
services: [helius, alchemy, goplus, cryptorank, postgres, nats]
branch: p5/P5-T068-live-read-only-check-with-your-keys-helius-alche
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T068 · Live read-only check with your keys: Helius, Alchemy, GoPlus and CryptoRank on registered addresses

## Goal / expected outcome

The keyless builds (RPC pools, wallet indexer, discovery, enrichment and risk clients, all built against Anvil, devnets and recorded fixtures) are proven against the live free-tier providers with your keys: Helius and Alchemy return balances for every registered address, GoPlus returns token and approval security for a sample, and CryptoRank returns calendar/funding data, all within quota, read-only, with no key in logs. Live response shapes are compared with the recorded fixtures and any drift is fixed or filed.

## Context & references

- Roadmap: ToDo T5.66 → R5.05, R5.12, R5.13 ("after T0.10, T5.04")
- Keys: P0-T010 (Helius, Alchemy, GoPlus, CryptoRank free keys in the sops file), P5-T003 (fallback RPC accounts and key restrictions); addresses: P5-T005
- Builds under test: P5-T018 (RPC pools/quotas), P5-T022 (indexer), P5-T032 (discovery connectors), P5-T035 (enrichment), P5-T036 (risk providers)
- Limits: [13 §7 RPC](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) (Helius Free 1M credits/10 rps; Alchemy Free 30M CU/month) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (GoPlus 150K CU/month, 30K/day, 150/min; CryptoRank 10/min, 10K credits/month; one account each) · secrets [07 §2](../../../docs/07-security-notes.md#2-secrets)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22))

## Requirements

- Read-only calls only: balances/assets (Helius DAS `getAssetsByOwner`, Alchemy/Blockscout token balances), `eth_feeHistory`/`getRecentPrioritizationFees` samples, GoPlus token/approval security for ≤ 20 tokens, CryptoRank calendar and funding for ≤ 20 projects.
- Every registered address (P5-T005) gets at least one successful live balance read; D18 shows them with the live source and timestamp.
- Quota usage after the run stays below 5% of each provider's daily share; the quota tracker (P1) records every call.
- Keys are read from the sops tmpfs by name only (`HELIUS_API_KEY`, `ALCHEMY_API_KEY`, `GOPLUS_API_KEY`, `CRYPTORANK_API_KEY`); a log/NATS capture of the run contains no key value.
- Live vs fixture: parse every live response with the same adapters; schema differences are fixed in the adapter (with a refreshed fixture) or filed as a bug.

## ToDo

- [ ] Run `./kanban preflight P5-T068` and confirm the env names resolve on the host (values never printed).
- [ ] Run the live smoke suite `tests/live/p5_providers/` (manual-trigger job; skipped in normal CI).
- [ ] Check D18: every registered address shows a live balance; D07 quota panel shows the usage.
- [ ] Diff live payload shapes against the recorded fixtures; refresh fixtures or file bugs.
- [ ] Grep the run's logs and NATS capture for key material (none allowed).
- [ ] Record commands, counts, quota usage and results in the progress log.

## Verification

### Tests
- Live smoke suite (manual trigger): one test per provider family, asserting HTTP success, parse success and quota accounting.
- Log-redaction check over the run's logs and NATS capture.

### Scenarios
- Given your registered vault and identity addresses, when the indexer polls live, then D18 shows balances from Helius/Alchemy with timestamps, and internal transfers classify as before.
- Given Helius returns 429 during the run, then the pool fails over to the fallback provider and the run still passes with the source recorded.
- Given a key is missing on the host, then `./kanban start` preflight refuses and the task is blocked on P0-T010/P5-T003 (no partial run).

### Stress / failure injection
- n/a: a short live smoke run within free quotas (load and chaos are covered against mocks in P5-T018 and P5-T062)

## Acceptance criteria

- [ ] Helius, Alchemy, GoPlus and CryptoRank live calls succeed on registered addresses/sample tokens
- [ ] Quotas respected and visible in D07
- [ ] No key material in logs or NATS
- [ ] Fixture drift fixed or filed

## Exceptions & edge cases

- A provider changed its free tier: record the new limit, update the quota table (P5-T018) and file a doc-sync note for 06/12.
- Provider outage on the day: rerun later; don't mark done on partial evidence.

## Cardinal rules (do NOT)

- Do NOT print, paste or commit key values; refer to env names only (07 §2).
- Do NOT create second accounts to stretch a free tier; no paid plans (12 §4).
- Do NOT use Etherscan as an input; Blockscout/own RPC only.
- Do NOT sign or broadcast anything in this task (read-only).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: record verified free-tier behaviour/limits observed live.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.66 when this lands.

## Branch & PR

- Branch: `p5/P5-T068-live-read-only-check-with-your-keys-helius-alche`
- PR title: `P5-T068: Live read-only check with your keys: Helius, Alchemy, GoPlus and CryptoRank on registered addresses`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T068` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T5.66: keys-last live check after P0-T010 and P5-T005)
