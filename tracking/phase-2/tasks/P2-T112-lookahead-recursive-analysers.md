---
id: P2-T112
kind: task
title: Clean-room Rust look-ahead, recursive and repainting bias analysers
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T105]
requirements: [R2.43]
roadmap_todos: [T2.27, T2.44]
modules: [M7]
dashboards: [D04]
tools: [cargo, uv]
mcp: []
env: []
services: []
branch: p2/P2-T112-lookahead-recursive-analysers
pr: ""
doc_sync: [docs/03-build-spec.md, docs/19-third-party-register.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T112 · Clean-room Rust look-ahead, recursive and repainting bias analysers

## Goal / expected outcome

Clean-room **Rust** look-ahead, recursive-formula and repainting analysers in `crates/mt-lab-core/src/bias/` (from freqtrade's published ideas only, **no GPL code**, [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20), [19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime)) that run on every validation and fail strategies whose signals change when future data is removed, whose indicators depend on start-up length, or whose closed-bar values repaint. They replace the vendored freqtrade copy planned under P2-B051; removing that copy is P2-T204.

## Context & references

- Roadmap: [R2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.44 (and T2.27 for the harness sections) · verified by P2-T160
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) supersedes the vendoring route of [17 §A P2-B051](../../../docs/17-decisions-register.md#a-s2-items-all-resolved): the analysers are rebuilt clean-room in Rust; [19 §4](../../../docs/19-third-party-register.md#4-copyleft-register--and-the-release-plan) (copyleft register: the vendored copy must be gone before any release)
- Clean-room rule: implement from the behaviour described in freqtrade's public docs and our own spec below; do not open, copy or translate freqtrade source files while writing this crate
- [D04 Bias checks tab](../../../docs/ui/dashboards/D04-research-lab.md) · [03 §8 item 3](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [03 M7](../../../docs/03-build-spec.md#m7-research-lab)
- Python research strategies (paper-only, `mt_research`) are analysed through the `mt-lab-core` binding (P2-T203) with the same code

## Requirements

- Look-ahead analyser: for K sampled signal timestamps, re-run the strategy on data truncated at each timestamp; any signal/indicator value differing from the full-data run = look-ahead; report the offending signal names, timestamps and indicator columns.
- Recursive analyser: compute indicators with start-up lengths {N, 2N, 4N} bars; relative deviation > 1e-6 on the evaluation window = recursive/start-up dependence; report columns.
- Repainting check: indicator values for closed bars must not change when later bars arrive (streaming vs batch comparison).
- Results: pass/fail per analyser with details, stored on the validation run; any fail blocks the 'bias checks' gate.
- Runtime: default K = 50 sample points; ≤ 15 min for a 1h-bar strategy over 2 years.

## ToDo

- [ ] Write a short clean-room spec (`crates/mt-lab-core/src/bias/SPEC.md`) from freqtrade's public documentation and this task, with the date and the sources read; no freqtrade source files consulted
- [ ] Implement `crates/mt-lab-core/src/bias/{lookahead,recursive,repaint}.rs` against the `MtStrategy` trait (templates and code strategies) and, through the binding, the Python research base
- [ ] Register them as validation sections; persist details for D04
- [ ] Fixture strategies (Rust, plus one Python research fixture per case): clean, look-ahead (reads the next bar's close), recursive (EMA without warm-up), repainting (uses the forming bar)
- [ ] `cargo deny` / licence-audit check (P0-T074) shows no GPL crate or file in `mt-lab-core`
- [ ] Tests + docs

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core bias`, `cargo clippy -p mt-lab-core`; Python research fixtures: `uv run pytest packages/mt_research -k bias` (through the binding).
- Unit: each fixture is classified correctly (clean passes all; each buggy one fails exactly its analyser). Every case from the earlier freqtrade-based plan is kept.
- Integration: analysers run on an EMA template via the truth runner and pass.

### Scenarios
- Given a strategy that peeks one bar ahead, when validated, then the look-ahead analyser fails and names the signal and timestamps.
- Given an indicator that needs 200 bars warm-up but gets 50, then the recursive analyser fails with the column name.
- Given the same fixtures run through the Python binding, then the classifications are identical to the Rust run.

### Stress / failure injection
- Strategy with 1m bars over 1 year: analyser sampling keeps runtime within the 15-min budget × 4 (documented) or the job times out cleanly.

## Acceptance criteria

- [ ] Four fixture strategies classified correctly (Rust and through the binding)
- [ ] Results visible per validation run
- [ ] No freqtrade or other GPL code in `mt-lab-core`; clean-room spec committed; licence audit clean
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test -p mt-lab-core`, `uv run pytest packages/mt_research -k bias`, `pit` check

## Exceptions & edge cases

- Stochastic strategies: seeds fixed for both runs; remaining nondeterminism reported as 'inconclusive', which counts as fail.
- Tick/L2 strategies: truncation done on event time; sampling on events, not bars.

## Cardinal rules (do NOT)

- Do NOT copy, translate or vendor freqtrade (GPL-3.0) code; ideas only, clean-room (17 §H, 19 §3).
- Do NOT add telemetry or referral IDs; pin images by digest.
- Do NOT read research/backtest data except through `pit(as_of)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: analysers are the clean-room Rust ones in `mt-lab-core`.
- `docs/19-third-party-register.md` §3: freqtrade row stays "ideas only"; the §4 vendored row is removed by P2-T204.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.44 when this and P2-T204 are done; T2.27 once every task mapped to it is done.

## Branch & PR

- Branch: `p2/P2-T112-lookahead-recursive-analysers`
- PR title: `P2-T112: Clean-room Rust look-ahead, recursive and repainting bias analysers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T112` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (freqtrade analysers vendored under third_party/ with GPL licence, isolated in mt_lab (17 §A P2-B051))
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (vendored freqtrade analysers replaced by clean-room Rust analysers in `mt-lab-core` (T2.44); all fixture cases kept, plus binding parity for Python research strategies; removal of any vendored copy split out to P2-T204; roadmap_todos [T2.27] → [T2.27, T2.44]; doc_sync third_party/LICENSES.md → docs/19; tools [uv] → [cargo, uv])
