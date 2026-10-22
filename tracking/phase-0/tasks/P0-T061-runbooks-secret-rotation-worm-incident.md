---
id: P0-T061
kind: task
title: Write runbooks: secret rotation, WORM incident and worm_owner ceremony
phase: 0
type: DOC
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T022, P0-T038]
requirements: [R0.N1, R0.07, R0.12]
roadmap_todos: [T0.90]
modules: [ops, M17]
dashboards: []
tools: [sops, age, docker]
mcp: []
env: []
services: []
branch: p0/P0-T061-runbooks-secret-rotation-worm-incident
pr: ""
doc_sync: [docs/runbooks/README.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T061 · Write runbooks: secret rotation, WORM incident and worm_owner ceremony

## Goal / expected outcome

`docs/runbooks/secret-rotation.md`, `docs/runbooks/worm-incident.md` and `docs/runbooks/worm-owner-ceremony.md` cover rotating every secret class (90-day venue keys, LLM keys, bot tokens, DB passwords, age identities), responding to an `audit.verify` mismatch, and running WORM migrations with the offline credential.

## Context & references

- [Roadmap P0 T0.90](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets) (rotation every 90 days)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- [15 §2.3 threat coverage](../../../docs/15-bots-hitl-and-worm-audit.md#23-what-this-protects-against)
- Inputs: P0-T022, P0-T038; the ceremony runbook is then used by P0-T013 (USER)
- Depends on: P0-T022, P0-T038

## Requirements

- Secret rotation: per class (exchange/broker keys every 90 days by default and immediately after a suspected leak, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl), 07 §2) — where it's issued, how to rotate with zero downtime (dual-key where supported), `sops` edit, `mt-secrets.service` reload, container restart order, verify, update `created` date; age identity rotation (`sops updatekeys`); quarterly drill entry.
- WORM incident: triage (which table/seq/day), preserve evidence (export the affected range + anchors to a new locked prefix), keep the integrity response in force (default `block_new_entries`: no new entries, exits continue, no loosening; [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)), compare with monthly export and restored backup, root-cause (bug vs tamper), corrections as **new rows** only, then `audit.integrity.ack` via C3 (break-glass `mtctl approve` + TOTP until Telegram C3 in P2), post-incident note.
- worm_owner ceremony: prerequisites, plug-in, `sops exec-env` command, migration, unplug, verify `pg_stat_activity` has no lingering `worm_owner` session, audit note.
- Each runbook dry-run once (scratch environment).

## ToDo

- [ ] Write the three runbooks; link from the index.
- [ ] Dry-run each on scratch; record dates.
- [ ] Cross-link from 15 §2.2.

## Verification

### Tests
- Dry runs: rotate the Grafana admin password and the LiteLLM master key on the host following the text; simulate a WORM mismatch on scratch and follow the incident runbook to `audit.integrity.ack`.

### Scenarios
- Given a venue key leaks (P2+), then the rotation runbook plus the P2 'keys leaked' runbook cover revoke → rotate → verify withdrawals.

### Stress / failure injection
- n/a: documentation; dry runs are the test.

## Acceptance criteria

- [ ] Three runbooks in standard format, dry-run once each
- [ ] Linked from index and 15 §2.2

## Exceptions & edge cases

- Rotation during market hours (later phases): the runbook says which keys need trading paused first.

## Cardinal rules (do NOT)

- Do NOT describe any procedure that UPDATEs or DELETEs WORM rows.
- Do NOT include secret values.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/runbooks/README.md`: add the three runbooks; `docs/15-bots-hitl-and-worm-audit.md` §2.2: link the ceremony and incident runbooks.
- `docs/roadmap/phase-0-foundations.md`: tick T0.90 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T061-runbooks-secret-rotation-worm-incident`
- PR title: `P0-T061: Write runbooks: secret rotation, WORM incident and worm_owner ceremony`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (incident runbook ends with audit.integrity.ack (16 §2.11, 17 §A P0-B001) instead of risk.halt.clear; no longer waits on P0-T013 (P0-T013 uses this runbook); rotation default 90 d; run fields added)
