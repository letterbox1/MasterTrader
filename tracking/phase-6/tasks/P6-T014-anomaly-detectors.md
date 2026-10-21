---
id: P6-T014
kind: task
title: mt_anomaly detectors on market, sentiment and event streams
phase: 6
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.05]
roadmap_todos: [T6.22]
modules: [M10]
dashboards: [D09]
branch: p6/P6-T014-anomaly-detectors
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T014 · mt_anomaly detectors on market, sentiment and event streams

## Goal / expected outcome

An `anomaly` service runs robust z-score, IsolationForest, change-point and correlation-break detectors over `md.*` bars, `feat.*` sentiment/regime and `evt.*` streams, writes `audit.anomaly` and publishes `alert.anomaly.*`.

## Context & references

- Roadmap: [R6.05](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.22
- Spec: [03 M10](../../../docs/03-build-spec.md#m10-anomaly-monitor--mt_anomaly) · [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M10 owns `audit.anomaly`, publishes `alert.anomaly.*`, consumes `md.*`, `text.*`, `evt.*`) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`anomaly` container)
- Cross-phase: P1 R1.02 bars, P4 R4.11 sentiment/regime features, P4 R4.08 events

## Requirements

- Detectors: robust z (median/MAD) on returns, volume, spread, funding; IsolationForest on multivariate feature windows (fit nightly, time-ordered, per asset class); change points (PELT via `ruptures`, or BOCPD) on volatility/sentiment; correlation breaks (rolling 30d correlation vs 1y baseline, Fisher z test) for key pairs (BTC-ETH, DXY-gold, SPY-VIX…).
- Runs on bars (1m/1h/1D) not raw ticks; DQ status `stale|bad` suppresses detections for that instrument.
- Each anomaly: id, detector, subject(s), score, threshold, window, `event_time`, inputs snapshot hash, severity (info/warn/high); dedupe and cool-down per (subject, detector) (default 60 min).
- Thresholds configurable per detector/asset class; false-positive budget target ≤ 3 high-severity alerts/day (tunable).
- Model artefacts (IsolationForest) logged to MLflow with training window.

## ToDo

- [ ] Package `packages/mt_anomaly/` with detector interfaces and the four detectors.
- [ ] Streaming runner (NATS consumer) + nightly Prefect fit job.
- [ ] `audit.anomaly` WORM migration; publish `alert.anomaly.{severity}.{kind}`.
- [ ] `anomaly` container in Compose.
- [ ] Backtest the detectors on recorded history; tune thresholds; record in MLflow.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each detector on synthetic series with an injected spike/level shift/correlation flip.
- Property: robust z is invariant to a single outlier in the baseline window.
- Integration: seeded bar stream → one `alert.anomaly.*` with cool-down respected.

### Scenarios
- Given a 10σ volume spike on ETHUSDT 1m bars, then a high-severity anomaly is written once and repeats are suppressed for 60 min.
- Given a stale feed, then no anomaly fires for that instrument.
- Given BTC-ETH 30d correlation drops from 0.85 to 0.3, then a correlation-break anomaly fires.

### Stress / failure injection
- Replay one day of 1m bars for the full universe at 50× speed: detector lag p95 < 5 s, CPU < 1 core average.

## Acceptance criteria

- [ ] Detector precision on labelled historical events reported in MLflow.
- [ ] Alert volume within the false-positive budget on a 30-day replay.
- [ ] WORM tests green for `audit.anomaly`.

## Exceptions & edge cases

- Restart: rolling windows rebuilt from Timescale via `pit`; no burst of stale alerts.
- New instrument with < baseline length: detectors abstain.

## Cardinal rules (do NOT)

- Do NOT let detectors trade or call M11; they only alert.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M10: detector parameters.
- `docs/02-v1-architecture.md` §6: `alert.anomaly.*` payload.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.22 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T014-anomaly-detectors`
- PR title: `P6-T014: mt_anomaly detectors on market, sentiment and event streams`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
