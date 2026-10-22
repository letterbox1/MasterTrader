---
id: P7-B010
kind: gap
title: Windows VPS for the MT5 bridge is outside the security model
phase: 7
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.10]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B010-windows-vps-not-in-security-model
pr: ""
doc_sync: [docs/07-security-notes.md]
doc_sync_status: done
found_in: docs/07-security-notes.md §1, §2, §5 (single Linux host, Tailscale-only, sops); docs/14-strategy-evidence-and-validation.md §8 (MT5 on a Windows VPS)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P7-B010 · Windows VPS for the MT5 bridge is outside the security model

## Goal / expected outcome

The docs agree and are specific enough to implement: add a '5.1 Optional Windows VPS (MT5 bridge)' subsection to 07 using P7-T035's requirements.

## Context & references

- Found in: `docs/07-security-notes.md §1, §2, §5 (single Linux host, Tailscale-only, sops); docs/14-strategy-evidence-and-validation.md §8 (MT5 on a Windows VPS)`
- Related: P7-T005, P7-T034, P7-T035

## Requirements

- **What:** The MT5 route adds a second host (Windows, third-party VPS) holding broker session credentials, not covered by 07.
- **Expected:** 07 covers the VPS: Tailscale-only, inbound deny-all, credential storage (DPAPI + sops source of truth), patch window, logging to Loki, rebuild procedure, egress IP for allow-lists.
- **Actual:** 07 assumes one host; nothing on VPS hardening or where the MT5 login lives.
- **Impact:** Implementers (P7-T005/T034/T035) have no security baseline to verify against. (severity S3)
- **Suggested fix:** Add a '5.1 Optional Windows VPS (MT5 bridge)' subsection to 07 using P7-T035's requirements.

## ToDo

- [x] Decision recorded in docs/17 (17 §D P7-B010): the MT5 Windows VPS is hardened, Tailscale-only, holds only the MT5 trade-only login and no other secrets
- [x] Owning docs carry it: 07 §5.1; 14 §8 item 2; roadmap R7.10/T7.43
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T005, P7-T035
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (07 §5.1; 14 §8 item 2; roadmap R7.10/T7.43)
- [x] Affected tasks consistent with it (P7-T005, P7-T035)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/07-security-notes.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B010-windows-vps-not-in-security-model`
- PR title: `P7-B010: fix windows VPS for the MT5 bridge is outside the security model`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §D P7-B010: the MT5 Windows VPS is hardened, Tailscale-only, holds only the MT5 trade-only login and no other secrets. Docs now carry it: 07 §5.1; 14 §8 item 2; roadmap R7.10/T7.43. Implementation owned by P7-T005, P7-T035. Root cause: 07 assumed a single Linux host.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P7-B010); docs updated: 07 §5.1; 14 §8 item 2; roadmap R7.10/T7.43; implementation owned by P7-T005, P7-T035
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
