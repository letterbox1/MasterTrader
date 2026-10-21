# D16 · System

| | |
|---|---|
| **Routes** | `/system` (Health), `/system/audit`, `/system/settings`, `/system/security`, `/system/backups` |
| **Modules** | M17 observability & audit, ops, security |
| **Phase** | 0 (Health, Settings), grows each phase |
| **Mock-up reference** | None (new) |

## Purpose

Operate the box: health, services, logs, audit trail, backups, security posture and settings, without SSH for everyday tasks.

## Health (`/system`)

| Tier | Layout |
|---|---|
| ≥ xl | Service grid (status, version, uptime, CPU/RAM, restarts, heartbeat) + host panel (CPU, RAM, disk per volume, GPU, temps, NTP offset) + SLO panel |
| ≤ ph | Host summary card → service cards → SLOs |

**Widgets:**

| Widget | Shows | Source |
|---|---|---|
| Services | Every container from architecture §3.2: status, image digest, uptime, restarts, heartbeat, health checks | `/system/services`, WS `system` |
| Host | CPU, RAM, disk (NVMe/HDD), GPU util/VRAM, network, NTP/chrony offset | `/system/health` |
| SLOs | Each SLO from architecture §9.2 with the current value and status | `/system/health?slo=1` |
| Logs | Loki-backed search: service, level, text, time range, `trace_id` jump | `/system/logs` |
| Grafana | Deep links to dashboards | — |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Restart service | `system.service.restart` | C2 (shows dependents; engine restart warns about open positions) |

## Audit (`/system/audit`)

**Audit log:** commands, risk changes, orders, LLM calls, MCP calls, mandate changes.
- **Columns:** time, source (web / telegram / mcp / system), command, args (secrets redacted), result, hash, **chain verification status**.
- **Filters:** source, command, date.
- **Actions:** verify the chain now; export.

## Settings (`/system/settings`)

| Section | Contents |
|---|---|
| Preferences | Theme, density, timezone (default Australia/Sydney), base currency (AUD), number formats |
| Notifications | Channels (Telegram, web), severity routing, quiet hours |
| Digests | (Shared with D13) |
| Schedules | Agent analysis cadence, backfills, retraining, reports |
| DQ thresholds | Stale/gap/divergence thresholds (loosening = C3) |
| Budgets | LLM gateway budgets (raising = C3) |
| Integrations | Venues/brokers, data sources, Telegram bot, Discord bot, Hindsight, gateway endpoints (custom endpoint URL), each with status and test button |
| Licence & data tags | Source licence/cost tags (paid sources can't be enabled) |

## Security (`/system/security`)

- **Keys** (metadata only, **values never shown**): venue, scope (trade-only ✔, withdrawals disabled ✔, IP allow-list ✔), age, rotation due.
- **Sessions:** active sessions, TOTP status, Telegram link status, MCP tokens (Phase 8).
- **Posture checklist** from security notes: disk encryption, firewall, Tailscale-only, image digests pinned, last vulnerability scan, telemetry checks for vendored components.

## Backups (`/system/backups`)

- Last backup (age, size, destination).
- Last **restore test** (pass/fail, date).
- WAL lag.
- Schedule.
- **Actions:** run backup (`system.backup.run`, C1), run restore test (`system.restore.test`, C1).

## Acceptance criteria

1. **Read-only on outage:** the System page loads even when Postgres is down, with read-only health from mt-api's own probes.
2. **No secrets:** secrets are never rendered or logged in the UI.
3. **Chain failures:** an audit-chain verification failure raises a critical banner.

## Backend contract

- **Queries:** `/system/health` (+ `slo`), `/system/services`, `/system/logs`, `/system/settings`, `/system/keys`, `/system/backups`, `/audit/log`.
- **WebSocket topics:** `system`, `heartbeat`.
- **Commands:** `system.service.restart`, `system.settings.update`, `system.backup.run`, `system.restore.test`, `system.key.rotate_reminder`, `audit.verify` _(added)_.
