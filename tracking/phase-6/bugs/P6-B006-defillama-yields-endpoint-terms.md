---
id: P6-B006
kind: gap
title: DefiLlama rule says `api.llama.fi` only, but the free yields API the allocator needs is served from the yields host
phase: 6
type: DOC
status: backlog
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
branch: p6/P6-B006-defillama-yields-endpoint-terms
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: docs/12-policy-and-compliance.md §4 (DefiLlama row) vs docs/13-wallets-treasury-and-onchain.md §4
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Check DefiLlama's official API docs for hosts and terms.
- [ ] Propose the 12 §4 wording.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 12 §4 and 13 §4 consistent; P6-T035 cites the rule.
- [ ] Root cause noted in the progress log.

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
