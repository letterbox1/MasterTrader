---
id: P6-T076
kind: task
title: crowdsim and scenario-twin containers on an isolated network with seeded crowdsim settings
phase: 6
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T050, P6-T075, P0-T020]
requirements: [R6.32, R6.33, R6.34]
roadmap_todos: [T6.42]
modules: [M14, mt-crowdsim, mt-engine, mt-api]
dashboards: [D16]
tools: [git, docker, cargo, supabase]
mcp: []
env: []
services: [nats, litellm, llm-local, supabase-postgres, mt-api]
branch: p6/P6-T076-crowdsim-and-scenario-twin-containers-on-an-isol
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T076 · crowdsim and scenario-twin containers on an isolated network with seeded crowdsim settings

## Goal / expected outcome

The `crowdsim` (`mt-crowdsim`) and `scenario-twin` (twin-mode `mt-engine`) containers run digest-pinned on their own `sim` network with no route to the signer, venue keys or the real engine's order subjects; their only LLM route is the gateway's `local-advisor` inside the LLM budget; and the `crowdsim.*` settings are seeded from 16 §2.14b through `mt-api` (source `seed`), so the simulator and the twin can run from the first paper weeks without anyone setting a value.

## Context & references

- Roadmap: [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.34](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.42
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) (isolated, no route to the signer, local model by default) · defaults [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) · decision [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)
- Security: [07 §5](../../../docs/07-security-notes.md#5-network--host) (networks, localhost binding) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (no keys in these containers) · data rules [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Settings pattern: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (agents seed configurable defaults; you review them in the go-live pack, P7-T070)
- Cross-phase: P0-T020 (Compose stack, digest pinning, networks)
- Depends on (this phase): P6-T050 (`mt-crowdsim`), P6-T075 (twin mode)
- Verified by: P6-T078 (isolation and provenance)

## Requirements

- Containers `crowdsim` and `scenario-twin` in Compose, images built from the workspace on a digest-pinned base; compose profile `sim` started only while `crowdsim.scenario_twin.enabled` is on or a manual run is requested.
- Network `sim`: reaches NATS (sim account), the LiteLLM gateway (local route) and Supabase Postgres (sim roles) only; no route to `signer`, venue egress or the `scrape` network; no ports published on the host.
- NATS account `sim`: publish `sim.>` only; subscribe to `sim.>` and the read-only event/text subjects the picker needs; no `ord.*`, `exec.*` or `risk.cmd.*` rights.
- Database roles `sim_crowdsim` and `sim_twin`: INSERT/SELECT on `risk.sim_*` and `risk.twin_*` only; SELECT through `pit` on the replay inputs; no grant on `journal.*`, `strategy.*`, `features.*`, `rag.*`, `models.label` or any secret store.
- No secret files mounted except the per-service NATS and DB credentials generated into the sealed file; no exchange, wallet or LLM-provider keys.
- Gateway: per-service virtual key restricted to the `local-advisor` route by default; cloud routes only if 16 §2.10 grants the simulator a budget.
- Settings seeded via `mt-api` (`system.settings.update`, source `seed`, idempotent, never overwriting your edits): `crowdsim.scenario_twin.enabled` (on during paper and before live), `crowdsim.scenarios_per_week` (3), `crowdsim.population` (200 agents, 10 rounds), `crowdsim.model_route` (`local-advisor`), `crowdsim.max_shock` (price ±15%, volatility ×3, spread ×5, liquidity ÷5). Raising `max_shock` or switching to a cloud route is C1 and shown in the go-live pack.

## ToDo

- [ ] Compose services `crowdsim` and `scenario-twin` (profile `sim`, healthchecks, resource limits, digest-pinned).
- [ ] `sim` network and firewall rules; no host ports.
- [ ] NATS `sim` account with publish/subscribe permissions above.
- [ ] SQL migration in `supabase/migrations/` for the `sim_crowdsim` / `sim_twin` roles and grants.
- [ ] LiteLLM virtual key for the simulator limited to `local-advisor`.
- [ ] Seed the five `crowdsim.*` settings through `mt-api` (idempotent, source `seed`); add them to the go-live pack rows (P7-T070).
- [ ] Image scan (trivy/grype) and exposure check (P0-T056 script) on the new containers.
- [ ] Tests; docs.

## Verification

### Tests
- `supabase test db`: the sim roles can't write `journal.*`, `strategy.*`, `features.*`, `rag.*` or `models.label`.
- `cargo test -p mt-api settings_seed_crowdsim`: five settings seeded with source `seed`; re-run adds nothing; your edit survives a re-seed.
- Compose check: no host port published; `sim` network has no route to `signer` (connection refused from inside the container).

### Scenarios
- Given the `crowdsim` container, when it tries to publish `ord.intent.test`, then NATS rejects it with a permissions error.
- Given the simulator key, when it requests `research-primary`, then LiteLLM refuses the route.

### Stress / failure injection
- Stop NATS or Postgres while the twin runs: the containers restart cleanly and the run is retried, with no writes outside `risk.sim_*` / `risk.twin_*`.

## Acceptance criteria

- [ ] Both containers run digest-pinned on the isolated `sim` network.
- [ ] No route to the signer, venue keys or real order subjects (tests).
- [ ] The five `crowdsim.*` settings are seeded and listed in the go-live pack.
- [ ] CI green (`supabase test db`, `cargo test`, image scan).

## Exceptions & edge cases

- Without a GPU the CPU `local-advisor` profile is slow; the weekly window and archetype batching (P6-T050) keep it workable; record wall times.
- Turning the twin off (`crowdsim.scenario_twin.enabled: false`) stops the profile; reports simply stop.

## Cardinal rules (do NOT)

- Do NOT mount exchange, wallet or LLM-provider keys into the simulator or twin containers.
- Do NOT give the `sim` network a route to the signer, venue egress or the real engine's order subjects.
- Do NOT turn any setting on or loosen it for the user beyond the documented defaults.
- Do NOT let `synthetic = true` rows reach features, training, RAG or memory.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: `crowdsim` and `scenario-twin` containers, `sim` network.
- `docs/07-security-notes.md` §5: the `sim` network and NATS account.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.42 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T076-crowdsim-and-scenario-twin-containers-on-an-isol`
- PR title: `P6-T076: crowdsim and scenario-twin containers on an isolated network with seeded crowdsim settings`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T076` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (new task for the scenario & crowd simulator workstream, 18 §2.4)
