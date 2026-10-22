---
id: P8-T033
kind: task
title: "Response-guard tests: Telegram rows, model_input_ok=false rows and tax PII never reach the MCP client"
phase: 8
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T006, P8-T008, P8-T009, P8-T013, P8-T032]
requirements: [R8.09]
roadmap_todos: [T8.63]
modules: [M20, M2, M18]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T033-response-guard-tests-telegram-rows-model-input-o
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/12-policy-and-compliance.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P8-T033 · Response-guard tests: Telegram rows, model_input_ok=false rows and tax PII never reach the MCP client

## Goal / expected outcome

A suite `tests/security/test_mcp_response_guard.py`, mandatory for merge, proves T8.63: through every MCP path (every read tool, every resource and notification, and raw `mt_api` calls with an MCP token), a Telegram-sourced row, a `model_input_ok = false` row, a TFN, a postal address and statement numbers never reach the MCP client unredacted, secrets are scrubbed, and untrusted text arrives wrapped and marked. Runs on seeded fixtures; no keys.

## Context & references

- Roadmap: [R8.09](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.63](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §A P8-B003](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [17 §B P0-B010](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (provenance columns)
- Compliance: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (MCP responses are an inference path) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (tax PII excluded from MCP responses)
- Precedent: P4-T050 (Telegram-text gate test for other inference paths).
- Related: P8-T006 (guard), P8-T008/T009/T013 (tools), P8-T032 (resources/notifications).

## Requirements

- Seed corpus (canary strings, each unique and searchable): a Telegram-sourced document and community post; a row with `model_input_ok = false` from a non-Telegram source; a journal note with a fake TFN, a postal address and a statement account number; a tax summary with PII fields; a news article with a fake API key and an embedded instruction; a legacy row with no provenance.
- Probe every MCP read tool and resource from the registry dump (not a hand-picked list), plus raw HTTP calls with an MCP token that skip `mt_mcp`, plus notifications from P8-T032.
- Assertions on the collected output: no Telegram canary text and no `model_input_ok = false` canary anywhere (postures may appear as numbers); TFN/address/statement canaries only as `[redacted]`; the fake key scrubbed and an alert raised; the article wrapped as `untrusted_text` with source and provenance; the no-provenance row absent.
- The same probes with a web session show the web rules unchanged (the guard is MCP-only).
- Marked a required CI check for PRs touching `mt_api`, `mt_core.schemas` or `mt_mcp`.

## ToDo

- [ ] Write the canary fixtures and the registry-driven probe harness.
- [ ] Write the suite; make it a required check.
- [ ] Run and record results (counts per tool, zero leaks) in the Progress log.
- [ ] Doc sync.

## Verification

### Tests
- The suite; plus a mutation check: disabling one guard stage (provenance, PII or wrapping) makes at least one test fail.

### Scenarios
- Given a Telegram post "buy X now", when every MCP read path is probed, then the post text appears nowhere; posture numbers do.
- Given a tax summary request via MCP, then TFN/address/statement fields are `[redacted]`.
- Given a new read endpoint added later without `pii`/`untrusted` annotations, then the registry-driven probe catches any canary leak in CI.

### Stress / failure injection
- Run the probes concurrently (20 workers) against 10,000 seeded rows: zero leaks, guard p95 within the P8-T006 target.

## Acceptance criteria

- [ ] Zero Telegram or `model_input_ok = false` canaries in any MCP output (tools, resources, notifications, raw calls)
- [ ] PII canaries only redacted; secret canary scrubbed with alert; untrusted text wrapped
- [ ] Mutation check proves the suite bites; required check in CI
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- A tool returns binary/attachments: attachments are never returned to MCP; the probe asserts that.
- A canary appears in a posture-derived ticker by coincidence: canaries are chosen so they can't be a valid ticker.

## Cardinal rules (do NOT)

- Do NOT use real Telegram content or real PII as fixtures; canaries only.
- Do NOT allow-list a leak to get green.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.63; R8.09 verified (link to CI run).
- `docs/12-policy-and-compliance.md` §5: link to the suite.

## Branch & PR

- Branch: `p8/P8-T033-response-guard-tests-telegram-rows-model-input-o`
- PR title: `P8-T033: Response-guard tests: Telegram rows, model_input_ok=false rows and tax PII never reach the MCP client`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T033` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R8.09 / T8.63 (registry-driven canary probes over tools, resources, notifications and raw calls; 17 §A P8-B003)
