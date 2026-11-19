# D16 · System

| | |
|---|---|
| **Routes** | `/system` (Health), `/system/audit`, `/system/settings`, `/system/security`, `/system/backups`; the Go-live preflight card (Phase 7) sits on `/system` |
| **Modules** | M17 observability & audit, ops, security |
| **Phase** | 0 (Health, Settings), grows each phase (Accounts in 3; preflight, Settings pack and drills in 7; MCP tokens in 8) |
| **Mock-up reference** | None (new) |

## Purpose

Operate the system wherever it runs (your workstation, or the runtime host after the Phase 7 shift): health, services, logs, audit trail, backups, security posture, deployment mode and settings, without SSH for everyday tasks.

## Health (`/system`)

| Tier | Layout |
|---|---|
| ≥ xl | Service grid (status, version, uptime, CPU/RAM, restarts, heartbeat) + host panel (CPU, RAM, disk per volume, GPU if present, temps, NTP offset) + deployment card + SLO panel |
| ≤ ph | Host summary card → service cards → deployment card → SLOs |

**Widgets:**

| Widget | Shows | Source |
|---|---|---|
| Services | Every container from architecture §3.2: status, image digest, uptime, restarts, heartbeat, health checks | `/system/services`, WS `system` |
| Host | The machine the services run on (the workstation by default): CPU, RAM, disk (NVMe/HDD), GPU util/VRAM (only when a GPU is present; the model profile in use, `models.gpu_profile`), network, NTP/chrony offset | `/system/health` |
| Deployment | Deployment mode (`deploy.mode`: workstation / hybrid / regional), where the web app is served (`web.host`: local Caddy or Vercel), the database (`db.target`: local self-hosted Supabase or Supabase cloud, with region), API exposure (`api.exposure`: tailnet / public), engine regions, age-key store (`secrets.age_identity_store`). Read-only here: changing the mode is an OPS task, and `api.exposure: public` or a new region is C3 ([16 §2.15](../../16-configuration-and-safety-model.md#215-platform-deployment-and-regions), [18 §5](../../18-platform-and-deployment.md#5-deployment-modes)) | `/system/deployment` _(added)_ |
| SLOs | Each SLO from architecture §9.2 with the current value and status | `/system/health?slo=1` |
| Logs | Loki-backed search: service, level, text, time range, `trace_id` jump | `/system/logs` |
| Grafana | Deep links to dashboards | — |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Restart service | `system.service.restart` | C2 (shows dependents; engine restart warns about open positions). mt-api never holds the Docker socket: restarts go through a restricted Docker-socket proxy that allows restarting only allow-listed containers; others show the button disabled |
| Run preflight (Phase 7) | `/system/preflight` (read): live keys trade-only/IP-locked, egress IP, venue timers, resting stops, backups, drills | C0 |
| Record a safety drill (Phase 7) | `ops.drill.record` (kill switch, dead-man, restart drills per venue; feeds the D03 safety-drills gate) | C1 |

### Go-live preflight (Phase 7)

A card on `/system` ([P7-T011](../../../tracking/phase-7/tasks/P7-T011-go-live-preflight.md)). Hidden before Phase 7.
- **Checks:** one row per entry criterion and per strategy/venue (paper/HITL period, tax regime, venue registry and AUSTRAC age, runbook drills, professional-advice items, live key audit, egress status, Settings pack approved), each pass/fail with an evidence link. Funding, live mode and capital steps are refused while any check fails.
- **Deployment readiness:** the target runtime host and options chosen in [P7-T071](../../../tracking/phase-7/tasks/P7-T071-choose-the-go-live-runtime-host-and-cloud-option.md) (default: stay on the workstation), YubiKey status ([P7-T072](../../../tracking/phase-7/tasks/P7-T072-move-the-age-identities-onto-a-yubikey-before-li.md)), and the last full verification suite run on the target ([P7-T073](../../../tracking/phase-7/tasks/P7-T073-shift-to-the-go-live-runtime-host-harden-migrate.md)) with its date and result.
- **Settings pack** ([P7-T070](../../../tracking/phase-7/tasks/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl.md)): the go-live pack. One page listing every value the agents seeded during the build: L0 ceilings and L1–L3 risk policy, sleeves and budgets, first strategy manifests. Each row shows the setting, its layer, the default (with the 16 or 14 link), the current value and any change since the seed. Values are edited in D03/D06 as usual (tighten C1, loosen C3), not here.
  - **Approve** (C3: Telegram approve + TOTP + cool-down) records one WORM row naming the policy and manifest versions approved. Any loosening after that turns the "Settings pack approved" check red again until re-approved.
  - States: not yet seeded (empty state with a link to D06) · ready to review · approval pending (C3 countdown) · approved (date, versions) · changed since approval (amber).

| Control | Command | Level |
|---|---|---|
| Approve the Settings pack | Pack approval command (name set in P7-T011/P7-T070) _(added)_ | C3 |

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
| **Accounts** (Phase 3) | Minimal registry of exchange/broker accounts and on-chain addresses (`ops.wallets`): register and tag (investment / trading, venue, residency use) via `wallet.register` / `wallet.tag` (C1), or load a seed file through `mt-api`. D18 extends this in Phase 5 |
| Configuration | Every setting from [16](../../16-configuration-and-safety-model.md) as a `SettingField`: effective value, the layer that set it, the default and change history ([ui §3.7](../README.md#37-settings-show-configurable-defaults-and-their-layer)) |
| Integrations | Venues/brokers, data sources, Telegram bot, Discord bot, Hindsight, gateway endpoints (custom endpoint URL), each with status and test button |
| Licence & data tags | Source licence/cost tags (paid sources can't be enabled) |

## Security (`/system/security`)

- **Keys** (metadata only, **values never shown**): venue, scope (trade-only ✔, withdrawals disabled ✔, IP allow-list ✔), age, rotation due.
- **Sessions:** your Supabase Auth account (password + TOTP; sign-ups off), active sessions, TOTP enrolment and MFA level (`aal2` needed for commands), last re-authentication (C2 needs one within 12 h by default), Telegram link status, MCP tokens (Phase 8; managed in D17).
- **Egress:** the fixed exit-node IP that exchange traffic leaves from, its country vs your configured residency, last check (every minute by default); a mismatch blocks new orders ([16 §3.2](../../16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
- **Posture checklist** from security notes: disk encryption, firewall, Tailscale-only, image digests pinned, last vulnerability scan, telemetry checks for vendored components. Before the shift the workstation baseline applies (disk encryption and Tailscale show as warnings, not failures); from the shift the live profile applies and they must pass ([18 §8–9](../../18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)).
- **Key store:** where the age identities live (OS keychain until Phase 7, then YubiKey).

## Backups (`/system/backups`)

- Last backup (age, size, destination). The method follows the database target ([18 §4.7](../../18-platform-and-deployment.md#47-backups)): pgBackRest + restic on the workstation; on Supabase cloud, its managed daily backups plus our own nightly logical dump to restic.
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

- **Queries:** `/system/health` (+ `slo`), `/system/services`, `/system/logs`, `/system/settings`, `/system/keys`, `/system/backups`, `/system/deployment` _(added)_, `/system/preflight` (P7, incl. the Settings pack), `/wallets?kind=account` (P3 Accounts), `/audit/log`.
- **WebSocket topics:** `system`, `heartbeat`.
- **Commands:** `system.service.restart`, `system.settings.update`, `system.backup.run`, `system.restore.test`, `system.key.rotate_reminder`, `audit.verify`, `audit.integrity.ack`, `wallet.register`, `wallet.tag`, `ops.drill.record` _(added)_, Settings pack approval (C3, P7) _(added)_.
