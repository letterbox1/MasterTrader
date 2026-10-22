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
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T027-recon-ageing-24h-halt
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T027 · Recon break ageing: unexplained > 24 h halts everything

## Goal / expected outcome

Any reconciliation mismatch left unexplained for 24 hours triggers a system-wide kill criterion: every live sleeve halts (kill switch ON, cancel all, optional flatten per config) until the break is resolved and a C3 restart is approved.

## Context & references

- Roadmap: [R7.06, R7.09 · ToDo T7.21, T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (any reconciliation mismatch unexplained within 24 h halts everything) · [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation) (explained = matched to a known journal event within 24 h) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6 (kill switch)
- Related: P7-T025, P7-T020 (framework), P7-T048, P7-T050

## Requirements

- System-scope `KillCriterion` reading `audit.recon` unexplained breaks with `first_seen_at`.
- Warn at 12 h (Telegram + ntfy; an alert-only setting, proposed for 16 §2.9), breach at 24 h (16 §2.9 default): kill ON with reason `recon_unexplained_24h` (stops new trading, cancels orders, applies each bot's `on_system_failure`, freezes treasury/earn moves; [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)), capital states → halted.
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
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §2.9: add the 12 h warning as a default (alert only).
- `docs/14-strategy-evidence-and-validation.md` §7: link the criterion.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21, T7.23 when this item is done.

## Branch & PR

- Branch: `p7/P7-T027-recon-ageing-24h-halt`
- PR title: `P7-T027: Recon break ageing: unexplained > 24 h halts everything`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (24 h explained rule per 16 §2.9; kill actions per 17 §B; 12 h warn proposed for 16 §2.9)
