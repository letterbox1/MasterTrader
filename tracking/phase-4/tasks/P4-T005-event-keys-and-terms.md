---
id: P4-T005
kind: task
title: Register free event-source keys and read news API terms
phase: 4
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R4.01, R4.08]
roadmap_todos: []
modules: [M2, M3]
dashboards: [D08]
branch: p4/P4-T005-event-keys-and-terms
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

# P4-T005 · Register free event-source keys and read news API terms

## Goal / expected outcome

Free keys for NASA FIRMS (`MAP_KEY`) and ACLED (research account) are in the secrets file, and you have read and recorded decisions on the Finnhub ML clause, CryptoPanic free-tier terms (attribution) and OpenSanctions' non-commercial licence, so each source starts with correct provenance flags.

## Context & references

- Roadmap: [R4.01, R4.08](../../../docs/roadmap/phase-4-intel.md#3-requirements) · Risks table 'Free-API terms change' (§7)
- Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext) (Finnhub 60/min, read its ML clause first; CryptoPanic read its terms first) · [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents) (ACLED research account)
- Gap: P4-B008 (these keys are not in P0 T0.10).
- Cross-phase: Finnhub and CryptoPanic keys come from P0 T0.10.

## Requirements

- FIRMS: request a free `MAP_KEY` at firms.modaps.eosdis.nasa.gov (email only).
- ACLED: register a research/personal account; note the access tier and usage limits.
- Decide per source, and write it into `config/intel/source_terms.yaml`: `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `attribution_required`.
- If Finnhub's terms forbid ML/model use of its news, set `model_input_ok: false` (headlines still display; no FinBERT/RAG/tier B).

## ToDo

- [ ] Request the FIRMS `MAP_KEY` and the ACLED access key; store both in the sops/age secrets file (`secrets/mt.sops.yaml`, see [07 §2](../../../docs/07-security-notes.md#2-secrets)) under `firms.map_key` and `acled.email`/`acled.key`.
- [ ] Read Finnhub's terms (ML clause), CryptoPanic's API terms (attribution) and OpenSanctions' licence (non-commercial use).
- [ ] Fill `config/intel/source_terms.yaml` with one entry per source and the date you read the terms.
- [ ] Tell the agent which sources you decided not to enable.

## Verification

### Tests
- Agent: `mt_data.text.config` loads `source_terms.yaml`; every enabled source has an entry (CI check).

### Scenarios
- Given Finnhub terms bar ML use, when its rows are ingested, then `model_input_ok = false` and the provenance gate (P4-T025) skips FinBERT/RAG for them.

### Stress / failure injection
- n/a: account/decision step.

## Acceptance criteria

- [ ] FIRMS and ACLED keys present in secrets (agent confirms by masked metadata in D16, not by value)
- [ ] `source_terms.yaml` committed with decisions for Finnhub, CryptoPanic, OpenSanctions, ACLED, GDELT, FIRMS

## Exceptions & edge cases

- ACLED may decline a personal account; then ACLED is skipped and UCDP + GDELT cover conflict events.

## Cardinal rules (do NOT)

- Do NOT create extra accounts to raise quotas.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: add licence/terms notes for FIRMS, ACLED, OpenSanctions in §2/§3
- `docs/roadmap/phase-4-intel.md`: note the terms decisions under §7 risks

## Branch & PR

- Branch: `p4/P4-T005-event-keys-and-terms`
- PR title: `P4-T005: Register free event-source keys and read news API terms`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T005`

## Progress log

- 2026-10-21 00:00 · planner · created
