---
id: P5-T049
kind: task
title: UI: D13 Tasks & Curation (inbox, communities, digests, history)
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T011, P5-T029, P5-T030, P5-T047, P0-T050]
requirements: [R5.23, R5.20, R5.21, R5.22]
roadmap_todos: [T5.31]
modules: [M15, M19]
dashboards: [D13]
tools: [pnpm, node>=20]
mcp: []
env: []
services: [mt-api]
branch: p5/P5-T049-ui-d13-tasks-curation
pr: ""
doc_sync: [docs/ui/dashboards/D13-tasks-curation.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T049 · UI: D13 Tasks & Curation (inbox, communities, digests, history)

## Goal / expected outcome

D13 is live at `/tasks` with Inbox (TaskCards sorted by urgency and value, detail with numbered steps, verified links, warnings, EV inputs), Communities (status suggested → joined → following → verified → left, last post, leave-when), Digests (cadence per type, quiet hours, AU timezone, preview) and History — with swipe actions on phones and identical effect to Telegram buttons.

## Context & references

- Roadmap: [R5.23](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.20–R5.22 · ToDo T5.31
- Spec: [D13](../../../docs/ui/dashboards/D13-tasks-curation.md) · [mobile & Telegram](../../../docs/ui/mobile-and-telegram.md) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)

## Requirements

- Acceptance (D13): official verified links only (unverified never clickable); Done/Skip/Snooze also from Telegram with identical effect; Discord follow tasks flip to verified automatically.
- All canonical 03 M19 task types (incl. GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER, REG_CHANGE); EV inputs on airdrop/launch tasks; Details opens the same detail as the Telegram Details button.
- Communities tab shows the 7-day delivery re-prompt and ≤ 3 new servers per week defaults ([16 §2.13](../../../docs/16-configuration-and-safety-model.md#213-curation)).
- Phones: swipe right = Done, left = Snooze, with confirm for anything that touches funds; tap = detail sheet.
- Commands: `task.done|skip|snooze` C0, `task.never` C1, `system.settings.update` C0 (digests).

## ToDo

- [ ] Build `/tasks` tabs and TaskCard/detail; Communities table/cards; Digests settings + preview; History.
- [ ] Wire WS `tasks`; optimistic updates with server reconciliation.
- [ ] Playwright flows + viewport matrix + axe; doc sync.

## Verification

### Tests
- Playwright: Done in UI and simulated Telegram callback produce the same final state.
- Playwright: a follow task flips to verified when a mocked delivery event arrives.
- Playwright: viewport matrix + axe; swipe gestures on phone profiles.

### Scenarios
- Given a task's link fails the blocklist at render, then it shows as plain text with "unverified".
- Given a task that touches funds (REVOKE_APPROVAL), when swiped, then a confirm sheet appears.

### Stress / failure injection
- Inbox with 1,000 tasks remains responsive (virtualised; interaction < 100 ms).

## Acceptance criteria

- [ ] Four tabs complete per spec
- [ ] D13 acceptance 1–3 met
- [ ] Viewport matrix + axe pass

## Exceptions & edge cases

- Offline phone: actions queue and replay with idempotency keys.

## Cardinal rules (do NOT)

- Do NOT render connect-wallet, sign-permit, approve-unknown-contract, seed/key entry, multi-wallet or automated-social controls anywhere (D12/D18 never-offered lists).
- Do NOT enforce confirmation levels only in the UI; the server enforces C0–C3 (02 §7.2).
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D13-tasks-curation.md`: mark implemented (the task-type list is already canonical).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.31 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T049-ui-d13-tasks-curation`
- PR title: `P5-T049: UI: D13 Tasks & Curation (inbox, communities, digests, history)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (canonical task types incl. REG_CHANGE; Details; curation defaults per 16 §2.13; P0 app shell dep)
