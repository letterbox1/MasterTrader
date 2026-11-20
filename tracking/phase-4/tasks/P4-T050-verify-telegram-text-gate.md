---
id: P4-T050
kind: task
title: Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)
phase: 4
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T019, P4-T025, P4-T027, P4-T029, P4-T030, P4-T032]
requirements: [R4.03, R4.02]
roadmap_todos: [T4.60]
modules: [M2, M9, M21]
dashboards: [D08]
tools: [uv, cargo, git, docker]
mcp: []
env: []
services: [supabase-postgres, nats, loki]
branch: p4/P4-T050-verify-telegram-text-gate
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T050 · Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)

## Goal / expected outcome

An automated end-to-end test suite, run in CI and as part of the exit demo, proves that a Telegram message (with a unique canary string) produces postures but **never** appears in FinBERT inputs, TEI requests, decision-svc prompts, `rag.doc_chunk`, `text.document`, agent context builders, any training-set export, NATS payloads outside the Telegram ingest process, logs or API responses.

## Context & references

- Roadmap: [R4.03](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.60](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 3
- Policy: [12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements) · [10 §4.3 operating rules](../../../docs/10-memory-rag-and-models.md#43-design)
- Related: P4-T025 guard, P4-T019 postures.
- Decisions: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B001: F3 provenance-first, Telegram only via F3b) and [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B003: `text.telegram_posture`, `posture.telegram.*`, consumers M4/M11 rules only).

## Requirements

- Canary: inject synthetic Telegram messages via a fake Telethon/Bot API source containing `MT-CANARY-<uuid>` + a valid EVM address.
- Probes: request spies on FinBERT runner, TEI client, decision-svc client, LiteLLM client, RAG writer; DB scan (`text.*`, `rag.*`, `models.*`, `audit.*`) for the canary; NATS tap on `>`; Loki query for the canary; API crawl of `/intel/*` and `/rag/search?q=<canary>`.
- Training-set exporters (the Python `mt_research` dataset builders and the Rust `mt-models` label/dataset exports) run with Telegram rows present → zero Telegram rows exported.
- Forged-flag case: a Telegram row with `model_input_ok=true` forced in a test DB is still refused by every boundary.
- Positive control: the canary address **does** appear in `text.telegram_mention` and `text.telegram_posture` / `posture.telegram.*`.
- Consumer probe: only the allow-listed consumers (M4 rules, M11 rules, intel-writer, mt-api display) hold subscriptions on `posture.telegram.>`; MCP responses (P8) are out of scope here but use the same provenance filter.

## ToDo

- [ ] Write the suite as Rust integration tests against the Compose stack (`cargo test --test telegram_gate`) plus the `mt_research` exporter check (`uv run pytest`) + fixtures.
- [ ] Add NATS tap + Loki query helpers.
- [ ] Wire into CI (nightly + on PRs touching `crates/mt-feeds`, `crates/mt-nlp`, `crates/mt-memory`, `crates/mt-models`, `crates/mt-agents`, `crates/mt-intel-writer`, `packages/mt_telegram_reader`, `packages/mt_extract`, `packages/mt_research`).
- [ ] Report artifact (JSON + markdown summary) saved for the exit demo.

## Verification

### Tests
- The suite itself (all probes above).
- Mutation check: temporarily bypassing the guard (the Rust `ModelInput` constructor or the Python decorator) in a test branch makes the suite fail (proves sensitivity).

### Scenarios
- Given a Telegram message mentioning `$ETH` and an address, then postures update and every probe reports zero canary hits.
- Given a developer adds a new model client without the guard, then the provenance lint (P4-T025) and this suite fail.

### Stress / failure injection
- Run with 10k canary messages: zero leaks; posture counts exact.

## Acceptance criteria

- [ ] Suite green in CI with zero canary hits outside allowed tables
- [ ] Mutation check proves the suite catches a removed guard
- [ ] Report saved for the exit demo
- [ ] CI green (`cargo test --test telegram_gate`, `cargo test -p mt-intel-writer`, `cargo clippy`, ruff, mypy, `uv run pytest` (`mt_telegram_reader`, `mt_research`), `pit` bypass check)

## Exceptions & edge cases

- Allowed locations: in-memory extractor only; `text.telegram_mention` stores the extracted address, never the canary text.

## Cardinal rules (do NOT)

- Do NOT mark this suite flaky/skip; failures block merges.
- Do NOT use real Telegram content in fixtures.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: §5: reference the gate test as the enforcement proof
- `docs/roadmap/phase-4-intel.md`: tick T4.60 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T050-verify-telegram-text-gate`
- PR title: `P4-T050: Telegram-text gate test (never reaches FinBERT, tier B, RAG, agents or training)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (canonical posture names and consumer allow-list probe (17 §A P4-B001, §D P4-B003))
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services postgres → supabase-postgres; tools +cargo; CI commands per 18 (cargo/uv/supabase/pnpm))
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (suite in Rust against the Compose stack + `mt_research` exporter check; CI paths are the new crates/packages)
