---
id: P7-T002
kind: task
title: Close or explicitly defer the lawyer advice items
phase: 7
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.13]
roadmap_todos: [T7.07]
modules: [M19]
dashboards: [D13]
branch: p7/P7-T002-lawyer-advice-items
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T002 · Close or explicitly defer the lawyer advice items

## Goal / expected outcome

Each lawyer item from 12 §6 is either answered in writing or explicitly deferred, and every venue/product that depends on a deferred item stays `blocked`/`read_only` in the venue registry.

## Context & references

- Roadmap: [R7.13 · ToDo T7.07](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) · [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (Hyperliquid, market-manipulation reach to spot tokens) · [D13](../../../docs/ui/dashboards/D13-tasks-curation.md) `PRO_ADVICE` task type
- Related: P7-T010 (register links each advice item to registry blocks), P7-T003 (venue checks), P7-T011 (preflight)

## Requirements

- Items: (1) whether market-manipulation law reaches spot tokens; (2) Hyperliquid exposure for an Australian; (3) a written 'private, non-commercial' boundary and what triggers a review.
- Each item ends in one state: `answered` (summary + document reference) or `deferred` (reason + revisit date); `deferred` keeps dependent products blocked (R7.13).
- Hyperliquid (trading and HLP) stays `read_only` unless item (2) is `answered` with a go-ahead and a consistent KYC country/location (12 §1).
- Optional and paid by you: the platform never buys advice; if you skip it, mark `deferred`.

## ToDo

- [ ] Open D13 → filter `PRO_ADVICE`; confirm the three lawyer tasks exist (P7-T010 seeds them if not).
- [ ] Decide per item: engage a lawyer, or defer. Record the decision in the task (summary, no client privilege text pasted).
- [ ] For answered items: attach the advice document via the upload control (encrypted store), set state `answered`.
- [ ] For deferred items: write the reason and a revisit date (default: next quarterly registry re-check).
- [ ] Check D06 → Venues: Hyperliquid stays `read_only` unless item (2) says otherwise; if it says go, request the registry change (C3) yourself.

## Verification

### Tests
- n/a (user action); P7-T010 tests that a `deferred` item keeps linked products blocked.

### Scenarios
- Given item (2) is deferred, when a bot targets Hyperliquid perps, then M11 rejects with reason `pending_advice:<task_id>`.
- Given item (3) is answered, then the boundary text summary is visible on the task and the review triggers are listed.

### Stress / failure injection
- n/a: one-off user decisions.

## Acceptance criteria

- [ ] All three lawyer items are `answered` or `deferred` with a reason and revisit date.
- [ ] No product linked to a deferred item is `allowed` in `ops.venue_registry`.
- [ ] Preflight (P7-T011) shows the professional-advice criterion green.

## Exceptions & edge cases

- Advice conflicts with the registry seed: the stricter outcome wins until you change the registry through C3.
- Residency change: all items re-open for the new jurisdiction (12 §1 'Moving countries').

## Cardinal rules (do NOT)

- Do NOT unblock Hyperliquid or any derivative product without a written answer.
- Do NOT paste privileged advice text into issues or chats; summarise.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT open multiple KYC accounts, use VPNs/proxies, or self-match across sub-accounts (12 §3).

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §6: mark each item answered/deferred with the date (no advice text).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.07 when this item is done.

## Branch & PR

- Branch: `p7/P7-T002-lawyer-advice-items`
- PR title: `P7-T002: Close or explicitly defer the lawyer advice items`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T002` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
