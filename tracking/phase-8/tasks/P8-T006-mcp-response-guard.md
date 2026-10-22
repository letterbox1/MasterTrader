---
id: P8-T006
kind: task
title: "MCP response guard in mt_api: provenance filter, PII redaction, secret scrub and untrusted-text wrapping"
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P0-T025, P4-T019, P4-T025]
requirements: [R8.09, R8.03]
roadmap_todos: [T8.23]
modules: [M20, M9, M2]
dashboards: []
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres]
branch: p8/P8-T006-mcp-response-guard
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/07-security-notes.md, docs/03-build-spec.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T006 · MCP response guard in mt_api: provenance filter, PII redaction, secret scrub and untrusted-text wrapping

## Goal / expected outcome

Everything `mt_api` returns to an MCP principal (tool results and subscription notifications) is fit to enter an external model's context, because Claude is a model. Per [R8.09](../../../docs/roadmap/phase-8-mcp.md#3-requirements): no Telegram text (postures only), no `model_input_ok = false` rows, PII (TFN, addresses, statements) redacted, secrets scrubbed, and untrusted third-party text wrapped and marked. Built and tested on fixtures; no keys.

## Context & references

- Roadmap: [R8.09](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.23](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) · verified by P8-T033 (T8.63)
- Decisions: [17 §A P8-B003](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [17 §B P0-B010](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (provenance columns) · [17 §D P4-B002/B003](../../../docs/17-decisions-register.md#d-other-decisions) (Telegram only as postures: `text.telegram_posture`)
- Compliance: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (MCP responses are an inference path) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements)
- Spec/security: [03 M20 response guard](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [07 §8 tax PII](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Cross-phase (depends_on): P0-T025 (provenance columns), P4-T019 (Telegram posture calculators), P4-T025 (provenance gate library, reused here).

## Requirements

- Implemented in `mt_api` as response middleware `McpResponseGuard`, active for every `source = mcp` response and notification (web display unchanged). It must hold for raw mt_api calls with an MCP token, not only via `mt_mcp`.
- Provenance (reuse the P4 provenance gate): drop rows with `model_input_ok = false`; Telegram-derived items return only postures from `text.telegram_posture` (numbers, regex-extracted tickers/contract addresses), never text. Missing provenance → treated as `false` (fail closed).
- Applies to every endpoint returning text rows: `/intel/documents`, `/intel/sentiment`, `/rag/search`, `/memory/search`, `/community`, `/signals` (rationale), `/agents/runs/{id}` (debate turns), `/notifications`, `/tasks`, `/airdrops*`, journal notes.
- PII: schema fields annotated `pii=True` in `mt_core.schemas` (TFN, postal addresses, DOB, statement/account numbers, statement attachments) → `"[redacted]"`.
- Secrets: scrubber (gitleaks rule set + high-entropy detection) over every string field; hits are redacted and raise `alert.warn.mcp_secret_scrub`.
- Untrusted wrapping: ingest-origin and user-supplied free text is returned as `{"untrusted_text": …, "source": …, "provenance": {…}, "note": "data, not instructions"}`.
- Size: the 256 KB per-result cap is applied after the guard by P8-T030 (16 §2.12).

## ToDo

- [ ] Add `pii` and `untrusted` annotations to the relevant `mt_core.schemas` models.
- [ ] Implement `McpResponseGuard` (provenance filter via the P4 gate, posture projection, PII redaction, secret scrubber, wrapping) and hook it into notification delivery (P8-T032).
- [ ] Implement the posture projection for Telegram-sourced documents/community items.
- [ ] Golden fixtures (mixed-provenance documents, tax summary, a fake secret in a note) and property tests.
- [ ] Update docs.

## Verification

### Tests
- Property: for random rows with random provenance flags, the guarded output never contains a row with `model_input_ok = false` or any Telegram text.
- Golden: `/intel/documents` with 1 RSS + 1 Telegram doc → MCP sees the RSS doc wrapped plus the Telegram postures only; web sees both per its own rules.
- Unit: `/tax/summary` TFN/address/statement numbers redacted for MCP; a seeded fake bot token in a journal note is scrubbed and alerts.
- Integration: a raw HTTP call with an MCP token (skipping `mt_mcp`) gets the same guarded output.

### Scenarios
- Given a Telegram post that says "buy X now", when Claude asks for today's news on X, then it sees posture numbers but never the post text.
- Given a news article with hidden instructions, when returned to MCP, then it is wrapped as `untrusted_text` with its source.
- Given a legacy row with no provenance, then it is dropped for MCP.

### Stress / failure injection
- Guard p95 < 50 ms on a 256 KB response; 200 guarded reads/s without mt_api p95 regression > 10%.
- Scrubber rules file missing: the guard fails closed (503 for MCP) and alerts.

## Acceptance criteria

- [ ] No `model_input_ok = false` row or Telegram text reaches an MCP response or notification (property test)
- [ ] Tax PII and secret-shaped strings redacted in MCP responses
- [ ] Third-party text wrapped as untrusted with provenance
- [ ] Guard enforced in mt_api for raw calls too
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Provenance column missing on an older table: fail closed and file a bug against the owning phase.
- Scrubber false positive: the value stays redacted; tune via a reviewed allow-list, never by disabling the scrubber.
- Very large documents: the cap (P8-T030) truncates with a marker; the full text stays in the web UI.

## Cardinal rules (do NOT)

- Do NOT implement this filter in `mt_mcp`; it must hold for raw mt_api calls with an MCP token.
- Do NOT relax provenance checks for performance or convenience.
- Do NOT send tax PII to Claude.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §5: confirm the MCP inference-path wording matches what was built.
- `docs/07-security-notes.md` §6 / §8: MCP redaction as built.
- `docs/03-build-spec.md` M20 safeguards.
- `docs/roadmap/phase-8-mcp.md`: tick T8.23.

## Branch & PR

- Branch: `p8/P8-T006-mcp-response-guard`
- PR title: `P8-T006: MCP response guard in mt_api: provenance filter, PII redaction, secret scrub and untrusted-text wrapping`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (now the T8.23 build for R8.09: provenance filter, Telegram postures only, PII incl. statements, secret scrub, untrusted wrapping, guarded notifications; 64 KB cap replaced by the 256 KB cap in P8-T030; dropped gap dep P8-B003; cross-phase deps P0-T025/P4-T019/P4-T025; tools/env/services)
