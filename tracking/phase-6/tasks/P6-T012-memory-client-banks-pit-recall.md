---
id: P6-T012
kind: task
title: mt_memory Hindsight client: banks, retain/recall, point-in-time recall and the memory API
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T011, P6-T006, P0-T034]
requirements: [R6.04]
roadmap_todos: [T6.21]
modules: [M9, M8]
dashboards: [D10, D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [hindsight, postgres, mt-api]
branch: p6/P6-T012-memory-client-banks-pit-recall
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T012 · mt_memory Hindsight client: banks, retain/recall, point-in-time recall and the memory API

## Goal / expected outcome

`mt_memory.agent_memory` wraps Hindsight with the five banks, provenance-checked retain, **point-in-time recall** (every memory carries `observed_at`/`ingested_at`; derived memories carry their latest source time; memory-off and frozen-snapshot modes for backtests) and the `recall_memory` agent tool, plus `/memory/search`, `/memory/banks` and `memory.delete`.

## Context & references

- Roadmap: [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.21
- Spec: [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) (banks, PIT recall) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory) · [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`memory.delete` C1, audited)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Memory tab · [D09](../../../docs/ui/dashboards/D09-agents.md) "Memory used"
- Decision: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P6-B016: `observed_at`/`ingested_at` on every memory; consolidated/reflection memories carry the latest source time and are excluded when > `as_of`; if not enforceable, backtests run with memory disabled or from a frozen per-`as_of` snapshot; PIT recall test mandatory) · [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory)
- Cross-phase: P0-T034 (command bus for `memory.delete`)
- Depends on (this phase): P6-T011, P6-T006

## Requirements

- Banks: `decisions`, `strategies`, `market-regimes`, `user`, `ops`; created idempotently at startup.
- Retain: every item carries `source`, `observed_at` (when the fact or event happened), `ingested_at` (when we stored it, Postgres `now()`), `sources[]`, `model_input_ok`; items derived from rows with `model_input_ok=false` or Telegram are refused.
- PIT recall: at `as_of`, a memory is visible only if `observed_at ≤ as_of` **and** `ingested_at ≤ as_of`. Consolidated/reflection memories (observations, mental models) carry the **latest** `observed_at`/`ingested_at` of their sources (lineage recorded at consolidation) and are excluded when that is > `as_of`. `mt_memory` enforces this by over-fetch ×3 then post-filter with the lineage check, since Hindsight's own API may not filter on these times (U).
- Backtest memory modes (lab setting per run): `filtered` (default, above), `frozen` (recall only from a per-`as_of` snapshot exported by `mt-memory snapshot --as-of`), `off`. If the PIT recall test (P6-T055) fails for `filtered`, the lab default becomes `off` and run reports say so.
- Live recall (no `as_of`) uses now; backtests must pass `as_of` (assertion).
- `recall_memory` tool returns memory ids, bank, timestamps as provenance for the Signal.
- API: `GET /memory/banks` (counts), `GET /memory/search?bank=&q=&as_of=`; `memory.delete` (C1) writes `audit.command` and a tombstone row (`ops.memory_tombstone`) so deletes are traceable.
- Recall latency budget: p95 < 600 ms (vendor 100–600 ms with CPU reranker).

## ToDo

- [ ] Implement the client (`packages/mt_memory/mt_memory/agent_memory.py`) on Hindsight's HTTP API.
- [ ] PIT filter on `observed_at`/`ingested_at` + derived-memory lineage (latest source time); frozen-snapshot export and `off` mode for the lab.
- [ ] Bind `recall_memory` into the P6-T006 tool belt.
- [ ] `mt_api` queries + `memory.delete` command + tombstones.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: PIT filter with synthetic timestamps, lineage exclusion of consolidated memories.
- Integration (compose): retain at t1, t2, t3; recall with as_of=t2 returns only t1/t2 items.
- API tests: delete is C1, audited, tombstoned.

### Scenarios
- Given a backtest at 2027-01-05, when the agent recalls `decisions`, then no memory created after 2027-01-05 appears (P6-T055 extends this).
- Given Hindsight consolidated an observation from memories at t1 and t5, when recalling with as_of=t3, then the observation is excluded.
- Given a retain request carrying a Telegram-provenance snippet, then it is refused and counted.
- Given a lab run with memory mode `frozen` at 2027-01-05, then recall reads only the snapshot taken at that `as_of`.

### Stress / failure injection
- 10k memories per bank; recall p95 < 600 ms with reranker candidates at 100.
- Hindsight down: recall returns `MEMORY_UNAVAILABLE` within 2 s; the debate continues without memory and says so.

## Acceptance criteria

- [ ] PIT integration test green.
- [ ] Recall p95 within budget on 10k items.
- [ ] Delete path audited.

## Exceptions & edge cases

- Clock skew between hosts irrelevant (single host) but timestamps are always UTC from Postgres `now()`.
- Bank missing after restore → recreated empty and alerted, never silently.

## Cardinal rules (do NOT)

- Do NOT recall without `as_of` inside backtests or the lab.
- Do NOT retain secrets, TFNs or personal identifiers.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §1: PIT mechanism incl. consolidated memories.
- `docs/02-v1-architecture.md` §7: `/memory/*` params, tombstone table.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.21 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T012-memory-client-banks-pit-recall`
- PR title: `P6-T012: mt_memory Hindsight client: banks, retain/recall, point-in-time recall and the memory API`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (PIT per 17 §A P6-B016: observed_at/ingested_at, derived memories carry latest source time, frozen-snapshot/off backtest modes; dep P0-T034; run fields)
