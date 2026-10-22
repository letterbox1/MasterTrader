---
id: P4-T040
kind: task
title: Sentiment and regime pipelines per market type plus the macro layer
phase: 4
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T027, P4-T039, P2-T120]
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M6]
dashboards: [D08, D02]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats]
branch: p4/P4-T040-sentiment-regime-per-market
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
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

# P4-T040 · Sentiment and regime pipelines per market type plus the macro layer

## Goal / expected outcome

`mt_features.sentiment` runs separate pipelines for **crypto, FX, gold/silver/metals, energy and equities/indices** plus a shared **macro layer** (USD, rates, calendar, risk-on/off). Each outputs, per instrument and per market type, a sentiment score, a fear/greed gauge, news-impact flags and a **regime label**, written as versioned `features.value` series (PIT) for strategies, D08 and the morning brief.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M6 sentiment & regime](../../../docs/03-build-spec.md#m6-features--mt_features) (crypto adds Fear & Greed, funding, OI, liquidations, long/short ratios)
- Cross-phase: P2-T120 (R2.46 feature framework) is a `depends_on` entry; P1 funding/OI from crypto feeds are reused.
- Decisions: Telegram postures are never M6 features ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P4-B003; [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features)); per-asset regime labels for validation are defined once in [16 §2.4.1](../../../docs/16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results).
- Verified by P4-T054 (IC report).

## Requirements

- Inputs: FinBERT doc sentiment (relevance-weighted, dedup-cluster-weighted), GDELT tone, CryptoPanic votes, event scores, positioning (P4-T039), and for crypto: Fear & Greed index (alternative.me free), funding, OI, liquidations, Binance free long/short ratios.
- **Excluded:** Telegram postures (`posture.telegram.*` / `text.telegram_posture` are consumed only by M4/M11 rules; never features, 12 §4, 17 §D). CI check: `mt_features` never imports or subscribes to them.
- Sentiment index per instrument: EWMA over 1 h / 24 h / 7 d; z-scored vs 90-day history; mention volume series.
- Regime label per market type: `{risk_on, risk_off, neutral}` macro and `{trend, range, crisis}` market regimes from deterministic rules (vol percentile, trend strength, sentiment z, VIX regime), versioned, thresholds configurable. The per-asset **bull/bear/chop** label is the 16 §2.4.1 definition (200-day average and ±10% 90-day return, configurable per asset class); it's published as a feature from the shared implementation, never redefined here.
- Features registered in `features.def` with version, inputs, PIT semantics; computed incrementally every 5 min and backfilled for history.

## ToDo

- [ ] Pipeline per market type sharing a common aggregator.
- [ ] Macro layer (USD index proxy, rates, calendar proximity, risk-on/off).
- [ ] Regime rules + versioning.
- [ ] Backfill job (PIT-safe).
- [ ] Tests.

## Verification

### Tests
- Unit: aggregator weights; z-score with insufficient history → null not 0.
- PIT test: feature at T uses only docs with `ingested_at ≤ T`.
- Golden: regime labels on a fixed historical window.

### Scenarios
- Given a crypto hack headline cluster, then crypto sentiment drops and news-impact flag `hack` is set for linked tokens.
- Given a source is muted, then its docs stop contributing from the mute time (no retro change).

### Stress / failure injection
- Backfill 1 year of features for the universe: completes within a night; memory bounded.

## Acceptance criteria

- [ ] Five market-type pipelines + macro layer producing features every 5 min
- [ ] PIT test green; features registered with versions
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Sparse coverage (illiquid instrument): emit null with a coverage flag instead of 0.

## Cardinal rules (do NOT)

- Do NOT include Telegram postures or any `model_input_ok=false` input.
- Do NOT read features except via `pit(as_of)` in research.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: M6: feature names/versions for sentiment & regime
- `docs/roadmap/phase-4-intel.md`: tick T4.27 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T040-sentiment-regime-per-market`
- PR title: `P4-T040: Sentiment and regime pipelines per market type plus the macro layer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (postures excluded from features (17 §D P4-B003); bull/bear/chop regime from 16 §2.4.1; explicit depends_on P2-T120)
