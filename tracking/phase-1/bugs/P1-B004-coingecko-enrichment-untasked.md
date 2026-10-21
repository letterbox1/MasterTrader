---
id: P1-B004
kind: gap
title: CoinGecko/DefiLlama enrichment has no ToDo, yet the retention test needs CoinGecko rows
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.09]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B004-coingecko-enrichment-untasked
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M1 (Enrichment) vs docs/roadmap/phase-1-data-and-monitoring.md T1.63
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B004 · CoinGecko/DefiLlama enrichment has no ToDo, yet the retention test needs CoinGecko rows

## Goal / expected outcome

A ToDo owns the enrichment connector and the encrypted, purge-on-exit cache

## Context & references

- Found in: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) lists CoinGecko Demo + DefiLlama enrichment; T1.63 tests "CoinGecko rows deleted after 24 h"; [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) also requires the cache to be **encrypted** and **deleted on exit**, which no mechanism describes
- Related items: P1-T008, P1-T029, P1-T059

## Requirements

- **Where:** [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) lists CoinGecko Demo + DefiLlama enrichment; T1.63 tests "CoinGecko rows deleted after 24 h"; [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) also requires the cache to be **encrypted** and **deleted on exit**, which no mechanism describes
- **Expected:** A ToDo owns the enrichment connector and the encrypted, purge-on-exit cache
- **Actual:** No ToDo; T1.63 would have nothing to test
- **Suggested fix:** Add the connector to T1.26 or a new ToDo; describe the encryption (pgcrypto with a sops key) and shutdown purge in 12 §4/§5. P1-T029 implements this meanwhile
- **Impact:** Retention verification impossible without it; CoinGecko terms at risk (severity S3)

## ToDo

- [ ] Edit roadmap §4 and 12 §4/§5
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above
- `docs/12-policy-and-compliance.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B004-coingecko-enrichment-untasked`
- PR title: `P1-B004: CoinGecko/DefiLlama enrichment has no ToDo, yet the retention test needs CoinGecko rows`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
