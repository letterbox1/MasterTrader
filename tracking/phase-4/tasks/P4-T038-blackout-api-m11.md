---
id: P4-T038
kind: task
title: Blackout query API ("event within N minutes") wired into M11
phase: 4
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T037]
requirements: [R4.10]
roadmap_todos: [T4.26]
modules: [M5, M11]
dashboards: [D06, D08, D02]
branch: p4/P4-T038-blackout-api-m11
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T038 · Blackout query API ("event within N minutes") wired into M11

## Goal / expected outcome

`mt_data.calendar.blackouts.active(instrument, at)` and `upcoming(instrument, within_min)` answer "is there an event within N minutes affecting this instrument?" from one source of truth; the P2 M11 event-blackout hook calls it (in-process cache refreshed by `cal.*`), so new entries are blocked inside blackout windows defined by D06 policy rules, while protective exits are never blocked.

## Context & references

- Roadmap: [R4.10](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.26](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 2
- Spec: [03 M5](../../../docs/03-build-spec.md#m5-calendars--mt_datacalendar) · [03 M11 pre-trade checks](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · UI [D06 Blackouts](../../../docs/ui/dashboards/D06-risk.md) · [D08 Calendar](../../../docs/ui/dashboards/D08-intel.md) (blackout windows match the risk manager's)
- Cross-phase: P2 R2.16 (event blackout hook), R2.11 policy model, D06 policy tree.
- Gap: P4-B004 (blackout defaults unspecified).

## Requirements

- Policy rules (from `risk.policy` blackout node): match by importance/kind/country/instrument tags/strategy tags; window `pre_min`/`post_min`; action `block_new_entries` (default) or `pause_strategy`.
- Seed default (tightening only, editable in D06): high-importance macro releases and CB decisions → 15 min before to 15 min after, `block_new_entries` for strategies tagged `scalper`/`intraday` (proposed; confirm via P4-B004).
- In-process index (interval tree per instrument) rebuilt on `cal.*` and policy change; lookup p99 < 20 µs so the pre-trade p99 < 1 ms budget holds.
- Calendar feed stale (> 24 h without refresh) → treat as **unknown**: M11 applies the configured fail-safe (default block new entries for scalpers in the hour around typical release times) and raises DQ.
- Rejections carry reason `blackout:{event_id}`; D06 'active blackouts' and D08 calendar markers read the same API.
- Endpoints: `/intel/calendar?with_blackouts=1`; risk state includes active blackouts (WS `cal`, `risk.state`).

## ToDo

- [ ] Blackout rule evaluator + interval index.
- [ ] M11 hook adapter (calls into `mt_risk` P2 interface).
- [ ] Stale-calendar fail-safe.
- [ ] Seed default rule as a C1 tightening change via `risk.policy.update`.
- [ ] Tests + latency micro-benchmark.

## Verification

### Tests
- Golden: rule × event fixtures → expected windows per instrument.
- Unit: protective exit (reduce-only/stop) inside a window passes; new entry rejected with reason.
- Benchmark: lookup p99 < 20 µs with 10k events.
- Property: the D08 markers and M11 decisions agree for random times.

### Scenarios
- Given NFP at 08:30 ET and a USD scalper, then at 08:20 ET a new entry is rejected `blackout:NFP` and at 08:46 it passes.
- Given a meeting moved by a day, then windows move after the superseding row.
- Given the calendar is stale, then the fail-safe applies and an alert fires.

### Stress / failure injection
- Change policy and calendar 100× per second in a test harness: no torn reads; pre-trade p99 still < 1 ms.

## Acceptance criteria

- [ ] M11 rejects new entries inside windows and allows protective exits (tests)
- [ ] Latency budget met
- [ ] Blackout set identical in D06, D08 and M11
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Loosening a blackout (shorter window, removal) is a risk loosening → C3 via P2 change control.
- Holidays/sessions closed: handled by session rules, not blackouts.

## Cardinal rules (do NOT)

- Do NOT block protective exits during blackouts.
- Do NOT duplicate blackout logic in the UI; read the API.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT make loosening risk anything but C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/03-build-spec.md`: M5/M11: blackout API and default rule
- `docs/ui/dashboards/D06-risk.md`: Blackouts node: fields implemented
- `docs/roadmap/phase-4-intel.md`: tick T4.26 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T038-blackout-api-m11`
- PR title: `P4-T038: Blackout query API ("event within N minutes") wired into M11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
