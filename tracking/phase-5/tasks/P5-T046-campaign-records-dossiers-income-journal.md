---
id: P5-T046
kind: task
title: Campaign records, project dossiers and airdrop/staking income journal links
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T010, P5-T023, P5-T044, P3-T008, P3-T011]
requirements: [R5.18]
roadmap_todos: [T5.29]
modules: [M4, M18]
dashboards: [D12, D14, D15]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T046-campaign-records-dossiers-income-journal
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/09-journal-and-tax.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T046 · Campaign records, project dossiers and airdrop/staking income journal links

## Goal / expected outcome

Every campaign has a `campaign_record` (wallet used, tasks done = "activity done to earn it", dates, costs, outcome); every project a cited `project_dossier`; and each airdrop/staking receipt becomes a WORM `journal.event` row (airdrop established / initial allocation; there is no separate income table) with AUD value at receipt, FX/price source and the classification evidence (general vs initial allocation) linked to the campaign record.

## Context & references

- Roadmap: [R5.18](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.29 · journal link test in P5-T056
- [08 records](../../../docs/08-airdrops-and-token-launches.md#records) · [09 key findings](../../../docs/09-journal-and-tax.md) (classification turns on what you did) · [D12 history](../../../docs/ui/dashboards/D12-airdrops.md)
- P3: journal writer (P3-T008), crypto rates and FX (P3-T011), AU_2026 crypto income (R3.06); [08 data model](../../../docs/08-airdrops-and-token-launches.md#data-model-postgres): airdrop income is a `journal.event` row linked to the campaign record

## Requirements

- Campaign record: created on first task/claim for an opportunity; appends task completions (from `task.done`), tx hashes, gas/fees (AUD), wallet; closes with outcome (received/none/rejected).
- Dossier: domain, contracts, team/funding, corroboration, risk reports (versions), Discord/X/docs links (verified), incidents, notes — rendered in D12 with citations.
- Income event: `airdrop_established` (tasks/genuine use done → ordinary income at market value on receipt, cost base = that value) vs `airdrop_initial_allocation` (no activity → $0 cost base, CGT on disposal) — (U) flagged for tax-agent confirmation; staking rewards likewise.
- Value at receipt per the [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) hierarchy (VWAP of our recorded trades on the primary AUD venue → USD venue VWAP × RBA AUD/USD → on-chain pool price at the event block; aggregators only as a cross-check), stored with method, source and timestamp; unpriced tokens → `value_unknown` + `TAX_QUESTION` task.
- Weekly digest includes the airdrop income summary.

## ToDo

- [ ] Implement `packages/mt_airdrop/records/` (campaign, dossier) and the `journal.event` adapter for income events (through the P3 writer).
- [ ] Classification rules + evidence linking; `TAX_QUESTION` task creation for uncertain cases.
- [ ] Endpoints for D12 history and D14/D15 drill-through; tests; doc sync.

## Verification

### Tests
- Unit: campaign with QUEST + CLAIM tasks → classification `airdrop_established` with evidence list.
- Unit: claim with no prior activity → `airdrop_initial_allocation`, cost base 0.
- Integration: income event appears in the journal with AUD value and links back to campaign and exec_log.

### Scenarios
- Given a claim of an unpriced token, then the journal event has `value_unknown`, a TAX_QUESTION task is created, and nothing is guessed.
- Given a misclassification found later, then a correction row supersedes it (WORM).

### Stress / failure injection
- n/a: per-event writes (low volume)

## Acceptance criteria

- [ ] Campaign record per campaign with activity evidence
- [ ] Dossier rendered with citations
- [ ] Income events with classification + evidence + AUD value
- [ ] Corrections append-only

## Exceptions & edge cases

- Receipt detected before the campaign record exists (surprise airdrop): create a campaign with `activity: none known` → initial allocation + TAX_QUESTION.

## Cardinal rules (do NOT)

- Do NOT present the classification as tax advice; mark (U) and route uncertain cases to the tax agent.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: record fields.
- `docs/09-journal-and-tax.md`: airdrop income event types and evidence links.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.29 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T046-campaign-records-dossiers-income-journal`
- PR title: `P5-T046: Campaign records, project dossiers and airdrop/staking income journal links`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (income as `journal.event` rows, no separate table; valuation per 16 §4.1; P3 deps)
