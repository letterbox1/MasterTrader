---
id: P6-B006
kind: gap
title: DefiLlama rule says `api.llama.fi` only, but the free yields API the allocator needs is served from the yields host
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.21]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B006-defillama-yields-endpoint-terms
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §4 (DefiLlama row) vs docs/13-wallets-treasury-and-onchain.md §4
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B006 · DefiLlama rule says `api.llama.fi` only, but the free yields API the allocator needs is served from the yields host

## Goal / expected outcome

The docs agree and are specific enough to build from: 12 §4 names every DefiLlama host the platform may call (official free API hosts), with caching/no-republishing terms.

## Context & references

- Found in: docs/12-policy-and-compliance.md §4 (DefiLlama row) vs docs/13-wallets-treasury-and-onchain.md §4
- [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (DefiLlama yields API, cached hourly)
- Affects: P6-T035

## Requirements

- **Steps to reproduce:** read docs/12-policy-and-compliance.md §4 (DefiLlama row) vs docs/13-wallets-treasury-and-onchain.md §4 and compare it with the cross-referenced sections listed under Context.
- **Expected:** 12 §4 names every DefiLlama host the platform may call (official free API hosts), with caching/no-republishing terms.
- **Actual:** 12 §4 allows 'api.llama.fi only'; 13 §4 relies on the 'DefiLlama yields API', whose pool endpoint is published on `yields.llama.fi` (not `api.llama.fi`).
- **Suggested fix:** Amend 12 §4 to 'official free API hosts only (api.llama.fi, yields.llama.fi, coins.llama.fi); no site scraping, unofficial APIs or republishing'. Interim: P6-T035 calls only the official yields endpoint documented by DefiLlama.
- **Impact:** Compliance rule blocks a required data source (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P6-B006): DefiLlama official free API hosts `api.llama.fi` and `yields.llama.fi` are allowed; site scraping isn't
- [x] Owning docs carry it: 12 §4 DefiLlama row; 06 DefiLlama rows; 13 §4 discovery bullet; roadmap R6.21
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T035
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (12 §4 DefiLlama row; 06 DefiLlama rows; 13 §4 discovery bullet; roadmap R6.21)
- [x] Affected tasks consistent with it (P6-T035)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT scrape DefiLlama site pages as a workaround.
- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: resolve the inconsistency.
- `docs/06-aggregators-and-market-providers.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B006-defillama-yields-endpoint-terms`
- PR title: `P6-B006: DefiLlama rule says `api.llama.fi` only, but the free yields API the allocator needs is served from the yields host`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B006` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P6-B006: DefiLlama official free API hosts `api.llama.fi` and `yields.llama.fi` are allowed; site scraping isn't. Docs now carry it: 12 §4 DefiLlama row; 06 DefiLlama rows; 13 §4 discovery bullet; roadmap R6.21. Implementation owned by P6-T035. Root cause: 12 §4 named only the TVL host.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P6-B006); docs updated: 12 §4 DefiLlama row, 06 DefiLlama rows, 13 §4, roadmap R6.21; implementation owned by P6-T035
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
