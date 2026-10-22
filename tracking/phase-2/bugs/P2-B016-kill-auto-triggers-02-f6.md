---
id: P2-B016
kind: gap
title: "Automatic kill triggers differ: 02 F6 lists daily loss, DQ, error rate and cost blow-out; 03 M11 and 16 §2.1 act more narrowly"
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.18]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B016-kill-auto-triggers-02-f6
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md F6 step 1 vs docs/03-build-spec.md M11 kill switch and docs/16-configuration-and-safety-model.md §2.1
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B016 · Automatic kill triggers differ: 02 F6 lists daily loss, DQ, error rate and cost blow-out; 03 M11 and 16 §2.1 act more narrowly

## Goal / expected outcome

The automatic kill triggers are listed the same way everywhere.

## Context & references

- [02 F6 step 1](../../../docs/02-v1-architecture.md#8-end-to-end-flows): "an automatic breach (daily loss, system drawdown stage 2, DQ, error rate, cost blow-out)".
- [03 M11 kill switch](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp): automatic only on system drawdown stage 2 and unexplained reconciliation mismatches; smaller breaches act narrowly (daily loss halts the sleeve, API errors pause the venue, cost blow-out pauses the bot) per 16 §2.1.
- Affects P2-T031.

## Requirements

- **Steps to reproduce:** Compare 02 F6 step 1 with 03 M11 'Kill switch → Triggers'.
- **Expected:** 02 F6 matches 03 M11 / 16 §2.1.
- **Actual:** 02 F6 makes daily loss, DQ, error rate and cost blow-out global kill triggers.
- **Suggested fix:** Edit 02 F6 step 1 to 'system drawdown stage 2 or an unexplained reconciliation mismatch; smaller breaches act on the sleeve/venue/bot (16 §2.1)'. P2-T031 already follows 03 M11.
- **Impact:** S3: a literal reading of 02 would halt everything on a single sleeve's daily loss.

## ToDo

- [x] Suggested fix applied (follows 03 M11 / 16 §2.1)
- [x] 02 F6 step 1 now lists only system drawdown stage 2 and unexplained reconciliation mismatch as automatic kill triggers; smaller breaches act narrowly
- [x] P2-T031 already follows 03 M11; no task change needed

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [x] Docs agree: 02 F6 links 03 M11 and 16 §2.1
- [x] Affected tasks reference the decision (P2-T031 follows 03 M11)

## Exceptions & edge cases

- Until resolved, the affected tasks follow 16/17 (the reference docs) as stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the docs and in policy.

## Doc sync on completion

- The doc(s) in `doc_sync`: aligned wording.

## Branch & PR

- Branch: `p2/P2-B016-kill-auto-triggers-02-f6`
- PR title: `P2-B016: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: 02 F6 automatic triggers aligned with 03 M11 / 16 §2.1
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/02-v1-architecture.md F6 step 1 (automatic kill triggers match 03 M11 and 16 §2.1)
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
