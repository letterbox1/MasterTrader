---
id: P2-B010
kind: gap
title: Kill-switch rung 6 'sweep hot balances to the vault' cannot exist in Phase 2
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.15, R2.18]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B010-kill-vault-sweep-phase-split
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M11 ladder rung 6; docs/14 §5
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B010 · Kill-switch rung 6 'sweep hot balances to the vault' cannot exist in Phase 2

## Goal / expected outcome

The docs say the sweep part of rung 6 arrives with the signer in Phase 5 (R5.07), so Phase 2 isn't judged on it.

## Context & references

- [03 M11 ladder](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [14 §5 ladder](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [P5 R5.07](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md)
- Affects P2-T018, P2-T031.

## Requirements

- **Steps to reproduce:** Rung 6 includes a vault sweep; the signer/hot wallets only exist from Phase 5.
- **Expected:** Note 'sweep: Phase 5 (R5.07); Phase 2 provides the hook'.
- **Actual:** No phase note; Phase 2 kill drill could be read as incomplete.
- **Suggested fix:** Add the note; P2-T031 exposes a no-op, logged sweep hook.
- **Impact:** S4: clarity only.

## ToDo

- [x] Decision recorded: kill stops new trading, cancels orders, applies each bot's failure policy, freezes new treasury/earn moves; the vault sweep arrives in P5 (default on); P2 has a logged no-op hook
- [x] Docs agree: 02 F6, 03 M11, 14 §5, roadmap R2.18
- [x] Tasks updated: P2-T031, P2-T018

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (02 F6 kill actions (no sweep in P2); 03 M11 kill switch (logged no-op sweep hook); 14 §5 ladder rung 6; roadmap R2.18)
- [x] Affected tasks reference the decision (P2-T031, P2-T018)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/03-build-spec.md` M11 and `docs/14-strategy-evidence-and-validation.md` §5: phase note.

## Branch & PR

- Branch: `p2/P2-B010-kill-vault-sweep-phase-split`
- PR title: `P2-B010: note vault sweep arrives in Phase 5`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §B (P2-B010); docs carry it (02 F6 kill actions (no sweep in P2); 03 M11 kill switch (logged no-op sweep hook); 14 §5 ladder rung 6; roadmap R2.18); implementation owned by P2-T031, P2-T018)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P2-B010)); docs updated: 02 F6 kill actions (no sweep in P2); 03 M11 kill switch (logged no-op sweep hook); 14 §5 ladder rung 6; roadmap R2.18; implementation owned by P2-T031, P2-T018
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
