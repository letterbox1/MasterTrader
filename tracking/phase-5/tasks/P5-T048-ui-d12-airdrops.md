---
id: P5-T048
kind: task
title: UI: D12 Airdrops & Launches (radar, detail, wallet & mandates)
phase: 5
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T011, P5-T041, P5-T043, P5-T044, P5-T046, P0-T050]
requirements: [R5.23]
roadmap_todos: [T5.31]
modules: [M15, M4, M19, M18]
dashboards: [D12]
tools: [pnpm, node>=20, uv]
mcp: []
env: []
services: [mt-api]
branch: p5/P5-T048-ui-d12-airdrops
pr: ""
doc_sync: [docs/ui/dashboards/D12-airdrops.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T048 · UI: D12 Airdrops & Launches (radar, detail, wallet & mandates)

## Goal / expected outcome

D12 is live at `/airdrops`, `/airdrops/:id` and `/airdrops/wallet`: radar with filters and Viable/Watching/Rejected/Claims segments, detail with overview, risk report (hard fails, findings, raw provider reports collapsed), viability/EV breakdown, eligibility, path (auto-claim with simulation diff or task steps) and history; wallet page with the airdrop identity wallets and burners (not the hot trading wallet), mandates (create = C3), approvals audit and exec log — passing the viewport matrix.

## Context & references

- Roadmap: [R5.23](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.31
- Spec: [D12](../../../docs/ui/dashboards/D12-airdrops.md) · components `RiskScoreBadge`, `TaskCard` ([components](../../../docs/ui/components.md)) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · [UI README](../../../docs/ui/README.md)
- Backend: queries/commands from P5-T011; WS topics `airdrop`, `tasks`, `kill`

## Requirements

- Radar card: identity, kind, stage, RiskScoreBadge (top 3 reasons), viability incl. **AU geo/KYC**, EV range, deadlines, eligibility, next action.
- Acceptance (D12): every rejected opportunity shows reasons; every auto-claim shows mandate + simulation + tx + journal links; AU restrictions visible before any task.
- Links re-checked against blocklists at render; unsafe links as plain text with warning.
- Actions: re-score C0, reject C1, add URL C0, execute claim C2 (simulation shown), create mandate C3, revoke mandate C1, revoke approval C2, sweep C2.
- Kill switch ON: banner and auto-claim controls disabled.
- Identity wallet widget: balance vs float (default ≤ A$300 per chain; burners ≤ A$50), gas budget used today (default A$20/day, alert at 80%), signer cap usage (defaults A$250 per transaction, A$1,000 per rolling 24 h), all read from the limits store ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)), never hard-coded.
- History shows the manual-sale disposal task for each claim (P5-B010).
- Layouts per tier (≥ 2xl 6/12/6; xl–md stacked; ≤ ph segmented cards); live updates p95 < 500 ms; tables ≤ 1 Hz.

## ToDo

- [ ] Build routes/components in `packages/mt_ui/web/` (or the P0 frontend app) using the DESIGN v2 preset.
- [ ] Wire queries, WS topics and command sheets with C-level UX (C2 hold-to-confirm on touch; C3 shows Telegram pending state).
- [ ] Playwright tests: flows + viewport matrix + axe; never-offered controls absent.
- [ ] Update D12 doc if any field/route changed.

## Verification

### Tests
- Playwright: radar filters, detail sections, mandate creation shows C3 pending until Telegram approval (mocked).
- Playwright: viewport matrix (DESIGN §6.8, 240 → 2560 px) + axe on all three routes.
- Playwright: a rejected item shows reasons; an auto-claim history row links mandate/simulation/tx/journal.

### Scenarios
- Given kill ON, when the user opens /airdrops/wallet, then the red banner shows and claim/execute controls are disabled.
- Given a link added to a blocklist, when the detail renders, then it is plain text with a warning.

### Stress / failure injection
- Radar with 2,000 opportunities: virtualised list, first render < 1.5 s on the laptop profile.

## Acceptance criteria

- [ ] Three routes complete per D12 spec
- [ ] D12 acceptance criteria 1–2 met
- [ ] Viewport matrix + axe pass
- [ ] No never-offered controls (test)

## Exceptions & edge cases

- WS gap: re-sync via REST on `seq` gap; mt-api down: read-only banner.

## Cardinal rules (do NOT)

- Do NOT render connect-wallet, sign-permit, approve-unknown-contract, seed/key entry, multi-wallet or automated-social controls anywhere (D12/D18 never-offered lists).
- Do NOT enforce confirmation levels only in the UI; the server enforces C0–C3 (02 §7.2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D12-airdrops.md`: mark implemented; note any deviations.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.31 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T048-ui-d12-airdrops`
- PR title: `P5-T048: UI: D12 Airdrops & Launches (radar, detail, wallet & mandates)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (identity wallets not hot per P5-B017; limits from 16 §2.7; disposal tasks in history; P0 app shell dep)
