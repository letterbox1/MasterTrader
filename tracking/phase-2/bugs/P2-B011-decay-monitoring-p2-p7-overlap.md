---
id: P2-B011
kind: gap
title: Decay monitoring and health check are required in both P2 (R2.21) and P7 (R7.07/T7.22)
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.21]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B011-decay-monitoring-p2-p7-overlap
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: done
found_in: docs/roadmap/phase-2-strategies-risk-lab.md R2.21; docs/roadmap/phase-7-prove-and-go-live.md R7.07/T7.22
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B011 · Decay monitoring and health check are required in both P2 (R2.21) and P7 (R7.07/T7.22)

## Goal / expected outcome

P7's item is scoped as live hardening of the P2 jobs, not a second build.

## Context & references

- [R2.21](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · [R7.07 / T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Affects P2-T034, P2-T060.

## Requirements

- **Steps to reproduce:** Both phases have a BUILD ToDo for the same rolling 60-trade/CUSUM/health-check jobs.
- **Expected:** P2 builds and runs them on paper; P7 extends them to live sub-accounts and kill-criteria wiring.
- **Actual:** Duplicate scope; risk of rebuilding.
- **Suggested fix:** Reword T7.22 to 'extend P2 decay jobs to live accounts and kill criteria (R7.06)'.
- **Impact:** S4: planning duplication only.

## ToDo

- [x] Decision recorded: decay/health jobs are built in P2 for paper; P7 extends them to live with kill criteria
- [x] Docs agree: 16 §2.6, roadmap R2.21 and R7.07/T7.22, 03 §8
- [x] Tasks updated: P2-T034, P2-T060

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §2.6 (one meaning per signal); roadmap P2 R2.21 (built for paper) and P7 R7.07 / T7.22 (extend the P2 jobs to live); 03 §8 item 8)
- [x] Affected tasks reference the decision (P2-T034, P2-T060 (P7 T7.22 extends them))

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md` T7.22 wording (via the Phase 7 planner).

## Branch & PR

- Branch: `p2/P2-B011-decay-monitoring-p2-p7-overlap`
- PR title: `P2-B011: scope P7 decay item as live hardening`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §B (P2-B011); docs carry it (16 §2.6 (one meaning per signal); roadmap P2 R2.21 (built for paper) and P7 R7.07 / T7.22 (extend the P2 jobs to live); 03 §8 item 8); implementation owned by P2-T034, P2-T060 (P7 T7.22 extends them))
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P2-B011)); docs updated: 16 §2.6 (one meaning per signal); roadmap P2 R2.21 (built for paper) and P7 R7.07 / T7.22 (extend the P2 jobs to live); 03 §8 item 8; implementation owned by P2-T034, P2-T060 (P7 T7.22 extends them)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
