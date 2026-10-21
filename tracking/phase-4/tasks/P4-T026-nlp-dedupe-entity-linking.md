---
id: P4-T026
kind: task
title: nlp stages: dedupe and entity/ticker linking
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T025]
requirements: [R4.06]
roadmap_todos: [T4.23]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T026-nlp-dedupe-entity-linking
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T026 · nlp stages: dedupe and entity/ticker linking

## Goal / expected outcome

Two `nlp` stages run after the provenance gate: **dedupe** (canonical URL + content hash exact match, then MinHash/cosine > 0.95 near-duplicate clustering for wire copies, keeping a `dup_count`) and **entity/ticker linking** (cashtags, symbol-master names/aliases, CIK, country/central-bank entities) producing `tickers[]` and `entities` on each document.

## Context & references

- Roadmap: [R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.23](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M2 processing](../../../docs/03-build-spec.md#m2-news--social--mt_datatext) · [06 §2 processing chain](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · [10 §3 item 5](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres) (MinHash or cosine > 0.95)
- Cross-phase: P1 FinanceDatabase symbol master (R1.05).

## Requirements

- Exact dedupe by `canonical_url` and `content_hash` (sha256 of normalised text).
- Near-dup: MinHash LSH (128 perms, Jaccard ≥ 0.9 on 5-shingles) within a 72-h window; cluster id stored; `+N similar` count exposed to D08.
- Linker: deterministic dictionary + rules first (cashtags, exact names, aliases, CIK), optional spaCy NER for ORG/GPE; ambiguous short tickers (e.g. `ON`, `IT`) require a cashtag or company-name co-occurrence.
- Country/region entities feed the exposure map (P4-T035).
- Stage latency p95 < 50 ms/document on CPU.

## ToDo

- [ ] Dedupe stage + `text.document_dup` cluster writes.
- [ ] Linker with alias tables built from the symbol master; ambiguity rules.
- [ ] Evaluation set of 300 hand-checked headlines (built from public news, committed as fixtures).
- [ ] Tests + metrics (dup rate, link precision).

## Verification

### Tests
- Unit: same AP story from 3 outlets → one cluster, `dup_count=3`.
- Golden: linker on the 300-headline set ≥ 0.9 precision, ≥ 0.8 recall.
- Property: dedupe is idempotent on replay.

### Scenarios
- Given a headline 'Apple supplier ON Semiconductor…', then `ON` links only via the company name rule.
- Given a correction republishes with a changed title, then it joins the original cluster and `supersedes` is set.

### Stress / failure injection
- 10k docs/hour burst: p95 stage latency < 50 ms; LSH index memory < 500 MB.

## Acceptance criteria

- [ ] Precision/recall targets met on the fixture set
- [ ] D08 dedup count available via `/intel/documents`
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Non-English docs: dedupe works; linker limited to cashtags/CIK; mark `lang`.
- Postgres down (02 §9.3): consumers pause and resume from the JetStream durable cursor; no item lost or duplicated.

## Cardinal rules (do NOT)

- Do NOT call any LLM for linking in this stage (deterministic only).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/03-build-spec.md`: M2 processing: dedupe thresholds and linker rules
- `docs/roadmap/phase-4-intel.md`: tick T4.23 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T026-nlp-dedupe-entity-linking`
- PR title: `P4-T026: nlp stages: dedupe and entity/ticker linking`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
