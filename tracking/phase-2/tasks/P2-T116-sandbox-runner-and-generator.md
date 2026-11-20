---
id: P2-T116
kind: task
title: Sandbox runner and LLM strategy generator
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T105, P2-T113, P2-T044, P2-T005, P0-T042, P6-T074, P2-T008, P2-T112]
requirements: [R2.45]
roadmap_todos: [T2.28]
modules: [M7, M0, M8, M21]
dashboards: [D03, D04]
tools: [cargo, docker, runsc]
mcp: []
env: []
services: [litellm]
branch: p2/P2-T116-sandbox-runner-and-generator
pr: ""
doc_sync: [docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T116 · Sandbox runner and LLM strategy generator

## Goal / expected outcome

`lab.generate_strategy` turns a natural-language description into a **Rust** strategy crate + manifest against our templates ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20); the Vibe-Trading research → strategy loop rebuilt in `mt-agents`), then compiles and tests it only inside the `sandbox` container (gVisor `runsc`, `--network none`, no secrets, read-only data mount, offline Rust toolchain with vendored crates): `cargo build`, its template tests, the never-build validator and the bias analysers, then a first backtest. It returns code + manifest + results for you to review before `strategy.create`.

## Context & references

- Roadmap: [R2.45](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.28 · verified by P2-T165 (escape test)
- [SPEC NN4](../../../SPEC.md#non-negotiable-requirements) · [03 M7](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [07 security notes](../../../docs/07-security-notes.md) (gVisor/`--network none`; never run cloned bot code outside the sandbox) · [01 §3.4 Vibe-Trading in-process exec risk](../../../docs/01-repo-vetting-report.md#34-hkudsvibe-trading--research-and-strategy-generation-layer) · [19 §3 Vibe-Trading (MIT, design rebuilt in Rust)](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime)
- Prerequisites (`depends_on`): `mt-agents` runtime and gateway client (P6-T074, built early under dependency gating); `sandbox` container + gVisor runtime + resource limits (P2-T044, T2.40); never-build validator (P2-T005, T2.20); Rust templates (P2-T008); bias analysers (P2-T112); LiteLLM gateway role keys (P0-T042).
- Budget: role `strategy-gen` default $0.50/day, over budget → local model fallback ([16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)).
- UI: [D03 'Describe it' tab](../../../docs/ui/dashboards/D03-strategies.md), [D04 generator panel](../../../docs/ui/dashboards/D04-research-lab.md)

## Requirements

- Generation: an `mt-agents` graph (`strategy_gen`) on gateway role `strategy-gen` (its own virtual key + daily budget, local fallback); prompt = your description + the `MtStrategy` trait API + template catalogue (Vibe-Trading prompt ideas adapted, NOTICE kept); output = a strategy crate (`src/lib.rs`, `Cargo.toml` with dependencies from the allow-list only) + `manifest.yaml`.
- Static gate before compiling: `syn`-based checks: `#![forbid(unsafe_code)]`, no `build.rs`, no proc-macro or `-sys` crates, dependency allow-list (`mt-engine` strategy API, `mt-core`, `mt-features`, approved vendored crates); no `std::process`, `std::net`, `std::env`, FFI, `include_bytes!`/`include_str!` outside the crate, file access outside `/tmp`; manifest schema + never-build validator (part A); max source size 200 KB.
- Sandbox run: `docker run --runtime=runsc --network none --read-only --cap-drop ALL --pids-limit 256 --memory 2g --cpus 2`, tmpfs `/tmp` (and `CARGO_TARGET_DIR` there), `cargo build --offline` against a vendored registry, no env secrets, data mounted read-only from a pre-built dataset snapshot; wall-clock cap 10 min (compile included).
- In the sandbox: compile, run the template tests, the never-build validator and the bias analysers (P2-T112), then a first backtest on the mounted snapshot; results returned as JSON over stdout only.
- Output to UI: code (read-only diff), manifest, sandbox log (incl. compiler output), analyser results, first backtest, leakage review (P2-T113); banner text 'Generated code ran in an isolated sandbox with no network or secrets.'
- Saving = `strategy.create` (C1) as `draft`; generated strategies are tagged `origin=generated` and count trials against their family. A strategy that failed to compile, its tests or the analysers can't be saved.

## ToDo

- [ ] Implement the `strategy_gen` graph in `crates/mt-agents/src/graphs/strategy_gen.rs` (prompting, response parsing, retries ≤ 2, compiler errors fed back once)
- [ ] Implement the `syn` static checker and dependency allow-list in `crates/mt-lab-core/src/sandbox/static_gate.rs`
- [ ] Implement `crates/mt-lab-core/src/sandbox/runner.rs` invoking the sandbox container with the flags above; output size cap 5 MB
- [ ] Sandbox image: pinned Rust toolchain + vendored crate registry (`cargo vendor`), refreshed only by a reviewed PR
- [ ] Dataset snapshot export for sandbox mounts (read-only Parquet subset)
- [ ] Wire `lab.generate_strategy` command and progress on `lab.job.{id}`
- [ ] Tests (recorded LLM responses) + docs

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core sandbox`, `cargo test -p mt-agents strategy_gen`, `cargo clippy`.
- Unit: the static checker rejects each forbidden construct (one fixture per item: `unsafe`, `build.rs`, `std::process`, `std::net`, `std::env`, FFI, disallowed crate, file write outside `/tmp`, oversize source).
- Integration: a benign recorded generation compiles in the sandbox, passes its template tests and the analysers, and returns a backtest JSON.
- Integration: generated code containing a sniping/copy-trading pattern is rejected by the never-build validator before compiling.
- Integration: generated code with a seeded look-ahead is rejected by the analysers and can't be saved.

### Scenarios
- Given generated code that opens a socket, then the static gate rejects it; if obfuscated, the sandbox network is absent and the run fails without egress.
- Given the gateway budget is exhausted, then generation falls back to `local-advisor` and says so.
- Given the sandbox times out at 10 min (compile included), then the job fails with the sandbox log and nothing is saved.

### Stress / failure injection
- Fork bomb / memory hog / compile-time blow-up (deep generic recursion) fixtures are contained by pids/memory/time limits and the workstation stays healthy (asserted in P2-T165).

## Acceptance criteria

- [ ] Generated code is compiled and executed only inside the `sandbox` container
- [ ] Static gate + never-build validator run before compiling; template tests + bias analysers before save
- [ ] User review required before save
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test`, `pit` check

## Exceptions & edge cases

- gVisor unavailable on the workstation: generator disabled with a clear error (never falls back to plain Docker or in-process).
- Generated manifest missing counterparty/kill criteria/benchmark: shown as validation errors; cannot save until filled.
- `mt-agents` runtime not yet built (P6-T074): the generator stays disabled with a clear message; template and code strategies are unaffected.

## Cardinal rules (do NOT)

- Do NOT compile or execute generated code in `backtest-worker`, `mt-api`, `mt-agents` or `engine`.
- Do NOT mount secrets, the Docker socket, the host cargo registry or writable volumes into the sandbox.
- Do NOT generate Python strategies: the generator emits Rust only (17 §H).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: generator flow (Rust output, `mt-agents` graph) and the static allow-list.
- `docs/07-security-notes.md`: exact sandbox flags and the offline Rust toolchain.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.28 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T116-sandbox-runner-and-generator`
- PR title: `P2-T116: Sandbox runner and LLM strategy generator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T116` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (sandbox/never-build/gateway deps, strategy-gen budget default)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (generator emits Rust strategy crates compiled and tested in the sandbox (offline toolchain, vendored crates, `syn` static gate, template tests + bias analysers before save); LLM loop is an `mt-agents` graph; depends_on + P6-T074, P2-T008, P2-T112, P2-T104 → P2-T105 (first backtest is a Rust truth run, the screener is Python research); tools [uv, docker, runsc] → [cargo, docker, runsc])
