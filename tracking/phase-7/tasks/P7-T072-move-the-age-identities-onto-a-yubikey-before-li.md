---
id: P7-T072
kind: task
title: Move the age identities onto a YubiKey before live money
phase: 7
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.01]
roadmap_todos: []
modules: [M17]
dashboards: []
tools: []
mcp: []
env: []
services: [yubikey]
branch: p7/P7-T072-move-the-age-identities-onto-a-yubikey-before-li
pr: ""
doc_sync: [docs/07-security-notes.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---
# P7-T072 · Move the age identities onto a YubiKey before live money

## Goal / expected outcome

Before live keys exist, the two age identities that protect the secrets file live on a hardware key instead of the OS keychain: the **host** identity (decrypts runtime secrets at start-up) and the **offline** identity (the `worm_owner` credential and secrets-file recovery). A stolen disk or backup then can't be decrypted ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode), [07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Context & references

- Until now the identities are in the OS keychain (`secrets.age_identity_store: keychain`, 16 §2.15). Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)
- The agent writes the exact commands (`age-plugin-yubikey`, re-encrypting the sops file to the new recipients) in this task before you start.
- Unblocks: P7-T073, P7-T007 (live keys).

## Requirements

- One YubiKey 5 series (about A$90–130); a second as a spare is recommended.
- About 20 minutes at the workstation with the key plugged in. PINs and touch policies as the agent's instructions say; the PIN is never typed into chat.

## ToDo

- [ ] Buy the YubiKey(s)
- [ ] Follow the agent's instructions to create both identities on the key and re-encrypt the secrets file
- [ ] Remove the keychain identities; agent confirms `secrets.age_identity_store: yubikey` and that services still start

## Verification

### Tests
- Agent: services start with the key present and fail closed without it; the sops file's recipients are the YubiKey identities only.

### Scenarios
- Given the key is unplugged, when the stack restarts, then secrets don't decrypt and trading stays flat.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Both identities on the YubiKey; keychain copies removed

## Exceptions & edge cases

- Lost or broken key: the spare key (or the offline recovery steps the agent wrote) restores access; without either, rotate every secret.

## Cardinal rules (do NOT)

- Never paste PINs, identities or secret values into chat, issues or logs.

## Doc sync on completion

- docs/07-security-notes.md: update to match what was built.

## Branch & PR

- Branch: `p7/P7-T072-move-the-age-identities-onto-a-yubikey-before-li`
- PR title: `P7-T072: Move the age identities onto a YubiKey before live money`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T072` run

## Progress log

- 2026-11-19 09:16 · cloud:vm:be04b6ae61f8 · created
