---
id: P6-T023
kind: task
title: GPU serving for tier B: vLLM pooling runner and ONNX Runtime
phase: 6
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.11]
roadmap_todos: [T6.40]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T023-gpu-serving-vllm-onnx
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T023 · GPU serving for tier B: vLLM pooling runner and ONNX Runtime

## Goal / expected outcome

`decision-svc` can serve own heads through a vLLM pooling runner (`/classify`, `--convert classify`) on the GPU and through ONNX Runtime on CPU, both bound to `127.0.0.1`/internal network with API keys, digest-pinned and monitored.

## Context & references

- Roadmap: [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.40
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (serving, hardware, AMD note: llama.cpp Vulkan) · [07 §5](../../../docs/07-security-notes.md#5-network--host) (local inference servers bind 127.0.0.1 + API key) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`decision-svc`) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)
- Gap: P6-B002 (latency numbers conflict)

## Requirements

- vLLM container (pinned digest) with pooling runner, LoRA adapter loading, `--enable-prefix-caching` **off**, fixed max batch, API key from sops; GPU device reservation.
- ONNX Runtime CPU worker image (FP32 for backtests; optional int8 for slow flags).
- Prometheus metrics: latency histograms per question/model, queue depth, GPU memory, timeouts, fallbacks.
- Degraded mode: GPU unavailable → route to ONNX CPU (slower) or disable non-critical questions; UI status `tierb_degraded`.
- AMD GPU path documented (no ROCm Laya; llama.cpp Vulkan for Qwen models) if the host has one.

## ToDo

- [ ] Compose services `vllm-classify` and `onnx-cpu` (internal network, healthchecks).
- [ ] Secrets wiring; API key required on every request.
- [ ] Grafana panel for tier-B latency vs SLO.
- [ ] Fallback routing config in `decision-svc`.
- [ ] Docs.

## Verification

### Tests
- Health + auth: unauthenticated request rejected.
- Smoke: classify a toy head via both runtimes; outputs match within 1e-4.

### Scenarios
- Given the GPU is removed (device unavailable), then `decision-svc` switches to ONNX CPU within 30 s and D10 shows degraded.
- Given a request without API key from another container, then 401.

### Stress / failure injection
- Covered by P6-T058 (p95 < 50 ms load test).

## Acceptance criteria

- [ ] Both runtimes healthy, internal-only, key-protected.
- [ ] Latency panel live.

## Exceptions & edge cases

- vLLM upgrade changes pooling semantics → pinned digest; upgrades are reviewed diffs.

## Cardinal rules (do NOT)

- Do NOT publish ports or run without API keys.
- Do NOT enable prefix caching on the decision path.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: serving config and measured numbers.
- `docs/02-v1-architecture.md` §3.2: decision-svc sidecars.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.40 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T023-gpu-serving-vllm-onnx`
- PR title: `P6-T023: GPU serving for tier B: vLLM pooling runner and ONNX Runtime`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
