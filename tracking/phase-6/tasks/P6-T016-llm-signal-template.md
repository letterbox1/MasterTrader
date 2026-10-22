---
id: P6-T016
kind: task
title: LLM-signal strategy template consuming M8 signals
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T004, P2-T003, P2-T004, P2-T033]
requirements: [R6.06]
roadmap_todos: [T6.23]
modules: [M0, M8]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p6/P6-T016-llm-signal-template
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T016 · LLM-signal strategy template consuming M8 signals

## Goal / expected outcome

An `llm_signal` template in `mt_strategy` turns `sig.agent.*` Signals into sized `OrderIntent`s through M11, runs unchanged in backtest (replaying stored Signals via `pit`), `paper` and `hitl` modes.

## Context & references

- Roadmap: [R6.06](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.23
- Spec: [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) (LLM-signal template) · [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) (strategies consume signals) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 4
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) (send signal to an LLM-signal strategy)
- Cross-phase: P2-T003 (strategy base), P2-T004 (manifest), P2-T033 (modes and approval routing), M11 via P2-T017
- Modes: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (`paper` / `hitl` / `autonomous`, per bot)
- Depends on (this phase): P6-T004 (tests replay recorded Signals; the scheduler P6-T008 isn't needed to build it)

## Requirements

- Manifest fields: `signal_source` (agent run schedule id or subject list), `min_confidence` (calibrated), `min_edge` (bps), `horizon_match`, `model_versions` and `prompt_versions` allowed, `training_cutoff` (auto-filled from the model registry), counterparty sentence, sleeve, kill criteria, benchmark.
- Signals are features visible from the Signal's `ts` (when it was produced, 03 M8), never from its `as_of`, so backtests can't see a Signal before it existed.
- Exit plan fixed at entry (14 §4); sizing via M11 sizing models; bots on this template run in `paper` (or `hitl`) only in P6; `autonomous` needs the gates + C3 and comes in P7.
- Optional tier-A stacker input: the Signal's calibrated confidence as a feature for tier A (cached).

## ToDo

- [ ] Template class `strategies/templates/llm_signal.py` + parameter schema + manifest validator rules.
- [ ] Signal replay source for backtests reading `audit.signal` via `pit`.
- [ ] D03 template form entry (template registry metadata).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: filtering by confidence/edge; Signal→OrderIntent mapping; exit plan attached.
- Backtest: replay of 20 recorded Signals gives the same trades in screening and Nautilus truth paths.
- PIT test: a Signal ingested at t is not visible at t−1s in the backtest.

### Scenarios
- Given a long Signal with confidence 0.62 and threshold 0.6, then one OrderIntent is sent to M11 and, for a bot in `hitl` mode, appears in the approval queue.
- Given a Signal from an unlisted prompt version, then the strategy ignores it and logs why.

### Stress / failure injection
- Burst of 100 Signals in 1 s: strategy processes them in order without duplicate intents (idempotent client IDs from signal id).

## Acceptance criteria

- [ ] Template available in D03, validated manifest.
- [ ] Backtest/paper parity on recorded Signals.
- [ ] CI green incl. `pit` check.

## Exceptions & edge cases

- Agent service down: strategy idles (no Signals) and reports `no_input`, never improvises.
- Kill switch ON: no intents; protective exits unaffected.

## Cardinal rules (do NOT)

- Do NOT let the template bypass M11 or enable `autonomous` mode.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M0: template fields.
- `docs/14-strategy-evidence-and-validation.md` §3: LLM-signal row evidence/priority note.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.23 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T016-llm-signal-template`
- PR title: `P6-T016: LLM-signal strategy template consuming M8 signals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (modes paper/hitl/autonomous (17 §B); Signal fields ts/confidence/edge per 03 M8; deps trimmed to P6-T004 + P2-T003/T004/T033; run fields)
