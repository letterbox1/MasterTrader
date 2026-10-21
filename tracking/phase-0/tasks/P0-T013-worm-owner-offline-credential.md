---
id: P0-T013
kind: task
title: Generate the offline worm_owner credential
phase: 0
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T003, P0-T022]
requirements: [R0.07, R0.N1]
roadmap_todos: [T0.23]
modules: [M17]
dashboards: []
branch: p0/P0-T013-worm-owner-offline-credential
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T013 · Generate the offline worm_owner credential

## Goal / expected outcome

The Postgres `worm_owner` password exists **only** in an offline sops file encrypted to your offline age identity (YubiKey slot 2), never in the runtime secrets file or on the host disk. Migrations that touch WORM tables are run by you, in a short ceremony, with the key plugged in.

## Context & references

- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Privileges row)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- Related: P0-T029 (role + grants), P0-T061 (ceremony runbook)
- Depends on: P0-T003, P0-T022
- Unblocks: P0-T029 WORM migrations

## Requirements

- Password: ≥ 32 random chars (`openssl rand -base64 36`), generated on your laptop, not the host.
- Stored in `offline/worm_owner.sops.yaml` encrypted **only** to the `mt-offline` age recipient; kept on removable media + a copy in your password manager's secure notes; never copied into `/etc/mastertrader/secrets.sops.yaml`.
- Ceremony (documented in P0-T061): plug key → `sops exec-env offline/worm_owner.sops.yaml 'uv run mt-migrate --worm'` → unplug; the password lives only in that process's environment.
- Rotation: on any suspicion and yearly; rotation is itself a ceremony (`ALTER ROLE` from the Postgres console).

## ToDo

- [ ] Generate the password on your laptop and create the offline sops file with the `mt-offline` recipient.
- [ ] Copy the file to two removable media (one off-site with the spare YubiKey) and add the password to the password manager.
- [ ] During P0-T029 review, set the role password from the Postgres console (`\password worm_owner`) with the key plugged in.
- [ ] Run the first WORM migration via the ceremony and log the date.

## Verification

### Tests
- Confirmation: on the host, a search of `/etc/mastertrader` and running process environments finds no worm_owner password after the ceremony; P0-T055 asserts app roles can't `SET ROLE worm_owner`.

### Scenarios
- Given the host is compromised, when an attacker reads tmpfs secrets, then they do not obtain `worm_owner` credentials.

### Stress / failure injection
- n/a: credential ceremony.

## Acceptance criteria

- [ ] Offline sops file exists encrypted only to the offline recipient
- [ ] Runtime secrets file has no `worm_owner` entry (checked by `secrets-lint`)
- [ ] First ceremony run logged

## Exceptions & edge cases

- Lost offline key and spare: recover via the password-manager copy, then rotate immediately.

## Cardinal rules (do NOT)

- Do NOT put the worm_owner password in the runtime secrets file, an env file, CI secrets or shell history.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: link the ceremony runbook from the Privileges row.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T013-worm-owner-offline-credential`
- PR title: `P0-T013: Generate the offline worm_owner credential`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
