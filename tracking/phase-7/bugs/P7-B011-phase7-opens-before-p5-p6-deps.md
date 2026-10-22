---
id: P7-B011
kind: gap
title: Phase 7 opens after P3 but its entry/kill rules need P5 and P6 deliverables
phase: 7
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B011-phase7-opens-before-p5-p6-deps
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: done
found_in: tracking/phase-7/PHASE.md opens_after [3]; docs/roadmap/phase-7-prove-and-go-live.md §2 (runbooks incl. wallet drained) and §7 rows; docs/14-strategy-evidence-and-validation.md §7 (capital to hold-and-earn)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P7-B011 · Phase 7 opens after P3 but its entry/kill rules need P5 and P6 deliverables

## Goal / expected outcome

The docs agree and are specific enough to implement: amend roadmap §2: 'wallet drained' drilled only if a hot/burner wallet exists; note in 14 §7 that without M22 the fallback is stables on venue + a user task.

## Context & references

- Found in: `tracking/phase-7/PHASE.md opens_after [3]; docs/roadmap/phase-7-prove-and-go-live.md §2 (runbooks incl. wallet drained) and §7 rows; docs/14-strategy-evidence-and-validation.md §7 (capital to hold-and-earn)`
- Related: P7-T045, P7-T022, P7-T057

## Requirements

- **What:** Entry criterion 'all runbooks drilled' includes 'wallet drained' (P5 T5.90), and the portfolio-DD/12-month rules route capital to hold-and-earn (P6 M22), but the phase can open once P3 is done.
- **Expected:** Either the entry criterion scopes 'wallet drained' to 'if any hot wallet is in use', and the hold-and-earn destination falls back to 'stables on venue + user task' when M22 isn't built — or opens_after includes 5 (and 6).
- **Actual:** The roadmap says P3–P6 don't block a P1 sleeve going micro-live, yet the entry criteria implicitly need P5.
- **Impact:** P7-T045 (and thus funding, P7-T057) could be blocked waiting for P5. (severity S3)
- **Suggested fix:** Amend roadmap §2: 'wallet drained' drilled only if a hot/burner wallet exists; note in 14 §7 that without M22 the fallback is stables on venue + a user task.

## ToDo

- [x] Decision recorded in docs/17 (17 §D P7-B011 (and §E)): P7 opens after P3 (hard-gated); items that need P5/P6 deliverables carry their own task dependencies; wallet-drained drill only if a hot/burner wallet exists; before the P6 treasury, flattened capital stays as stables on the venue + a USER task
- [x] Owning docs carry it: roadmap Phase 7 header and §2 entry criteria; 14 §7 note; tracking PHASE.md opens_after [3], hard_gate
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T021 (depends on P5-T036), P7-T045, P7-T022, P7-T011, P7-T008 (ops.wallets from P3-T012)
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (roadmap Phase 7 header and §2 entry criteria; 14 §7 note; tracking PHASE.md opens_after [3], hard_gate)
- [x] Affected tasks consistent with it (P7-T021 (depends on P5-T036), P7-T045, P7-T022, P7-T011, P7-T008 (ops.wallets from P3-T012))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md`: apply the agreed fix.
- `docs/14-strategy-evidence-and-validation.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B011-phase7-opens-before-p5-p6-deps`
- PR title: `P7-B011: fix phase 7 opens after P3 but its entry/kill rules need P5 and P6 deliverables`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §D P7-B011 (and §E): P7 opens after P3 (hard-gated); items that need P5/P6 deliverables carry their own task dependencies; wallet-drained drill only if a hot/burner wallet exists; before the P6 treasury, flattened capital stays as stables on the venue + a USER task. Docs now carry it: roadmap Phase 7 header and §2 entry criteria; 14 §7 note; tracking PHASE.md opens_after [3], hard_gate. Implementation owned by P7-T021 (depends on P5-T036), P7-T045, P7-T022, P7-T011, P7-T008 (ops.wallets from P3-T012). Root cause: entry and kill rules implicitly needed P5/P6 while the phase opened after P3.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P7-B011 (and §E)); docs updated: roadmap Phase 7 header and §2 entry criteria; 14 §7 note; tracking PHASE.md opens_after [3], hard_gate; implementation owned by P7-T021 (depends on P5-T036), P7-T045, P7-T022, P7-T011, P7-T008 (ops.wallets from P3-T012)
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
