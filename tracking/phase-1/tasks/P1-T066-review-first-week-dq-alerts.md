---
id: P1-T066
kind: task
title: Tune noisy DQ thresholds from the soak week's alert stats (tightening only)
phase: 1
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T065]
requirements: [R1.10]
roadmap_todos: [T1.04]
modules: [M16]
dashboards: [D07]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api, nats]
branch: p1/P1-T066-review-first-week-dq-alerts
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T066 · Tune noisy DQ thresholds from the soak week's alert stats (tightening only)

## Goal / expected outcome

The agent classifies every DQ alert kind from the 7-day soak (P1-T065) as useful, noisy or missing from the recorded stats, and tunes the thresholds before P2 relies on DQ to pause strategies: **tightening only**, inside the defaults of [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means), applied as C1 setting versions with source `agent_tuning`. Anything that would need loosening is not applied; it goes into the go-live pack (P7-T070) as a proposal with its evidence, for you to approve (C3) or reject. You can also change any threshold yourself at any time in D07/settings.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Defaults: [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) (stale 2 s / 60 s, wide spread 3×, divergence 25 bps crypto / 5 bps FX, bad tick z ≥ 8) · [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab · loosening is C3 ([02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)); in P1 via the break-glass CLI ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B002/P1-B009)
- Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (configurable values are agent-drafted and approved once in the go-live pack) · re-platform brief §2 (P1-T066 converted: tightening only)
- Inputs: the soak report and `audit.dq_event` / alert delivery rows from P1-T065
- Depends on (this phase): P1-T065. Review of any loosening proposal: P7-T070

## Requirements

- Read the soak week's incidents (`audit.dq_event`), alert deliveries (`ops.notification`) and the recorded data from the Parquet catalog; compute per alert kind and instrument: count, duration, time-of-day/session clustering, and whether a real fault (gap, resync, venue status, skew) explains it
- Classify each kind: **useful** (explained by a real fault), **noisy** (no fault found, e.g. bad-tick flags at every US open), **missing** (a real fault with no alert)
- For missing alerts: tighten the threshold (C1, `system.settings.update`, source `agent_tuning`), never beyond what the replay shows is needed
- For noisy alerts: first fix the cause where it's ours (session calendar, spread band, venue maintenance windows, hysteresis on recovery only); only if a threshold change is still needed and it would loosen, record it as a **proposal** in the go-live pack (P7-T070) with the replay evidence; do not apply it
- Never loosen a freshness threshold or the ≤ 250 ms reaction SLO; a bot that tolerates older data uses the slow profile (60 s default)
- Every applied change is a versioned WORM setting row; the progress log lists each change and each proposal

## ToDo

- [ ] Export the soak week's incidents and alert counts per kind/instrument/session from `audit.dq_event` and `ops.notification`
- [ ] Classify each alert kind (useful/noisy/missing) with its evidence
- [ ] Replay the soak week through `mt-monitor` with candidate thresholds (`cargo run -p mt-monitor -- replay --from … --to …`) and record before/after counts
- [ ] Apply tightening changes via `system.settings.update` (C1, source `agent_tuning`); fix ours-to-fix causes as follow-up bugs (`./kanban new --kind bug`)
- [ ] Write loosening proposals into the go-live pack input for P7-T070 (not applied)
- [ ] Confirm the following 48 h are quieter (or explain why not) in the progress log
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-monitor replay`: replaying the soak week with the tuned thresholds gives the alert counts recorded in the report (deterministic)
- `cargo test -p mt-api settings`: a tuning change with source `agent_tuning` that loosens a value is rejected (only C1 tightening is allowed from this path)

### Scenarios

- Given bad-tick alerts fire at every US open and the replay shows a spread-band cause, when tuned, then the session-open spread band is fixed (ours) and no threshold is loosened; if a loosening is still needed it appears as a proposal in the go-live pack
- Given a real 3 s gap on a fast feed produced no alert, when tuned, then the gap threshold is tightened (C1) and the replay now alerts

### Stress / failure injection

- n/a: offline analysis and setting changes; the replay is deterministic

## Acceptance criteria

- [ ] Every alert kind from the soak week classified with evidence; tightening changes applied (C1) as WORM setting versions; loosening proposals recorded for P7-T070, none applied
- [ ] Alert counts before/after recorded from the replay

## Exceptions & edge cases

- Never loosen a freshness threshold or the ≤ 250 ms reaction SLO to reduce noise; fix the cause of noisy alerts
- If the soak week had no alerts of a kind, keep the 16 §2.2 default and note "no data"

## Cardinal rules (do NOT)

- Do NOT loosen any threshold from this task; loosening is C3 and needs your approval (go-live pack or `mtctl approve` + TOTP)
- Do NOT hide genuine stale/bad data from the risk manager
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); setting changes are new versions ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.04 once every task traced to it in PHASE.md is done; note P1-T066 next to it (T1.04 is now an agent tuning task, tightening only).
- `docs/03-build-spec.md` §M16: record the tuned default thresholds

## Branch & PR

- Branch: `p1/P1-T066-review-first-week-dq-alerts`
- PR title: `P1-T066: Tune noisy DQ thresholds from the soak week's alert stats (tightening only)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T066` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C3 via break-glass CLI (P1-B009); thresholds as settings with 16 §2.2 defaults)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from USER to an agent OPS task per 17 §G and the re-platform brief §2: the agent tunes from the soak week's alert stats, tightening only within the 16 §2.2 defaults; loosening becomes a proposal in the go-live pack P7-T070; tools cargo/supabase, services supabase-postgres, mt-api, nats)
