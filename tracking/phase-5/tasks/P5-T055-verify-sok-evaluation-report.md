---
id: P5-T055
kind: task
title: SoK evaluation report: precision/recall vs the rule-based baseline
phase: 5
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T039]
requirements: [R5.13]
roadmap_todos: [T5.62]
modules: [M4]
dashboards: []
tools: [uv, jupyter]
mcp: []
env: []
services: [mlflow]
branch: p5/P5-T055-verify-sok-evaluation-report
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T055 · SoK evaluation report: precision/recall vs the rule-based baseline

## Goal / expected outcome

A written evaluation report (`docs/reports/p5-sok-risk-evaluation.md`, numbers only, no dataset content) gives precision/recall/F1 of the rule-based baseline and the advisory model on SoK (time-split) and on SolRPDS/Pump.fun (Solana), with CRPWarner's published P 91.8% / R 85.9% as a reference point, and recommends thresholds.

## Context & references

- Roadmap: ToDo T5.62 → R5.13 ("Calibration report")
- Notebook P5-T039 · [research CRPWarner/SoK](../../../docs/research/airdrops-rugpull-discord.md)

## Requirements

- Metrics per dataset and per rug type (SoK has 14 types); confusion matrices; Brier/ECE for the model; coverage (share of tokens with full features).
- Baseline remains authoritative; report states whether the model is useful as an advisory signal.
- Threshold recommendation for `reject` vs `watch`, with expected false-positive rate on established tokens.
- Licence statement per dataset; no redistribution of labels.

## ToDo

- [ ] Run the notebook from a clean environment; export metrics.
- [ ] Write the report with tables and recommendations.
- [ ] Apply recommended thresholds via a config PR (tighten freely; loosening needs your C3 approval, 16 §1).

## Verification

### Tests
- Reproducibility: two runs produce identical metrics (seeded).

### Scenarios
- Given the baseline recall on SoK < 80%, then the report lists the missed rug types and follow-up tasks are filed.

### Stress / failure injection
- n/a: offline report

## Acceptance criteria

- [ ] Report merged with metrics, thresholds and licence notes
- [ ] Thresholds config updated or explicitly unchanged with rationale

## Exceptions & edge cases

- If datasets are unavailable, the report states which and the phase exit uses the remaining ones (documented).

## Cardinal rules (do NOT)

- Do NOT include dataset rows or labels in the repo.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: link the report under Calibrate.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.62 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T055-verify-sok-evaluation-report`
- PR title: `P5-T055: SoK evaluation report: precision/recall vs the rule-based baseline`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T055` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (threshold loosening is C3)
