---
id: P8-B003
kind: gap
title: MCP responses are a model input, but provenance and PII filtering for MCP isn't specified
phase: 8
type: DOC
status: backlog
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
doc_sync_status: n/a
found_in: docs/12-policy-and-compliance.md §5; docs/03-build-spec.md M20; docs/07-security-notes.md §8
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
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

- [ ] Confirm the proposed resolution (with the user if it changes behaviour)
- [ ] Edit the listed docs so they agree with each other
- [ ] Write or point to the test in the implementing P8 task that pins the behaviour
- [ ] Note the resolution in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and mutually consistent
- [ ] Implementing task test exists and passes
- [ ] Resolution noted in the Progress log

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
