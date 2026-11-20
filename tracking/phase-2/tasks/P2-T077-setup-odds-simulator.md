---
id: P2-T077
kind: task
title: "Setup-odds simulator ('time machine') in mt-lab-core and on approval cards"
phase: 2
type: BUILD
status: backlog
priority: medium
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P0-T027, P2-T038, P1-T009]
requirements: [R2.59]
roadmap_todos: [T2.43]
modules: [M7, M15]
dashboards: [D04, D05]
tools: [cargo, pnpm, git]
mcp: []
env: []
services: [supabase-postgres]
branch: p2/P2-T077-setup-odds-simulator
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/ui/dashboards/D05-execution.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T077 · Setup-odds simulator ("time machine") in mt-lab-core and on approval cards

## Goal / expected outcome

For a proposed entry (instrument, side, entry, stop, target, setup id), `mt_lab_core::odds` (Rust, `crates/mt-lab-core/src/odds/`, 18 §2.1) replays N continuations (default 10,000, configurable) bootstrapped from the instrument's own recent bars, plus every past occurrence of the same setup found point-in-time, and returns win rate, R-multiple distribution, MAE/MFE and time to target/stop. The odds appear in the lab (D04) and as an odds block on the ApprovalCard (web) and the Telegram approval card. Idea from day-trader-skill's "Time Machine" (MIT), rebuilt in Rust ([19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime)); any text copied keeps its MIT notice in `NOTICE`. Notebooks reach the same engine through the `mt-lab-core` binding (P2-T203).

## Context & references

- Roadmap: [R2.59 / T2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md#4-todo-sets)
- Approval cards: P2-T038 (ApprovalCard), P2-T039 (Telegram cards); lab worker P2-T101; `pit(as_of)` P0-T027
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Inputs only via `pit(as_of)`; the replay never sees a bar after `as_of`.
- Seeded and reproducible: same inputs + seed → same odds; seed and data range recorded with the result.
- Block bootstrap of intraday returns (session-aware; block length configurable) plus historical analogues (same setup id detected in past data); both reported separately and combined.
- Outputs: win rate, expected R, R quantiles (p5/p25/p50/p75/p95), MAE/MFE, median time to target/stop, sample size; a low-sample warning below a configurable minimum (default 30 analogues).
- Runs in-process in `mt-api` for the card path (the crate is linked, no job hop) and as a lab job for D04, with a time budget (default 2 s for the card path, configurable); if it can't finish in time the card shows "odds pending", never blocks approval.
- Informational only: never changes M11's verdict, sizing or limits.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P2-T077` checks them before start.

## ToDo

- [ ] Odds engine (bootstrap + analogue search) with seed handling in `crates/mt-lab-core/src/odds/` (seeded `rand_chacha` RNG so results are reproducible across platforms)
- [ ] Lab API endpoint + D04 view
- [ ] Odds block on ApprovalCard and Telegram card (with the low-sample warning)
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core odds`, `cargo test -p mt-api odds`, `pnpm test`.
- Unit: fixed seed → identical output; block bootstrap preserves session boundaries.
- Unit: analogue search with a synthetic series containing 40 planted setups finds all 40 and nothing after `as_of`.
- Integration: approval card renders odds within the time budget, or "odds pending".

### Scenarios
- Given a setup with fewer than 30 analogues, then the card shows the low-sample warning.
- Given the lab job times out, then approval proceeds normally and the odds attach later.

### Stress / failure injection
- 1,000 concurrent card requests: time budget honoured, no impact on the order path latency.

## Acceptance criteria

- [ ] Odds reproducible from the recorded seed
- [ ] Leak test proves no post-`as_of` data is used
- [ ] Odds never alter M11 decisions (test)
- [ ] CI green (`cargo clippy -- -D warnings`, `cargo test -p mt-lab-core -p mt-api`, `pnpm test`, `pit` bypass check)

## Exceptions & edge cases

- Instruments with too little history: show "not enough history" instead of odds.
- Closed sessions/holidays: bootstrap skips non-trading periods.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt-api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).
- Do NOT present odds as a promise or let them auto-approve anything; approval stays with you or the bot's mode rules.

## Doc sync on completion

- `docs/03-build-spec.md`: M7 lab gains the setup-odds function
- `docs/14-strategy-evidence-and-validation.md`: odds as a pre-trade context check (not a gate)
- `docs/ui/dashboards/D05-execution.md`: ApprovalCard odds block
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.43

## Branch & PR

- Branch: `p2/P2-T077-setup-odds-simulator`
- PR title: `P2-T077: Setup-odds simulator ("time machine") in mt-lab-core and on approval cards`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T077` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust/Python split per 18 §2; `cargo` + `uv run pytest` commands; tools [uv, pnpm, git] → [uv, cargo, pnpm, git]; services [postgres] → [supabase-postgres])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (`mt_lab.odds` (Python) → `mt_lab_core::odds` (Rust) per 18 §2.1/R2.59, linked into `mt-api` for the card path; same tests under `cargo test`; title updated; tools [uv, cargo, pnpm, git] → [cargo, pnpm, git])
