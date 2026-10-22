---
id: P1-B004
kind: gap
title: CoinGecko/DefiLlama enrichment has no ToDo, yet the retention test needs CoinGecko rows
phase: 1
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B004-coingecko-enrichment-untasked
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M1 (Enrichment) vs docs/roadmap/phase-1-data-and-monitoring.md T1.63
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P1-B003/P1-B004/P1-B012): T1.34 owns the CoinGecko/DefiLlama enrichment with a ≤ 24 h encrypted cache; 12 §4 records pgcrypto with a key from the sops file and purge on shutdown
- [x] Aligned docs carry it: roadmap phase 1 §4 T1.34 (→ R1.05, R1.09); 12 §4 (CoinGecko row)
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T029 (now traced to T1.34), P1-T059

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (roadmap phase 1 §4 T1.34 (→ R1.05, R1.09); 12 §4 (CoinGecko row))
- [x] Decision and owning tasks noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B003/P1-B004/P1-B012; docs carry it (roadmap phase 1 §4 T1.34 (→ R1.05, R1.09); 12 §4 (CoinGecko row)); implementation owned by P1-T029 (now traced to T1.34), P1-T059
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B003/P1-B004/P1-B012); docs updated: roadmap phase 1 §4 T1.34 (→ R1.05, R1.09); 12 §4 (CoinGecko row); implementation owned by P1-T029 (now traced to T1.34), P1-T059
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
