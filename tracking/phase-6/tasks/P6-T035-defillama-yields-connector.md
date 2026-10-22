---
id: P6-T035
kind: task
title: DefiLlama yields connector with hourly cache and risk-haircut inputs
phase: 6
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T006, P1-T007, P1-T029]
requirements: [R6.21]
roadmap_todos: [T6.28]
modules: [M22, M1]
dashboards: [D18]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [defillama-yields-api, postgres, prefect]
branch: p6/P6-T035-defillama-yields-connector
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T035 · DefiLlama yields connector with hourly cache and risk-haircut inputs

## Goal / expected outcome

An `mt_data` connector pulls DefiLlama pool yields (free) at most hourly, caches them with provenance, and computes risk-haircut inputs (protocol age, audits, TVL trend) for allow-listed pools only.

## Context & references

- Roadmap: [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (DefiLlama yields API, free, cached hourly; never rely on `apyReward`) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (DefiLlama: official API only, no scraping/republishing)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B006: official free API hosts `api.llama.fi` and `yields.llama.fi` are allowed; site scraping isn't) · [06](../../../docs/06-aggregators-and-market-providers.md) DefiLlama row
- Cross-phase: P1-T006 (quota tracker), P1-T007 (provenance tagging), P1-T029 (DefiLlama client to reuse)

## Requirements

- Fetch pools from the official free host `yields.llama.fi` (`/pools`; no key) for allow-listed protocols; tests run on recorded JSON; fields `apyBase`, `apyReward` (stored, never used for allocation), `tvlUsd`, `pool`, `chain`, `stablecoin`, timestamp.
- Cache hourly in `market.yield_snapshot` (hypertable) with provenance (`source=defillama`, `display_ok`, `commercial_ok=false`); no republishing.
- Haircut inputs: protocol age (launch date in allow-list), audit count, 30d TVL trend (slope, drawdown) → `risk_haircut_bps` per pool (formula documented, conservative defaults).
- Quota tracker entry; backoff on 429; staleness flag after 3 h.

## ToDo

- [ ] Connector + Prefect hourly flow.
- [ ] Hypertable migration.
- [ ] Haircut calculator.
- [ ] Quota + staleness metrics.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: parser on recorded JSON; haircut formula golden values.
- Integration: hourly flow idempotent per hour bucket.

### Scenarios
- Given DefiLlama is down, then the last snapshot is used until 3 h old, then allocation is paused with reason `stale_yields`.
- Given a pool with high `apyReward` and low `apyBase`, then only `apyBase` reaches the allocator.

### Stress / failure injection
- Simulate 429 bursts: connector backs off and never exceeds the free limit.

## Acceptance criteria

- [ ] Hourly snapshots stored with provenance.
- [ ] Haircuts computed for every allow-listed pool.

## Exceptions & edge cases

- Pool id changes upstream → mapping table flags unmapped allow-list entries.

## Cardinal rules (do NOT)

- Do NOT scrape defillama.com pages or use unofficial endpoints; only `yields.llama.fi` / `api.llama.fi`.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: yields endpoint and limits.
- `docs/13-wallets-treasury-and-onchain.md` §4: haircut formula.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T035-defillama-yields-connector`
- PR title: `P6-T035: DefiLlama yields connector with hourly cache and risk-haircut inputs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (DefiLlama official hosts only per 17 §D P6-B006; cross-phase deps P1-T006/T007/T029; run fields)
