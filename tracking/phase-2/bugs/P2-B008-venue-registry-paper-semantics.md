---
id: P2-B008
kind: gap
title: Venue registry semantics for paper/testnet orders are undefined
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.17]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B008-venue-registry-paper-semantics
pr: ""
doc_sync: [docs/12-policy-and-compliance.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §2; docs/roadmap/phase-2-strategies-risk-lab.md §7
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B008 · Venue registry semantics for paper/testnet orders are undefined

## Goal / expected outcome

The registry says whether `read_only`/`blocked` products may be paper-traded (sandbox/testnet) and how testnet venues are registered.

## Context & references

- [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [roadmap §7 'Carry stays paper until the venue registry allows it'](../../../docs/roadmap/phase-2-strategies-risk-lab.md)
- Affects P2-T016, P2-T023, P2-T009.

## Requirements

- **Steps to reproduce:** Roadmap §7 expects carry (perps) to run on paper while perps are blocked; 12 §2 says the risk manager blocks orders to any venue/product not `allowed`, with no mode distinction.
- **Expected:** Rule: paper/sandbox/testnet orders allowed for `allowed` and `read_only`/`blocked` products (flagged `paper_only_venue`), never for live; testnet venues registered as their own rows.
- **Actual:** Literal reading blocks paper research on blocked products, contradicting the roadmap.
- **Suggested fix:** Add a `paper_allowed` column (default true) and the mode rule to 12 §2; P2-T016 implements it.
- **Impact:** S3: carry/unlock research and the paper clock for carry would be blocked or the check bypassed.

## ToDo

- [x] Decision recorded: paper/testnet orders allowed for `allowed` or `read_only`; `blocked` products only if marked `paper_ok`; testnets are their own rows
- [x] Docs agree: 12 §2
- [x] Tasks updated: P2-T016 (check), P2-T009 (carry/unlock templates)

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given Bybit perps `blocked`, when a paper order is placed on Bybit testnet, then it is allowed and flagged; a live order is rejected.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (12 §2 (paper/testnet rule and `paper_ok` flag in the registry table))
- [x] Affected tasks reference the decision (P2-T016, P2-T009)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: paper rule + column.

## Branch & PR

- Branch: `p2/P2-B008-venue-registry-paper-semantics`
- PR title: `P2-B008: define venue registry paper/testnet semantics`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B008); docs carry it (12 §2 (paper/testnet rule and `paper_ok` flag in the registry table)); implementation owned by P2-T016, P2-T009)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B008)); docs updated: 12 §2 (paper/testnet rule and `paper_ok` flag in the registry table); implementation owned by P2-T016, P2-T009
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
