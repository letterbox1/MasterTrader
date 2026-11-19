---
id: P4-T071
kind: task
title: "Verify congressional disclosures: golden files, dates, no duplicates"
phase: 4
type: VERIFY
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T070]
requirements: [R4.17]
roadmap_todos: [T4.68]
modules: [M2]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T071-verify-congressional-disclosures
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T071 · Verify congressional disclosures: golden files, dates, no duplicates

## Goal / expected outcome

Evidence that congressional disclosures parse correctly on real filings, keep both transaction and filing dates, and never duplicate on re-poll.

## Context & references

- Roadmap: [R4.17 / T4.68](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Builds on P4-T070
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Run the golden-file, date and re-poll tests on the current month's filings.
- Spot-check three events in D08 against the source filings.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P4-T071` checks them before start.

## ToDo

- [ ] Run golden-file and date tests
- [ ] Run the re-poll duplicate test
- [ ] Spot-check three events against source filings
- [ ] Record results in the progress log

## Verification

### Tests
- Golden files on the latest filings.
- Re-poll twice: event count unchanged.

### Scenarios
- Given a filing for an asset not in the instrument master, then it appears unlinked in D08 and links after the master updates.

### Stress / failure injection
- n/a: covered by P4-T070's backfill test

## Acceptance criteria

- [ ] All checks pass
- [ ] Evidence linked in the progress log

## Exceptions & edge cases

- No filings in the test window: use the previous month's filings and note it.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt_api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.68

## Branch & PR

- Branch: `p4/P4-T071-verify-congressional-disclosures`
- PR title: `P4-T071: Verify congressional disclosures: golden files, dates, no duplicates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T071` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
