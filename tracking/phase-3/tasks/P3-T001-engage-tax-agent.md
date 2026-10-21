---
id: P3-T001
kind: task
title: Engage a registered tax agent and send the question list
phase: 3
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R3.07]
roadmap_todos: [T3.01]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T001-engage-tax-agent
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T001 · Engage a registered tax agent and send the question list

## Goal / expected outcome

A registered Australian tax agent is engaged in writing and has received the seven 09 questions, with **investor vs trader-in-business** flagged as the one that must be answered **before any live trade (P7 entry)**. This satisfies exit criterion 3 ("the agent is engaged") together with P3-T038 (questions logged).

## Context & references

- Roadmap: [R3.07, T3.01](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 3
- Question list: [09 Questions for your tax agent](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks) · [12 §6 professional advice triggers](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15)
- Why it matters: [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (a high-volume autonomous system may be "carrying on a business")
- P7 entry criterion needs the answer: [P7 T7.01](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Related: P3-T038 (questions stored as `TAX_QUESTION` tasks), P3-T002 (2027 reform follow-up), P3-T025 (regime switch records the answer)

## Requirements

- Agent must be a **registered tax agent** (check the Tax Practitioners Board public register) with crypto + CFD/derivatives experience.
- Send all 7 questions from 09: (1) carrying on a business? (2) futures treatment (3) exact 2027 transitional mechanism incl. crypto (4) Div 775 thresholds/elections for broker cash (5) DTAs AU-UAE/CY/EG (6) Egypt stamp duty; Cyprus Art. 20E status vs non-dom (7) AU CARF start date.
- Ask for a **written** answer to Q1 with a target date at least 4 weeks before the planned P7 start (indicatively before May 2027).
- No TFN, statements or personal identifiers go into git, chat or issues; the engagement letter lives outside the repo (or as an encrypted attachment per 07 §8).

## ToDo

- [ ] Shortlist 2–3 agents; confirm each on the TPB register; note fee quotes (outside the repo)
- [ ] Sign the engagement letter; store it in your personal records (not git)
- [ ] Email the 7 questions (copy them from 09 or export from D15 Questions once P3-T038 lands); state Q1 is blocking for live trading
- [ ] Record in this file's progress log: agent firm name (no personal IDs), engagement date, promised answer date for Q1
- [ ] Mark each `TAX_QUESTION` task as `sent` in D15 Questions (or via `task.done` once P3-T038 is live)
- [ ] Diary a follow-up 2 weeks after sending

## Verification

### Tests

- n/a (USER action); confirmation is the progress-log entry plus the `TAX_QUESTION` tasks showing status `sent`

### Scenarios

- Given the agent is engaged, when D15 Questions is opened, then all 7 questions show status `sent` with the send date.
- Given no written Q1 answer by the P7 planning date, when P7 entry is checked, then P7 stays blocked (T7.01) and the engine keeps reporting both regimes (P3-T025).

### Stress / failure injection

- n/a: human engagement step

## Acceptance criteria

- [ ] Engagement confirmed in writing; progress log names the firm and the date
- [ ] All 7 questions sent; Q1 explicitly marked as needed before any live trade
- [ ] Promised answer date for Q1 recorded

## Exceptions & edge cases

- Agent declines crypto/derivatives work → engage another; do not proceed to P7 without an answer.
- Agent answers "depends on facts" → capture the facts they need as new `TAX_QUESTION` tasks; regime stays `both`.
- Not tax advice: the engine's figures are inputs for the agent, never a substitute.

## Cardinal rules (do NOT)

- Do NOT put a TFN, address, engagement letter or statements in git, issues or chat.
- Do NOT set a regime in D15 from your own judgement; only from the agent's written answer (P3-T025).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/roadmap/README.md` §6 USER register: no change (generated block) — the main agent refreshes it on build.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.01 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T001-engage-tax-agent` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T001: Engage a registered tax agent and send the question list`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
