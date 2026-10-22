---
id: P6-T027
kind: task
title: Bake-off contender containers: Laya, Clef-flash, Kev, JSON baseline
phase: 6
type: OPS
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T068, P0-T020, P0-T022]
requirements: [R6.12, R6.N2]
roadmap_todos: [T6.40]
modules: [M21]
dashboards: [D10]
tools: [git, docker, sops]
mcp: []
env: []
services: [gpu, huggingface-hub]
branch: p6/P6-T027-bakeoff-contender-containers
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, third_party/LICENSES.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T027 · Bake-off contender containers: Laya, Clef-flash, Kev, JSON baseline

## Goal / expected outcome

Every bake-off contender runs locally, digest-pinned, bound to `127.0.0.1`/internal network with an API key: Laya server (`LAYA_API_KEY`), self-hosted Clef-flash (FP8 ~11.5 GB or NF4 8 GB), Kev-4B/9B (only if P6-T068 found a public, licence-compatible release), the SemIf service from P4 and a JSON-generation baseline on `local-advisor`.

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.40
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (contenders, Laya serving notes) · [10 §4.1](../../../docs/10-memory-rag-and-models.md#41-what-decision-models-are-and-the-candidates) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · [07 §7](../../../docs/07-security-notes.md#7-supply-chain)
- [research: decision models](../../../docs/research/decision-models-system-one.md)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B003: Kev only if a public, licence-compatible release exists; checked by P6-T068)
- Cross-phase: P0-T020 (Compose), P0-T022 (secrets → tmpfs)
- Verified by: P6-T069 (port/API-key check, T6.73, R6.N2)
- Depends on (this phase): P6-T068

## Requirements

- Compose profile `bakeoff` (not started by default) with pinned digests or locally built images from pinned commits.
- Each server binds to `127.0.0.1`/the internal network and requires an API key from the sops file (R6.N2, 07 §5); no published ports; outbound internet off after weights are fetched.
- GPU sharing: contenders run one at a time via the harness (VRAM 16–24 GB); a lock prevents co-scheduling with production vLLM beyond capacity.
- Licence entries in `third_party/LICENSES.md` (Laya Apache-2.0, Clef weights Apache-2.0, SemIf MIT, Kev per P6-T068).
- Telemetry grep on each image/codebase.

## ToDo

- [ ] Compose profile + start/stop scripts used by the harness.
- [ ] Weights download script with checksum pinning (HF revision).
- [ ] API key wiring.
- [ ] GPU lock.
- [ ] Licence + telemetry review.
- [ ] Docs.

## Verification

### Tests
- Smoke: each contender answers one typed question with a valid probability vector.
- Auth: request without key rejected.
- Egress: no outbound traffic during inference.

### Scenarios
- Given Kev was marked dropped in P6-T068, then the profile omits it and the harness reports it as excluded.

### Stress / failure injection
- Start Clef-flash while production vLLM is loaded: the GPU lock refuses or pauses the bake-off rather than OOM-ing production.

## Acceptance criteria

- [ ] All available contenders smoke-tested.
- [ ] Licences and exclusions documented.

## Exceptions & edge cases

- AMD GPU: Laya has no ROCm build — run Laya on CPU (~0.7 s/question, batch by question) and Qwen-based models via llama.cpp Vulkan.

## Cardinal rules (do NOT)

- Do NOT use hosted/paid versions of any contender.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: contender serving notes.
- `third_party/LICENSES.md`: contender licences.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.40 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T027-bakeoff-contender-containers`
- PR title: `P6-T027: Bake-off contender containers: Laya, Clef-flash, Kev, JSON baseline`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Kev per 17 §D P6-B003 via agent check P6-T068 (not the USER item); R6.N2; cross-phase deps P0-T020/T022; run fields)
