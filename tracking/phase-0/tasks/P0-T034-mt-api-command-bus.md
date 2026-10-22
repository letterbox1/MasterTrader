---
id: P0-T034
kind: task
title: Implement the command bus with idempotency and audit.command
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T032, P0-T031]
requirements: [R0.08]
roadmap_todos: [T0.24]
modules: [mt_api, M17]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats, prefect-server]
branch: p0/P0-T034-mt-api-command-bus
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T034 · Implement the command bus with idempotency and audit.command

## Goal / expected outcome

`POST /api/v1/commands/{command}` accepts `{args, idempotency_key, reason}`, validates args against the command's typed schema, enforces idempotency, writes `audit.command` before and after execution with source/actor/trace_id, and dispatches to a registered handler. P0 registers the system commands it needs; later phases add theirs without touching the bus.

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation) (idempotency per confirm sheet)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls) (one command layer)
- Related: P0-T035 (levels), P0-T031
- Depends on: P0-T032, P0-T031

## Requirements

- Registry: `@command(name, level, args=Struct, result=Struct, scopes=...)`; unknown command → 404 problem+json; schema in OpenAPI per command.
- P0 commands: `system.settings.update` (C0 for preferences, layout and digests; C1 to tighten or for schedules; C3 to loosen, e.g. raise an LLM budget or a DQ threshold, via the diff classifier hook; 02 §7.2), `system.backup.run` (C1), `system.restore.test` (C1), `audit.verify` (C1), `risk.kill.on` (Kill), `risk.kill.off` (C3), `system.key.rotate_reminder` (C0), `system.service.restart` (C2; registered here with a 501 stub; P0-T065 wires it through `docker-proxy`, allow-listed containers only, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B012), `audit.integrity.ack` (C3; handler in P0-T038).
- Idempotency: `ops.idempotency_key (key, command, args_hash, status, response, created_at)`, TTL 24 h; same key + same args → replay stored response (200, header `Idempotent-Replay: true`); same key + different args → 409; in-flight duplicate → 409 `in_progress`.
- Audit: `accepted` row written **before** the handler runs (if it fails to write → 503, handler never runs); terminal row (`applied|failed|rejected`) after; `source` from the authenticated principal (`web` session, `telegram`/`mcp` token, `system` for internal).
- Args redaction before audit; `args_hash` = sha256 of canonical args (unredacted) for idempotency comparison.
- Every command publishes `audit.command.{status}` on NATS for the WS `notifications`/`system` topics.
- Handler timeout default 10 s; long jobs return `202` with a job id and finish via Prefect.

## ToDo

- [ ] Implement registry, endpoint, idempotency store, audit integration and NATS publish.
- [ ] Register the P0 commands with stub/real handlers (kill → NATS KV `kill`; backup/restore → Prefect deployment run; verify → P0-T038).
- [ ] Add `GET /audit/log` basic query (paged) used by D16 (filters in P0-T046).
- [ ] Tests below.

## Verification

### Tests
- Integration: a C0 command writes two `audit.command` rows (accepted, applied) with valid chain and `trace_id`.
- Idempotency: replay returns identical body; different args → 409; concurrent duplicates → exactly one execution.
- Failure: audit write fails (DB paused) → 503 and handler not called (spy).

### Scenarios
- Given the web double-submits a confirm sheet, when both requests arrive, then one executes and the other gets 409 in-progress or the replayed result.
- Given an unknown command name, then 404 problem+json and an `audit.command` row `rejected` (so probing is visible).

### Stress / failure injection
- 200 commands/s mixed (C0) for 5 min: p99 < 50 ms excluding handler time (SLO, 02 §9.2); chain valid afterwards.

## Acceptance criteria

- [ ] Bus + registry + idempotency + audit implemented
- [ ] P0 commands registered with correct levels
- [ ] Exactly-once execution under duplicate submits (tested)
- [ ] No command executes without an `accepted` audit row (tested)
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Kill ON must not be blocked by idempotency storage being down: Kill path writes NATS KV first, records through the JetStream WORM buffer (P0-T031, 16 §3.3), and still returns success (see P0-T035).

## Cardinal rules (do NOT)

- Do NOT add any write endpoint outside `/commands/{command}`.
- Do NOT execute a handler before its audit row exists (except Kill ON, whose record goes through the JetStream buffer right after the KV write).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: document idempotency semantics (24 h TTL, 409 rules) and the P0 command levels.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T034-mt-api-command-bus`
- PR title: `P0-T034: Implement the command bus with idempotency and audit.command`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (settings levels per 02 §7.2, restart via docker-proxy (17 §D P0-B012), audit.integrity.ack registered, Kill recorded via JetStream buffer, command-bus SLO; run fields added)
