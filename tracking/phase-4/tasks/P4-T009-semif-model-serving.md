---
id: P4-T009
kind: task
title: Serve Qwen3.5-4B for SemIf with pinned revisions
phase: 4
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.12]
roadmap_todos: [T4.41]
modules: [M21]
dashboards: [D10, D16]
branch: p4/P4-T009-semif-model-serving
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T009 · Serve Qwen3.5-4B for SemIf with pinned revisions

## Goal / expected outcome

A local inference server (vLLM on NVIDIA, or llama-server with Vulkan on AMD, or llama.cpp CPU fallback) serves Qwen3.5-4B at a pinned model revision, exposing next-token **logits** for option tokens, bound to `127.0.0.1`/the internal network with an API key, ready for `decision-svc` (P4-T029).

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.41](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Risk 'CPU-only SemIf is slow'
- Design: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (SemIf on Qwen3.5-4B; determinism controls; AMD → llama.cpp Vulkan) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Evidence: [decision-models research](../../../docs/research/decision-models-system-one.md) (4B balanced accuracy 0.81; 0.6B worse than chance)
- Security: [07 §5](../../../docs/07-security-notes.md#5-network--host) (inference servers bind to 127.0.0.1 and require an API key)
- Cross-phase: P0 T0.01 GPU decision.

## Requirements

- Model: Qwen3.5-4B, revision pinned by commit hash in `config/models/semif.yaml`; weights checksum verified at start.
- Serving: GPU path vLLM (logprobs/logits endpoint) or llama-server (`--logits-all` equivalent / `n_probs`); CPU path llama.cpp with the same API shape.
- Determinism settings: prefix caching **off**, fixed batch (1 or padded fixed), FP32 logits readout where the backend allows, seed fixed.
- Bound to internal network only; `SEMIF_API_KEY` from secrets; no published port.
- Expose `/health` and Prometheus metrics (latency, queue depth, tokens/s).

## ToDo

- [ ] Add `semif-llm` service to Compose (GPU or CPU profile), digest-pinned image.
- [ ] Download weights to the models volume via a script that verifies the pinned revision + sha256.
- [ ] Configure determinism flags and API key; document GPU vs CPU profiles.
- [ ] Benchmark: latency p50/p95 for one document × 5 binary questions on this host (GPU and/or CPU); record in MLflow.
- [ ] Register the model in `models.registry` (tier B stage 1, revision, backend, benchmark).

## Verification

### Tests
- Smoke: a fixed prompt returns identical option-token logits on 50 repeated calls (flip rate 0 at the API level).
- Security: request without API key → 401; from scrape network → unreachable.

### Scenarios
- Given no GPU (T0.01 = CPU fallback), when started with the CPU profile, then it serves at reduced speed and `decision-svc` restricts to the relevance gate (Risk mitigation).
- Given the weights' checksum mismatches the pinned revision, then the service refuses to start.

### Stress / failure injection
- Queue 500 requests: backpressure (HTTP 429/queue) instead of OOM; memory within the VRAM/RAM budget; recovery after queue drains.

## Acceptance criteria

- [ ] Model served at the pinned revision with determinism flags on
- [ ] Benchmark recorded (p50/p95 per document × 5 questions) and registered
- [ ] API key + internal binding verified
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- On AMD (e.g. 7900 XTX) use llama.cpp Vulkan: no ROCm build is assumed.
- GPU OOM → automatic restart into CPU profile is NOT automatic; it alerts and `decision-svc` degrades (02 §9.3 'GPU unavailable').

## Cardinal rules (do NOT)

- Do NOT use Qwen3-0.6B for SemIf (worse than chance).
- Do NOT enable prefix caching on the decision path.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3: record the chosen backend, revision and measured latency
- `docs/roadmap/phase-4-intel.md`: tick T4.41 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T009-semif-model-serving`
- PR title: `P4-T009: Serve Qwen3.5-4B for SemIf with pinned revisions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
