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
depends_on: [P0-T005, P0-T020, P0-T022, P4-T029]
requirements: [R6.11, R6.N2, R6.N3]
roadmap_todos: [T6.40]
modules: [M21]
dashboards: [D10]
tools: [git, docker, sops, nvidia-smi]
mcp: []
env: []
services: [gpu, prometheus, grafana]
branch: p6/P6-T023-gpu-serving-vllm-onnx
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T023 · GPU serving for tier B: vLLM pooling runner and ONNX Runtime

## Goal / expected outcome

`decision-svc` can serve own heads through a vLLM pooling runner (`/classify`, `--convert classify`) on the GPU and through ONNX Runtime on CPU, both bound to `127.0.0.1`/internal network with API keys, digest-pinned and monitored.

## Context & references

- Roadmap: [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.40
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (serving, hardware, AMD note: llama.cpp Vulkan) · [07 §5](../../../docs/07-security-notes.md#5-network--host) (local inference servers bind 127.0.0.1 + API key) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`decision-svc`) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)
- Decision: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P6-B002: ~2–12 ms per decision on GPU (0.6B), p95 SLO < 50 ms; CPU 100–400 ms) · [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B010: prefix caching off on the decision path)
- Cross-phase: P0-T005 (GPU decision), P0-T020 (Compose), P0-T022 (secrets → tmpfs), P4-T029 (decision-svc stage 1)
- Verified by: P6-T069 (port/API-key check, T6.73), P6-T058 (latency, T6.71)

## Requirements

- vLLM container (pinned digest) with pooling runner, LoRA adapter loading, prefix caching **off** on the decision path (shared-prefix mode only in a separate offline/backfill instance whose scores are marked non-deterministic and never used for decisions or backtests), fixed batch, bound to `127.0.0.1`/the internal network with an API key from the sops file (R6.N2, 07 §5); GPU device reservation.
- Latency targets (R6.N3): ~2–12 ms typical and p95 < 50 ms per decision on GPU (0.6B); CPU ONNX 100–400 ms, used for slow flags only; never on the order path.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (prefix caching off on decision path (17 §A P4-B010); latency per 17 §B P6-B002 (R6.N3); 127.0.0.1 + API key (R6.N2); cross-phase deps P0-T005/T020/T022/P4-T029; run fields)
