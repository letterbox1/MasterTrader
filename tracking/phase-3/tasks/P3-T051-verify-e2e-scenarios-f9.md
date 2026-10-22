---
id: P3-T051
kind: task
title: End-to-end scenarios for the tax flow F9 and D14/D15
phase: 3
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T013, P3-T014, P3-T018, P3-T034, P3-T040, P3-T041, P3-T055, P3-T056, P2-T001]
requirements: [R3.01, R3.03, R3.04, R3.13, R3.14, R3.15, R3.16, R3.17]
roadmap_todos: [T3.20, T3.29]
modules: [M18]
dashboards: [D14, D15]
tools: [git, uv, node>=20, pnpm, docker]
mcp: []
env: []
services: [postgres, nats, mt-api, journal, engine, Binance testnet]
branch: p3/P3-T051-verify-e2e-scenarios-f9
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T051 · End-to-end scenarios for the tax flow F9 and D14/D15

## Goal / expected outcome

Scripted end-to-end scenarios run on the full stack (paper engine → journal → lots → AU_2026 → D14/D15) and prove the F9 flow and the dashboards' acceptance criteria, including unhappy paths.

## Context & references

- Roadmap: [R3.01, R3.03, R3.04, R3.13, R3.14](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Flows: [02 F2 step 7, F9](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · acceptance [D14](../../../docs/ui/dashboards/D14-journal.md), [D15](../../../docs/ui/dashboards/D15-tax.md), [D16 Accounts](../../../docs/ui/dashboards/D16-system.md)
- Cross-phase prerequisite (depends_on): P2-T001 (trade-only testnet keys used by the paper engine for the one live S1 run; no money)

## Requirements

- Scenarios (Playwright + API, in `tests/e2e/journal/`):
- S1 paper fill on Binance testnet → D14 row ≤ 5 s with fee, AUD/USD/native, FX source; lot opened; D15 Lots shows it.
- S2 perp funding payment → event via ccxt ledger → D15 Income/revenue item.
- S3 internal transfer exchange → own address with fee → no disposal; lots relocate.
- S4 sell across lots with a `tax.lot.select` (C1) → specific-ID match; without → FIFO with reason.
- S5 crypto↔crypto swap → disposal + new lot.
- S6 restated fee from a statement → correction chain visible in D14; nothing edited.
- S7 regime set without an answer → refused; with Q1 answered (test data) → badge changes; both columns until then.
- S8 residency EG test period (scratch env) → `tax.residency.changed` → venue registry blocks crypto → crypto order rejected by M11, D15 red flag; removing it requires C3.
- S9 recon break injected → alert on Telegram/ntfy/UI, D14 widget red, runbook resolves it.
- S10 report generate twice → same hash; export accountant pack.
- S11 staking reward with no AUD-venue trades in its minute → valued by USD VWAP × RBA with method shown in D14 (16 §4.1); no aggregator value stored.
- S12 register an address and tag it `investment` on the D16 Accounts page → a transfer to it is internal (no disposal).
- S13 lock FY (C3) → a late event is held; unlock (C3, reason) → it lands; a note with a screenshot stores the file once under `data/attachments/<sha256>`.

## ToDo

- [ ] Write scenario scripts + fixtures
- [ ] Run on the full compose stack (CI nightly + before the exit demo)
- [ ] Record results

## Verification

### Tests

- The scenarios above, automated.

### Scenarios

- S1–S13 as listed (each has given/when/then in the script docstring).

### Stress / failure injection

- n/a here (see P3-T052)

## Acceptance criteria

- [ ] S1–S13 pass on the full stack
- [ ] Results + screenshots attached to the PR

## Exceptions & edge cases

- Testnet flakiness: scenarios use recorded fixtures where a live testnet is unavailable, but S1 must run live at least once before the exit demo.

## Cardinal rules (do NOT)

- Do NOT stub M11 in S8; the real risk manager must reject.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20, T3.29 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T051-verify-e2e-scenarios-f9`
- PR title: `P3-T051: End-to-end scenarios for the tax flow F9 and D14/D15`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (added S11 valuation hierarchy, S12 Accounts page, S13 FY lock + content-addressed attachments; S8 via residency contract; new deps P3-T055/T056 + P2-T001 (keys last); tools/services filled)
