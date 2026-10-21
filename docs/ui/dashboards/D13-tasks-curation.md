# D13 · Tasks & Curation

| | |
|---|---|
| **Route** | `/tasks` (tabs: Inbox · Communities · Digests · History) |
| **Modules** | M19 curation, M4 airdrops, M2 (Discord/Telegram), M11 approvals, M18 tax questions |
| **Phase** | 5 |
| **Mock-up reference** | Manual social queue in `vetted-launch-radar-au-eofy-tax-ledger.png` |

## Purpose

One place for everything that needs a human:
- airdrop/ICO steps and social-engagement requirements;
- **Discord servers and announcement channels to follow**;
- Telegram channels to join;
- manual claims and approval revokes;
- tax-agent questions.

Each task comes with exact steps and verified links.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ xl | Inbox list (12) + task detail (12) |
| md–lg | List; detail as a drawer |
| ≤ ph | Card list; swipe right = Done, swipe left = Snooze (with confirm for anything that touches funds); tap = detail sheet |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Inbox** | `TaskCard`s sorted by urgency (deadline) and value: type (JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION), project, deadline, estimated minutes, risk/viability, steps preview | `/tasks`, WS `tasks` |
| Task detail | Numbered steps; **official links only** with "verified via …" tags; warnings (never connect main wallet, never sign Permit); related opportunity; "leave when" condition | `/tasks/{id}` |
| **Communities** | Curated Discord/Telegram/Galxe list: project, platform, invite link (verified), **which announcement channel to Follow**, destination inbox channel (`#mt-inbox`), status (suggested / joined / following / verified / left), last post received, "leave when" | `/community`, WS `tasks` |
| **Digests** | Cadence settings per type (instant / daily / weekly; quiet hours; AU timezone), preview of the next digest, delivery channels (Telegram, web) | `/system/settings?section=digests` |
| **History** | Completed / skipped / expired tasks with outcomes (e.g. airdrop received) | `/tasks?status=closed` |

## Actions

| Control | Command | Level |
|---|---|---|
| Done | `task.done` | C0 (for Discord follow tasks the bot then verifies delivery → status "verified" or re-prompt) |
| Skip | `task.skip` | C0 |
| Snooze 1d/1w | `task.snooze` | C0 |
| Never (project) | `task.never` | C1 |
| Open link | External (new tab) | C0 (blocklist check at render) |
| Mark community left | `task.done` (leave task) | C0 |
| Update digest settings | `system.settings.update` | C0 |

## Acceptance criteria

1. **Links:** every task has official, verified links only. Unverified links can't be rendered as clickable.
2. **Phones:** Done/Skip/Snooze also work from Telegram buttons with identical effect (same command).
3. **Discord verification:** follow tasks flip to "verified" automatically once posts arrive.

## Backend contract

- **Queries:** `/tasks` (+ `/{id}`), `/community`, `/system/settings?section=digests`.
- **WebSocket topics:** `tasks`.
- **Commands:** `task.done|skip|snooze|never`, `system.settings.update`.
