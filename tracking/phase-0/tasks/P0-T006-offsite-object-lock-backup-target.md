---
id: P0-T006
kind: task
title: Open the off-site backup target with Object Lock
phase: 0
type: USER
status: ready
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.04]
modules: [M17]
dashboards: []
tools: []
mcp: []
env: []
services: [backblaze-b2]
branch: p0/P0-T006-offsite-object-lock-backup-target
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T006 · Open the off-site backup target with Object Lock

## Goal / expected outcome

An off-site, immutable target exists for (a) the pgBackRest repo + WAL archive, (b) restic snapshots, and (c) WORM seals and monthly immutable exports. Default: **Backblaze B2** buckets with **Object Lock in compliance mode**; the free alternative is a second box running restic `rest-server --append-only`. Credentials are restricted per bucket and stored in the secrets file.

## Context & references

- [Roadmap P0 T0.04](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (daily seal, backups)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- Related: P0-T039 backups, P0-T037 seals, P0-T040 exports
- The roadmap README §6 register row for T0.04 now matches the phase doc (Object Lock / append-only, R0.07; P0-B015 closed).
- Unblocks: the live checks against the real target: P0-T057 (first off-site backup + restore test) and P0-T063 (soak: seals and exports anchored). P0-T037, P0-T039 and P0-T040 are built and tested against MinIO with Object Lock, so they don't wait for this task (build first, keys last)

## Requirements

- Three private buckets with Object Lock enabled **at creation** (it can't be added later on B2):
- `mt-pgbackrest`: compliance retention **35 days** (must not exceed pgBackRest's effective retention, or expiry fails); `mt-restic`: compliance 35 days; `mt-worm-seal`: compliance **2557 days (7 years)** for seals and monthly WORM exports.
- One application key **per bucket**, limited to that bucket (list/read/write; no delete on `mt-worm-seal`); key ids/secrets → the sops secrets file `~/.config/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `pgbackrest:`, `restic:`, `worm_seal:`.
- Free alternative: second box (e.g. a Raspberry Pi + USB disk at another location) running `rest-server --append-only --private-repos`, reachable over Tailscale only.
- Cost note: B2 is pay-as-you-go storage (first 10 GB free); it is storage, not data, and is the docs' named default. Log the expected size (~50–200 GB in year 1).
- Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.
- Env names the late live checks use (names only; values stay in the secrets file): `PGBACKREST_REPO1_S3_KEY`, `PGBACKREST_REPO1_S3_KEY_SECRET`, `PGBACKREST_REPO1_CIPHER_PASS`, `RESTIC_PASSWORD`, `B2_ACCOUNT_ID`, `B2_ACCOUNT_KEY`, `MT_WORM_SEAL_S3_KEY_ID`, `MT_WORM_SEAL_S3_SECRET`.

## ToDo

- [ ] Create the B2 account with MFA (or prepare the second box); log which option you chose.
- [ ] Create the three buckets with Object Lock and the default retentions above.
- [ ] Create one restricted application key per bucket; record key id + key in the password manager.
- [ ] Generate a restic repository password and a pgBackRest `repo1-cipher-pass` (≥ 32 random chars each) in the password manager.
- [ ] Once P0-T022 lands, add all values to the secrets file; log 'stored'.
- [ ] Write the bucket names/endpoint (not secret) into `infra/backup/targets.yaml` for P0-T057.

## Verification

### Tests
- Object Lock probe (run in P0-T057): upload a test object to `mt-worm-seal`, then try to delete it with the same key → must fail.

### Scenarios
- Given an attacker has the host's B2 key, when they try to delete or overwrite a locked object, then B2 refuses until retention expires.
- Given the second-box option, when a client without the append-only bypass tries `restic forget --prune`, then rest-server refuses.

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Three buckets with Object Lock (compliance) and the stated retentions exist (or an append-only rest-server box over Tailscale)
- [ ] Per-bucket restricted keys; secrets only in password manager / secrets file
- [ ] Delete probe fails on a locked object

## Exceptions & edge cases

- Compliance mode can't be shortened, even by you: double-check retention values before saving.
- If B2 is unacceptable, the rest-server box must be at a different physical location from the host.

## Cardinal rules (do NOT)

- Do NOT use Object Lock *governance* mode for `mt-worm-seal` (bypassable).
- Do NOT give the host a master application key.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/07-security-notes.md` §8: record the chosen target and retention values (no secrets).
- `docs/roadmap/phase-0-foundations.md`: tick T0.04 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T006-offsite-object-lock-backup-target`
- PR title: `P0-T006: Open the off-site backup target with Object Lock`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); keys-last: build tasks use MinIO, live use in P0-T057/P0-T063; env names named; P0-B015 closed; run fields added)
