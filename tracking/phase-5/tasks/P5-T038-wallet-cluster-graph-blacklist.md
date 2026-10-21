---
id: P5-T038
kind: task
title: Wallet-cluster detection (funding graph) and entity blacklist
phase: 5
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T035]
requirements: [R5.13, R5.18]
roadmap_todos: [T5.26]
modules: [M4]
dashboards: [D12]
branch: p5/P5-T038-wallet-cluster-graph-blacklist
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T038 · Wallet-cluster detection (funding graph) and entity blacklist

## Goal / expected outcome

Our own wallet-cluster detection builds a funding graph of early buyers/holders (common funder within 3–5 hops, same-slot or bundled buys, shared CEX-withdrawal origin) and hard-fails tokens where a large share of supply sits with one cluster; a **blacklist** of projects, deployers, domains and funding wallets confirmed as scams auto-flags any later project linked to them.

## Context & references

- Roadmap: [R5.13](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.18 · ToDo T5.26
- [03 M4](../../../docs/03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop) (the highest-value check) · [08 fresh launches & memecoins](../../../docs/08-airdrops-and-token-launches.md#fresh-launches--memecoins) · [08 records: blacklist](../../../docs/08-airdrops-and-token-launches.md#records)

## Requirements

- Graph build: first N (default 100) buyers/holders → trace inbound funding up to 5 hops via RPC/Blockscout/Helius within quotas; stop at known CEX hot wallets (labelled) and record "CEX withdrawal origin".
- Cluster rules: common funder within 3–5 hops; same slot/block buys; bundled buys (Jito bundle / same tx); share of supply per cluster; hard fail when one cluster (excluding pools/lockers/burn) holds ≥ 30% (config).
- Single-wallet flags: funded minutes before launch from a mixer or fresh exchange withdrawal, buys in the deploy block, links to blacklisted deployers, sells into every pump.
- Blacklist (`curation.blacklist_project` + address/domain links): entries only from confirmed outcomes (rug observed, user confirmation, or reputable report); every later project whose deployer/funder/domain links within 2 hops → hard fail with path shown.
- Results in `curation.wallet_cluster` and members; graph snapshot JSON for D12.

## ToDo

- [ ] Implement `packages/mt_airdrop/risk/clusters/` (tracer, cluster rules, supply share).
- [ ] Implement `risk/blacklist.py` with add (C1 command `airdrop.reject` with `blacklist=true`) and link-propagation checks.
- [ ] CEX hot-wallet label list (curated, versioned).
- [ ] Tests on fixture graphs + one real recorded launch; doc sync.

## Verification

### Tests
- Unit: synthetic graph where 8 buyers share a funder at 3 hops → one cluster, supply share computed.
- Unit: blacklist propagation — new token by a blacklisted deployer → hard fail with path.
- Integration: recorded Pump.fun launch fixture reproduces the known bundled-buy cluster.

### Scenarios
- Given 40% of supply held by wallets funded from one address 2 hops away, then hard fail "cluster holds 40% of supply".
- Given an unrelated project shares only a CEX withdrawal origin, then no blacklist hit (CEX nodes are stop nodes).

### Stress / failure injection
- Trace budget: ≤ 2,000 RPC credits per token; 50 tokens/day within the Helius 1M/month budget (report the actual cost).

## Acceptance criteria

- [ ] Cluster detection with the three patterns
- [ ] Supply-share hard fail
- [ ] Blacklist with link propagation
- [ ] RPC cost per token measured and within budget

## Exceptions & edge cases

- Trace truncated by budget: mark `partial` → autonomous paths blocked.

## Cardinal rules (do NOT)

- Do NOT add blacklist entries from unverified rumours (Telegram chatter is not evidence).
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: cluster thresholds and blacklist evidence rules.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.26 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T038-wallet-cluster-graph-blacklist`
- PR title: `P5-T038: Wallet-cluster detection (funding graph) and entity blacklist`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
