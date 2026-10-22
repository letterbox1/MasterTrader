# D16 · System

| | |
|---|---|
| **Routes** | `/system` (Health), `/system/audit`, `/system/settings`, `/system/security`, `/system/backups` |
| **Modules** | M17 observability & audit, ops, security |
| **Phase** | 0 (Health, Settings), grows each phase (Accounts in 3; preflight and drills in 7; MCP tokens in 8) |
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
| Restart service | `system.service.restart` | C2 (shows dependents; engine restart warns about open positions). mt-api never holds the Docker socket: restarts go through a restricted Docker-socket proxy that allows restarting only allow-listed containers; others show the button disabled |
| Run preflight (Phase 7) | `/system/preflight` (read): live keys trade-only/IP-locked, egress IP, venue timers, resting stops, backups, drills | C0 |
| Record a safety drill (Phase 7) | `ops.drill.record` (kill switch, dead-man, restart drills per venue; feeds the D03 safety-drills gate) | C1 |

## Audit (`/system/audit`)

**Audit log:** commands, risk changes, orders, LLM calls, MCP calls, mandate changes, from the canonical WORM tables (`audit.command`, `audit.order`, `audit.fill`, `audit.llm_call`, `audit.dq_event`, `audit.cost_event`, `audit.recon`, `audit.decision_run`, `audit.seal`, `audit.integrity_incident`, `audit.mcp_call`).
- **Columns:** time, source (web / telegram / mcp / system), command, args (secrets redacted), result, hash, **chain verification status**.
- **Filters:** source, command, table, date.
- **Actions:** verify the chain now (`audit.verify`, C1); export.

**Integrity** ([16 §2.11](../../16-configuration-and-safety-model.md#211-worm-integrity)):
- Last hourly incremental check and last daily full verify against the external seal.
- On a mismatch: the configured action (default `block_new_entries`: no new entries, exits and protective orders continue, no risk loosening; options `alert_only` · `halt_all`; changing it is a setting, loosening = C3), the incident (`audit.integrity_incident`) and an **Acknowledge** action (`audit.integrity.ack`, C3) after you've investigated. Every incident and ack is a new WORM row.

## Settings (`/system/settings`)

| Section | Contents |
|---|---|
| Preferences | Theme, density, timezone (default Australia/Sydney), base currency (AUD), number formats |
| Notifications | Channels (Telegram, web), severity routing, quiet hours |
| Digests | (Shared with D13) |
| Schedules | Agent analysis cadence, backfills, retraining, reports |
| DQ thresholds | Stale/gap/divergence thresholds (defaults 2 s fast / 60 s slow stale, spread 3× normal; loosening = C3) |
| Budgets | LLM gateway budgets (default monthly cap US$40; raising = C3) |
| Failure behaviour | Audit-integrity action (default `block_new_entries`), NATS buffer bound (default 1 GB or 24 h; new entries stop above 80%), reconciliation cadence ([16 §2.9](../../16-configuration-and-safety-model.md#29-reconciliation)) |
| **Accounts** (Phase 3) | Minimal registry of exchange/broker accounts and on-chain addresses (`ops.wallets`): register and tag (investment / trading, venue, residency use) via `wallet.register` / `wallet.tag` (C1), or load a seed file through `mt_api`. D18 extends this in Phase 5 |
| Configuration | Every setting from [16](../../16-configuration-and-safety-model.md) as a `SettingField`: effective value, the layer that set it, the default and change history ([ui §3.7](../README.md#37-settings-show-configurable-defaults-and-their-layer)) |
| Integrations | Venues/brokers, data sources, Telegram bot, Discord bot, Hindsight, gateway endpoints (custom endpoint URL), each with status and test button |
| Licence & data tags | Source licence/cost tags (paid sources can't be enabled) |

## Security (`/system/security`)

- **Keys** (metadata only, **values never shown**): venue, scope (trade-only ✔, withdrawals disabled ✔, IP allow-list ✔), age, rotation due.
- **Sessions:** active sessions, TOTP status, last re-authentication (C2 needs one within 12 h by default), Telegram link status, MCP tokens (Phase 8; managed in D17).
- **Egress:** the fixed exit-node IP that exchange traffic leaves from, its country vs your configured residency, last check (every minute by default); a mismatch blocks new orders ([16 §3.2](../../16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
- **Posture checklist** from security notes: disk encryption, firewall, Tailscale-only, image digests pinned, last vulnerability scan, telemetry checks for vendored components.

## Backups (`/system/backups`)

- Last backup (age, size, destination).
- Last **restore test** (pass/fail, date).
- WAL lag (continuous WAL archive).
- Schedule (defaults: nightly incremental, weekly full, monthly restore test, monthly immutable WORM export).
- The sops/age secrets file's backup status (it lives outside the repo; values never shown).
- **Actions:** run backup (`system.backup.run`, C1), run restore test (`system.restore.test`, C1).

## Acceptance criteria

1. **Read-only on outage:** the System page loads even when Postgres is down, with read-only health from mt-api's own probes.
2. **No secrets:** secrets are never rendered or logged in the UI.
3. **Chain failures:** an audit-chain verification failure raises a critical banner.

## Backend contract

- **Queries:** `/system/health` (+ `slo`), `/system/services`, `/system/logs`, `/system/settings`, `/system/keys`, `/system/backups`, `/system/preflight` (P7), `/wallets?kind=account` (P3 Accounts), `/audit/log`.
- **WebSocket topics:** `system`, `heartbeat`.
- **Commands:** `system.service.restart`, `system.settings.update`, `system.backup.run`, `system.restore.test`, `system.key.rotate_reminder`, `audit.verify`, `audit.integrity.ack`, `wallet.register`, `wallet.tag`, `ops.drill.record` _(added)_.
