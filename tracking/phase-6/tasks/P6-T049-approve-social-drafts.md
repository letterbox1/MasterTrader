---
id: P6-T049
kind: task
title: Optional: approve, edit or skip social drafts and click Post yourself
phase: 6
type: USER
status: backlog
priority: low
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P6-T047]
requirements: [R6.31]
roadmap_todos: [T6.05]
modules: [M23]
dashboards: [D13]
branch: p6/P6-T049-approve-social-drafts
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T049 · Optional: approve, edit or skip social drafts and click Post yourself

## Goal / expected outcome

You review drafts in D13 (or Telegram), approve/edit/skip each, and click Post yourself in the web-intent window; you paste the post URL back.

## Context & references

- Roadmap: [R6.31](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.05
- Optional: only if P6-T003 recorded `yes`; otherwise cancel this item.
- Spec: [13 §8](../../../docs/13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social)
- UI: [D13](../../../docs/ui/dashboards/D13-tasks-curation.md) social drafts
- Depends on (this phase): P6-T047

## Requirements

- Only post what you genuinely mean; keep the disclosure line.
- Skip anything that reads like shilling.

## ToDo

- [ ] Open D13 → Social drafts.
- [ ] Approve/edit/skip; on approve, the X window opens prefilled — read it, click Post.
- [ ] Paste the post URL into the task to close it.
- [ ] Note in the progress log how many drafts you used vs skipped after one week.

## Verification

### Tests
- n/a: human action.

### Scenarios
- Given an approved draft, when you post and paste the URL, then the task is marked done with proof.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] At least one draft flow completed end-to-end (or module cancelled).

## Exceptions & edge cases

- You can turn M23 off at any time.

## Cardinal rules (do NOT)

- Do NOT post from any account other than your own.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §8: usage note.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.05 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T049-approve-social-drafts`
- PR title: `P6-T049: Optional: approve, edit or skip social drafts and click Post yourself`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
