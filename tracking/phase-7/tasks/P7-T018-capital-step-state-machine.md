---
id: P7-T018
kind: task
title: Capital-step state machine and clean-week evaluator
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T017]
requirements: [R7.05]
roadmap_todos: [T7.21]
modules: [M11]
dashboards: [D06, D03]
branch: p7/P7-T018-capital-step-state-machine
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T018 · Capital-step state machine and clean-week evaluator

## Goal / expected outcome

Each sleeve has a persisted capital state (`paper → micro_live → step_1 … step_n → full`, plus `halted`, `review_30d`, `retired`) driven by evidence: a step becomes **eligible** only after 4 consecutive clean weeks, and the evaluator records why each week was or was not clean.

## Context & references

- Roadmap: [R7.05 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (micro-live A$2–5k; scale P1 + add P2 in 25% steps after 4 clean weeks each; up to A$10–25k) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 6 · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Related: P7-T019 (proposal + C3 approval), P7-T016 (review sign-off input), P7-T020/T022/T027 (kill inputs), gap P7-B003 (clean-week and 25% base undefined)

## Requirements

- States and transitions (WORM log `risk.capital_step`): paper → micro_live (on funding, P7-T057); micro_live/step_k → step_k+1 (on C3 approval only); any → halted (kill criterion); halted → review_30d (portfolio DD) or → previous state (after a reviewed restart, C3); any → retired (12-month review or two DD events).
- Clean week (default, configurable tighter): no kill-criterion breach; no unexplained recon break open > 24 h; no decay alert or health-check halt; DQ-paused time < 10% of the sleeve's trading hours; weekly review signed off; live P&L within the backtest's 5th–95th band for that horizon; zero risk-limit breaches (rejects are fine).
- Step size: +25% of the **current** sleeve capital per step (default, see P7-B003), capped by the sleeve's target (A$10–25k for P1) and the hard-ceilings file.
- Any non-clean week resets the 4-week counter to 0.
- Evaluator runs Monday 08:00 Australia/Sydney after the review pack; publishes `risk.capital.status` on NATS and `risk.event`.

## ToDo

- [ ] `packages/mt_risk/capital_steps/` (state machine, evaluator, policy model).
- [ ] Migration `risk.capital_step` (WORM) and `risk.capital_policy` (versioned policy; tighten C1, loosen C3).
- [ ] Clean-week input adapters (kill, recon, decay, DQ, review sign-off, P&L band).
- [ ] NATS subject `risk.capital.status`; `/risk/capital-steps` query.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: transition table exhaustive (illegal transitions rejected); counter resets on any dirty week.
- Property: capital never increases without an approval event; capital after n steps ≤ ceiling.
- Golden: 8-week fixture with one dirty week in week 3 → eligible only after week 7.

### Scenarios
- Given 4 clean weeks, then the sleeve shows 'step eligible' and a proposal is created (P7-T019) — capital does not change yet.
- Given week 2 had an unsigned review, then week 2 is dirty with reason 'review missing' and the counter is 0.
- Given a kill criterion fires, then state → halted and any pending proposal is cancelled.

### Stress / failure injection
- Replay 2 years of synthetic weekly inputs for 10 sleeves: deterministic results; DB failure mid-evaluation → no partial state (single transaction).

## Acceptance criteria

- [ ] State machine with WORM log and reasons per week.
- [ ] Clean-week definition implemented and configurable (tighten C1, loosen C3).
- [ ] No path increases capital without C3 (P7-T019).
- [ ] CI green.

## Exceptions & edge cases

- Week spans DST: weeks are Australia/Sydney calendar weeks.
- Sleeve with zero trades in a week: counts as clean only if the strategy's expected trade rate allows it (no trades expected) — else 'insufficient activity' (dirty).

## Cardinal rules (do NOT)

- Do NOT let the evaluator change capital directly; it only proposes.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: clean-week definition and step base.
- `docs/03-build-spec.md` M11: capital steps.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T018-capital-step-state-machine`
- PR title: `P7-T018: Capital-step state machine and clean-week evaluator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
