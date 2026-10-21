---
id: P7-T001
kind: task
title: Record the tax agent's investor-vs-trader decision in D15
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.13]
roadmap_todos: [T7.01]
modules: [M18]
dashboards: [D15, D13]
branch: p7/P7-T001-tax-agent-regime-decision
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T001 · Record the tax agent's investor-vs-trader decision in D15

## Goal / expected outcome

Your tax agent's written answer on **investor vs trader-in-business** is stored, and the FY regime in D15 is set from it, before any live trade. This is a Phase 7 entry criterion and is checked by the go-live preflight (P7-T011).

## Context & references

- Roadmap: [R7.13 · ToDo T7.01](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) (tax agent: investor vs trader, before any live trade) · [09 tax-agent questions](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks) · [D15](../../../docs/ui/dashboards/D15-tax.md) Questions tab (`tax.regime.set`)
- Cross-phase: P3 T3.01 (agent engaged, question list sent) and T3.02 (2027 CGT reform status) must be done; this item only records the answer.
- Related: P7-T011 (preflight reads `journal.residency`/regime per FY), P7-T010 (advice register)

## Requirements

- Functional: the regime for the current FY (and FY2027-28 if the agent answered) is set to `investor`, `trader_in_business` or `both` per activity, via `tax.regime.set` in D15.
- Functional: the agent's written answer (letter/email PDF) is attached to the `TAX_QUESTION` task as a file reference stored in the encrypted document store, not in git.
- Non-functional: TFN and personal details stay column-encrypted (`pgcrypto`) and out of LLM prompts (07 §8).
- Unblocks: P7-T011 preflight, P7-T057 funding.

## ToDo

- [ ] Get the written answer from your tax agent (email or letter) on investor vs trader-in-business for each activity (spot crypto, CFDs/FX, perps).
- [ ] Open D15 → Questions → the `TAX_QUESTION` 'investor vs trader-in-business' task; paste a one-paragraph summary (no TFN) and attach the PDF via the upload control.
- [ ] In D15 → FY selector, choose the current FY and run `tax.regime.set` per activity as advised; confirm the regime badge changes.
- [ ] If the agent also answered the 2027 CGT reform question (T3.02), record it on that task too.
- [ ] Mark the task Done in D13/Telegram; tell the agent (planner) the task is complete so P7-T011 can re-run.

## Verification

### Tests
- Unit/integration: n/a (user action); P7-T011 preflight includes a check `tax_regime_set(fy)` that this satisfies.

### Scenarios
- Given the regime is unset when preflight runs, then the 'tax agent answered' entry criterion shows ✖ and funding stays blocked.
- Given you set `trader_in_business` for perps only, when D15 recomputes, then the summary shows perps as revenue and spot as CGT.

### Stress / failure injection
- n/a: one-off user decision.

## Acceptance criteria

- [ ] D15 shows a regime badge for the current FY (not 'undecided').
- [ ] The `TAX_QUESTION` task is Done with the agent's answer attached (file reference only).
- [ ] `/system/preflight` (P7-T011) reports the tax criterion as passed.

## Exceptions & edge cases

- Agent says 'cannot decide until activity is known': set `both` (engine reports both ways), record the deferral and the date to revisit; preflight treats an explicit, dated deferral as **not** passed for live trading.
- Residency change mid-FY: set the regime per residency period (09).

## Cardinal rules (do NOT)

- Do NOT paste the TFN, the agent's letter or personal details into chats, issues or git.
- Do NOT go live while the regime is undecided.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/09-journal-and-tax.md`: note the decided regime as configuration, not advice (one line, no personal data).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.01 when this item is done.

## Branch & PR

- Branch: `p7/P7-T001-tax-agent-regime-decision`
- PR title: `P7-T001: Record the tax agent's investor-vs-trader decision in D15`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T001` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
