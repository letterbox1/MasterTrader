---
id: P1-B020
kind: gap
title: Network placement and egress of the alert.* consumer are undefined
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.14]
roadmap_todos: [T1.31, T1.43]
modules: [M17]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B020-alert-consumer-network-placement
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §3.1
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B020 · Network placement and egress of the alert.* consumer are undefined

## Goal / expected outcome

02 §3.1 states which container runs the single `alert.*` consumer, which networks it joins, and which internet egress it has, so it can read NATS, receive Grafana/Alertmanager webhooks, publish to ntfy and reach the Telegram Bot API and your SMTP server, without widening any other network.

## Context & references

- Found in: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks): `core` egress = "venues and LLM APIs via allow-list" (no Telegram API or SMTP); `ntfy` sits on `edge` only; `obs` has "Telegram API (alerts)" egress although alerts leave only through the `alert.*` fan-out ([02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats)); [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) puts alerts in `telegram-bot`
- Related requirement: [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDos T1.31, T1.43 · tasks P1-T044 (ntfy), P1-T045 (fan-out), P1-T060 (alert path test)
- Decision context: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B006 (ntfy on Tailscale only, upstream relay for iOS), P1-B007 (one fan-out)

## Requirements

- **Steps to reproduce:** place `telegram-bot` (the consumer) on `core` per 02 §3.1 → it can't reach `ntfy` on `edge`, and `core` egress doesn't include `api.telegram.org` or your SMTP host; Alertmanager on `obs` can't reach it either
- **Expected:** one documented placement, e.g. the consumer joins `core` (NATS) and `obs` (webhook from Alertmanager), publishes to ntfy via Caddy's internal address, and the egress allow-list for that container alone adds `api.telegram.org:443` and the configured SMTP host; `obs` loses its Telegram egress
- **Actual:** no network path satisfies all four needs as written
- **Suggested fix:** amend 02 §3.1 (members + egress for `telegram-bot`; drop Telegram egress from `obs`) and 07 §9
- **Impact:** S3: P1-T045 must pick a placement; P1-T060 can't pass until the paths exist

## ToDo

- [x] Placement adopted from the recommendation (17 preamble: suggested fix applies)
- [x] Edited 02 §3.1 (alert consumer on `core` + `obs` + `edge`, own egress allow-list for Telegram Bot API + SMTP; `obs` Telegram egress only for the P0 interim route) and 07 §9
- [x] P1-T044, P1-T045 and P1-T060 point at 02 §3.1

## Verification

### Tests

- Doc review: 02 §3.1, §3.2, §6 and 07 §9 agree on where the consumer runs and what it may reach

### Scenarios

- Given the documented placement, when P1-T045's integration test runs on the Compose networks, then NATS, Alertmanager webhook, ntfy, Telegram and SMTP paths all work and nothing else gains egress

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Decision recorded in 02 §3.1 / 07 §9 (suggested fix per 17 preamble)
- [x] P1-T044 / P1-T045 match the documented placement

## Exceptions & edge cases

- Interim (until decided): P1-T045 runs the consumer in `telegram-bot` on `core` + `obs`, with a per-container egress allow-list for Telegram and SMTP; this keeps every other container's egress unchanged

## Cardinal rules (do NOT)

- Do NOT widen `core` or `obs` egress for all containers to make alerts work
- Do NOT bypass the single `alert.*` path (e.g. Alertmanager sending to Telegram directly)

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.1: members and egress for the alert consumer; `obs` egress
- `docs/07-security-notes.md` §9: note the alert consumer's egress

## Branch & PR

- Branch: `p1/P1-B020-alert-consumer-network-placement`
- PR title: `P1-B020: Define network placement and egress of the alert.* consumer`

## Progress log

- 2026-10-22 00:00 · aligner · opened during docs/16–17 task alignment; owned by P1-T045 (interim placement) and P1-T060 (proves the paths)
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: 02 §3.1 and 07 §9 define the alert consumer placement and egress; P0 direct Alertmanager → Telegram route is temporary until P1-T045
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/02-v1-architecture.md §3.1 (alert consumer networks/egress, P0 direct route temporary until P1-T045), docs/07-security-notes.md §9; P1-T044/T045/T060 updated
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
