---
id: P5-B018
kind: gap
title: EV time value and default haircut have no documented default
phase: 5
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.14]
roadmap_todos: []
modules: [M4]
dashboards: [D12]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B018-ev-time-value-and-haircut-defaults-unspecified
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md, docs/08-airdrops-and-token-launches.md]
doc_sync_status: done
found_in: P5-T007
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: 2026-11-19
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B018 · EV time value and default haircut have no documented default

## Goal / expected outcome

[16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) lists a default for the EV time value (AUD per minute of your time) and the default haircut used by the [08 EV gate](../../../docs/08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes), so the P5-T007 seed takes every EV input from a documented default instead of an agent draft.

## Context & references

- Found in: P5-T007 (converted from a USER task to an agent seed task per [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)).
- 08 EV formula names `your_minutes × time_value` and `haircut`; 16 §2.7 gives only the hurdle (5% p.a.); P5-T040 reads both from settings.
- Related: P5-T040 (EV gate), P5-T007 (seed), P7-T070 (go-live pack review).

## Requirements

- **Steps to reproduce:** look for a time-value or default-haircut default in 08, 13 or 16.
- **Expected:** a documented, configurable default for each (16 §2.7), as for the hurdle.
- **Actual:** none; P5-T007 has to draft them.
- **Impact:** S4: the seed drafts conservative values (they can only remove opportunities from the digest compared with zero) and you review them in the go-live pack; nothing is blocked.

## ToDo

- [x] Take the values drafted in P5-T007 and add them to 16 §2.7 as configurable defaults (with the reasoning), and link them from the 08 EV gate
- [x] Record the outcome in the decisions register if the values change
- [x] Confirm the P5-T007 seed now cites 16 §2.7 for every EV input

## Verification

### Tests
- n/a: documentation gap; the P5-T007 doc-parse test checks the seed against 16 §2.7 once the rows exist.

### Scenarios
- Given 16 §2.7 lists the time value and haircut, when the P5-T007 seed runs, then every EV input carries a 16 §2.7 `seed_source`.

### Stress / failure injection
- n/a: documentation.

## Acceptance criteria

- [x] 16 §2.7 lists default time value and haircut
- [x] P5-T007 seed sources updated

## Exceptions & edge cases

- If the values are left for the go-live pack review, the drafted values stay in place and this gap stays open at S4 (it doesn't block the phase).

## Cardinal rules (do NOT)

- Do NOT pick values that add opportunities to the digest compared with a zero time value and zero haircut.
- Do NOT hard-code the numbers; they belong in 16 §2.7 and the settings defaults file.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §2.7: add the two rows.
- `docs/08-airdrops-and-token-launches.md`: link the EV gate's time value and haircut to 16 §2.7.

## Branch & PR

- Branch: `p5/P5-B018-ev-time-value-and-haircut-defaults-unspecified`
- PR title: `P5-B018: EV time value and default haircut have no documented default`
- PR checklist: docs synced · item ticked

## Progress log

- 2026-11-19 00:00 · aligner · opened during the re-platform task wave (P5-T007 conversion)
- 2026-11-19 · main · resolved: 16 §2.7 now lists time value A$1/min and default haircut 50% (conservative), linked from 08 EV gate; P5-T007 cites them. Values are defaults, not decisions, so no 17 row needed.
- 2026-11-19 09:44 · cloud:vm:be04b6ae61f8 · verified: 16 §2.7 rows 'EV time value' (A$1/min) and 'EV default haircut' (50%); 08 EV gate links them; P5-T007 cites 16 §2.7
- 2026-11-19 09:44 · cloud:vm:be04b6ae61f8 · commits: ab8a69e
- 2026-11-19 09:44 · cloud:vm:be04b6ae61f8 · done
- 2026-11-19 09:44 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in this wave
