---
id: P2-T204
kind: task
title: Remove the vendored freqtrade analysers and their copyleft-register row
phase: 2
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T112, P2-T160, P0-T074]
requirements: [R2.43]
roadmap_todos: [T2.44]
modules: [M7, third_party]
dashboards: []
tools: [git, cargo]
mcp: []
env: []
services: []
branch: p2/P2-T204-remove-the-vendored-freqtrade-analysers-and-thei
pr: ""
doc_sync: [docs/19-third-party-register.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T204 · Remove the vendored freqtrade analysers and their copyleft-register row

## Goal / expected outcome

No GPL code remains in the repository: once the clean-room Rust analysers (P2-T112) catch the seeded bugs (P2-T160), any vendored freqtrade analyser copy under `third_party/` (the P2-B051 route) is deleted, its row leaves the copyleft register ([19 §4](../../../docs/19-third-party-register.md#4-copyleft-register--and-the-release-plan)) and `just licence-audit` (P0-T074) passes with no GPL item in `third_party/` ([17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)).

## Context & references

- Roadmap: [R2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.44
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (clean-room Rust analysers replace the vendored copy) · [19 §3–§4](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime) · superseded route: P2-B051 / [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Built on: P2-T112 (clean-room analysers), P2-T160 (seeded look-ahead bug caught), P0-T074 (licence audit)

## Requirements

- Precondition: P2-T112's four fixture cases and P2-T160's seeded bug pass with the Rust analysers alone (same cases the vendored analysers were meant to pass).
- Delete `third_party/freqtrade_analysers/` (if it was ever added) and any adapter or import-linter contract that referenced it; if it never existed, record that fact with the audit output.
- Remove the freqtrade line from `third_party/LICENSES.md` and the "Vendored freqtrade analysers" row from the 19 §4 table (doc sync).
- `just licence-audit` reports no GPL item in `third_party/` and no freqtrade file anywhere (filename and content-hash scan).

## ToDo

- [ ] Re-run `cargo test -p mt-lab-core bias` and the P2-T160 scenario; attach results
- [ ] Delete the vendored copy and its references (or confirm none exist)
- [ ] Update `third_party/LICENSES.md`
- [ ] Run `just licence-audit` and attach the output
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core bias`, `just licence-audit`, `git grep -i freqtrade -- third_party/ crates/ packages/` (only docs/NOTICE mentions allowed).
- The P2-T160 seeded-bug test still passes after deletion.

### Scenarios
- Given the deletion, when the validation suite runs on the four fixture strategies, then each is classified exactly as before.
- Given someone re-adds GPL code under `third_party/` outside `third_party/copyleft/`, then the licence audit fails CI.

### Stress / failure injection
- n/a: a deletion and an audit; no runtime path.

## Acceptance criteria

- [ ] No freqtrade/GPL code in the repository; licence audit clean
- [ ] Analyser and seeded-bug tests green after removal
- [ ] Register row removed (doc sync queued)

## Exceptions & edge cases

- If the audit finds other GPL code, file a bug (pm-triage) instead of deleting it here.

## Cardinal rules (do NOT)

- Do NOT delete the vendored copy before the Rust analysers pass the same tests.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT commit secrets or paste them into chats/issues/logs (07 §2).

## Doc sync on completion

- `docs/19-third-party-register.md` §4: remove the vendored-analysers row.
- `docs/03-build-spec.md` M7: drop the "removed when they land" note.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.44.

## Branch & PR

- Branch: `p2/P2-T204-remove-the-vendored-freqtrade-analysers-and-thei`
- PR title: `P2-T204: Remove the vendored freqtrade analysers and their copyleft-register row`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T204` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (T2.44: the vendored freqtrade copy (P2-B051 route) must go once the clean-room analysers pass the same tests)
