---
id: P4-T073
kind: task
title: ONNX export and Rust/Python parity for the Chronos, TimesFM and Kronos forecasters
phase: 4
type: VERIFY
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T042]
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M6, M7, M21]
dashboards: []
tools: [cargo, uv, git]
mcp: []
env: []
services: [supabase-postgres, mlflow, mt-scheduler]
branch: p4/P4-T073-onnx-export-and-rust-python-parity-for-the-chron
pr: ""
doc_sync: [docs/03-build-spec.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
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

# P4-T073 · ONNX export and Rust/Python parity for the Chronos, TimesFM and Kronos forecasters

## Goal / expected outcome

For each volatility/volume forecaster of P4-T042 (Chronos Bolt small, TimesFM, Kronos) a recorded result says whether its ONNX export runs from Rust (`mt-models`, `ort`) with forecasts matching the Python reference on a fixed sample. Models that pass run nightly from Rust; models that don't keep running as `mt_research` batch jobs (offline features only, never on the decision path) and are recorded as such, so no forecaster is served from Rust without a passed parity check.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) (forecast models via ONNX in `mt-models`; U: export support per model)
- Spec: [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features) (forecast models run in `mt_research`; ONNX in Rust where they export cleanly (U))
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) · [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) (promoted models are exported to ONNX and run in Rust)
- Parity rule: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (Rust and Python scores match on a fixed sample before promotion; `mt-lab-core` runs the checks, [10 §6](../../../docs/10-memory-rag-and-models.md#6-where-this-lands-in-the-build))
- Related: P4-T042 (forecast runners, export scripts), P4-T054 (IC report uses these features), P4-T061 (exit demo evidence).

## Requirements

- Fixed sample: 50 instruments × 30 forecast origins from history read through `pit(as_of)`, inputs ending strictly before each origin.
- Per model: forecasts from the Rust `ort` runner match the Python reference (same pinned checkpoint) within a configurable tolerance (default relative difference ≤ 1e-3 on each quantile, set in `config/models/parity.yaml`); sampling-based models are compared in their deterministic mode (fixed seed / median forecast) only.
- Per model result recorded in `config/models/forecasters.yaml` and MLflow: `runtime: rust_onnx` (passed) or `runtime: python` (export failed or out of tolerance, with the reason); the P4-T042 job reads this field to choose the runner.
- Exported files pinned: checkpoint revision, opset, export tool version and sha256; `mt-models` refuses a file whose sha256 doesn't match.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env` names, `services`); `./kanban preflight P4-T073` checks them before start.

## ToDo

- [ ] Build the fixed sample and the Python reference forecasts (`mt_research`, `uv run`)
- [ ] Export each forecaster to ONNX (`mt_research` export scripts from P4-T042) and record revision, opset and sha256
- [ ] Parity harness in `mt-lab-core` (Rust) comparing the `mt-models` runner with the reference
- [ ] Record each model's runtime decision in `config/models/forecasters.yaml` and MLflow; file a gap item for any model left on Python (pm-triage)
- [ ] Wire the parity check into CI for changes to the export scripts, ONNX files or the `mt-models` runner
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Parity per model on the fixed sample (`cargo test -p mt-lab-core`).
- Unit: the runner chooser in the P4-T042 job follows `runtime` from `forecasters.yaml`.
- Unit: `mt-models` refuses an ONNX file with a wrong sha256.

### Scenarios
- Given Kronos fails to export (U), then it stays on the Python runner with the reason recorded, and the other two run from Rust.
- Given a new checkpoint revision is pinned, then parity re-runs and the model stays on its previous runtime until it passes.

### Stress / failure injection
- n/a: correctness check on a fixed sample; the nightly runtime budget is measured in P4-T042.

## Acceptance criteria

- [ ] A recorded parity result and runtime decision for each of the three forecasters
- [ ] No model runs from Rust without a passed parity check (test)
- [ ] CI green (`cargo test -p mt-lab-core -p mt-models`, `cargo clippy`, ruff, mypy, `uv run pytest` (`mt_research`), `pit` bypass check)

## Exceptions & edge cases

- A model that needs custom ONNX operators or dynamic control flow that `ort` can't run stays on Python; that's a recorded outcome, not a failure of this task.
- GPU absent: parity runs on CPU FP32.

## Cardinal rules (do NOT)

- Do NOT loosen the parity tolerance to get green; a change to the default goes through the configuration doc.
- Do NOT read inputs except through `pit(as_of)`; no look-ahead in the sample.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`), unpinned checkpoints or vendored code with telemetry/referral IDs; pin by digest and hash.

## Doc sync on completion

- `docs/03-build-spec.md`: M6: record which forecasters run from Rust and which stay in `mt_research`
- `docs/10-memory-rag-and-models.md`: record the parity results
- `docs/roadmap/phase-4-intel.md`: tick T4.27 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T073-onnx-export-and-rust-python-parity-for-the-chron`
- PR title: `P4-T073: ONNX export and Rust/Python parity for the Chronos, TimesFM and Kronos forecasters`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T073` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (ONNX export/parity check for the forecasters; models that fail stay `mt_research` batch jobs per 03 M6)
