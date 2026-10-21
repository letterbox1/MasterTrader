---
id: P4-T016
kind: task
title: Finnhub news connector (60 calls/min, terms-aware)
phase: 4
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T005]
requirements: [R4.01]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
branch: p4/P4-T016-finnhub-news
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T016 · Finnhub news connector (60 calls/min, terms-aware)

## Goal / expected outcome

`mt_data.text.finnhub` pulls Finnhub general market news (forex, crypto, general) and company news for the equity watchlist within the free 60 calls/min limit, with provenance flags set from the terms decision in P4-T005 (if the ML clause forbids model use, `model_input_ok = false`).

## Context & references

- Roadmap: [R4.01](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Risk 'Free-API terms change'
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- Related: P4-T005 (terms), P4-T037 (Finnhub IPO/earnings calendar).

## Requirements

- Quota tracker budget 50/min (throttle before 60/min); key from secrets.
- Company news per watchlist ticker every 30 min, rotated to stay within budget; general news every 5 min.
- Provenance from `source_terms.yaml`; display headline + summary + link.

## ToDo

- [ ] Connector + quota budget.
- [ ] Rotation scheduler for company news.
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: fixture → `RawTextItem` with correct flags.
- Unit: scheduler never exceeds 50 calls/min (fake clock).

### Scenarios
- Given `model_input_ok=false` for Finnhub, then its items appear in D08 but never get FinBERT/tier B/RAG (enforced by P4-T025).
- Given 429 from Finnhub, then back off and alert.

### Stress / failure injection
- n/a: bounded by quota; covered by P4-T058.

## Acceptance criteria

- [ ] 24-h run with zero 429s
- [ ] Provenance flags match `source_terms.yaml`
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Free-tier endpoints change: mark the source `bad` and alert rather than switching to an unofficial endpoint.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT exceed or try to work around the free quota.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2/§3: Finnhub terms decision
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T016-finnhub-news`
- PR title: `P4-T016: Finnhub news connector (60 calls/min, terms-aware)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
