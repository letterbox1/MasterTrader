---
id: P0-T053
kind: task
title: Run the Playwright viewport matrix and axe on the shell and D16
phase: 0
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T050, P0-T051, P0-T052, P0-T015]
requirements: [R0.N6, R0.11]
roadmap_todos: [T0.64]
modules: [M15]
dashboards: [D16]
branch: p0/P0-T053-playwright-viewport-matrix-axe
pr: ""
doc_sync: [DESIGN.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T053 · Run the Playwright viewport matrix and axe on the shell and D16

## Goal / expected outcome

CI runs Playwright across the full DESIGN §6.8 matrix (33 viewports, portrait + landscape, 240 → 2560 px) on the shell, the login screens, every D16 route and the `/__components` gallery, checking the seven pass criteria with automated assertions plus axe, and stores screenshots as artifacts.

## Context & references

- [Roadmap P0 R0.N6](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.64](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [DESIGN §6.8 test matrix](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- [DESIGN §6.7 touch](../../../DESIGN.md#67-touch--input)
- [DESIGN §9 accessibility](../../../DESIGN.md#9-accessibility)
- [03 M15](../../../docs/03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api) (Playwright matrix in CI)
- [Roadmap P0 §6 exit criteria](../../../docs/roadmap/phase-0-foundations.md#6-exit-criteria-demo) (4)
- Depends on: P0-T050, P0-T051, P0-T052, P0-T015

## Requirements

- Viewports exactly from DESIGN §6.8: desktop 2560×1440, 1920×1080, 1680×1050, 1536×864, 1440×900; laptop 1366×768, 1280×800, 1280×720; tablet landscape 1366×1024, 1194×834, 1180×820, 1024×768; tablet portrait 1024×1366, 834×1194, 820×1180, 768×1024; foldable 884×1104, 280×653, 300×750; phone portrait 430×932, 412×915, 390×844, 375×667, 360×780, 320×568; phone landscape 932×430, 844×390, 667×375, 568×320; floor 240×320.
- Per viewport × page assertions: (1) `document.documentElement.scrollWidth <= innerWidth`; (2) no clipped/overlapping text (element-overlap + `scrollWidth > clientWidth` on text nodes without `truncate`+tooltip); (3) kill switch + mode badge visible and reachable in ≤ 1 tap; (4) touch targets ≥ 44px with `hasTouch` contexts, ≥ 32px otherwise; (5) contrast via axe `color-contrast`; (6) no fixed element covers content (bounding-box intersection of fixed bars with main content); (7) 200 % zoom reflow at 1280 → 640 CSS px and 320 CSS px width check.
- axe-core: zero serious/critical violations on every page at 1920×1080 and 390×844.
- Runs on PRs touching `apps/web/**` (chromium only, all viewports) and nightly (chromium + webkit); screenshots uploaded as artifacts; total runtime ≤ 12 min (parallel shards).
- Kill-switch keyboard check: reachable within 2 Tab presses from the top bar (DESIGN §9).

## ToDo

- [ ] Write `apps/web/e2e/matrix.spec.ts` with the viewport table and the seven checks as reusable helpers.
- [ ] Add axe checks and the keyboard check.
- [ ] Run against the built app served by a test Caddy + mocked mt-api (MSW or a fixture server).
- [ ] Wire into CI `web` job with sharding and artifacts.
- [ ] Fix any failures found (or file bugs in this phase).

## Verification

### Tests
- The matrix itself; plus a negative fixture page with a `w-[300px]` fixed element that must fail check 1 at 240 px (proves the check works).

### Scenarios
- Given a developer adds an unprefixed `grid-cols-12`, when CI runs at 320×568, then check 1 or 2 fails with a screenshot.
- Given a fixed status bar overlaps content, then check 6 fails.

### Stress / failure injection
- n/a: deterministic visual checks; runtime budget ≤ 12 min tracked.

## Acceptance criteria

- [ ] All 33 viewports × (shell, login, 5 D16 routes, gallery) pass the seven checks
- [ ] axe: zero serious/critical
- [ ] Negative fixture fails as expected
- [ ] Required in CI for `apps/web/**` changes
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Webkit flakiness on fonts: wait for `document.fonts.ready` before measuring.
- Very-short (≤ 400 px tall) cases rely on `very-short` rules; screenshots reviewed once manually.

## Cardinal rules (do NOT)

- Do NOT drop viewports or loosen thresholds to get green.
- Do NOT snapshot-approve visual diffs without reviewing them.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `DESIGN.md` §6.8: link the spec file as the reference implementation of the matrix.
- `docs/roadmap/phase-0-foundations.md`: tick T0.64 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T053-playwright-viewport-matrix-axe`
- PR title: `P0-T053: Run the Playwright viewport matrix and axe on the shell and D16`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
