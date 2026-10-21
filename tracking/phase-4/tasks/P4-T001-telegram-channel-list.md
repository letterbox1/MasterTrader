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
depends_on: []
requirements: [R4.02]
roadmap_todos: [T4.01]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T001-telegram-channel-list
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T001 · List the Telegram channels to monitor (postures only)

## Goal / expected outcome

A reviewed list of up to 500 public Telegram channels/supergroups (crypto calls, project announcements, macro/news channels) exists in `config/intel/telegram_channels.yaml`, ranked by priority so the `FLOOD_WAIT`-aware join queue (P4-T018) can join them slowly from the dedicated account. It unblocks Telegram posture ingestion.

## Context & references

- Roadmap: [R4.02](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.01](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §4 Telegram row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (own long-standing account, joined channels only, cap 500 / 1,000 with Premium)
- Accounts: [07 §10](../../../docs/07-security-notes.md#10-social--scraping-accounts) (dedicated number, 2FA password, encrypted session)
- Cross-phase: P0 T0.06 (dedicated Telegram number, `api_id`/`api_hash`) must be done.
- Unblocks: P4-T018 (join queue), P4-T019 (postures).

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
