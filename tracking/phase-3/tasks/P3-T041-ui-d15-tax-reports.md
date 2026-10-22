---
id: P3-T041
kind: task
title: D15 Tax and Reports dashboard
phase: 3
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T039, P3-T029, P3-T036, P3-T055, P0-T048, P0-T049, P0-T050]
requirements: [R3.14]
roadmap_todos: [T3.29]
modules: [M18, M15]
dashboards: [D15]
tools: [git, node>=20, pnpm]
mcp: []
env: []
services: [mt-api]
branch: p3/P3-T041-ui-d15-tax-reports
pr: ""
doc_sync: [docs/ui/dashboards/D15-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T041 · D15 Tax and Reports dashboard

## Goal / expected outcome

`/tax` implements D15 with tabs Summary · Capital gains · Income · PAYG · Lots · Residency · Reports · Questions: FY selector, jurisdiction badge from residency, regime badge (investor / trader / both), both-ways summary cards with rule version and FX source, discount-boundary rule-check panel, wash-sale warnings, Egypt red flag, snapshot status, and "Not tax advice" in every footer — exit criterion 2 on screen.

## Context & references

- Roadmap: [R3.14, T3.29](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 2 · dashboard spec [D15](../../../docs/ui/dashboards/D15-tax.md)
- Mock-up fix list in D15 (lot method, FY labels, citations, not-advice) · viewport matrix [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase prerequisites (depends_on): P0-T048 (typed API + WS client), P0-T049 (component library, confirm sheets), P0-T050 (app shell)
- Commands: [D15 actions](../../../docs/ui/dashboards/D15-tax.md) (lock/unlock FY C3, unlock needs a reason; `task.answer` C1; residency add C1 with preview, C3 if it loosens) · decisions [17 §D P3-B005/B006/B007/B016](../../../docs/17-decisions-register.md#d-other-decisions)

## Requirements

- Summary: `TaxSummaryCard`s for net capital gain, carried-forward losses, revenue/trading income, Div 775, crypto income, foreign income + tax paid, estimated tax impact (informational); each card shows rule version (AU_2026 / AU_2027_REFORM) + FX source (RBA); regime toggle shows both computations.
- Capital gains: per-event table (acquired, disposed, holding days both excluded, discount eligibility, cost base, proceeds, gain/loss, method, wash-sale flag).
- Income, PAYG (quarters, due dates, basis excluding capital gains, **both ATO methods** — notice amount and rate × instalment income — with the one your notice uses marked, history), Lots (`LotTable` incl. FX-cash lots, unrealised, discount-eligible countdown, 30 Jun 2027 snapshot status, I1 snapshot), Residency (timeline, active plugin per period, I1 both ways), Reports (generate/export, history with hashes), Questions (TAX_QUESTION list incl. perps treatment (default revenue (U)), status, answers via `task.answer` C1; an answer can set the regime).
- Actions/levels: generate C1, export C0, residency add C1 with preview (C3 when the registry diff loosens), regime set C1 (after an answer), lot select C1 (audited), answer a question C1, **lock / unlock FY C3** (unlock needs a reason; held-event count shown while locked).
- Rule-check panel shows the golden discount boundary (bought 2 Feb → eligible 3 Feb next year) result from the server.
- Every number drills down to journal events (D15 acceptance 1).

## ToDo

- [ ] Routes `apps/web/src/routes/tax/*`, components `TaxSummaryCard`, `LotTable`, residency timeline
- [ ] Confirm sheets for C1 actions (preview for residency)
- [ ] Playwright matrix + axe; Vitest
- [ ] Docs

## Verification

### Tests

- Playwright: all tabs across the viewport matrix; axe no serious violations; footer text present on every tab.
- E2E: set regime with an answered question → badge changes; without → server refusal displayed.
- Vitest: drill-down link from a summary card leads to the filtered events list.

### Scenarios

- Given no agent answer, when Summary opens, then both columns show and the regime badge reads `both`.
- Given residency EG is active, when any crypto row is shown, then a red compliance flag appears.
- Given you unlock a locked FY, when you confirm, then the C3 flow (Telegram approve + TOTP + cool-down) starts and the page shows it pending.
- Given the 30 June 2027 snapshot is incomplete, when Lots opens, then a red banner links the runbook.

### Stress / failure injection

- Lots tab with 200k lots stays responsive (virtualised; server pagination).

## Acceptance criteria

- [ ] All 8 tabs per spec
- [ ] Both-ways summary + PAYG visible with provenance (exit criterion 2)
- [ ] Viewport matrix + axe green
- [ ] Not-advice footer on every tab
- [ ] CI green (lint, types, tests, `pit` check, Playwright viewport matrix + axe; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- ≤ ph: tabs as a select, lots as cards.
- FY with `needs_classification` items → blocking notice on Summary.

## Cardinal rules (do NOT)

- Do NOT render any edit control on journal records; corrections are server-side superseding events.
- Do NOT compute tax figures in the browser; the UI only displays server results.
- Do NOT hide the not-advice footer at any breakpoint.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D15-tax.md`: tick acceptance criteria; note deviations.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.29 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T041-ui-d15-tax-reports`
- PR title: `P3-T041: D15 Tax and Reports dashboard`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T041` run · Playwright matrix screenshots attached

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (PAYG both methods (P3-B005), FY lock/unlock C3 and `task.answer` C1 (P3-B006), residency loosening C3 (P3-B007), perps question (P3-B016); P3-T055 + P0 depends_on; tools/services filled)
