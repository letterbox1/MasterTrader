---
id: P2-T113
kind: task
title: LLM leakage review via the gateway with audited waivers
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101]
requirements: [R2.43]
roadmap_todos: [T2.27]
modules: [M7, M21]
dashboards: [D04, D03]
branch: p2/P2-T113-llm-leakage-review
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T113 · LLM leakage review via the gateway with audited waivers

## Goal / expected outcome

An adversarial leakage checklist is run by a model through the LiteLLM gateway on each strategy's code; it answers present/absent per item quoting exact lines (verified against the file), any 'present' blocks the strategy, and you can waive an item with a reason that is written to the WORM audit.

## Context & references

- Roadmap: [R2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27 · verified by P2-T160
- [14 §6 gate 1](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (checklist items, quote exact line, waiver audited) · [10 §5 gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (per-role virtual keys, budgets, local fallback)
- Missing waiver command in the catalogue: P2-B056
- Cross-phase: P0 T0.45 LiteLLM config (role keys) and T0.23 WORM layer

## Requirements

- Checklist (versioned `leakage_checklist_v1`): look-ahead, survivorship, repainting indicators, costs, fill realism, full-sample fitting, regime coverage, alignment.
- Prompt includes only the strategy's own code + manifest (no data rows, no secrets, no Telegram text); calls go via gateway role `lab-review` (or `strategy-gen` key) with its daily budget; route research-primary → research-custom → local-advisor.
- Structured JSON output per item: `present|absent|unsure`, file, line range, quoted text; the quote must match the file at those lines exactly or the item becomes `unsure` (hallucination guard).
- `present` or `unsure` blocks the 'leakage review' gate until fixed (new code version) or waived.
- Waiver: command `lab.leakage.waive` (C1, reason required) → `audit.command` + insert-only `audit.leakage_waiver` row referencing the review id and item; waivers never carry over to a new code version.
- Every LLM call logged in `audit.llm_call` (model, prompt hash, cost).

## ToDo

- [ ] Write `leakage_checklist_v1` prompt + JSON schema in `mt_lab/review/`
- [ ] Implement gateway client (OpenAI-compatible) using the role virtual key from secrets; budget-exhausted fallback to local model
- [ ] Implement quote verification against the source file
- [ ] Implement `lab.leakage.waive` command handler in `mt_api` and the `audit.leakage_waiver` migration (insert-only)
- [ ] Register as a validation section; store review + waivers for D03/D04
- [ ] Tests with recorded model responses (no live calls in CI)

## Verification

### Tests
- Unit: quote verification marks a mismatched quote `unsure`.
- Unit: JSON schema violations → retry once, then `unsure` for all items.
- Integration (recorded responses): seeded look-ahead fixture → 'look-ahead: present' quoting the `shift(-1)` line.
- Integration: waiver writes `audit.command` + `audit.leakage_waiver`; UPDATE on the waiver row fails.

### Scenarios
- Given the gateway budget is exhausted, when a review runs, then it falls back to `local-advisor` and the report shows the model used.
- Given the gateway is down entirely, then the leakage section is 'pending' and the gate stays blocked (never auto-pass).
- Given a waived item and a new code version, then the waiver does not apply and the review re-runs.

### Stress / failure injection
- Strategy file of 3,000 lines: chunked by function with line offsets preserved; token budget per call ≤ the role's limit.

## Acceptance criteria

- [ ] Every checklist item answered with verified quotes or `unsure`
- [ ] Waivers audited (WORM) and scoped to one code version
- [ ] No live LLM calls in CI
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Generated strategies (P2-T116) are reviewed the same way after leaving the sandbox.
- Model returns 'absent' for everything on obviously buggy fixture: covered by P2-T160 which requires both analysers and review to catch the seeded bug.

## Cardinal rules (do NOT)

- Do NOT send data rows, secrets or environment details to the model; code + manifest only.
- Do NOT let an 'unsure' or gateway failure count as a pass.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT update or delete WORM rows (`audit.*`); corrections are new rows referencing the original (15 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: checklist version and waiver flow.
- `docs/02-v1-architecture.md` §7.2: add `lab.leakage.waive` (per P2-B056).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T113-llm-leakage-review`
- PR title: `P2-T113: LLM leakage review via the gateway with audited waivers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T113` run

## Progress log

- 2026-10-21 00:00 · planner · created
