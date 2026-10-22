---
id: P6-T030
kind: task
title: Model promotion gates, rollback and the veto threshold
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T029]
requirements: [R6.14, R6.12]
roadmap_todos: [T6.27]
modules: [M21, M7]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, mlflow, nats, decision-svc]
branch: p6/P6-T030-model-promotion-gates-veto
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T030 · Model promotion gates, rollback and the veto threshold

## Goal / expected outcome

Models move candidate → shadow → production only through `models.promote` with automated gates (calibration, out-of-sample worst fold vs a frozen baseline, latency SLO, flip rate, provenance), C2 normally and **C3** when the model is used by `autonomous` bots (02 §7.2); `models.rollback` (C1) restores the previous production model instantly.

## Context & references

- Roadmap: [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.27
- Spec: [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) (promoted only through §8 gates, teacher in shadow) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (veto above calibrated threshold)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Actions (promote C2/C3, rollback C1; promotion impossible without gates)
- Roadmap risk: worst-fold promotion vs a frozen baseline
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) ([17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) P6-B015)
- Depends on (this phase): P6-T029

## Requirements

- Gate checks (defaults from 16 §2.10, read from settings): coverage at ≥ 0.75 precision, ECE ≤ 0.05, Brier ≤ baseline, worst walk-forward fold not worse than the frozen baseline (current production or SemIf), latency p95 within SLO (< 50 ms GPU), flip rate ≤ 0.1%, dataset provenance clean, calibration report present, post-cutoff rule (P6-T017) for LLM-derived labels.
- Shadow stage: default ≥ 14 days in shadow (scored, never acting) meeting the thresholds above before production (16 §2.10); the teacher stays in shadow after promotion.
- Veto enablement is a separate gated flag per question requiring precision ≥ the veto target (default 0.90, 16 §2.10) on holdout and in shadow.
- `models.promote` / `models.rollback` audited; registry status history kept (append-only).
- Tier-A candidates from distillation use the same command with P2's tier-A gate set.

## ToDo

- [ ] Gate runner `mt_models.gates`.
- [ ] Commands with level logic (C2 / C3 if any consumer bot is `autonomous`).
- [ ] Registry status history table.
- [ ] Rollback path (KV routing switch < 5 s).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each gate pass/fail; level selection C2 vs C3.
- Integration: promote → decision-svc routes to new model; rollback → previous within 5 s.

### Scenarios
- Given a candidate with better accuracy but worse worst-fold Brier than the frozen baseline, then promotion is refused with the reason shown.
- Given a model used by an `autonomous` bot, then promotion requires C3.
- Given a bad production model, then `models.rollback` restores the previous one and audits it.

### Stress / failure injection
- Rollback under load (1,000 decisions/s): no failed decisions during the switch.

## Acceptance criteria

- [ ] Promotion impossible without passing gates (API test).
- [ ] Rollback < 5 s.
- [ ] Teacher remains in shadow after promotion (shadow sampler still active).

## Exceptions & edge cases

- Baseline missing (first ever model) → baseline = SemIf stage-1 metrics.

## Cardinal rules (do NOT)

- Do NOT add a gate bypass flag.
- Do NOT promote on accuracy alone.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: gate defaults.
- `docs/03-build-spec.md` M21: promotion levels.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.27 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T030-model-promotion-gates-veto`
- PR title: `P6-T030: Model promotion gates, rollback and the veto threshold`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (16 §2.10 gate defaults incl. ≥ 14 days shadow and veto 0.90; C3 for models used by autonomous bots (02 §7.2, 17 §B modes); run fields)
