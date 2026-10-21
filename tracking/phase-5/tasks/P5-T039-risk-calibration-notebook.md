---
id: P5-T039
kind: task
title: Risk calibration notebook on SoK, SolRPDS, Pump.fun corpus and MemeTrans
phase: 5
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T037, P5-T038]
requirements: [R5.13]
roadmap_todos: [T5.26]
modules: [M4, M7]
dashboards: []
branch: p5/P5-T039-risk-calibration-notebook
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T039 · Risk calibration notebook on SoK, SolRPDS, Pump.fun corpus and MemeTrans

## Goal / expected outcome

A reproducible notebook (`notebooks/m4_risk_calibration.ipynb` + `mt_airdrop.risk.calibrate`) evaluates the rule-based score on the **SoK** rug-pull dataset (2,391 labelled ETH/BSC contracts) plus SolRPDS, the Pump.fun corpus and MemeTrans (private), fits an advisory calibrated model, and registers it in MLflow with provenance flags.

## Context & references

- Roadmap: [R5.13](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.26 · report P5-T055
- [08 Calibrate](../../../docs/08-airdrops-and-token-launches.md#pipeline) · [research dataset notes](../../../docs/research/airdrops-rugpull-discord.md) · [12 §4 datasets row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)

## Requirements

- Datasets stored under `data/private/` (git-ignored), with licence rows: SoK (attribution (U), no redistribution), SolRPDS (CC BY), Pump.fun corpus (CC BY), MemeTrans (CC BY-NC-SA → any model trained on it `commercial_ok=false`).
- Features computed from archived contract/bytecode data, **point-in-time** (only information available at the token's evaluation time; no future holders/prices).
- Outputs: precision/recall/F1 of the rule baseline at reject thresholds, calibrated probability model (isotonic/logistic) with Brier/ECE, threshold recommendation; train/test split by time.
- Model registered in MLflow with dataset hashes and licence flags; advisory only (never overrides hard fails or the rule decision).

## ToDo

- [ ] Write dataset loaders + licence manifests in `packages/mt_airdrop/risk/calibrate/`.
- [ ] Build the PIT feature replay over archived data; notebook with evaluation.
- [ ] MLflow registration; tests for loaders and leakage; doc sync.

## Verification

### Tests
- Unit: loader schema tests per dataset.
- Leakage test: features for a token use only data with `event_time` ≤ evaluation time.
- Unit: MemeTrans-trained model artefact carries `commercial_ok=false`.

### Scenarios
- Given a time-split evaluation, when the model is fitted on 2020–2022 and tested on 2023, then metrics are reported with confidence intervals.

### Stress / failure injection
- n/a: offline batch notebook

## Acceptance criteria

- [ ] Notebook reproducible from a clean checkout + private data
- [ ] Baseline and model metrics produced
- [ ] Model in MLflow with licence flags
- [ ] No leakage (test)

## Exceptions & edge cases

- Some SoK contracts lack verified source: evaluate bytecode-only features; report coverage.

## Cardinal rules (do NOT)

- Do NOT commit any dataset or redistribute labels.
- Do NOT let the advisory model override the rule-based decision.
- Do NOT train on rows with `train_ok=false`.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: calibration results summary (link to P5-T055 report).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.26 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T039-risk-calibration-notebook`
- PR title: `P5-T039: Risk calibration notebook on SoK, SolRPDS, Pump.fun corpus and MemeTrans`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
