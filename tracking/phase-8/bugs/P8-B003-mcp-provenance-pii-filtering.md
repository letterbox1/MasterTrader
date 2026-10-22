---
id: P8-B003
kind: gap
title: MCP responses are a model input, but provenance and PII filtering for MCP isn't specified
phase: 8
type: DOC
status: done
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.03, R8.06]
roadmap_todos: [T8.20]
modules: [M20]
dashboards: []
branch: p8/P8-B003-mcp-provenance-pii-filtering
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §5; docs/03-build-spec.md M20; docs/07-security-notes.md §8
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B003 · MCP responses are a model input, but provenance and PII filtering for MCP isn't specified

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add "MCP responses" to the 12 §5 inference-path list; state in 03 M20 and 07 §6/§8 that `mt_api` applies a response guard for `source = mcp` (provenance filter with Telegram postures only, PII redaction, secret scrub, untrusted wrapping).

## Context & references

- Compliance: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) · [SPEC NN10](../../../SPEC.md#non-negotiable-requirements) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Implementing task: P8-T006

## Requirements

- **Steps to reproduce:** Read 12 §5 "Inference paths (tier B, agents, RAG retrieval) refuse rows with `model_input_ok = false`" and 03 M20's read scope, which includes "news/event summaries" and "journal/tax summaries".
- **Expected:** MCP tool results (which go into Claude's context) are listed as an inference path: Telegram text and other `model_input_ok = false` rows are filtered, and tax PII (07 §8) is redacted.
- **Actual:** MCP isn't named as an inference path; nothing stops `/intel/documents` from returning Telegram-sourced text, or `/tax/*` from returning TFN/addresses, to Claude.
- **Impact:** Breach of SPEC NN10 / Telegram API ToS §1.5 and leak of tax PII to an external LLM (S2)
- **Suggested fix:** add "MCP responses" to the 12 §5 inference-path list; state in 03 M20 and 07 §6/§8 that `mt_api` applies a response guard for `source = mcp` (provenance filter with Telegram postures only, PII redaction, secret scrub, untrusted wrapping).

## ToDo

- [x] Decision recorded: 17 §A (P8-B003): MCP responses pass the provenance filter like any model input: no Telegram text, no `model_input_ok = false` rows, PII redacted, untrusted text wrapped
- [x] Docs carry it: 12 §5 inference paths incl. MCP responses; 03 M20 response guard; 02 §7.4 Responses; 07 §6 and §8; roadmap R8.09/T8.23/T8.63
- [x] Implementation owned by P8-T006 (guard, T8.23), P8-T033 (guard tests, T8.63)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 12 §5 inference paths incl. MCP responses; 03 M20 response guard; 02 §7.4 Responses; 07 §6 and §8; roadmap R8.09/T8.23/T8.63)
- [x] Implementing work owned and its test named: P8-T006 (guard, T8.23), P8-T033 (guard tests, T8.63)
- [x] Root cause noted: 12 §5 listed inference paths before MCP was scoped

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: as described in the suggested fix.
- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/07-security-notes.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B003-mcp-provenance-pii-filtering`
- PR title: `P8-B003: fix mCP responses are a model input, but provenance and PII filtering for MCP isn't specified`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B003` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P8-B003); docs checked: 12 §5 inference paths incl. MCP responses; 03 M20 response guard; 02 §7.4 Responses; 07 §6 and §8; roadmap R8.09/T8.23/T8.63; implementation owned by P8-T006 (guard, T8.23), P8-T033 (guard tests, T8.63); root cause: 12 §5 listed inference paths before MCP was scoped
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P8-B003); docs updated: 12 §5 inference paths incl. MCP responses; 03 M20 response guard; 02 §7.4 Responses; 07 §6 and §8; roadmap R8.09/T8.23/T8.63; implementation owned by P8-T006 (guard, T8.23), P8-T033 (guard tests, T8.63)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
