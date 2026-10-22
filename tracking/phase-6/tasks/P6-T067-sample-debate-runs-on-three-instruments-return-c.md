---
id: P6-T067
kind: task
title: Sample debate runs on three instruments return complete Signals
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T004, P6-T007, P6-T008, P6-T012]
requirements: [R6.01]
roadmap_todos: [T6.66]
modules: [M8, M9, M21]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [agents, litellm, llm-local, hindsight, tei-embed, tei-rerank, postgres, nats]
branch: p6/P6-T067-sample-debate-runs-on-three-instruments-return-c
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T067 · Sample debate runs on three instruments return complete Signals

## Goal / expected outcome

Evidence for R6.01 ("Sample runs"): three debate runs, on one crypto, one FX and one equity instrument, each return a `Signal` carrying **every 03 M8 field** with its provenance, stored in `audit.decision_run`/`audit.signal` and published on `sig.agent.*`. The runs use the keyless stack (the `local-advisor` route on `llm-local` and recorded gateway responses), so they need no API key; the live-provider run is P6-T070.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.66
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) (`Signal` fields: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B014) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 1–3
- Gateway: [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (`local-advisor` served by `llm-local` from P0)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) run detail
- Depends on (this phase): P6-T004 (Signal schema), P6-T007 (debate graph), P6-T008 (`agents.run_analysis`), P6-T012 (memory recall tool)
- Related: P6-T062 (full F4 flow with settlement), P6-T070 (same runs against your live keys)

## Requirements

- Instruments: `BTCUSDT.BINANCE` (crypto), `EURUSD` (FX), one liquid US equity (e.g. `SPY` or `AAPL`); standard depth.
- Route: debate role pinned to `local-advisor` (keyless) or replayed recorded responses; no paid provider is called.
- Each Signal: all 03 M8 fields present and typed; `confidence` is the calibrated value; `sources[]` non-empty for any non-flat direction; every number in `rationale_summary` maps to a source (`unsourced_numbers=false`, or the flag shows in D09); `model_versions`/`prompt_versions` match the prompt registry (P6-T005); `run_id` links to `audit.decision_run`.
- Every LLM call of each run is in `audit.llm_call` with the run's `run_id` (writer from P0).
- Tools read only through `pit(as_of)`; memory recall passes `as_of`.

## ToDo

- [ ] Script `tools/verify/sample_runs.py` that issues `agents.run_analysis` (C1) for the three instruments and collects run/signal ids.
- [ ] Field-completeness check against the 03 M8 list (schema introspection, not a hand list).
- [ ] Provenance check: each source resolves to a stored row (bar, document, filing, memory, tool output) with `as_of ≤` the run's `as_of`.
- [ ] Join `audit.llm_call` on `run_id`; confirm counts per run.
- [ ] Record run ids, signal ids and the check output in the progress log.

## Verification

### Tests
- Integration (CI, recorded responses): the script on the three instruments; asserts every 03 M8 field and provenance rule.
- Unit: the field-completeness checker fails on a Signal missing `edge` (negative control).

### Scenarios
- Given `EURUSD` at standard depth, when the run finishes, then the Signal has every 03 M8 field and ≥ 1 source per numeric claim.
- Given the equity has no fundamentals tool data, then the fundamentals analyst returns `DATA_UNAVAILABLE` and the Signal still validates.
- Given a source whose `as_of` is later than the run's `as_of` (seeded), then the check fails and names it.

### Stress / failure injection
- Run the three analyses concurrently: no cross-run state; each Signal's `run_id` matches its own LLM calls.
- Stop `hindsight` during one run: the run completes without memory and says so; the Signal is still complete.

## Acceptance criteria

- [ ] Three Signals with every 03 M8 field and resolvable provenance.
- [ ] `audit.llm_call` rows for every call of each run.
- [ ] No paid provider spend during the test (spend endpoint shows $0 for remote routes).

## Exceptions & edge cases

- `llm-local` too slow on CPU for standard depth: use quick depth and note it; the field and provenance checks still apply.
- A run that fails schema validation twice emits no Signal: that is a test failure here, not a pass.

## Cardinal rules (do NOT)

- Do NOT call a paid provider or use your API keys in this task (live check is P6-T070).
- Do NOT hand-edit stored Signals or audit rows to make the check pass.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; agents output Signals only, never orders.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a prompt, memory bank or training set (12 §4–5).
- Do NOT commit secrets; do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M8: link the sample-run check.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.66 (and note this task ID).

## Branch & PR

- Branch: `p6/P6-T067-sample-debate-runs-on-three-instruments-return-c`
- PR title: `P6-T067: Sample debate runs on three instruments return complete Signals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T067` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T6.66 (sample runs, keyless on `local-advisor`; 03 M8 Signal fields per 17 §D)
