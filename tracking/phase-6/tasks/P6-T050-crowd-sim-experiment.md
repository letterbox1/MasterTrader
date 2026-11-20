---
id: P6-T050
kind: task
title: mt-crowdsim scenario & crowd simulator (clean-room Rust, seeded, capped shocks)
phase: 6
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T074, P0-T042, P0-T044, P4-T013, P4-T033]
requirements: [R6.32, R6.34]
roadmap_todos: [T6.30]
modules: [M14, mt-crowdsim, mt-agents]
dashboards: [D06, D14]
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [litellm, llm-local, supabase-postgres, nats]
branch: p6/P6-T050-crowd-sim-experiment
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, docs/02-v1-architecture.md, docs/research/mirofish.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T050 · mt-crowdsim scenario & crowd simulator (clean-room Rust, seeded, capped shocks)

## Goal / expected outcome

`mt-crowdsim` turns a headline or event into a simulated crowd reaction and a **scenario**: a population of LLM persona agents (retail, funds, market makers, media, bots; default 200 agents × 10 rounds) runs seeded and recorded on the local model, and the run yields a sentiment path plus price, volatility, spread and liquidity shocks capped by `crowdsim.max_shock`. Each week it picks the week's top events plus one tail scenario. The scenario twin (P6-T075) injects these scenarios into a second paper engine, and the pre-live stress tests (P7-T069) replay them. It is a **go-live tool**, not an optional experiment, and is built early: it needs only the P0 gateway and local model, the event feeds and the `mt-agents` runtime.

## Context & references

- Roadmap: [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.34](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.30
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) (what it does, boundaries, "build early") · defaults [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) · decision [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (supersedes P6-B009's "otherwise skip") · [19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime) (MiroFish/OASIS: idea only, clean-room)
- Spec: [03 M14](../../../docs/03-build-spec.md#m14-scenario--crowd-simulator-go-live-tool) (heading kept for links; now the go-live simulator) · flow [02 F12](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 1–2 · [research: MiroFish](../../../docs/research/mirofish.md) (AGPL, Zep Cloud, insecure defaults: why we take the idea, not the code)
- Data rules: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (synthetic rows: `synthetic = true`, `train_ok = false`, `model_input_ok = false`)
- UI: [D06](../../../docs/ui/dashboards/D06-risk.md) Stress tab (simulated scenarios, P7) · [D14](../../../docs/ui/dashboards/D14-journal.md) scenario-twin report (P6-T077)
- Cross-phase: P0-T042 (LiteLLM gateway, audit callback), P0-T044 (`local-advisor` on `llm-local`), P4-T013 (GDELT news volume/tone and headlines), P4-T033 (global event pollers in `mt-events`). Other event sources (P4-T034 conflict/sanctions, P4-T035 event score, calendars) are read when present and mocked in tests; they are not dependencies
- Depends on (this phase): P6-T074 (`mt-agents` runtime). Not on P6-T003: the simulator is not an optional module (16 §2.14a marks `modules.crowdsim.enabled` superseded)
- Used by: P6-T075 (scenario twin), P6-T076 (containers and settings), P6-T078 (isolation/provenance tests), P7-T069 (pre-live stress replay)

## Requirements

- **Clean-room Rust** in `crates/mt-crowdsim`: no MiroFish or OASIS code, no Zep or any hosted memory; persona agents run on the `mt-agents` runtime (P6-T074).
- **Inputs:** one headline or event from `text.document` / `text.geo_event` (read through `pit(as_of)`), or a tail-scenario template (e.g. exchange outage, stablecoin de-peg, surprise rate move) chosen from a seeded list.
- **Weekly pick** (`crowdsim.scenarios_per_week`, default 3): the week's top events by event score when available (else by news volume and severity) plus one tail scenario; the pick and its reasons are stored.
- **Population** (`crowdsim.population`, default 200 persona agents, 10 rounds): archetype mix (retail, funds, market makers, media, bots) and per-agent traits drawn from the run seed; each round agents read the previous round's crowd state and post a stance and intensity. Archetype prompts live in the prompt registry (versioned).
- **Seeded and recorded:** run seed, config hash, prompt versions, model route and revision, and every round's aggregate stored; the same seed + config + recorded model responses replays to the same scenario byte for byte (replay mode reads recorded responses, never the model).
- **Scenario output:** sentiment path per round, then a shock vector per affected instrument or asset class (price %, volatility ×, spread ×, liquidity ÷, onset and decay), mapped from the crowd path by a deterministic Rust function. Every shock is **clamped to `crowdsim.max_shock`** (defaults price ±15%, volatility ×3, spread ×5, liquidity ÷5); clamping is recorded.
- **Export format:** the scenario is written in the shock format `risk.stress.run` reads (T7.27 / P7-T068), so the same row feeds the twin and the stress tab.
- **Model route:** `crowdsim.model_route`, default `local-advisor`; a cloud route is used only inside the LLM budget (16 §2.10). Until 16 §2.10 lists a budget for simulator calls, cloud routes are refused (U, raised in the report) and the run stays local.
- **Provenance:** every row the simulator writes carries `synthetic = true`, `train_ok = false`, `model_input_ok = false`; tables in the `risk` schema (`risk.sim_run`, `risk.sim_scenario`; names proposed for 02 §5 via doc sync), insert-only.
- **Isolation:** no venue keys, no signer route, no `ord.*` publish rights; NATS permissions allow only `sim.*` subjects and reads of the event subjects (enforced in P6-T076, tested in P6-T078).
- **Commands/queries:** `sim.crowdsim.run` (C1: run one scenario now from an event id or template) and `GET /sim/scenarios`, `GET /sim/runs` through `mt-api`.
- Nothing is hard-coded: population, rounds, archetype mix, scenarios per week and caps are settings (16 §2.14b), seeded by P6-T076.

## ToDo

- [ ] Create `crates/mt-crowdsim` (population, rounds, crowd state, shock mapper, clamp) on the `mt-agents` runtime.
- [ ] Archetype prompts in the prompt registry; `NOTICE` only if any text is adapted from an Apache/MIT source.
- [ ] Event reader through `pit(as_of)` and the weekly picker (top events + one tail template), with fixtures for tests.
- [ ] Seeded RNG, run recorder and replay mode (recorded responses).
- [ ] SQL migration in `supabase/migrations/` for `risk.sim_run` and `risk.sim_scenario` (insert-only, `synthetic`, `train_ok`, `model_input_ok` columns with check constraints).
- [ ] Scenario export in the `risk.stress.run` shock format; publish `sim.scenario.new`.
- [ ] `sim.crowdsim.run` command and `/sim/*` queries in `mt-api`.
- [ ] Weekly job registered with `mt-scheduler` (P1-T077) when it exists; until then the command runs it.
- [ ] Tests (see Verification); docs.

## Verification

### Tests
- `cargo test -p mt-crowdsim` and `cargo clippy`; `supabase test db` (insert-only grants; `synthetic` rows must have `train_ok = false` and `model_input_ok = false`).
- Unit: shock mapper monotonicity; clamp at every cap; archetype mix sums to the population; weekly picker on fixture events.
- Determinism: the same seed, config and recorded responses produce an identical scenario hash on two runs.
- Integration (fake gateway + `local-advisor` fixtures): a CPI-surprise headline yields a scenario row, a run row and a `sim.scenario.new` message.

### Scenarios
- Given a central-bank surprise headline, when the simulator runs with seed 42, then it stores a 10-round sentiment path and a shock vector within `crowdsim.max_shock`, and replaying seed 42 returns the same scenario.
- Given a raw crowd path that would imply a −30% price move, then the stored shock is −15% and the clamp is recorded.
- Given `crowdsim.model_route` set to a cloud route with no simulator budget, then the run uses `local-advisor` and says why.

### Stress / failure injection
- Full default run (200 agents × 10 rounds) on the CPU `local-advisor` profile completes inside the weekly window; record wall time and calls (archetype batching per round keeps calls bounded).
- Gateway down mid-run: the run stops cleanly, is marked `failed` and leaves no partial scenario; LLM budget exhausted: the run continues on `local-advisor` or stops cleanly.

## Acceptance criteria

- [ ] A seeded run produces a scenario within the caps and replays identically.
- [ ] The weekly pick yields 3 scenarios (2 events + 1 tail by default) from fixtures.
- [ ] Every simulator row is `synthetic = true` with `train_ok = false` and `model_input_ok = false`.
- [ ] Scenarios export in the `risk.stress.run` format.
- [ ] CI green (`cargo test`, `cargo clippy`, `supabase test db`, `pit` bypass check).

## Exceptions & edge cases

- Non-determinism of a live model: scenarios are stored from the run, and replays use the recorded responses; variance across 3 seeds is reported for each weekly event.
- No qualifying events in a week: tail templates fill the slots and the report says so.
- An event that names an instrument outside the bots' universe maps to its asset class; nothing is invented for instruments the twin doesn't trade.
- Simulated results are an extra input, never a gate, unless 16 says so.

## Cardinal rules (do NOT)

- Do NOT copy MiroFish or OASIS code, and do NOT use Zep Cloud or any hosted service; idea only (19 §3).
- Do NOT give the simulator venue keys, a signer route or any order subject; it never trades real paper or live accounts.
- Do NOT let `synthetic = true` rows reach features, model training, RAG or memory, whatever the settings say (18 §2.4, 12 §5).
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT inject a shock outside `crowdsim.max_shock`, and do NOT hard-code the caps.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M14: scenario format, weekly pick, table names.
- `docs/18-platform-and-deployment.md` §2.4: confirm the boundaries as built.
- `docs/02-v1-architecture.md` §5/§6 and F12: `risk.sim_run`, `risk.sim_scenario`, `sim.*` subjects.
- `docs/research/mirofish.md`: note that the clean-room Rust simulator replaced the experiment.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.30 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T050-crowd-sim-experiment`
- PR title: `P6-T050: mt-crowdsim scenario & crowd simulator (clean-room Rust, seeded, capped shocks)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (M14 local-memory-backend/hardened-config rule, else skipped (17 §D P6-B009); run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (optional module off by default (P6-T003, agent); depends on nothing human)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (re-scoped from the optional OASIS experiment to the `mt-crowdsim` go-live simulator in Rust; no longer optional; depends only on P6-T074, P0 gateway/local model and the P4 event feeds, not on P6-T003; priority high)
