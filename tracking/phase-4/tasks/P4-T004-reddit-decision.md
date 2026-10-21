---
id: P4-T004
kind: task
title: Confirm whether Reddit API access was granted
phase: 4
type: USER
status: backlog
priority: low
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T4.05]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T004-reddit-decision
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T004 · Confirm whether Reddit API access was granted

## Goal / expected outcome

A recorded yes/no on Reddit API access (applied for in P0 T0.08, before 2026-10-31). If **no** (expected), Reddit stays shown as *deferred* in D08 Sources. If **yes**, a follow-up optional BUILD item is filed for a PRAW connector, bearing in mind the reported 2027 sunset of the public Data API.

## Context & references

- Roadmap: ToDo [T4.05](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Scope 'Out' (Reddit optional)
- Timeline: [06 §0](../../../docs/06-aggregators-and-market-providers.md#0-️-time-sensitive-actions) (new access closes 2026-10-31; RSS ends 2026-11-13; Data API closes 2027-01 → 03, all U)
- Gap: P4-B009 (Reddit timeline likely makes this moot by P4).

## Requirements

- Record: was access granted (yes/no), client id stored in secrets if yes, and the date checked.
- If yes: the agent files `P4-T0xx Reddit connector (optional)` with official OAuth only; `train_ok = false` by default (12 §4).

## ToDo

- [ ] Check the email account used in T0.08 for Reddit's API decision.
- [ ] If granted: put `client_id`/`client_secret` into the sops/age secrets file (`secrets/mt.sops.yaml`, see [07 §2](../../../docs/07-security-notes.md#2-secrets)); never paste them anywhere else.
- [ ] Write the yes/no outcome in this task's progress log.

## Verification

### Tests
- n/a: decision record; if yes, the follow-up connector item carries its own tests.

### Scenarios
- Given no reply was received, then treat it as 'no' and keep Reddit deferred.

### Stress / failure injection
- n/a: decision step.

## Acceptance criteria

- [ ] Outcome recorded in the progress log
- [ ] D08 Sources shows Reddit as disabled with the reason when 'no'

## Exceptions & edge cases

- Reddit RSS and RSS-Bridge's Reddit bridge are not fallbacks (RSS ends 2026-11-13).

## Cardinal rules (do NOT)

- Do NOT use Reddit RSS or scraping as a substitute.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.05; note the outcome in §7 risks
- `docs/06-aggregators-and-market-providers.md`: update §0 Reddit row with the outcome

## Branch & PR

- Branch: `p4/P4-T004-reddit-decision`
- PR title: `P4-T004: Confirm whether Reddit API access was granted`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T004`

## Progress log

- 2026-10-21 00:00 · planner · created
