---
id: P0-T060
kind: task
title: Write runbooks: backup & restore, host rebuild
phase: 0
type: DOC
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T039, P0-T041, P0-T019]
requirements: [R0.N4, R0.N2]
roadmap_todos: [T0.90]
modules: [ops]
dashboards: []
branch: p0/P0-T060-runbooks-backup-restore-host-rebuild
pr: ""
doc_sync: [docs/runbooks/README.md, docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T060 · Write runbooks: backup & restore, host rebuild

## Goal / expected outcome

`docs/runbooks/backup-restore.md` and `docs/runbooks/host-rebuild.md` let you (or an agent) restore the database to a point in time and rebuild the host from bare metal using only the repo, the hardware keys, the password manager and the off-site buckets — each runbook tested once by following it literally.

## Context & references

- [Roadmap P0 T0.90](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [02 §8 flows (F5, F6, F11)](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (F11)
- [Roadmap §5 runbooks track](../../../docs/roadmap/README.md#5-cross-phase-tracks)
- Inputs: P0-T039, P0-T041, P0-T019, P0-T057 (measured RTO)
- Depends on: P0-T039, P0-T041, P0-T019

## Requirements

- Format per runbook: purpose, when to use, prerequisites (keys, access), numbered steps with exact commands, verification, rollback, measured duration (RTO/RPO), last tested date.
- Backup & restore: PITR to a timestamp, full-cluster restore to a new host, single-table inspection via scratch restore, restic file restore; RPO target ≤ 1 min (WAL `archive_timeout=60`); RTO measured from P0-T057.
- Host rebuild: OS + LUKS install, `infra/host` playbook, Tailscale join, secrets file restore from restic + age identity on YubiKey, `docker compose up`, restore DB, verify (`audit.verify`, health), re-enable schedules.
- No secrets in the runbooks; reference secret **names** only.
- `docs/runbooks/README.md` index listing all runbooks (P0 + placeholders for later phases: keys leaked, server down with positions, bad data, wallet drained).

## ToDo

- [ ] Write both runbooks and the index.
- [ ] Dry-run host rebuild on a VM following the text literally; fix gaps.
- [ ] Record last-tested dates and durations.

## Verification

### Tests
- Literal dry run on a VM (host rebuild) and on a scratch DB (restore); log any step that needed improvisation and fix the text.

### Scenarios
- Given the host's NVMe dies, when following host-rebuild.md on new hardware, then the stack is back with data up to ≤ 1 min before failure.

### Stress / failure injection
- n/a: documentation; the dry run is the test.

## Acceptance criteria

- [ ] Both runbooks exist in the standard format
- [ ] Each dry-run once with dates/durations recorded
- [ ] Index lists P0 runbooks and later placeholders

## Exceptions & edge cases

- If the YubiKeys are lost, the runbook points to the password-manager recovery path and immediate rotation.

## Cardinal rules (do NOT)

- Do NOT include secret values, IPs or hostnames that aid an attacker.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/runbooks/README.md`: new index; `docs/07-security-notes.md` §9: link the runbooks.
- `docs/roadmap/phase-0-foundations.md`: tick T0.90 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T060-runbooks-backup-restore-host-rebuild`
- PR title: `P0-T060: Write runbooks: backup & restore, host rebuild`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
