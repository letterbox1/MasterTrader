---
id: P6-T078
kind: task
title: Verify simulator isolation, synthetic-row refusal and seeded replay
phase: 6
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T050, P6-T075, P6-T076]
requirements: [R6.34, R6.32]
roadmap_todos: [T6.75]
modules: [M14, M6, M9, M21]
dashboards: []
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [nats, supabase-postgres, litellm, llm-local]
branch: p6/P6-T078-verify-simulator-isolation-synthetic-row-refusal
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T078 · Verify simulator isolation, synthetic-row refusal and seeded replay

## Goal / expected outcome

Proof that the simulator stays a simulator: `synthetic = true` rows are refused by features, model training, RAG and memory; the simulator and the twin can't reach the signer, venue keys or the real paper/live accounts; and the same seed replays the same scenario.

## Context & references

- Roadmap: [R6.34](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.75
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) (boundaries) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) ("synthetic data is never used for features, training or RAG, whatever these settings say") · data rules [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (`synthetic = true` with `train_ok = false`, `model_input_ok = false`, refused like Telegram text)
- Depends on (this phase): P6-T050, P6-T075, P6-T076
- Related: P4-T050 (the Telegram-text gate test this mirrors), P6-T056 (label provenance)

## Requirements

- Provenance: a seeded `synthetic = true` row (scenario, twin report, any derived text) is refused at every consumer boundary: feature evaluator (`mt-features`), dataset builder (`mt_research` via the `mt_store` binding), RAG indexer and search (`mt-memory`), Hindsight retain, tier-B question boundary (`mt-models`), agent tool trait (`mt-agents`) and MCP (when present).
- Settings can't override it: with every simulator setting at its most permissive value, the refusals still hold.
- Isolation: from inside `crowdsim` and `scenario-twin`, the signer, venue endpoints and real `ord.*` subjects are unreachable; the twin's DB role can't write the journal or real accounts' tables.
- Replay: same seed + config + recorded responses → identical scenario hash; different seed → different scenario.

## ToDo

- [ ] Provenance suite: seed synthetic rows and assert each consumer refuses them (counters increment).
- [ ] Isolation suite: network, NATS permission and DB grant probes from inside both containers.
- [ ] Seeded replay test.
- [ ] Wire the suites into CI; progress log with results.

## Verification

### Tests
- `cargo test -p mt-crowdsim -p mt-features -p mt-memory -p mt-models -p mt-agents synthetic_refused`; `uv run pytest` for the dataset builder's refusal in `mt_research`; `supabase test db` for grants.
- Probes from inside the containers (`docker compose exec`) to the signer and venue hosts fail.

### Scenarios
- Given a synthetic scenario headline in `text.*`, when the RAG indexer runs, then it is skipped and counted.
- Given a twin report row, when the distillation dataset builder runs, then the row is excluded with reason `synthetic`.
- Given the twin process, when it publishes `ord.intent.*`, then NATS rejects it.

### Stress / failure injection
- Flood 10k synthetic rows during an ingest burst: zero reach any index, feature or training set.

## Acceptance criteria

- [ ] Every consumer refuses synthetic rows (suite green).
- [ ] Isolation probes all fail as expected.
- [ ] Seeded replay is byte-identical.
- [ ] CI green.

## Exceptions & edge cases

- A consumer that doesn't exist yet in this build (e.g. MCP before P8) is listed as "not present" and its check runs when it lands (P8 reuses this suite).

## Cardinal rules (do NOT)

- Do NOT weaken a refusal to make a fixture pass; fix the fixture.
- Do NOT let Telegram text or `synthetic = true` rows (any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §5: link the test suite.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.75 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T078-verify-simulator-isolation-synthetic-row-refusal`
- PR title: `P6-T078: Verify simulator isolation, synthetic-row refusal and seeded replay`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T078` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (new task for the scenario & crowd simulator workstream, 18 §2.4)
