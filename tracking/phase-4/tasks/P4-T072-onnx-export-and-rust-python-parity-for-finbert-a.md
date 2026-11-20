---
id: P4-T072
kind: task
title: ONNX export and Rust/Python parity for FinBERT and the GLiNER entity model
phase: 4
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T026, P4-T027]
requirements: [R4.06]
roadmap_todos: [T4.23]
modules: [M2, M7, M21]
dashboards: [D08]
tools: [cargo, uv, git]
mcp: []
env: []
services: [mlflow]
branch: p4/P4-T072-onnx-export-and-rust-python-parity-for-finbert-a
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
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

# P4-T072 · ONNX export and Rust/Python parity for FinBERT and the GLiNER entity model

## Goal / expected outcome

The FinBERT sentiment model (P4-T027) and the optional GLiNER entity model (P4-T026) are exported to ONNX by `mt_research` (Python) and served from Rust in `mt-nlp` through `ort`; this check proves that the Rust outputs match the Python reference on a fixed sample before either model is switched on in the pipeline, as [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) requires for every model trained or exported in Python and served from Rust.

## Context & references

- Roadmap: [R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.23](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20): the NLP pipeline runs in Rust with FinBERT and the entity model via ONNX/`ort`; training and export stay Python ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)).
- Models: [10 §2](../../../docs/10-memory-rag-and-models.md#2-local-embedders--rerankers) (FinBERT runs in `mt-nlp` as ONNX; fine-tuning stays in `mt_research`) · [10 §6](../../../docs/10-memory-rag-and-models.md#6-where-this-lands-in-the-build) (`mt-lab-core` runs the Rust/Python parity checks)
- Related: P4-T026 (GLiNER export script + optional NER stage), P4-T027 (FinBERT export script + `ort` runner), P4-T025 (provenance guard on both sides), P4-T061 (exit demo evidence). GLiNER via ONNX is unverified (U, 18 §2.1).

## Requirements

- Fixed parity sample: 500 finance sentences/headlines (public, committed as fixtures, no Telegram text) plus 50 long documents that exercise the sentence-window aggregation.
- FinBERT: per-class probabilities from the Rust `ort` runner match the Python reference (PyTorch, same pinned revision) within a configurable tolerance (default max absolute difference 1e-4, set in `config/models/parity.yaml`); argmax label agreement 100 % on the sample; tokenizer token ids identical.
- GLiNER: entity spans and labels identical on the sample; scores within the same configurable tolerance. If the export is not faithful (U), the NER stage stays off, the linker runs on dictionaries and rules only, and a gap item is filed (pm-triage); nothing ships unchecked.
- The exported files are pinned: model revision, opset, export tool version and sha256 recorded in `config/models/onnx.yaml` and MLflow; `mt-nlp` refuses to load a file whose sha256 doesn't match.
- Both sides read inputs through the P4-T025 guard; the sample holds no `model_input_ok = false` rows.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env` names, `services`); `./kanban preflight P4-T072` checks them before start.

## ToDo

- [ ] Build the parity sample fixtures and the Python reference outputs (`mt_research`, `uv run`)
- [ ] Parity harness in `mt-lab-core` (Rust) that runs the `mt-nlp` runners and compares with the Python reference
- [ ] Record revision, opset, export tool version, sha256 and parity results in `config/models/onnx.yaml` and MLflow
- [ ] Wire the parity check into CI for any change to the export scripts, the ONNX files or the `mt-nlp` runners
- [ ] Turn the GLiNER stage on only if its parity passes; otherwise file the gap and keep it off
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Parity: FinBERT probabilities within tolerance and 100 % argmax agreement on the fixed sample (`cargo test -p mt-lab-core`).
- Parity: GLiNER spans/labels identical and scores within tolerance (or the stage recorded as off with a gap item).
- Unit: tokenizer ids from the Rust `tokenizers` crate equal the Python tokenizer on the sample.
- Unit: `mt-nlp` refuses an ONNX file with a wrong sha256.

### Scenarios
- Given a new FinBERT revision is exported, when the parity check runs, then a mismatch blocks the switch and the old pinned file stays in use.
- Given an `ort` upgrade changes numerics beyond the tolerance, then CI fails before the upgrade merges.

### Stress / failure injection
- n/a: correctness check on a fixed sample; throughput is covered by P4-T027 and P4-T058.

## Acceptance criteria

- [ ] FinBERT parity passes on the fixed sample and is recorded in MLflow
- [ ] GLiNER parity passes, or the NER stage is off with a filed gap item
- [ ] Pinned revision, opset and sha256 recorded; load-time hash check proven
- [ ] CI green (`cargo test -p mt-lab-core -p mt-nlp`, `cargo clippy`, ruff, mypy, `uv run pytest` (`mt_research`), `pit` bypass check)

## Exceptions & edge cases

- GPU absent: parity runs on CPU (FP32) only; that is the serving path for both models.
- A model whose ONNX export needs custom operators is not served from Rust until they are supported; it stays off (no Python fallback on the pipeline path).

## Cardinal rules (do NOT)

- Do NOT loosen the parity tolerance to get green; a change to the default goes through the configuration doc.
- Do NOT put Telegram text (or any `model_input_ok = false` row) in the parity sample, a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`), unpinned model revisions or vendored code with telemetry/referral IDs; pin by digest and hash.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §2: record the FinBERT/GLiNER export revision, tolerance and parity result
- `docs/roadmap/phase-4-intel.md`: tick T4.23 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T072-onnx-export-and-rust-python-parity-for-finbert-a`
- PR title: `P4-T072: ONNX export and Rust/Python parity for FinBERT and the GLiNER entity model`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T072` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (ONNX export/parity check for models trained in Python and served from Rust in `mt-nlp`)
