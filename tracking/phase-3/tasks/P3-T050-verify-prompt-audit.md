---
id: P3-T050
kind: task
title: Prompt audit proving no TFN or address reaches the LLM gateway
phase: 3
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T007, P3-T039, P0-T042]
requirements: [R3.N1]
roadmap_todos: [T3.64]
modules: [M18, M21, M17]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, litellm, journal]
branch: p3/P3-T050-verify-prompt-audit
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T050 · Prompt audit proving no TFN or address reaches the LLM gateway

## Goal / expected outcome

An automated audit shows that no tax-sensitive field (TFN, address, raw statements, residency evidence) is reachable by the LiteLLM gateway, agents or decision services — by grants, by network/secret scoping and by content scanning of logged prompts.

## Context & references

- Roadmap: [R3.N1, T3.64](../../../docs/roadmap/phase-3-journal-and-tax.md) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) · provenance [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Cross-phase prerequisite (depends_on): P0-T042 (LiteLLM gateway, writes `audit.llm_call` from P0 per [17 §D P6-B010](../../../docs/17-decisions-register.md#d-other-decisions)); P6 agents must keep passing this audit

## Requirements

- Grant audit: roles used by `litellm`, `agents`, `decision-svc`, `nlp` have no SELECT on `journal.*` except `journal.llm_safe_summary`; no EXECUTE on decrypt helpers.
- Secret audit: only `journal` mounts the master key; data keys exist only wrapped in `ops.journal_data_key`, which no other role can read (envelope encryption, P3-T006).
- Content audit: seed canary values (fake TFN `123 456 782`-style pattern, fake address string) into `journal.taxpayer_profile` in a test env; run every agent/tool path available; scan `audit.llm_call` prompts + LiteLLM logs → zero canary hits.
- CI static check: any code importing `mt_journal.crypto` outside `packages/mt_journal/` fails the build.
- Job runs in CI and monthly in production (canary-free mode: pattern scan of `audit.llm_call` for TFN-like 9-digit checksummed numbers).

## ToDo

- [ ] Write `tests/security/test_prompt_audit.py` (grants, secrets, canary)
- [ ] Monthly Prefect flow `security-prompt-audit`
- [ ] CI import guard
- [ ] Record results

## Verification

### Tests

- As above; negative test: temporarily grant SELECT in a scratch DB → audit fails.

### Scenarios

- Given a prompt that asks an agent for "my TFN", when run in the test env, then the agent cannot retrieve it and no canary appears in `audit.llm_call`.

### Stress / failure injection

- n/a: security audit

## Acceptance criteria

- [ ] Zero canary hits
- [ ] Grant + secret audits pass
- [ ] Monthly flow scheduled
- [ ] Import guard in CI

## Exceptions & edge cases

- New services added later inherit the audit through the role list; the audit fails closed if an unknown role has journal grants.

## Cardinal rules (do NOT)

- Do NOT use a real TFN as a canary.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.64 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T050-verify-prompt-audit`
- PR title: `P3-T050: Prompt audit proving no TFN or address reaches the LLM gateway`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secret audit covers the envelope-encryption master key and key table (P3-B009); explicit P0-T042 depends_on; tools/services filled)
