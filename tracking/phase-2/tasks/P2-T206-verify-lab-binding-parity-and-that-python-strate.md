---
id: P2-T206
kind: task
title: Verify lab binding parity and that Python strategies stay on paper
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T203, P2-T205, P2-T105, P2-T114, P2-T007]
requirements: [R2.60]
roadmap_todos: [T2.74]
modules: [M7, M0]
dashboards: [D04]
tools: [git, cargo, uv]
mcp: []
env: []
services: [supabase-postgres, mlflow]
branch: p2/P2-T206-verify-lab-binding-parity-and-that-python-strate
pr: ""
doc_sync: [docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T206 · Verify lab binding parity and that Python strategies stay on paper

## Goal / expected outcome

Evidence that the lab split is safe: the same backtest and validation run from Rust and from a notebook through the binding give identical results, and a Python strategy can't be switched out of paper ([R2.60](../../../docs/roadmap/phase-2-strategies-risk-lab.md), T2.74).

## Context & references

- Roadmap: [R2.60 / T2.74](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · decision [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)
- Builds on P2-T203 (binding), P2-T205 (port path), P2-T105 (truth runner), P2-T114 (validation suite), P2-T007 (mode ceiling)

## Requirements

- Parity matrix on recorded fixtures (crypto, FX, US equity): dataset hash, cost totals, truth trade list, metrics, every validation section and gate verdict, setup odds (same seed): Rust run vs notebook-through-binding run must be byte-identical (floats compared bitwise; any tolerance is a failure).
- Paper-only rule: a `lang=python` strategy can't get a bot mode above `paper` via web, Telegram, `mt-api` or MCP paths; the attempt is refused and audited.
- Results attached to the progress log.

## ToDo

- [ ] Build the parity matrix runner (`cargo test -p mt-lab-core binding_parity -- --ignored` drives both sides)
- [ ] Run it on the three fixtures; attach the report
- [ ] Run the paper-only refusal checks on every command path
- [ ] Record results in the progress log

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core binding_parity -- --ignored`, `uv run pytest packages/mt_research -k parity`, `cargo test -p mt-api python_strategy_mode`.
- Every comparison bitwise-equal; every non-paper mode request for a Python strategy refused.

### Scenarios
- Given the same backtest started from D04 and from a notebook, then both result rows carry the same trade-list hash and gate verdicts.
- Given a Python research strategy, when `bot.set_mode hitl` is sent from Telegram, then it is refused with "port to Rust first" and `audit.command` has the row.

### Stress / failure injection
- Run the parity matrix with 4 parallel workers: results still identical (no shared mutable state across the boundary).

## Acceptance criteria

- [ ] Parity report attached: identical on all three fixtures
- [ ] Python strategies refused above `paper` on every path

## Exceptions & edge cases

- A harness section not yet exposed by the binding is listed as "not exposed", which fails this check until P2-T203 covers it.

## Cardinal rules (do NOT)

- Do NOT loosen the comparison to a tolerance to get green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.74.

## Branch & PR

- Branch: `p2/P2-T206-verify-lab-binding-parity-and-that-python-strate`
- PR title: `P2-T206: Verify lab binding parity and that Python strategies stay on paper`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T206` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (T2.74: lab binding parity and the paper-only rule for Python strategies need their own check)
