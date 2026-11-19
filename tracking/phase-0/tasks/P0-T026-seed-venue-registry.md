---
id: P0-T026
kind: task
title: Seed ops.venue_registry from the 12 §2 starting classifications (your checks refine it)
phase: 0
type: OPS
status: backlog
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T025]
requirements: [R0.06]
roadmap_todos: [T0.11, T0.22]
modules: [ops, M11, mt-store]
dashboards: []
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T026-seed-venue-registry
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T026 · Seed ops.venue_registry from the 12 §2 starting classifications (your checks refine it)

## Goal / expected outcome

The agent drafts `infra/seed/venue_registry.yaml` from the [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) starting list and classifications, marks every unverified fact `(U)`, and loads it with source `seed`, so `ops.venue_registry_current` lists every venue with a safe status for paper work. When your AUSTRAC/retail checks (P0-T011) arrive, they are loaded on top as source `user` (new version rows); the seed never overwrites them. Nothing in the build waits on your checks; live use of any venue is gated later (P7 go-live pack, P7-T070).

## Context & references

- [Roadmap P0 R0.06](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.11, T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [12 §1 AU boundary](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption)
- [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (USER-blocker rule: the agent seeds defaults, the human reviews)
- Related: P0-T011 (your checks, optional refinement before live), P0-T025 (table + loader), P1-T069 (quarterly re-check)
- Depends on: P0-T025

## Requirements

- Seed is idempotent: re-running with the same file creates no new versions; a changed row creates one new version; a row whose current version has source `user` is never replaced by a `seed` row.
- Starting statuses follow 12 §2 and are **never more permissive than it**: OKX AU derivatives `blocked` (paper only); Bybit/Bitget/MEXC/Gate/KuCoin `read_only`; Hyperliquid `read_only` pending advice; Polymarket `blocked`; netting brokers `stp: n/a (netting)` ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P2-B006).
- A venue may be `allowed` only with an AUSTRAC/licence check date. Seeded venues without your check date get `read_only` with `paper_ok: true` on their products (paper and testnet work; live doesn't), and `reason` says "seed: awaiting your check (P0-T011)".
- Leverage values respect the L0 ceiling from settings (P0-T025 validation).
- No secrets in the YAML (venue names, ABNs and public facts only).

## ToDo

- [ ] Draft `infra/seed/venue_registry.yaml` from 12 §2 (every unverified field `(U)`), validated against the loader schema.
- [ ] Run `cargo run -p mt-store -- seed venues infra/seed/venue_registry.yaml --source seed`.
- [ ] Add a CI check that the YAML validates.
- [ ] Add the `--source user` path for P0-T011's results and a test that `seed` never overwrites `user`.
- [ ] Paste `SELECT venue, status, source, austrac_checked_at FROM ops.venue_registry_current` output into the PR.

## Verification

### Tests
- CI: YAML validates against the loader schema.
- `cargo test -p mt-store seed`: seed twice → version count unchanged; a `user` version followed by a `seed` run stays current.
- pgTAP: no current row is `allowed` without `austrac_checked_at`.

### Scenarios
- Given your checks (P0-T011) arrive and are loaded with `--source user`, then exactly one new version per changed venue is created and the seed no longer touches those rows.
- Given you re-check a venue next quarter and edit the YAML, when the loader runs, then exactly one new version row is created.

### Stress / failure injection
- n/a: one-off data load.

## Acceptance criteria

- [ ] Every 12 §2 venue present in the current view with source and status
- [ ] No venue `allowed` without a check date; paper works for seeded venues
- [ ] Idempotent re-run and `user`-wins rule proven
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- A venue missing from 12 §2 stays absent (absent = blocked by M11 default-deny in P2).
- P0-T011 never arrives before go-live: the venues stay `read_only` for live; the P7 go-live pack (P7-T070) lists them for your review.

## Cardinal rules (do NOT)

- Do NOT mark a venue `allowed` without an AUSTRAC/licence check date.
- Do NOT seed a status more permissive than 12 §2, and do NOT overwrite a `user` version.
- Do NOT do the human's venue checks for them or present seeded facts as verified.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: note the seed/user sources; replace starting classifications only with verified ones.
- `docs/roadmap/phase-0-foundations.md`: tick T0.11, T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T026-seed-venue-registry`
- PR title: `P0-T026: Seed ops.venue_registry from the 12 §2 starting classifications`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (netting STP per 17 §D; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (USER dependency P0-T011 removed per 17 §G: the agent seeds from 12 §2 (source `seed`, nothing `allowed` without a check date) and your checks load on top as source `user`; loader is the `mt-store` Rust CLI)
