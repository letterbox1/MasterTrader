---
id: P4-T001
kind: task
title: List the Telegram channels to monitor (postures only)
phase: 4
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T002, P4-T006]
requirements: [R4.02]
roadmap_todos: [T4.01]
modules: [M2]
dashboards: [D08]
tools: []
mcp: []
env: []
services: [telegram-account]
branch: p4/P4-T001-telegram-channel-list
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
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

# P4-T001 · List the Telegram channels to monitor (postures only)

## Goal / expected outcome

A reviewed list of up to 500 public Telegram channels/supergroups (crypto calls, project announcements, macro/news channels) exists in `config/intel/telegram_channels.yaml`, ranked by priority so the `FLOOD_WAIT`-aware join queue (P4-T018) can join them slowly from the dedicated account. You also create the Telethon session once on the host with the P4-T006 login script. Together these unblock the live Telegram check (P4-T068); the build tasks run on fixtures and don't wait for this.

## Context & references

- Roadmap: [R4.02](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.01](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §4 Telegram row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (own long-standing account, joined channels only, cap 500 / 1,000 with Premium)
- Accounts: [07 §10](../../../docs/07-security-notes.md#10-social--scraping-accounts) (dedicated number, 2FA password, encrypted session)
- Cross-phase: P0-T002 (T0.06: dedicated Telegram number, `api_id`/`api_hash`) is a `depends_on` entry; so is P4-T006 (the login script).
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B002/B003): Telegram is postures only, stored in `text.telegram_posture`, published on `posture.telegram.*`, consumed only by M4/M11 rules (D08 shows the numbers).
- Unblocks: P4-T068 (live check of the join queue and postures on your account).

## Requirements

- Only **public** channels/supergroups you would join by hand; no private invite-scraping, no member-list harvesting.
- Total ≤ 500 entries (hard cap enforced by the join queue); mark the top 50 as `priority: 1` so they join first.
- Each entry: `handle` (e.g. `@somechannel`), `kind` (channel/supergroup), `topic` (crypto-calls / project / macro / news), `why`, optional `asset_hint` (ticker or chain).
- Telegram text will **never** be shown to a model; the list only drives counts/addresses → postures. Pick channels for *what they mention*, not for their analysis.

## ToDo

- [ ] Open the template the agent created at `config/intel/telegram_channels.example.yaml` and copy it to `config/intel/telegram_channels.yaml` (no secrets in it, so it can live in git).
- [ ] Add channels in priority order (≤ 500), one YAML item each with `handle`, `kind`, `topic`, `why`, `priority` (1–3).
- [ ] Remove any channel that requires a phone-number reveal, payment, or a bot-captcha that asks for more than a button tap.
- [ ] Commit the file on branch `p4/P4-T001-telegram-channel-list` (or hand it to the agent) and note the count in the progress log.
- [ ] Confirm the dedicated account (T0.06) is logged in only on your phone + the server session; never on a shared device.
- [ ] Once P4-T006 has landed, run `ops/scripts/telethon_login.py` on the host yourself and type the login code and 2FA password at its prompt. It writes the session straight into the encrypted file outside the repo (`/etc/mastertrader/telethon.session.sops`). Never paste the code or password into a chat, issue or log.

## Verification

### Tests
- Agent runs `python -m mt_data.text.telegram.validate_list config/intel/telegram_channels.yaml` (schema, ≤ 500, no duplicates) once P4-T018 lands.

### Scenarios
- Given the list has 520 entries, when validated, then it fails with 'cap 500 exceeded' and you trim it.
- Given a handle is a private invite link, when validated, then it is rejected (public handles only).

### Stress / failure injection
- n/a: human list-making step.

## Acceptance criteria

- [ ] `config/intel/telegram_channels.yaml` exists with ≤ 500 public entries and priorities set
- [ ] Validator passes with 0 errors
- [ ] Progress log records the count and the date
- [ ] Telethon session created on the host by you (the agent confirms only that the encrypted file exists, never its contents)

## Exceptions & edge cases

- If you have Telegram Premium the policy cap is 1,000, but MasterTrader keeps 500 as its own cap.
- Channels that later go private or ban the account are dropped by the queue and flagged in D08 Sources; re-review monthly.

## Cardinal rules (do NOT)

- Do NOT use your personal Telegram account; only the dedicated number from T0.06.
- Do NOT bulk-join by hand to 'speed things up'; joins go through the queue.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.01

## Branch & PR

- Branch: `p4/P4-T001-telegram-channel-list`
- PR title: `P4-T001: List the Telegram channels to monitor (postures only)`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T001`

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (posture table/subject names per 17 §D; session login moved here as your step; depends on P0-T002 + P4-T006; build tasks no longer wait for this list)
