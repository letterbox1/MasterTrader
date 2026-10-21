---
id: P7-T027
kind: task
title: Recon break ageing: unexplained > 24 h halts everything
phase: 7
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T025, P7-T020]
requirements: [R7.06, R7.09]
roadmap_todos: [T7.21, T7.23]
modules: [M11, M16]
dashboards: [D06, D07]
branch: p7/P7-T027-recon-ageing-24h-halt
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T027 · Recon break ageing: unexplained > 24 h halts everything

## Goal / expected outcome

Any reconciliation mismatch left unexplained for 24 hours triggers a system-wide kill criterion: every live sleeve halts (kill switch ON, cancel all, optional flatten per config) until the break is resolved and a C3 restart is approved.

## Context & references

- Roadmap: [R7.06, R7.09 · ToDo T7.21, T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (any reconciliation mismatch unexplained within 24 h halts everything) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6 (kill switch)
- Related: P7-T025, P7-T020 (framework), P7-T048, P7-T050

## Requirements

- System-scope `KillCriterion` reading `audit.recon` unexplained breaks with `first_seen_at`.
- Warn at 12 h (Telegram + ntfy), breach at 24 h: kill ON with reason `recon_unexplained_24h`, capital states → halted.
- Turning kill OFF is C3 and requires zero unexplained breaks (F6: trigger condition cleared).
- Ageing survives restarts (computed from stored `first_seen_at`).

## ToDo

- [ ] Criterion implementation + warn/breach alerts.
- [ ] Kill-off precondition check.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: 11:59 (ok), 12:00 (warn), 24:00 (breach) with an injected clock.
- Integration: breach sets kill ON; kill OFF refused while the break is unresolved; allowed (C3) after resolution.

### Scenarios
- Given a balance break on Independent Reserve unexplained for 24 h, then every sleeve on every venue halts, not just that venue's.

### Stress / failure injection
- Monitor restart at hour 23: breach still fires at 24 h.

## Acceptance criteria

- [ ] 24 h unexplained break halts everything; kill OFF gated on resolution.
- [ ] CI green.

## Exceptions & edge cases

- Break explained after 23 h: no breach; the event is still logged.
- Venue outage making recon impossible for 24 h: treated as unexplained (fail closed).

## Cardinal rules (do NOT)

- Do NOT make the 24 h window per-venue or longer.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: 12 h warn added.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21, T7.23 when this item is done.

## Branch & PR

- Branch: `p7/P7-T027-recon-ageing-24h-halt`
- PR title: `P7-T027: Recon break ageing: unexplained > 24 h halts everything`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
