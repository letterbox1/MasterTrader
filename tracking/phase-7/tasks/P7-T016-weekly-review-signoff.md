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
requirements: [R7.03, R7.15]
roadmap_todos: [T7.05, T7.26]
modules: [M18, M15]
dashboards: [D14]
tools: [git, uv, pnpm, node>=20]
mcp: []
env: []
services: [postgres, mt-api, telegram bot api]
branch: p7/P7-T016-weekly-review-signoff
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/02-v1-architecture.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T016 · Weekly review sign-off in the journal (D14 Reviews tab)

## Goal / expected outcome

You can review a pack and sign it off from web or phone; sign-offs are WORM journal records, and every live week must have one (exit criterion 3). Under the default clean-week rule ([16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)) a missing sign-off doesn't make a week dirty; it shows as a warning on the capital-step proposal.

## Context & references

- Roadmap: [R7.03 · ToDo T7.05](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [D14](../../../docs/ui/dashboards/D14-journal.md) (journal; records never editable) · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · [mob §2](../../../docs/ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open)
- Related: P7-T015, P7-T018 (capital-step proposal shows unsigned weeks), P7-T060 (you doing the reviews), P7-T067 (Phase 7 API catalogue)

## Requirements

- Command `journal.review.signoff {pack_id, notes, actions[]}` (C1); actions are follow-ups that become `curation.task` items.
- Table `journal.weekly_review` (WORM): pack id, signed_at, notes, per-trade review tags ('followed plan?', mistake type), actions.
- D14 → Reviews tab: list of weeks with status (pending/signed/overdue); review page shows the pack and a sign-off form; phone flow ≤ 3 taps from the Telegram digest to sign-off.
- Reminder: Telegram nudge Monday 18:00 and Wednesday 18:00 if unsigned (configurable); overdue after 7 days → shown as overdue in D14 and as a warning on any capital-step proposal covering that week. Making a signed review part of the clean-week rule is an optional tightening (C1), off by default (16 §2.5).

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
- Given a pack is unsigned after 7 days, then the week shows 'overdue' and the capital-step proposal shows 'review missing for week N' as a warning (the week stays clean under the 16 §2.5 default).
- Given you add an action 'tighten BTC max position', then a task is created and linked.

### Stress / failure injection
- n/a: single-user, low volume; covered by integration tests.

## Acceptance criteria

- [ ] Sign-off works on web and phone; WORM rows written.
- [ ] Overdue reviews show in D14 and on capital-step proposals.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (clean week per 16 §2.5: an unsigned review is a warning, not a dirty week; R7.15 share)
