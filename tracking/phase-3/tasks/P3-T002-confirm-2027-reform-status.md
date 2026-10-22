---
id: P3-T002
kind: task
title: Ask the tax agent to confirm the 2027 CGT reform status and transition
phase: 3
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P3-T001]
requirements: [R3.08]
roadmap_todos: [T3.02]
modules: [M18]
dashboards: [D15]
tools: []
mcp: []
env: []
services: [registered tax agent]
branch: p3/P3-T002-confirm-2027-reform-status
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

# P3-T002 · Ask the tax agent to confirm the 2027 CGT reform status and transition

## Goal / expected outcome

You have the tax agent's written view on whether the AU CGT reform (CPI indexation + 30% minimum tax from 1 July 2027) is law, and how the 30 June 2027 transitional value is set (deemed market-value disposal or other), so the `AU_2027_REFORM` flag (P3-T029) can be set correctly before FY2027-28.

## Context & references

- Roadmap: [R3.08, T3.02](../../../docs/roadmap/phase-3-journal-and-tax.md) · fixed date 2027-06-30 / 2027-07-01 in [roadmap README §4](../../../docs/roadmap/README.md#4-fixed-external-dates)
- Conflict: [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (reported Act, Royal Assent 26 Jun 2026) vs [11 §3](../../../docs/11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) ("budget proposal, not law" as of 28 Sep 2026)
- Related: P3-T029 (flag), P3-T030 (snapshot job); snapshot price convention decided in [17 §A P3-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (defaults, your agent to confirm)

## Requirements

- Ask specifically: (a) enacted or not, with the Act number; (b) start date; (c) the transitional mechanism for assets held on 30 June 2027 and whether it applies to crypto; (d) whether the default snapshot price convention per asset class is acceptable ([16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change): crypto VWAP of recorded trades 23:55:00–23:59:59 AEST on the primary venue; ASX official close; US/EU last trade at or before 23:59:59 AEST; FX RBA rate for the day) — this is also 09 question 10; (e) whether the 30% minimum tax applies per gain or to the year.
- Answer needed **before 2027-06-30**; the snapshot job runs regardless (it costs nothing).

## ToDo

- [ ] Send questions (a)–(e) to the agent (can be in the same email as P3-T001)
- [ ] Record the answer summary in the `TAX_QUESTION` task for Q3 (no personal data)
- [ ] If enacted: open a follow-up to flip `AU_2027_REFORM` on via config for FY2027-28 (P3-T029 explains how)
- [ ] If the agent's market-value convention differs from the 16 §4.2 defaults, change the per-asset-class setting (a configuration change, recorded as a new version row) before 2027-06-01

## Verification

### Tests

- n/a (USER action)

### Scenarios

- Given the agent says the reform is law with a deemed disposal at 30 June 2027 end of day, when P3-T030 is configured, then its convention matches and nothing changes.
- Given the agent says it is not law, when FY2027-28 starts, then the flag stays off and D15 still shows both regimes side by side.

### Stress / failure injection

- n/a: human advice step

## Acceptance criteria

- [ ] Written answer to (a)–(e) recorded in the Q3 `TAX_QUESTION` task
- [ ] Decision on the flag noted in the progress log with the date

## Exceptions & edge cases

- No answer by 2027-06-01 → the snapshot still runs (P3-T030), flag stays off, D15 keeps the dual view.
- Mechanism changes after the snapshot → the snapshot is WORM; any re-valuation is a new superseding snapshot row, never an edit.

## Cardinal rules (do NOT)

- Do NOT turn the `AU_2027_REFORM` flag on without the agent's written confirmation.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.02 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T002-confirm-2027-reform-status` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T002: Ask the tax agent to confirm the 2027 CGT reform status and transition`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (question (d) now asks to confirm the 16 §4.2 snapshot convention; P3-B002 closed; services filled)
