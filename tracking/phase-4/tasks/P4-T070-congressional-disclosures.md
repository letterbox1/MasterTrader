---
id: P4-T070
kind: task
title: "Congressional trading disclosures connector (House Clerk PTRs)"
phase: 4
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P1-T009]
requirements: [R4.17]
roadmap_todos: [T4.33]
modules: [M2, M3]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T070-congressional-disclosures
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
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

# P4-T070 · Congressional trading disclosures connector (House Clerk PTRs)

## Goal / expected outcome

`mt_data.text.congress` polls the House Clerk's financial-disclosure index for periodic transaction reports (PTRs), parses each filing (member, asset/ticker, transaction type, amount range, transaction date, filing date) and publishes them as events linked to instruments. The Senate eFD is added only if its terms allow automated personal access (U). Idea from day-trader-skill (MIT).

## Context & references

- Roadmap: [R4.17 / T4.33](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Source framework: P4-T010; instrument master: P1-T009
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Official sources only: House Clerk disclosure index and filings; polite polling (default every 6 h, configurable) with a declared User-Agent and back-off.
- Keep both dates: transaction date and filing date (filings may lag trades by up to 45 days); events are timestamped at the **filing** date for point-in-time use.
- Provenance tags on every row (`source = house_clerk`, licence/terms note, `model_input_ok = true`, `train_ok = false`).
- Map assets to instruments where possible; unmapped assets stored unlinked.
- Senate eFD: an agent checks its terms (U) first; build only if automated personal access is allowed.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P4-T070` checks them before start.

## ToDo

- [ ] Check the House Clerk and Senate eFD terms and record them (U)
- [ ] House Clerk index poller + filing parser (PDF/XML)
- [ ] Instrument mapping + event publishing with provenance
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: golden files from 5 real PTR filings parse to the expected rows.
- Unit: event `as_of` equals filing date, not transaction date.
- Integration: re-polling the same index creates no duplicate events.

### Scenarios
- Given an amended filing, then a new event row with `supersedes` is written.

### Stress / failure injection
- Backfill of a year of filings: rate limit and back-off hold; no duplicates.

## Acceptance criteria

- [ ] Golden-file tests pass
- [ ] Events carry filing-date timestamps and provenance
- [ ] CI green (ruff, mypy, `uv run pytest`, `pit` bypass check)

## Exceptions & edge cases

- Scanned PDFs that don't parse: store with `parse_status = failed` and alert once per day, never guess values.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 (`mt-risk`) via `mt-api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).
- Do NOT treat a disclosure as a trade trigger on its own; it's delayed context.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 add the congressional disclosures source row
- `docs/roadmap/phase-4-intel.md`: tick T4.33

## Branch & PR

- Branch: `p4/P4-T070-congressional-disclosures`
- PR title: `P4-T070: Congressional trading disclosures connector (House Clerk PTRs)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T070` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (CI commands per 18 (cargo/uv/supabase/pnpm))
