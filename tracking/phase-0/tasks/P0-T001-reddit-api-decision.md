---
id: P0-T001
kind: task
title: Decide on Reddit and apply for API access before 2026-10-31
phase: 0
type: USER
status: ready
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T0.08]
modules: [M2]
dashboards: []
tools: []
mcp: []
env: []
services: [reddit]
branch: p0/P0-T001-reddit-api-decision
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T001 · Decide on Reddit and apply for API access before 2026-10-31

## Goal / expected outcome

A recorded yes/no decision on Reddit as an optional source, made **before 2026-10-31** (Reddit reportedly stops accepting new API access requests then). If yes, the free personal API application is submitted from a dedicated account and its credentials are stored safely. Nothing in the plan depends on Reddit, so "no" is a valid outcome; the point is not to lose the option by missing the deadline.

## Context & references

- [Roadmap P0 T0.08](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [06 §0 time-sensitive actions](../../../docs/06-aggregators-and-market-providers.md#0-️-time-sensitive-actions)
- [06 §2 social stack](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)
- [07 §10 social accounts](../../../docs/07-security-notes.md#10-social--scraping-accounts)
- [12 §4 platform rules](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- [Roadmap §4 fixed dates](../../../docs/roadmap/README.md#4-fixed-external-dates)
- Unblocks: optional Reddit connector in P4 only

## Requirements

- Deadline: application submitted (or decision 'no' recorded) by **2026-10-31** (target 2026-10-28 to leave slack).
- Dedicated Reddit account (not your personal one), 2FA on, used read-only; official OAuth API only (PRAW), never scraping or Reddit RSS (reported to end 2026-11-13).
- Reddit is a *sunsetting* source (06 §0): never core; no AI training on Reddit data without approval (12 §4).
- Outputs: client id / secret / user agent → the sops secrets file `~/.config/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022). Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Read 06 §0 and decide: is a sunsetting, optional Reddit feed worth one account? Write the decision and reason in this task's progress log.
- [ ] If **no**: log `decision: no Reddit`, tick the remaining boxes as `n/a` in the log, and finish.
- [ ] If **yes**: create a dedicated Reddit account with a unique email and 2FA (authenticator app).
- [ ] Go to reddit.com/prefs/apps → 'create another app' → type **script**, name `mastertrader-reader`, redirect `http://localhost:8080` (unused); then submit the Data API access request form for personal, non-commercial, read-only use.
- [ ] Record client id, client secret and a user agent of the form `linux:mastertrader-reader:0.1 (by /u/<account>)` in your password manager now; move them into the secrets file under `reddit:` once P0-T022 lands.
- [ ] Log the submission date and any ticket/confirmation number (not the secret) in the progress log.

## Verification

### Tests
- n/a (USER action); confirmation is the Reddit app page showing the app and the request acknowledgement.

### Scenarios
- Given the decision is 'yes', when the request is submitted before 2026-10-31, then the app id appears on reddit.com/prefs/apps and the log has the date.
- Given the request is refused or never answered, then Reddit stays deferred and P4 proceeds without it (no rework).

### Stress / failure injection
- n/a: account action, no system behaviour.

## Acceptance criteria

- [ ] Decision (yes/no + reason) logged by 2026-10-31
- [ ] If yes: application submitted by 2026-10-31 and credentials held only in the password manager / secrets file
- [ ] No Reddit credential appears in git, chat or any ticket

## Exceptions & edge cases

- Reddit closes intake early: log it and treat Reddit as unavailable; X stays deferred regardless.
- Approval arrives during P4+: the connector is optional in P4 and must stay off the critical path.

## Cardinal rules (do NOT)

- Do NOT use your personal Reddit account or create several accounts.
- Do NOT build anything on Reddit RSS or RSS-Bridge's Reddit bridge (sunset 2026-11-13).
- Do NOT apply for X API access (deferred, paid).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md` §0: record the decision and date (yes/no) in the Reddit row.
- `docs/roadmap/phase-0-foundations.md`: tick T0.08 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T001-reddit-api-decision`
- PR title: `P0-T001: Decide on Reddit and apply for API access before 2026-10-31`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); run fields added)
