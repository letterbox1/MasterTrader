---
id: P4-T065
kind: task
title: D02 positioning, sentiment, prediction-market and nowcast widgets go live
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T039, P4-T041, P4-T036, P4-T043, P1-T049]
requirements: [R4.11, R4.09]
roadmap_todos: [T4.32]
modules: [M6, M3]
dashboards: [D02]
tools: [pnpm, node>=20, uv, git]
mcp: []
env: []
services: [postgres, mt-api]
branch: p4/P4-T065-d02-positioning-sentiment-prediction-market-and-
pr: ""
doc_sync: [docs/ui/dashboards/D02-markets.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T065 · D02 positioning, sentiment, prediction-market and nowcast widgets go live

## Goal / expected outcome

The D02 widgets that P1 shipped with an 'Arrives in Phase 4' empty state now show live data: the macro strip gains nowcasts (GDPNow, Cleveland Fed inflation), and the Positioning panel gains retail sentiment (Myfxbook / IG / OANDA books) and Kalshi/Polymarket event probabilities, served by `/markets/matrix?group=macro|positioning` from the P4 ingestion (P4-T039, P4-T036) and features (P4-T041).

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) ("the D02 widgets that show 'arrives in P4' go live") · [R4.09](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.32](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- UI: [D02 Macro strip / Positioning](../../../docs/ui/dashboards/D02-markets.md) ('Arrives in P4' rows; never placeholder data, DESIGN §10)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P1-B003/B004/B012): D02 shows 'arrives in P4' states for P4-fed widgets
- Cross-phase (`depends_on`): P1-T049 (D02 matrix + macro strip with the empty states)
- Related: P4-T039 (positioning/nowcast ingestion), P4-T036 (prediction markets, Polymarket disabled for AU), P4-T041 (positioning z / nowcast surprise features), P4-T043 (API), P4-T059 (viewport matrix).

## Requirements

- `/markets/matrix?group=macro` adds GDPNow and Cleveland Fed nowcast tiles (value, last vintage time, change vs previous vintage); `group=positioning` adds retail long % + contrarian z per FX/metal pair (per source) and event probabilities with 1-day change.
- Each tile names its source and shows its freshness; disabled sources (e.g. OANDA books if P1-T056 failed, Polymarket while residency is AU) render a disabled state with the reason, never sample data.
- WS updates throttled ≤ 1 Hz per tile (02 §6); PIT-correct values only (latest vintage as of now).
- Remove the 'Arrives in Phase 4' state only for widgets whose source is live; keep it for anything still pending.

## ToDo

- [ ] Extend the `/markets/matrix` macro/positioning groups in `mt_api` (OpenAPI + types)
- [ ] Wire the D02 macro strip and Positioning panel components to the new fields
- [ ] Disabled-with-reason and stale states
- [ ] Playwright specs at sm/md/xl + axe
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- API: macro/positioning groups return the new fields with source + freshness.
- Playwright: a seeded GDPNow vintage and a Myfxbook snapshot render in D02; a disabled Polymarket shows its reason.
- Unit: tile formatter for probabilities and contrarian z.

### Scenarios
- Given Myfxbook is down, then its tiles go stale with the last update time and IG/OANDA keep showing.
- Given a new GDPNow vintage arrives, then the tile updates within one WS cycle and keeps the previous vintage for the change.

### Stress / failure injection
- n/a: low-volume views; the viewport matrix runs in P4-T059.

## Acceptance criteria

- [ ] Macro strip shows nowcasts; Positioning shows retail sentiment and event probabilities
- [ ] No 'Arrives in Phase 4' state remains for a live source; no placeholder data anywhere
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix + axe)

## Exceptions & edge cases

- OANDA books endpoint unavailable (P1-T056 result): that column is disabled with the reason.
- Polymarket stays disabled while residency is AU (never via VPN/proxy, 12 §1).

## Cardinal rules (do NOT)

- Do NOT show sample or placeholder data.
- Do NOT call providers from the browser; only `mt_api`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D02-markets.md`: remove 'Arrives in P4' for the widgets now live
- `docs/roadmap/phase-4-intel.md`: tick T4.32 when P4-T036 and P4-T039 are also done

## Branch & PR

- Branch: `p4/P4-T065-d02-positioning-sentiment-prediction-market-and-`
- PR title: `P4-T065: D02 positioning, sentiment, prediction-market and nowcast widgets go live`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T065` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T4.32 D02 widgets go live (17 §D P1-B003/B004/B012))
