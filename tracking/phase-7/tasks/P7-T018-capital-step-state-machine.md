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
depends_on: [P7-T017, P2-T010]
requirements: [R7.05]
roadmap_todos: [T7.21]
modules: [M11]
dashboards: [D06, D03]
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T018-capital-step-state-machine
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T018 · Capital-step state machine and clean-week evaluator

## Goal / expected outcome

Each live bot (rolled up per sleeve) has a persisted capital state (`paper → micro_live` at its starting allocation `→ step_1 … step_n → target_cap`, plus `halted`, `review_30d`, `retired`) driven by evidence: a step becomes **eligible** only after 4 consecutive clean weeks, steps go down automatically on warnings and halts, and the evaluator records why each week was or was not clean ([16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)).

## Context & references

- Roadmap: [R7.05 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (capital steps, clean week) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) (starting allocation per bot, default A$2,000; clean week; +25% of current; step-down) · [17 §A P7-B003](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (L0 ceilings in the bot strategy settings) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 6 · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Related: P7-T019 (proposal + C3 approval), P7-T016 (review sign-off, shown as a warning), P7-T020/T022/T027 (kill inputs), gap P7-B003 (resolved: 16 §2.5) · cross-phase P2-T010 (layered policy store, `depends_on`)

## Requirements

- States and transitions (WORM log `risk.capital_step`): paper → micro_live at the bot's **starting allocation** (an L4 strategy setting set when the bot goes live; default A$2,000, suggested A$2–5k) on funding (P7-T057, `risk.capital.fund` C3); step_k → step_k+1 (+25% of the **current** allocation, A → 1.25A, up to the sleeve's target cap) on C3 approval only; a **kill-criterion warning** → back one step (automatic, a tightening); a **halt** (kill criterion, health check, sleeve halt) → `halted`, and after your review the restart (`risk.sleeve.restart`, C3) resumes at the **starting allocation**; system drawdown stage 2 → `review_30d` (P7-T022); → `retired` when two stage-2 events end the programme or you retire the bot (e.g. at the recurring 12-month review).
- Clean week (16 §2.5 default; a calendar week Mon–Sun, Sydney): no kill-criterion breach; no unexplained reconciliation mismatch; no S1/S2 incident on that bot; live implementation shortfall ≤ 1.5× modelled; weekly P&L inside the backtest's 5th–95th percentile band (P7-T017). A decay downgrade also makes the week not clean (14 §6). Extra conditions (e.g. a signed weekly review) are optional tightenings (C1).
- Step size: +25% of the **current** allocation per step (16 §2.5 default), capped by the sleeve's target cap (a sleeve setting, e.g. A$10–25k for P1) and the L0 hard ceilings in the bot strategy settings (17 §E). All values are settings: tighten C1, loosen C3.
- Any non-clean week resets the 4-week counter to 0.
- Evaluator runs Monday 08:00 Australia/Sydney after the review pack; publishes `risk.capital.status` on NATS and `risk.event`.

## ToDo

- [ ] `packages/mt_risk/capital_steps/` (state machine, evaluator, policy model).
- [ ] Migration `risk.capital_step` (WORM); capital-step settings (starting allocation per bot, step %, clean weeks needed, target cap) as L3/L4 settings in the layered policy (P2-T010; tighten C1, loosen C3).
- [ ] Clean-week input adapters (kill criteria, recon, S1/S2 incidents, shortfall, P&L band, decay downgrade) and step-down handlers (warning → back one step; halt → starting allocation after review).
- [ ] NATS subject `risk.capital.status`; `/risk/capital-steps` query.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: transition table exhaustive (illegal transitions rejected); counter resets on any dirty week.
- Property: capital never increases without an approval event; capital after n steps ≤ min(target cap, L0 ceiling); a warning steps back exactly one step; a halt + reviewed restart returns exactly the starting allocation.
- Golden: 8-week fixture with one dirty week in week 3 → eligible only after week 7.

### Scenarios
- Given 4 clean weeks, then the sleeve shows 'step eligible' and a proposal is created (P7-T019) — capital does not change yet.
- Given week 2's implementation shortfall was 1.7× modelled, then week 2 is dirty with reason 'shortfall 1.7× > 1.5×' and the counter is 0.
- Given a bot at step 2 (A$3,125 from a A$2,000 start) gets a kill-criterion warning, then it steps back to step 1 (A$2,500) immediately.
- Given a kill criterion fires, then state → halted, any pending proposal is cancelled, and after your review the C3 restart resumes at the starting allocation.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (clean week, +25% of current, step-down rules and per-bot starting allocation default A$2,000 per 16 §2.5/17 §A P7-B003; L0 ceilings in strategy settings per 17 §E; dep P2-T010)
