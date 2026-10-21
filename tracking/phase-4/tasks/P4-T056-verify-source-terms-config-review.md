---
id: P4-T056
kind: task
title: Config review: prediction markets read-only and per-source terms/provenance
phase: 4
type: VERIFY
status: backlog
priority: high
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T036, P4-T016, P4-T017, P4-T024]
requirements: [R4.09, R4.01, R4.05]
roadmap_todos: []
modules: [M2, M3]
dashboards: [D08]
branch: p4/P4-T056-verify-source-terms-config-review
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T056 · Config review: prediction markets read-only and per-source terms/provenance

## Goal / expected outcome

A checklist review (recorded in this file and as `ops/reviews/p4-sources.md`) confirms: Polymarket disabled or lawfully reachable without VPN/proxy, Kalshi read-only, no trading code paths; every enabled source has a terms entry and correct provenance flags; deferred/excluded sources (Reddit, X, Instagram/TikTok/LinkedIn/Facebook/Threads scrapers, Nitter, snscrape, twscrape) are absent or disabled.

## Context & references

- Roadmap: [R4.09](../../../docs/roadmap/phase-4-intel.md#3-requirements) (verified by config review) · [R4.01, R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Policy: [12 §1](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [06 §2 Excluded row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)

## Requirements

- Review covers `prediction_markets.yaml`, `source_terms.yaml`, `text.source` table, Compose env (no proxy/VPN vars), venue registry entries.
- Any finding becomes a P4 bug item.

## ToDo

- [ ] Run `python -m mt_data.text.audit_sources` (lists enabled sources with flags).
- [ ] Complete the checklist; file bugs for findings.
- [ ] Save the review.

## Verification

### Tests
- The audit script itself has a unit test for flag listing.

### Scenarios
- Given a source lacks a terms entry, then the review fails and the source is disabled until fixed.

### Stress / failure injection
- n/a: review.

## Acceptance criteria

- [ ] Review saved with zero open findings (or bugs filed and fixed)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Residency change later re-triggers this review (12 §1).

## Cardinal rules (do NOT)

- Do NOT approve a source whose terms are unread.
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: §4: link the review record
- `docs/roadmap/phase-4-intel.md`: note the item in §7 risks / progress

## Branch & PR

- Branch: `p4/P4-T056-verify-source-terms-config-review`
- PR title: `P4-T056: Config review: prediction markets read-only and per-source terms/provenance`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
