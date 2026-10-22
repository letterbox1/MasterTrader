---
id: P2-T038
kind: task
title: Approvals API, ApprovalCard component and approvals sheet
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T033, P2-T020, P0-T036, P0-T048, P0-T049]
requirements: [R2.51, R2.54]
roadmap_todos: [T2.32, T2.34]
modules: [M15, M11]
dashboards: [D01, D05, D03]
tools: [uv, pnpm]
mcp: []
env: []
services: [nats]
branch: p2/P2-T038-approvals-api-approvalcard
pr: ""
doc_sync: [docs/ui/components.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T038 · Approvals API, ApprovalCard component and approvals sheet

## Goal / expected outcome

Web approvals work end to end: `/approvals?status=pending`, `/bots/{id}/approvals`, WS approval events, `approval.approve` (C2) / `approval.approve_partial` / `approval.reject`, a shared `ApprovalCard` component (risk preview, reasons, chart link, TTL countdown, hold-to-confirm) and the top-bar approvals sheet; Part B embeds the card in D01 Needs-you and D05 Approvals.

## Context & references

- Roadmap: [R2.51, R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDos T2.32, T2.34
- Design: [15 §1.3 card content](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) · [components ApprovalCard](../../../docs/ui/components.md) · [ui §3.3 C2 hold-to-confirm](../../../docs/ui/README.md#33-actions--confirmation)
- UI: [D05 Approvals](../../../docs/ui/dashboards/D05-execution.md) · [D01 Needs you](../../../docs/ui/dashboards/D01-cockpit.md)
- Decisions: [17 §D P2-B058](../../../docs/17-decisions-register.md#d-other-decisions) (web card = Telegram card capabilities; **no bulk approve** except the batched dynamic-selection card, 15 §1.3) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (TTLs; large orders > 2% of sleeve or > A$5,000 → hold-to-confirm on web; MCP cards TTL 5 min).
- Cross-phase (`depends_on`): WS hub (P0-T036), typed API/WS client (P0-T048), component library v0 incl. confirm sheets (P0-T049).
- P2-T142 (D01) and P2-T149 (D05) own the page layouts; this task delivers the component + API.

## Requirements

- Queries: `/approvals?status=pending|decided`, `/bots/{id}/approvals`; WS topic `approvals` (new, decided, expired).
- Commands: `approval.approve` (C2), `approval.approve_partial` (C2, fraction 0.5, bot requests), `approval.reject` (C1), `bot.pause` (C1); large orders (default > 2% of sleeve or > A$5,000 notional) need **hold-to-confirm** on web (TOTP on Telegram, P2-T039).
- Batched card for one dynamic-selection bot: per-line toggles, one combined risk preview, `approval.approve` with the selected lines (C2). No other bulk approve.
- `ApprovalCard` props: request (bot, instrument, side, size, type/price, stop/target, risk preview R & % of sleeve, exposure after fill, blackout/DQ warnings, reasons, chart deep link), TTL countdown synced to server time, buttons Approve / Approve ½ / Reject / Pause bot; expired → moves to history automatically.
- Top-bar approvals icon count + sheet listing pending cards.
- Phone: approve in ≤ 2 taps after opening (D05 acceptance 1).

## ToDo

- [ ] mt_api routers + WS topic
- [ ] `apps/web/src/components/trading/ApprovalCard.tsx` + stories + tests
- [ ] Approvals sheet + top-bar count
- [ ] Playwright flow test
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- API tests: approve after expiry → 409 'expired'; double approve → idempotent.
- Component tests: countdown, expiry state, disabled buttons after decision.
- Playwright: approve from the sheet on 390×844 in ≤ 2 taps.

### Scenarios
- Given a pending card with 10 s left, when the TTL hits 0, then the card shows 'Expired' and buttons disable on every open client.
- Given you tap Approve ½ on web, when processed, then the order re-checks risk at half size and the card shows the outcome.

### Stress / failure injection
- 50 pending approvals: sheet renders < 200 ms; WS updates throttled ≤ 1 Hz per card.

## Acceptance criteria

- [ ] API + component + sheet live
- [ ] TTL countdown matches server ±1 s
- [ ] Viewport matrix passes (covered in P2-T062)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- WS gap: client re-syncs via `/approvals` (seq gap detection).
- Clock skew on device: countdown uses server `ts`.

## Cardinal rules (do NOT)

- Do NOT let the UI decide expiry; the server decides.
- Do NOT approve multiple cards with one tap; the only exception is the batched card of one dynamic-selection bot (17 §D, 15 §1.3).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/components.md`: ApprovalCard props as built.
- `docs/02-v1-architecture.md` §7.3: `approvals` WS topic.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32, T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T038-approvals-api-approvalcard`
- PR title: `P2-T038: Approvals API, ApprovalCard component and approvals sheet`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no bulk approve except batched dynamic card (17 §D), large-order hold-to-confirm per 16 §2.3, cross-phase UI deps)
