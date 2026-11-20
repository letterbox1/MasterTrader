---
id: P2-T078
kind: task
title: "Verify setup odds: reproducible, leak-free, never changes M11"
phase: 2
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T077]
requirements: [R2.59]
roadmap_todos: [T2.73]
modules: [M7, M11]
dashboards: [D04, D05]
tools: [cargo, git]
mcp: []
env: []
services: [supabase-postgres]
branch: p2/P2-T078-verify-setup-odds
pr: ""
doc_sync: [docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T078 · Verify setup odds: reproducible, leak-free, never changes M11

## Goal / expected outcome

Evidence that setup odds are reproducible from their seed, never use data after `as_of`, appear on approval cards and never change what M11 allows.

## Context & references

- Roadmap: [R2.59 / T2.73](../../../docs/roadmap/phase-2-strategies-risk-lab.md#4-todo-sets)
- Builds on P2-T077
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Run the seeded reproducibility, leak and no-override tests from P2-T077 on recorded data for three instruments (crypto, FX, US equity).
- Attach outputs to the progress log.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P2-T078` checks them before start.

## ToDo

- [ ] Run reproducibility test on three instruments
- [ ] Run the post-`as_of` leak test
- [ ] Run the M11 no-override test
- [ ] Record results in the progress log

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core odds -- --include-ignored` (recorded-data cases), `cargo test -p mt-api odds`.
- Re-run with the same seed: byte-identical odds.
- Inject a future bar: the leak test fails the build.

### Scenarios
- Given an approval with odds attached, when you approve or reject, then the outcome and the odds are both recorded in the approval audit row.

### Stress / failure injection
- n/a: covered by P2-T077's concurrency test

## Acceptance criteria

- [ ] All three checks pass on three instruments
- [ ] Evidence linked in the progress log

## Exceptions & edge cases

- If recorded data for an instrument is missing, substitute another of the same asset class and note it.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt-api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).

## Doc sync on completion

- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.73

## Branch & PR

- Branch: `p2/P2-T078-verify-setup-odds`
- PR title: `P2-T078: Verify setup odds: reproducible, leak-free, never changes M11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T078` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line; services [postgres] → [supabase-postgres])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (odds engine is Rust (`mt-lab-core`); commands → `cargo test`; tools [uv, git] → [cargo, git])
