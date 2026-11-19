---
id: P2-T048
kind: task
title: Seed the initial risk policy (L1–L3) and L0 ceilings from the 16 §2 defaults
phase: 2
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T011, P2-T012, P2-T043]
requirements: [R2.14, R2.19, R2.55]
roadmap_todos: [T2.01]
modules: [M11]
dashboards: [D03, D06]
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p2/P2-T048-seed-risk-policy-ceilings
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T048 · Seed the initial risk policy (L1–L3) and L0 ceilings from the 16 §2 defaults

## Goal / expected outcome

The risk policy starts populated: policy versions for L1 Global, L2 Venues and L3 Sleeves and the L0 hard ceilings exist, each value equal to its default in [16 §2](../../../docs/16-configuration-and-safety-model.md#2-default-values-all-configurable), recorded as WORM policy rows with source `seed`. Paper trading can start without asking you anything. You review and approve the effective values once, in the go-live pack (P7-T070), and can change any of them in D03/D06 at any time (tightening immediate, loosening C3).

## Context & references

- Roadmap: [R2.14, R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.01
- Defaults: [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) · [§2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) · [§2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [§2.8](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts) · [§3.1 dead-man](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)
- Decisions: [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (configurable values are settings, not questions) · [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (agents draft, you approve once at go-live)
- Built on: P2-T011/T012 (policy model, layered merge), P2-T043 (D03 strategy settings, D06 Policy).
- Unblocks: paper trading (P2-T067). Approval: P7-T070.

## Requirements

- A **policy seed** generated from one machine-readable defaults file (`config/defaults/risk.yaml`) whose values match 16 §2 exactly; the doc and the file are checked against each other in a test, so they can't drift.
- Seeded fields: risk per trade 1% of sleeve; max position 10% (memecoin 2%); daily loss 3% of sleeve (Sydney day); sleeve drawdown 10% halve / 15% halt; system drawdown 10% no new entries / 25% flatten + 30-day lock; open positions 10 per sleeve; leverage 1× (crypto derivatives ≤ 2×); venue concentration ≤ 25%; price collars 2% / 0.5% / 1%; API-error pause 5 in 60 s → 10 min; cost blow-out 1.5× over 20 fills; stale thresholds 2 s / 60 s; decision deadlines 1 s / 10 s / 5 min / 1 h; HITL TTLs 60 s / 15 min / 4 h; large-order threshold > 2% of sleeve or > A$5,000; dead-man 5 s / 10 s; `on_system_failure: flatten`; blackouts 15 min either side for `event_sensitive` bots.
- **L0 ceilings** seeded at the top of each field's accepted range in 16 §2 (e.g. risk per trade ≤ 2%, crypto-derivatives leverage ≤ 2×), so no default sits above its ceiling.
- Seeding is idempotent: re-running doesn't add versions when nothing changed; it never overwrites a value you've set (your rows win; the seed only fills fields with no value).
- Rows go through `mt-api` commands with source `seed` and are WORM (`risk.change`); no direct SQL writes.

## ToDo

- [ ] Write `config/defaults/risk.yaml` from 16 §2 and a test that parses 16 §2 tables and compares
- [ ] `mt policy seed` (CLI over `mt-api`) creating L0–L3 versions with source `seed`
- [ ] Run it in the workstation stack; screenshot D03 Ceilings and D06 Policy showing the seeded values
- [ ] Add the effective values to the go-live pack generator (P7-T070 reads it)
- [ ] Tests; progress log; `./kanban done P2-T048`

## Verification

### Tests
- `cargo test -p mt-risk policy_seed`: every seeded value equals the defaults file; defaults file equals 16 §2 (doc-parse test).
- Re-run the seed: no new versions. Set one value by hand, re-run: your value stays.
- A value above an L0 ceiling is rejected at save.

### Scenarios
- Given a fresh workstation stack, when `mt policy seed` runs, then `/risk/changes` lists the L0–L3 rows with source `seed` and D06 shows each value with its 16 link.
- Given the seed ran, when you tighten daily loss to 2% in D06, then it applies at once and a later seed run leaves it at 2%.

### Stress / failure injection
- Seed while Postgres is restarting: the command fails cleanly with no partial version (one transaction per layer).

## Acceptance criteria

- [ ] L0–L3 policy versions exist with source `seed`, matching 16 §2
- [ ] Doc ↔ defaults-file test passes
- [ ] Idempotent and never overwrites user values

## Exceptions & edge cases

- A default marked (U) in 16 is seeded as written and flagged `unverified` in D06 until its RESEARCH task confirms it.

## Cardinal rules (do NOT)

- Every value comes from the defaults file; nothing hard-coded in code.
- Policy rows are WORM; corrections are new versions.
- Never loosen a value on a re-seed.

## Doc sync on completion

- docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md: update to match what was built.

## Branch & PR

- Branch: `p2/P2-T048-seed-risk-policy-ceilings`
- PR title: `P2-T048: Seed the initial risk policy (L1–L3) and L0 ceilings from the 16 §2 defaults`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reworked: review prefilled 16 §2 defaults and set values and L0 ceilings in the settings (no host file, 17 §E); loosening C3)

- 2026-11-19: Converted from a USER task to an agent task (17 §G): configurable values are seeded from the 16/14 defaults and approved once in the go-live pack (P7-T070), never asked during the build.
