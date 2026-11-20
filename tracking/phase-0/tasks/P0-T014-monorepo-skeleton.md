---
id: P0-T014
kind: task
title: Create the Cargo + uv workspace monorepo skeleton with quality tooling and a just entry point
phase: 0
type: BUILD
status: ready
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.01, R0.N5]
roadmap_todos: [T0.20]
modules: [mt-core, mt-store, mt-api, mt-obs]
dashboards: []
tools: [git, cargo, uv, python>=3.12, just, pre-commit, gitleaks]
mcp: []
env: []
services: []
branch: p0/P0-T014-monorepo-skeleton
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T014 · Create the Cargo + uv workspace monorepo skeleton with quality tooling and a just entry point

## Goal / expected outcome

The canonical layout of [18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout) / [03 §3](../../../docs/03-build-spec.md#3-repository-layout) exists: a **Cargo workspace** (`crates/`) with every crate of 18 §2.1 as a compiling stub, a **uv workspace** (`packages/`) with only the Python packages of 18 §2.2, `apps/web/` (placeholder; scaffolded in P0-T047), `supabase/` (placeholder; filled in P0-T070/P0-T024), `infra/`, `third_party/LICENSES.md`, and one **`just`** entry point. `just check` (clippy, cargo test, ruff, mypy, pytest) passes on a clean clone; pre-commit with gitleaks is on.

## Context & references

- [Roadmap P0 R0.01, R0.N5](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.20](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2 language split](../../../docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary) · [18 §3 layout](../../../docs/18-platform-and-deployment.md#3-repository-layout)
- [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout) (canonical tree; [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19))
- [03 §9 hygiene](../../../docs/03-build-spec.md#9-future-proof-hygiene) · [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain)
- Unblocks: P0-T015 CI, P0-T016/P0-T017 `mt-core`, P0-T020 Compose, P0-T047 web, P0-T070 Supabase stack

## Requirements

- **Rust:** root `Cargo.toml` with `[workspace] members = ["crates/*"]`, `resolver = "2"`, shared `[workspace.package]` (edition 2021, MSRV pinned in `rust-toolchain.toml`) and `[workspace.dependencies]` (tokio, serde, thiserror, tracing, sqlx, pyo3, axum pinned); `Cargo.lock` committed.
- Crate stubs (one `lib.rs`/`main.rs` + one test each), exactly the 33 crates of the 18 §2.1 list: `mt-core, mt-api, mt-risk, mt-deadman, mt-engine, mt-recorder, mt-connectors, mt-scheduler, mt-features, mt-nlp, mt-agents, mt-memory, mt-models, mt-anomaly, mt-lab-core, mt-crowdsim, mt-airdrop, mt-airdrop-exec, mt-curation, mt-social, mt-onchain, mt-treasury, mt-signer, mt-journal, mt-feeds, mt-events, mt-intel-writer, mt-monitor, mt-store, mt-obs, mt-telegram-bot, mt-mcp, mt-mm-adapter`. Strategies are not a stub crate: built-in templates live in `crates/mt-engine/src/strategy/`, and each `strategies/<name>/` crate joins the workspace (`members` also globs `strategies/*`) when it is created (18 §2.1).
- **Python 3.12, uv:** root `pyproject.toml` with `[tool.uv.workspace] members = ["packages/*"]`; `uv.lock` committed **with hashes**. Package stubs (`__init__.py`, `py.typed`, one smoke test) for the five packages of the 18 §2.2 list only: `mt_research` (training, exploration, offline batch reports), `mt_extract` (trafilatura), `mt_telegram_reader` (Telethon), `mt_ledger_import` (ccxt ledger import), `mt_mt5_bridge` (optional; the Windows-only `MetaTrader5` dependency sits behind an optional extra so the stub imports on Linux/macOS). No Python package duplicates a Rust crate (agents, memory, features, anomaly, models runtime, NLP, airdrop, curation, social, connectors, scheduling and the lab harness are Rust, 17 §H); the `mt_store` Python module is built from `crates/mt-store` by maturin (P0-T071), not a separate package.
- Top level per 03 §3: `apps/web/`, `supabase/`, `infra/`, `services/`, `strategies/`, `third_party/` (+ `LICENSES.md`: name, upstream URL, pinned commit, licence, telemetry check date), `tests/`, `notebooks/`, `docs/runbooks/`.
- Lints: `cargo clippy --workspace --all-targets -- -D warnings`, `cargo fmt --check`, `cargo deny` (licences, advisories); ruff (lint + format, line length 110, rules E,F,I,B,UP,S,ASYNC), mypy `--strict` on Python packages touched in P0, pytest; coverage ≥ 80 % on P0 crates (`cargo llvm-cov`) and packages.
- `justfile` with `fmt`, `lint`, `type`, `test`, `check` (all of them), `db-reset`, `db-test` (wired in P0-T070) recipes; CI calls `just check`.
- pre-commit: cargo fmt, clippy (changed crates), ruff, ruff-format, mypy, **gitleaks** (pinned rev), check-yaml, end-of-file, `no-commit-to-branch main`.
- `.gitignore` covers `target/`, `.env*`, `*.sops.dec*`, `secrets*.yaml` except `*.example.yaml`, `/data`, `node_modules`, `supabase/.temp`.

## ToDo

- [ ] Create root `Cargo.toml`, `rust-toolchain.toml` and the 33 crate stubs; `cargo build --workspace`.
- [ ] Create root `pyproject.toml`, the uv workspace and the 5 package stubs; run `uv lock`.
- [ ] Create top-level folders with one-line READMEs; add `third_party/LICENSES.md` with the table header and vendoring rules (07 §7).
- [ ] Configure clippy, rustfmt, `deny.toml`, ruff, mypy, pytest and coverage.
- [ ] Add `.pre-commit-config.yaml` with pinned revs incl. gitleaks; `.gitleaks.toml` allow-lists only `tests/fixtures/fake_secrets/`.
- [ ] Add the `justfile` (`lint`, `type`, `test`, `check`, placeholders for `db-reset`/`db-test`).
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- Rust: `cargo test --workspace` (one test per crate stub); `cargo clippy --workspace --all-targets -- -D warnings`.
- Python: `uv run pytest` (each package's `test_import.py`).
- Tooling: `pre-commit run --all-files` clean; `cargo build --locked` and `uv sync --locked` succeed on a fresh clone (CI job); `just check` runs every step.

### Scenarios
- Given a developer adds `AWS_SECRET_ACCESS_KEY=...` to a file, when committing, then gitleaks blocks the commit.
- Given `uv.lock` or `Cargo.lock` is out of date, when CI runs `uv sync --locked` / `cargo build --locked`, then it fails.

### Stress / failure injection
- n/a: scaffolding.

## Acceptance criteria

- [ ] `just check` passes on a clean clone (`cargo build --locked`, `uv sync --locked`)
- [ ] All 33 crates compile and all 5 Python packages import; clippy `-D warnings` and mypy strict clean
- [ ] `pre-commit run --all-files` clean; gitleaks blocks a planted secret
- [ ] `third_party/LICENSES.md` exists with the table and rules
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Crate or package list changes later (e.g. a new Rust crate in P5): add then; stubs here are placeholders, not designs.
- A Python package found to need nothing Python-only moves to a Rust crate (18 §2 rule); record it in 18.

## Cardinal rules (do NOT)

- Do NOT install anything with `curl | sh`; use pinned toolchains and packages only (07 §7).
- Do NOT add runtime dependencies to stubs beyond what P0 needs.
- Do NOT create a Python package for something 18 §2.1 puts in Rust (no `mt_agents`, `mt_memory`, `mt_features`, `mt_models`, `mt_anomaly`, `mt_lab`, `mt_airdrop`, `mt_curation`, `mt_social`, no LangGraph, Prefect or OpenBB dependency; 17 §H).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` §3 (canonical tree) and `docs/18-platform-and-deployment.md` §3: align with what was built.
- `README.md`: add 'Getting started' (`just`, `cargo`, `uv sync`, `pre-commit install`).
- `docs/roadmap/phase-0-foundations.md`: tick T0.20 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T014-monorepo-skeleton`
- PR title: `P0-T014: Create the Cargo + uv workspace monorepo skeleton with quality tooling`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (03 §3 is the canonical layout (17 §B P0-B006), adds mt_onchain (23 packages); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Cargo workspace with the 18 crates of 18 §2.1 + uv workspace with only the 12 Python packages of 18 §2.2; `supabase/` replaces `migrations/`; `just` entry point; clippy/cargo deny added)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (workspace now lists the 33 crates of 18 §2.1 (adds mt-connectors, mt-scheduler, mt-features, mt-nlp, mt-agents, mt-memory, mt-models, mt-anomaly, mt-lab-core, mt-crowdsim, mt-airdrop, mt-curation, mt-social, mt-feeds, mt-mm-adapter) and only the 5 Python packages of 18 §2.2 (mt_research, mt_extract, mt_telegram_reader, mt_ledger_import, mt_mt5_bridge); strategies/* joins the workspace)
