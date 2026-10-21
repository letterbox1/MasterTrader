---
id: P4-T029
kind: task
title: decision-svc stage 1: SemIf option-logit readout, KV publishing, determinism logging
phase: 4
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T028, P4-T009, P4-T025]
requirements: [R4.12]
roadmap_todos: [T4.28]
modules: [M21]
dashboards: [D01, D02, D08]
branch: p4/P4-T029-semif-readout-service
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T029 · decision-svc stage 1: SemIf option-logit readout, KV publishing, determinism logging

## Goal / expected outcome

`decision-svc` answers registry questions by reading **option-token logits** from Qwen3.5-4B (SemIf pattern, no text generation): it consumes `text.doc.new` and `models.tierb.ask`, returns normalised option probabilities, publishes `dec.tierb.{question}.{subject}`, updates KV `tierb_scores`, and logs every decision with `prompt_hash`, `model_revision`, `question_version` under the determinism controls.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.28](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (stage 1, determinism controls, outputs to NATS KV, veto only above calibrated threshold) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Flow: [02 F3 steps 5–7](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · degraded: [02 §9.3 GPU unavailable](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Research: [SemIf](../../../docs/research/decision-models-system-one.md) (0.81 balanced accuracy at 4B; prefix reuse flipped 5–6/777)
- Gap: P4-B010 (shared-prefix mode vs prefix caching off).

## Requirements

- Readout: build prompt from the question template + state; one forward pass; take logits of each option's first token (options tokenised to unique first tokens; validated at registry load); softmax over options only.
- Determinism: prefix caching off, fixed batch (1 or fixed padded), fixed seed, FP32 softmax on logits, pinned revision; log `prompt_hash` (sha256 of the exact prompt), `model_revision`, `question_version`, backend.
- Outputs: `dec.tierb.{question}.{subject}` + KV `tierb_scores` key `{question}:{subject}` with TTL by question (e.g. 24 h news).
- **Uncalibrated** stage 1: veto question output is advisory only (no `risk.event`) until a calibrated high-precision threshold exists (P4-T048/T053); then only above it.
- Concurrency: bounded worker pool; queue with priority (watchlist docs first); shed load by skipping non-gate questions when the queue > N.
- CPU mode (no GPU): only `relevance` runs; other questions disabled with status `degraded` (Risk mitigation).
- Shadow-check hook stub (5% to teacher) left disabled for P6.

## ToDo

- [ ] Readout core (`mt_models.tierb.semif`) + option-token validator.
- [ ] Consumers for `text.doc.new` and `models.tierb.ask`; publisher + KV writer.
- [ ] Audit writer to `audit.tierb_decision`.
- [ ] Load-shedding + CPU-mode policy.
- [ ] Metrics: latency p50/p95 per question, queue depth, abstain rate, flip-rate probe (re-ask 1% and compare).
- [ ] Tests.

## Verification

### Tests
- Unit: option tokenisation collision detected at load.
- Golden: 30 fixed prompts → stored probabilities; re-run equals within 1e-6 (CPU) / flip rate 0 on argmax (GPU).
- Integration: `text.doc.new` → `dec.tierb.relevance.{doc}` + KV entry + audit row.
- Guard: Telegram subject refused.

### Scenarios
- Given the LLM server is down, then decisions queue (bounded), D08 shows 'Scoring…' then 'Tier B unavailable', tier A unaffected.
- Given a burst of 5,000 docs, then relevance runs for watchlist docs first and other questions are shed with a metric.

### Stress / failure injection
- Latency/throughput run: record docs/min for relevance-only and full v1 set on this host (GPU and CPU); results into MLflow.

## Acceptance criteria

- [ ] v1 questions answered for live docs; KV + NATS + audit populated
- [ ] Determinism logging present on 100% of decisions
- [ ] Flip-rate probe reported in metrics
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Prompt longer than budget: state builder truncates; never the template.
- Restart: in-flight requests re-queued idempotently (decision id = hash(question version, subject, prompt_hash)).

## Cardinal rules (do NOT)

- Do NOT generate text or parse JSON from the model.
- Do NOT emit `risk.event` vetoes from uncalibrated scores.
- Do NOT enable prefix caching on the decision path.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3 stage 1: measured latency, CPU mode behaviour
- `docs/02-v1-architecture.md`: §9.2: add SemIf stage-1 latency target
- `docs/roadmap/phase-4-intel.md`: tick T4.28 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T029-semif-readout-service`
- PR title: `P4-T029: decision-svc stage 1: SemIf option-logit readout, KV publishing, determinism logging`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
