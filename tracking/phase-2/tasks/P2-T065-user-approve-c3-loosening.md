---
id: P2-T065
kind: task
title: Approve a test C3 loosening with TOTP and cool-down
phase: 2
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T053, P0-T062]
requirements: [R2.19]
roadmap_todos: [T2.07]
modules: [M11]
dashboards: [D06]
tools: []
mcp: []
env: []
services: [telegram, mt-web]
branch: p2/P2-T065-user-approve-c3-loosening
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T065 · Approve a test C3 loosening with TOTP and cool-down

## Goal / expected outcome

You prove the TOTP + cool-down path by approving one real (paper) risk loosening — exit criterion 3 (C3 part).

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.07 · exit criterion 3
- [mob §3 C3 confirmations](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [16 §2.3 C3 cool-down 15 min](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)
- Decision: Telegram C3 replaces the P0 break-glass CLI once it works ([17 §D P0-B002](../../../docs/17-decisions-register.md#d-other-decisions), roadmap T2.24); this task proves it and then retires break-glass.
- Cross-phase (`depends_on`): your TOTP (P0-T062).

## Requirements

- Pick a harmless loosening, e.g. paper trend sleeve max open positions 10 → 11.
- Do it from the phone (web or Telegram) to also prove mob §4 acceptance 2.

## ToDo

- [ ] In D06 Policy, change the value and Save
- [ ] In Telegram: Approve → enter TOTP
- [ ] Watch the cool-down (15 min) and the 'Applied' message
- [ ] Revert with a tightening (applies instantly)
- [ ] Retire the break-glass path: set `c3.break_glass_enabled = false` in D16 settings (a tightening, C1); confirm `mtctl approve` is now refused
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T065`

## Verification

### Tests
- Agent checks `risk.change` rows: pending → applied with your approval refs; revert applied immediately.

### Scenarios
- Given you enter a wrong TOTP first, when submitted, then it is rejected and you can retry within the window.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Loosening applied only after TOTP + cool-down
- [ ] Revert applied instantly
- [ ] Break-glass C3 path retired (setting off, `mtctl approve` refused)

## Exceptions & edge cases

- Missed the approval window: request expires; repeat.

## Cardinal rules (do NOT)

- Do NOT share your TOTP seed or codes anywhere.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/07-security-notes.md` §6: note C3 tested on phone.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.07 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T065-user-approve-c3-loosening` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T065: Approve a test C3 loosening with TOTP and cool-down`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T065` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (retire the P0 break-glass C3 path after Telegram C3 passes (T2.24, 17 §D); cool-down default)
