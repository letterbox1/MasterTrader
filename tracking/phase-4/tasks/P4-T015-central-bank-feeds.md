---
id: P4-T015
kind: task
title: Central-bank statements, minutes and speeches feeds
phase: 4
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T011]
requirements: [R4.01]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T015-central-bank-feeds
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
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

# P4-T015 · Central-bank statements, minutes and speeches feeds

## Goal / expected outcome

Statements, minutes, press releases and speeches from the Fed, ECB, BoE, BoJ, SNB, RBA, BoC and RBNZ (plus regulators you choose) are ingested via their official RSS feeds (or RSS-Bridge where none exists), tagged with `cb` and `doc_type`, and high-priority so policy statements reach D08 and the brief quickly.

## Context & references

- Roadmap: [R4.01](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- Calendars & CBs: [06 §3](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers)
- Related: P4-T037 (meeting schedules), P4-T029 (event_type flags).

## Requirements

- Config `config/intel/central_banks.yaml`: per bank feed URLs by `doc_type` (statement/minutes/speech/press/research).
- Poll every 2 min within ±30 min of a scheduled decision (from the calendar), otherwise every 15 min.
- Documents carry `cb` (FED/ECB/BOE/BOJ/SNB/RBA/BOC/RBNZ), `doc_type`, `speaker` when present.
- Public-domain/government content: `train_ok`/`model_input_ok` true by default (confirm per bank's terms).

## ToDo

- [ ] Write `central_banks.yaml` with verified feed URLs.
- [ ] Speaker/doc_type parsing per bank.
- [ ] Calendar-aware poll cadence hook (stub until P4-T037 lands, then wired).
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: one fixture per bank → correct `cb`/`doc_type`.
- Unit: cadence switches to 2 min inside the decision window.

### Scenarios
- Given an RBA decision at 14:30 Sydney time, then the statement is ingested within 3 min of publication.
- Given a bank changes its feed URL, then the source goes stale and D08 Sources shows it.

### Stress / failure injection
- n/a: low volume; covered by P4-T058.

## Acceptance criteria

- [ ] All 8 banks ingesting; statements tagged correctly in a 1-week run
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- BoJ/SNB feeds may be Japanese/German-first: store `lang`; translation is out of scope.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT scrape press-conference video/audio.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §3 calendars & CBs: list feed URLs used
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T015-central-bank-feeds`
- PR title: `P4-T015: Central-bank statements, minutes and speeches feeds`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (front-matter run fields added; no decision changes)
