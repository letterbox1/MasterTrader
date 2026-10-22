---
id: P6-T053
kind: task
title: Verify LLM budgets, monthly cap and local fallback (budget test)
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T009, P6-T010]
requirements: [R6.07, R6.03]
roadmap_todos: [T6.70]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [litellm, llm-local, grafana]
branch: p6/P6-T053-verify-llm-budget-fallback
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T053 · Verify LLM budgets, monthly cap and local fallback (budget test)

## Goal / expected outcome

The budget test proves that per-role and monthly limits hold, exhausted budgets fall back to local models with the badge shown, raises need C3, and alerts fire — including under gateway/provider failure.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.70
- Roadmap: R6.07 'Budget test' · [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Depends on (this phase): P6-T009, P6-T010 (fake provider only; the live check with your keys is P6-T070)
- Defaults under test: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)

## Requirements

- Scenarios run against a fake provider with controllable cost/latency/errors; no keys needed.
- Defaults under test (settings, 16 §2.10): US$40 per UTC month, daily debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; whichever runs out first (role day or monthly cap) routes to `local-advisor`.
- Every call, including fallbacks, still lands in `audit.llm_call` (R6.03).
- Measure overspend at the boundary (≤ one call's cost).
- Check UI badge, spend endpoint, Grafana alerts, `audit.llm_call.fallback_used`.

## ToDo

- [ ] Test plan + fake provider in compose test profile.
- [ ] Run all scenarios; capture evidence (screenshots, query outputs).
- [ ] Record results in the progress log.

## Verification

### Tests
- Integration suite `tests/integration/test_llm_budgets.py`.

### Scenarios
- Given `debate` exhausted, then the next debate call uses `local-advisor` and D09 shows the local badge.
- Given MTD over cap, then all roles fall back; given local also down, then calls fail with `budget_exhausted_no_local` and alert.
- Given a budget raise via C1, then rejected; via C3, applied after cool-down.

### Stress / failure injection
- Provider returns 50% 5xx: fallback chain research-primary → research-custom → local-advisor works; error rate panel shows it.
- Provider latency 30 s: timeouts trigger fallback, agents degrade but don't hang.

## Acceptance criteria

- [ ] All scenarios pass with evidence.
- [ ] Overspend bound documented.

## Exceptions & edge cases

- Real provider spend during tests must be zero (fake provider only).

## Cardinal rules (do NOT)

- Do NOT run budget tests against the real paid provider.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: verified behaviour.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.70 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T053-verify-llm-budget-fallback`
- PR title: `P6-T053: Verify LLM budgets, monthly cap and local fallback (budget test)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (maps to new T6.70 (+R6.03); 16 §2.10 defaults under test; keyless (no P6-T001 dependency, live check P6-T070); run fields)
