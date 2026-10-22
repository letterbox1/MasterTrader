---
id: P1-T029
kind: task
title: Add CoinGecko Demo and DefiLlama enrichment with a 24 h cache
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T008]
requirements: [R1.09, R1.08]
roadmap_todos: [T1.34, T1.26]
modules: [M1]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p1/P1-T029-coingecko-defillama-enrichment
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/12-policy-and-compliance.md]
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

# P1-T029 · Add CoinGecko Demo and DefiLlama enrichment with a 24 h cache

## Goal / expected outcome

Crypto enrichment (market cap, supply, categories from CoinGecko Demo; TVL from DefiLlama `api.llama.fi`) is cached under its terms: CoinGecko rows carry `retention_days=1`, are encrypted at rest and purged on exit, which gives P1-T059 real rows to test retention.

## Context & references

- Roadmap: requirements [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.34](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.26](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Enrichment: CoinGecko Demo, DefiLlama) · terms [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (CoinGecko: one key, cache ≤ 24 h, encrypted, deleted on exit, attribution; DefiLlama: `api.llama.fi` only) · [06 §3 Skip list](../../../docs/06-aggregators-and-market-providers.md#skip-list) (CoinGecko not a price archive)
- Roadmap ToDo T1.34 now names the CoinGecko/DefiLlama enrichment with the ≤ 24 h encrypted cache (gap P1-B004 closed); 12 §4 records pgcrypto with a key from the sops file and purge on shutdown
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): CoinGecko is built keyless against recorded fixtures (rows written through the real tagged write path so P1-T059 can test retention); the live call with your CoinGecko Demo key (P0-T010) runs in P1-T073. DefiLlama (`api.llama.fi`) is keyless and runs live here
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T008

## Requirements

- CoinGecko Demo key read from the secrets file at runtime (none in CI); calls through the quota tracker with the Demo plan's monthly/minute budget (recorded in `config/quotas.yaml`, confirmed live in P1-T073)
- Store in `market.enrichment_cache` with `retention_days=1`, `display_ok=true` (with attribution), `train_ok=false`, `commercial_ok=false`; values encrypted with pgcrypto using a key from sops
- Purge on service shutdown (hook from P1-T008) and by the hourly retention job
- DefiLlama TVL via `api.llama.fi` only, stored with its own provenance; no site scraping
- UI attribution string "Data from CoinGecko" wherever shown

## ToDo

- [ ] Implement both adapters and the encrypted cache table
- [ ] Wire retention + shutdown purge
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: provenance defaults; encryption round-trip
- Integration: rows older than 24 h removed by retention; shutdown purge empties the cache

### Scenarios

- Given the service stops, when it shuts down cleanly, then CoinGecko rows are deleted; given it crashes, then the next start purges before fetching

### Stress / failure injection

- n/a: low volume; quota tracker covers rate

## Acceptance criteria

- [ ] No CoinGecko row older than 24 h + one retention interval exists (checked by P1-T059)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Never use CoinGecko prices to build long history or bars

## Cardinal rules (do NOT)

- Do NOT archive CoinGecko data beyond 24 h or use it as a price source for bars
- Do NOT scrape DefiLlama's website or use unofficial endpoints
- Do NOT use CoinGecko values as stored journal/tax values; display and cross-check only ([16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal))
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.34, T1.26 once every task traced to it in PHASE.md is done; note P1-T029 next to it.
- `docs/03-build-spec.md` §M1: note enrichment cache and its retention
- `docs/12-policy-and-compliance.md` §4: link the implementation of the CoinGecko rule

## Branch & PR

- Branch: `p1/P1-T029-coingecko-defillama-enrichment`
- PR title: `P1-T029: Add CoinGecko Demo and DefiLlama enrichment with a 24 h cache`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (traced to new T1.34 (P1-B004 closed); keyless build, live CoinGecko in P1-T073; cross-check only per 16 §4.1)
