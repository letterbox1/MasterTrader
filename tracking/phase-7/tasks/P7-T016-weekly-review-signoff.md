---
id: P7-T016
kind: task
title: Weekly review sign-off in the journal (D14 Reviews tab)
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T015]
requirements: [R7.03]
roadmap_todos: [T7.05]
modules: [M18, M15]
dashboards: [D14]
branch: p7/P7-T016-weekly-review-signoff
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/02-v1-architecture.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T016 · Weekly review sign-off in the journal (D14 Reviews tab)

## Goal / expected outcome

You can review a pack and sign it off from web or phone; sign-offs are WORM journal records, and a missing sign-off for a live week blocks that week from counting as 'clean' for capital steps.

## Context & references

- Roadmap: [R7.03 · ToDo T7.05](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [D14](../../../docs/ui/dashboards/D14-journal.md) (journal; records never editable) · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · [mob §2](../../../docs/ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open)
- Related: P7-T015, P7-T018 (clean-week definition consumes sign-offs), P7-T060 (you doing the reviews)

## Requirements

- Command `journal.review.signoff {pack_id, notes, actions[]}` (C1); actions are follow-ups that become `curation.task` items.
- Table `journal.weekly_review` (WORM): pack id, signed_at, notes, per-trade review tags ('followed plan?', mistake type), actions.
- D14 → Reviews tab: list of weeks with status (pending/signed/overdue); review page shows the pack and a sign-off form; phone flow ≤ 3 taps from the Telegram digest to sign-off.
- Reminder: Telegram nudge Monday 18:00 and Wednesday 18:00 if unsigned; overdue after 7 days → capital-step evaluator treats the week as not clean.

## ToDo

- [ ] Migration + command + query `/journal/reviews`.
- [ ] D14 Reviews tab (list, review page, sign-off form) with viewport matrix.
- [ ] Telegram reminder job and deep link.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: sign-off creates a WORM row; a second sign-off for the same pack is a new row with `supersedes_id`.
- Playwright: digest deep link → review → sign-off in ≤ 3 taps at 375×667 and 280×653.

### Scenarios
- Given a pack is unsigned after 7 days, then the week shows 'overdue' and the capital-step state shows 'week not clean: review missing'.
- Given you add an action 'tighten BTC max position', then a task is created and linked.

### Stress / failure injection
- n/a: single-user, low volume; covered by integration tests.

## Acceptance criteria

- [ ] Sign-off works on web and phone; WORM rows written.
- [ ] Overdue reviews feed the clean-week evaluator.
- [ ] CI green incl. viewport matrix.

## Exceptions & edge cases

- Offline phone: sign-off is not queued offline (mob §1); the UI says so.
- Pack regenerated after sign-off: sign-off stays linked to the original pack id; the new pack needs its own sign-off.

## Cardinal rules (do NOT)

- Do NOT allow edits to a signed review; corrections supersede.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D14-journal.md`: Reviews tab.
- `docs/02-v1-architecture.md` §7: `journal.review.signoff`, `/journal/reviews`.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.05 when this item is done.

## Branch & PR

- Branch: `p7/P7-T016-weekly-review-signoff`
- PR title: `P7-T016: Weekly review sign-off in the journal (D14 Reviews tab)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
