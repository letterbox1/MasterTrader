---
id: P0-B019
kind: gap
title: P0 tunables without a default in doc 16
phase: 0
type: DOC
status: done
priority: low
size: S
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.08, R0.10, R0.12, R0.14, R0.N4]
roadmap_todos: []
modules: [mt_api, M17, ops]
dashboards: [D16]
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B019-p0-tunables-without-a-default-in-doc-16
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md]
doc_sync_status: done
found_in: docs/16-configuration-and-safety-model.md §2
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B019 · P0 tunables without a default in doc 16

## Goal / expected outcome

Every number the P0 tasks treat as a user-changeable setting has its default recorded in [16](../../../docs/16-configuration-and-safety-model.md) ("this doc is the reference"), so tasks link to one place instead of carrying their own provisional values.

## Context & references

- Found in: `docs/16-configuration-and-safety-model.md` §2 while aligning Phase 0 tasks to docs/16–17 (2026-10-22)
- Cardinal rule: nothing a user may want to change is hard-coded; it goes in the configuration doc as a default (AGENTS §4)
- Affected tasks: P0-T033 (login lockout, absolute session lifetime), P0-T035 (confirm-token TTL, C3 approval TTL), P0-T023 (Loki retention), P0-T037 (seal grace period, anchor retry window), P0-T039 (backup times, pgBackRest full-backup retention), P0-T065 (default restart allow-list), P0-T018 (heartbeat interval for non-engine services)

## Requirements

- **Steps to reproduce:** Search 16 §2–§3 for each value below.
- **Expected:** Each has a default (and accepted range where relevant) in 16, like the C3 cool-down (§2.3) or the WORM integrity action (§2.11).
- **Actual:** None of these are in 16; the P0 tasks currently carry them as setting defaults of their own:
  - confirm-token TTL 120 s and C3 approval TTL 10 min (P0-T035; 16 §2.3 has the cool-down and HITL order TTLs only);
  - login lockout 5 failures / 15 min with doubling to 24 h, and absolute session lifetime 7 d (P0-T033; ui §3.6 has only the 12 h idle timeout);
  - Loki retention 30 d (range 30–90 d, roadmap T0.46) (P0-T023);
  - seal grace period 10 min and anchor retry hourly for 24 h (P0-T037);
  - backup times (weekly full Sun 02:00, nightly incremental 02:00 Australia/Sydney) and pgBackRest full-backup retention 4 (P0-T039);
  - default `docker-proxy` restart allow-list (P0-T065);
  - heartbeat interval for non-engine services (P0-T018 uses the 1 s engine cadence from 16 §3.1).
- **Impact:** Low: values stay configurable in the tasks, but 16 isn't yet the single reference for them.
- **Suggested fix:** Add a short "Platform & ops" subsection to 16 §2 listing these defaults (and ranges), then point the tasks at it.

## ToDo

- [x] Values taken from the P0 task defaults (17 §E: configurable values are settings, not questions)
- [x] Doc 16 updated: confirm-token TTL 120 s and C3 approval TTL 10 min in §2.3; lockout, session lifetime, heartbeat 1 s, Loki 30 d [30–90 d], seal grace 10 min, anchor retry hourly 24 h, backup schedule + pgBackRest retention 4, docker-proxy restart allow-list in new §2.14 Platform & operations
- [x] P0-T018, P0-T023, P0-T033, P0-T035, P0-T037, P0-T039 and P0-T065 link 16 §2.3 / §2.14
- [x] Regression check stays with P0-T017's defaults-file test (each default references its 16 section)

## Verification

### Tests
- Doc check: each listed value appears once in 16 with a default; `infra/config/defaults.yaml` (P0-T017) references the 16 section for each.

### Scenarios
- Given a developer needs the C3 approval TTL, then 16 gives the default and the task links there.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Every listed value has a default in 16 (§2.3, §2.14)
- [x] Affected tasks link to it
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user prefers different values, the tasks are updated before they start; nothing is built yet.

## Cardinal rules (do NOT)

- Do NOT hard-code any of these values in code; they're settings with defaults.
- Do NOT close without updating 16.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §2: add the platform/ops defaults.

## Branch & PR

- Branch: `p0/P0-B019-p0-tunables-without-a-default-in-doc-16`
- PR title: `P0-B019: P0 tunables without a default in doc 16`
- PR checklist: docs synced · task file ticked · `./kanban done P0-B019` run

## Progress log

- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · opened
- 2026-10-22 00:00 · aligner · filed during the 16–17 alignment; left open (needs a doc-16 change, outside this agent's scope). Root cause: 16 covers trading/safety defaults but not platform/ops tunables introduced by the P0 task plan.
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: defaults from the P0 tasks added to 16 §2.3 and new §2.14; tasks linked. Root cause: 16 covered trading/safety defaults but not platform/ops tunables introduced by the P0 plan
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/16 §2.3 (confirm-token and C3 approval TTLs) + new §2.14 Platform & operations; P0-T018/T023/T033/T035/T037/T039/T065 link it
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
