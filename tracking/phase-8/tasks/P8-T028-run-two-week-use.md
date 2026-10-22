---
id: P8-T028
kind: task
title: Two weeks of MCP use, then review the D17 audit
phase: 8
type: RUN
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T018, P8-T019, P8-T020, P8-T021, P8-T022, P8-T023, P8-T024, P8-T025, P8-T026, P8-T027, P8-T033, P8-T034, P8-T035]
requirements: [R8.04, R8.07]
roadmap_todos: [T8.80]
modules: [M20]
dashboards: [D17]
tools: [uv, git]
mcp: []
env: []
services: [postgres, tailscale, telegram-bot]
branch: p8/P8-T028-run-two-week-use
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T028 · Two weeks of MCP use, then review the D17 audit

## Goal / expected outcome

You use MasterTrader through Claude for 14 consecutive days (paper/practice, or micro-live only if P7 has already opened it and you choose so). Reviews at day 7 and day 14 of `audit.mcp_call` find nothing surprising, or every surprise is filed as a P8 bug and resolved.

## Context & references

- Roadmap: ToDo [T8.80](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) · [R8.04, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements)
- UI: [D17 Session activity](../../../docs/ui/dashboards/D17-mcp-console.md)
- Related: P8-T017 (incident runbook if anything goes wrong).

## Requirements

- Clock: start date logged; 14 consecutive days; at least one MCP session per day (gaps noted).
- Day-7 and day-14 review (agent prepares, you sign off): calls per tool and group (reads included, from `audit.mcp_call`); denied/never attempts; rate-limited and capped calls; approvals approved/rejected/expired and median approval latency against the 5-min TTL; any calls you don't recognise; injection-like reasons; tools never used (candidates to disable); token expiry status and any indefinite tokens.
- Invariants for the whole window: zero MCP orders executed without your approval; zero successful never-exposed calls (incl. `approval.*`, `mcp.*`); zero loosening applied without C3; daily `audit.verify` green.
- Each surprise → a `P8-Bnnn` bug with session id and severity.

## ToDo

- [ ] Log the start date in the Progress log.
- [ ] Day 7: generate the review from `/audit/log?source=mcp` and `/mcp/sessions`; you sign it off.
- [ ] Day 14: same; confirm the invariants.
- [ ] File and triage bugs for anything surprising.
- [ ] Disable tools you never used (C1) if you agree.

## Verification

### Tests
- Invariant queries (SQL against `audit.mcp_call` / `audit.command` / `risk.approval`) run daily and saved with each review.

### Scenarios
- Given a call at 03:00 that you didn't make, when the review finds it, then follow the incident runbook and file an S1/S2 bug.

### Stress / failure injection
- n/a: observation window.

## Acceptance criteria

- [ ] 14 days completed with two signed reviews
- [ ] Invariants held for the whole window
- [ ] All surprises filed; no open S1/S2 from the window

## Exceptions & edge cases

- A serious incident resets the clock after the fix (log the reason).
- Travel without Tailscale: missed days are noted, not faked.

## Cardinal rules (do NOT)

- Do NOT loosen MCP policy, widen token scopes or add indefinite tokens during the window to "try it out"; such changes restart the clock.
- Do NOT treat an expired approval as a failure to fix by lengthening the TTL without your decision (it's a 16 §2.3 setting).
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.80 with the dates and review links.

## Branch & PR

- Branch: `p8/P8-T028-run-two-week-use`
- PR title: `P8-T028: Two weeks of MCP use, then review the D17 audit`
- PR checklist: review notes committed (no secrets) · bugs filed · `./kanban done P8-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (auto-rule exception removed (no skip-approval), invariants incl. `approval.*`/`mcp.*` and C3 loosening, reads from `audit.mcp_call`, indefinite-token check, TTL is a setting; deps P8-T033/T034/T035; tools/env/services)
