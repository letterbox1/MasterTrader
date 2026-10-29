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
depends_on: [P0-T001]
requirements: []
roadmap_todos: [T4.05]
modules: [M2]
dashboards: [D08]
tools: []
mcp: []
env: []
services: [reddit-api]
branch: p4/P4-T004-reddit-decision
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md, docs/06-aggregators-and-market-providers.md]
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

# P4-T004 · Confirm whether Reddit API access was granted

## Goal / expected outcome

A recorded yes/no on Reddit API access (applied for in P0 T0.08, before 2026-10-31). If **no** (expected), Reddit stays shown as *deferred* in D08 Sources. If **yes**, a follow-up optional BUILD item is filed for a PRAW connector, bearing in mind the reported 2027 sunset of the public Data API.

## Context & references

- Roadmap: ToDo [T4.05](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Scope 'Out' (Reddit optional)
- Timeline: [06 §0](../../../docs/06-aggregators-and-market-providers.md#0-️-time-sensitive-actions) (new access closes 2026-10-31; RSS ends 2026-11-13; Data API closes 2027-01 → 03, all U)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B009): Reddit stays optional. If access wasn't granted by the 2026-10-31 deadline, Reddit stays out and needs no build item.
- Cross-phase: P0-T001 (T0.08, the application before 2026-10-31) is a `depends_on` entry.

## Requirements

- Record: was access granted (yes/no), client id stored in secrets if yes, and the date checked.
- If yes: the agent files `P4-T0xx Reddit connector (optional)` with official OAuth only, built to the commitments made in the 2026-10-29 request ([12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)): read-only; the requested subreddits only; ~4–6 requests/min with back-off; hourly per-asset aggregates only (`train_ok = false`, `model_input_ok` for the aggregates only); no usernames stored; raw text deleted within 24 h and never written to WORM/journal tables; local sentiment model only, never a third-party AI service; no training or fine-tuning. Only worth building if the public Data API isn't closing before it would be useful (06 §0: 2027-01 → 03 (U)).
- If no: Reddit is out; D08 Sources shows it as not available, and nothing is built.

## ToDo

- [ ] Check the email account used in T0.08 for Reddit's API decision.
- [ ] If granted: put `client_id`/`client_secret` into the sops/age secrets file outside the repo (`/etc/mastertrader/secrets.sops.yaml`, P0-T022; see [07 §2](../../../docs/07-security-notes.md#2-secrets)); never paste them anywhere else.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Reddit optional per 17 §D (P4-B009); secrets file outside the repo (17 §D P0-B018); depends on P0-T001)
