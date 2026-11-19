---
id: P0-T013
kind: task
title: Generate the offline worm_owner credential (before live money; the build uses a throwaway one)
phase: 0
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T022, P0-T031, P0-T061]
requirements: [R0.07, R0.N1]
roadmap_todos: [T0.23]
modules: [M17]
dashboards: []
tools: [sops, age, openssl, psql, supabase, just]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T013-worm-owner-offline-credential
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T013 · Generate the offline worm_owner credential (before live money; the build uses a throwaway one)

## Goal / expected outcome

Before live money, the Postgres `worm_owner` password for the real stack exists **only** in an offline sops file encrypted to your **offline** age identity (OS keychain or removable media now; on a YubiKey once P7-T072 is done), never in the runtime secrets file or on the workstation/runtime host disk. Migrations that touch WORM tables (`-- mt:worm` files) are applied to that stack by you, in a short ceremony. Until then the build, tests and paper stack use a generated throwaway `worm_owner` (dev/paper data only), so no agent task waits on this.

## Context & references

- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Privileges row)
- [18 §4.4 point-in-time and WORM](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm) (offline `worm_owner`; cloud caveat)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) · [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- Related: P0-T029 (role + `-- mt:worm` guard), P0-T061 (ceremony runbook), P7-T072 (YubiKey), P7-T073 (the shift and its live migrations)
- Depends on: P0-T022 (secrets layout), P0-T031 (the WORM migrations to run), P0-T061 (the ceremony runbook)
- Gates: live money (via the P7 go-live preflight), not the soak or any P0 build task

## Requirements

- Password: ≥ 32 random chars (`openssl rand -base64 36`), generated on a machine you control, never typed into chat.
- Stored in `offline/worm_owner.sops.yaml` encrypted **only** to the offline age recipient; kept on removable media + a copy in your password manager's secure notes; never copied into `~/.config/mastertrader/secrets.sops.yaml`.
- Ceremony (documented in P0-T061): unlock the offline identity → `sops exec-env offline/worm_owner.sops.yaml 'just db-migrate'` (the recipe switches to `worm_owner` only for `-- mt:worm` files) → lock it again; the password lives only in that process's environment.
- The ceremony runs against the stack that will hold live money (the workstation's self-hosted Supabase, or Supabase cloud if you choose it at the shift; on cloud the platform operator still holds the real superuser, so the external seal is what proves tampering, 18 §4.4).
- Rotation: on any suspicion and yearly; rotation is itself a ceremony (`ALTER ROLE` from a `psql` session as an admin role).

## ToDo

- [ ] Generate the password and create the offline sops file with the offline recipient.
- [ ] Copy the file to two removable media (one off-site) and add the password to the password manager.
- [ ] Before the first live-stack WORM migration, set the role password (`ALTER ROLE worm_owner PASSWORD …` via `psql`, from the env, never typed into history).
- [ ] Run the WORM migrations via the ceremony and log the date.

## Verification

### Tests
- Confirmation: on the workstation, a search of `~/.config/mastertrader`, `/run/secrets` and running process environments finds no ceremony `worm_owner` password afterwards; P0-T055 asserts app roles can't `SET ROLE worm_owner`.

### Scenarios
- Given the workstation is compromised, when an attacker reads tmpfs secrets, then they do not obtain the ceremony `worm_owner` credential.

### Stress / failure injection
- n/a: credential ceremony.

## Acceptance criteria

- [ ] Offline sops file exists encrypted only to the offline recipient
- [ ] Runtime secrets file has no `worm_owner` entry (checked by `secrets-lint`)
- [ ] First ceremony run logged

## Exceptions & edge cases

- Lost offline identity: recover via the password-manager copy, then rotate immediately.
- You move to Supabase cloud at the shift: repeat the ceremony against the cloud project (P7-T073).

## Cardinal rules (do NOT)

- Do NOT put the ceremony worm_owner password in the runtime secrets file, an env file, CI secrets or shell history.
- Do NOT reuse the dev/paper throwaway credential for the live stack.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keys-last: no longer blocks P0-T029 (CI uses a throwaway password); depends on the migrations + ceremony runbook; secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); run fields added)
- 2026-11-19: Workstation-first (17 §G): the build and paper stack generate a throwaway `worm_owner` credential automatically (dev/paper data only). This ceremony, encrypted to the offline age identity, is done once before live money and gates P7-T057, not the soak.
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (body aligned: ceremony via `just db-migrate` for `-- mt:worm` files on the Supabase stack, offline identity in the keychain/removable media until P7-T072; YubiKey tool and service dropped; gates live money, not P0)
