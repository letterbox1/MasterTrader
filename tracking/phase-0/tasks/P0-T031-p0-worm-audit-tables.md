---
id: P0-T031
kind: task
title: Create the P0 WORM audit tables and correction views
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T030]
requirements: [R0.07, R0.08]
roadmap_todos: [T0.23]
modules: [M17, mt_obs]
dashboards: []
branch: p0/P0-T031-p0-worm-audit-tables
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T031 · Create the P0 WORM audit tables and correction views

## Goal / expected outcome

The P0 WORM tables exist via the helper — `audit.command`, `audit.auth_event`, `audit.llm_call`, `audit.seal`, `audit.incident`, `audit.verify_run` — with `mt_obs.audit` writers, `trace_id` on every row, and the correction pattern (`supersedes_id` + `*_current` views that pick the latest row per key).

## Context & references

- [Roadmap P0 R0.07, R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.1 scope](../../../docs/15-bots-hitl-and-worm-audit.md#21-scope)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Corrections)
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every LLM call, every mt_api command)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`audit.command` source = web|telegram|mcp|system)
- Depends on: P0-T030

## Requirements

- `audit.command`: `id uuid`, `command`, `level` (C0|C1|C2|C3|KILL), `source` (`web|telegram|mcp|system`), `actor`, `args_redacted jsonb`, `args_hash bytea`, `idempotency_key`, `reason`, `status` (`accepted|rejected|pending_confirmation|applied|failed|cancelled`), `result jsonb`, `error_type`, `trace_id`, `event_time`, `ingest_time`, `supersedes_id` + chain columns. Status changes are **new rows** referencing the first via `supersedes_id`.
- `audit.auth_event`: login success/failure, TOTP enrol/verify, logout, session expiry, lockout — no passwords, no TOTP codes.
- `audit.llm_call`: `model`, `route`, `role`, `prompt_hash`, `response_hash`, `prompt_text`, `response_text`, `tokens_in/out`, `cost`, `latency_ms`, `trace_id` (03 M17). Writer is LiteLLM's callback (P0-T042).
- `audit.seal`, `audit.verify_run`, `audit.incident` schemas defined here; filled by P0-T037 / P0-T038.
- `mt_obs.audit.write(table, row)` async writer using the role `mt_obs_rw`/`mt_api_rw`; never blocks the caller on seals; failures raise (no silent drop) and increment `mt_audit_write_failures_total`.
- Views `audit.command_current` etc.: `DISTINCT ON (root_id) ... ORDER BY root_id, seq DESC`.

## ToDo

- [ ] Migrations (WORM-tagged, run by ceremony) creating the six tables via `create_worm_table()`; register in `audit.worm_registry`.
- [ ] Implement `mt_obs.audit` writers and redaction of args (reuse the secret regex).
- [ ] Create `*_current` views and tests.
- [ ] Document the correction pattern with an example in `mt_obs` README.

## Verification

### Tests
- Integration: insert → chain valid; status transition creates a new row and the current view shows the latest.
- Unit: args redaction removes secrets/TOTP codes before insert.
- Privilege: app roles cannot UPDATE any of the six tables.

### Scenarios
- Given a command fails after acceptance, then `audit.command` has two rows (accepted, failed) with the same root and the current view shows `failed`.
- Given Postgres is down, when a command arrives, then mt-api rejects it with 503 problem+json (no command executes unaudited).

### Stress / failure injection
- Burst: 500 commands/s for 60 s through `mt_obs.audit.write` → no lost rows, chain valid (feeds P0-T059).

## Acceptance criteria

- [ ] Six WORM tables registered and chained
- [ ] Writers + redaction + current views tested
- [ ] No command path can execute without its audit row (tested)
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Very large LLM prompts: store text up to 1 MB per field; above that store the hash + object path (P6 decides storage).

## Cardinal rules (do NOT)

- Do NOT log TOTP codes, passwords or session tokens in any audit row.
- Do NOT execute a command if its `accepted` audit row failed to write.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §5.3: add the P0 audit tables to the core entities list.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T031-p0-worm-audit-tables`
- PR title: `P0-T031: Create the P0 WORM audit tables and correction views`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
