---
id: P0-T052
kind: task
title: Build D16 System: Audit, Security and Settings pages
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T050, P0-T046, P0-T038]
requirements: [R0.11, R0.07]
roadmap_todos: [T0.26]
modules: [M15, M17]
dashboards: [D16]
branch: p0/P0-T052-d16-audit-security-settings
pr: ""
doc_sync: [docs/ui/dashboards/D16-system.md, docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T052 · Build D16 System: Audit, Security and Settings pages

## Goal / expected outcome

`/system/audit` lists commands and other audit rows with source, args (redacted), result, hash and chain-verification status, with filters, export and a 'Verify now' action (`audit.verify`); `/system/security` shows key metadata (never values), sessions/TOTP status and the posture checklist; `/system/settings` edits preferences/notifications/budgets with the right confirmation levels. A chain failure raises a critical banner.

## Context & references

- [Roadmap P0 R0.11, R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (Audit, Settings, Security)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)
- [components §4 forms](../../../docs/ui/components.md#4-forms--controls)
- D16 routes `/system/security` and `/system/backups` are missing from ui §1 IA: P0-B014.
- Depends on: P0-T050, P0-T046, P0-T038

## Requirements

- Audit table columns: time, source (web/telegram/mcp/system), command, level, args (redacted), status, hash (short, copyable), chain status (✓ verified up to last run / ✗ mismatch / … pending); filters source, command, date; CSV export of the visible page (C0).
- 'Verify now' → `audit.verify` (C1) → progress via WS → result toast; mismatch → critical red banner (D16 acceptance 3) persisting until resolved.
- Security: key metadata table (service, name, age, rotate due) from `/system/keys`; sessions (current + others, logout others); TOTP status; posture checklist fed by `infra/host/checklist.sh` results + last scan date (P0-T056).
- Settings: Preferences (theme, density, timezone default Australia/Sydney, base currency AUD, number formats) as C0; Notifications/Budgets edits via `system.settings.update` with server-classified level — raising budgets = C3 via `C3Flow`; Integrations list with status (Telegram bot, LiteLLM, TEI, backups) and 'test' buttons that call read-only health checks.
- Licence & data tags section lists `ops.data_source` with licence/cost; paid sources can't be enabled (button disabled with reason).

## ToDo

- [ ] Build Audit, Security, Settings routes.
- [ ] Wire `audit.verify`, `system.settings.update` (with classify → C0/C1/C3).
- [ ] Vitest tests; Playwright flows.

## Verification

### Tests
- Unit: chain status rendering for ok/mismatch/pending; args never show redacted secrets.
- Integration: raising an LLM budget shows `C3Flow` and does not apply until approval + TOTP + cool-down (with SimClock on server).

### Scenarios
- Given verify finds a mismatch, then the critical banner shows on every route and D16 Audit highlights the first bad row.
- Given the user lowers a budget, then it applies immediately (tighten = C1) and is audited.

### Stress / failure injection
- Audit table with 100k rows paginated + virtualised remains responsive (logged).

## Acceptance criteria

- [ ] Audit/Security/Settings pages implemented per D16
- [ ] Chain failure banner works
- [ ] C3 for loosening settings enforced end to end
- [ ] No secret values rendered (tested)
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Telegram/MCP tokens section shows 'Arrives in Phase 2/8' empty state.

## Cardinal rules (do NOT)

- Do NOT render key values, even masked partially.
- Do NOT let the UI decide confirmation levels; it reads them from the preview response.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/ui/dashboards/D16-system.md`: tick Audit/Security/Settings widgets live in P0; `docs/ui/README.md` §1: add `/system/security` and `/system/backups` routes.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T052-d16-audit-security-settings`
- PR title: `P0-T052: Build D16 System: Audit, Security and Settings pages`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
