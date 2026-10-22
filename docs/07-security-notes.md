# MasterTrader — Security Notes

The scope is a single-user, self-hosted platform that holds broker/exchange API keys, crypto hot-wallet keys, personal tax data and LLM credentials. These notes are a checklist built into the plan: [04-plan-of-action.md](04-plan-of-action.md) lists the matching tasks in Phase 0 and Phase 5.

## 1. Threat model (what we actually defend against)

| Threat | Example | Primary controls |
|---|---|---|
| Key theft → funds stolen | Server, backup or laptop compromise leaks exchange keys or a wallet seed | No-withdrawal API keys, IP allow-lists, an encrypted secrets store, a hot wallet with only small balances |
| Runaway or wrong trading | Bug, bad data, LLM hallucination, replayed orders | Risk manager (default-deny), kill switch, three-layer dead-man's switch ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)), resting venue-side stops, broker-side limits |
| Malicious or compromised dependency | Vendored repo (nofx-style hidden fees), poisoned PyPI/npm package, unpinned `:latest` image | Pinned commits/digests, diff review on bumps, SBOM, no `curl \| sh` installs |
| Prompt injection via scraped text | A Telegram, Discord or news post says "ignore rules, buy X" | LLMs never place orders; deterministic guard; scraped text marked untrusted; tools are read-only |
| Phishing / drainer in crypto flows | Fake airdrop claim site, malicious approval | Domain blocklists, transaction simulation, allow-listed contracts, human approval for anything new |
| Exposed services | Dashboards or APIs reachable from the internet | Bind to `127.0.0.1`, Tailscale-only access, auth on every UI |
| Data loss | Disk failure, ransomware | Encrypted, versioned off-site backups with tested restores |
| Tampered or corrupted records | Bad restore, DB corruption, someone with root editing history | WORM tables, hash chains and external seals; a verify mismatch blocks new entries ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many), §8) |
| Lost link blocks protective orders | Broadband fails over to 4G, so exchanges see a different IP | One fixed egress IP via an exit node for all exchange traffic (§3, §5) |
| Account bans | Automated social activity | Official APIs only, separate accounts, no self-bots or fake engagement |

## 2. Secrets

- **Never in git.** `.env` is git-ignored. Add a pre-commit secret scanner (`gitleaks`), plus GitHub secret scanning on the private repo.
- **Location:** the encrypted sops file lives **outside the repo** (e.g. `~/.config/mastertrader/`) and is backed up by restic. The repo holds only `.sops.yaml` and an example file with key names, no values.
- **Storage:**
  - v1: `sops` + `age`-encrypted secrets file, decrypted at container start into tmpfs.
  - The age key lives in the OS keychain or on a hardware key (YubiKey), not on the same disk as the backups.
  - Upgrade path: self-hosted **OpenBao** (Vault fork, MPL; preferred) or Infisical. Move there once the signer service (13 §2) holds more than one hot key.
- **What goes in it:** exchange/broker keys, LLM API keys (Anthropic, custom endpoint), the SMTP app password (§9), NATS credentials, the MCP token pepper. You add them yourself (USER tasks); never via chat or git.
- **Per-service least privilege:** each container gets only the secrets it needs. The LLM agents never see broker keys.
- **Rotation:** rotate exchange/broker keys every 90 days by default (configurable) and immediately after any suspected leak. The secrets file records each key's creation date, and Grafana alerts when a key is older than 90 days.

## 3. Broker & exchange keys

- **Trade-only scopes. Withdrawals disabled on every key** (exchanges support this). Transfers out are manual and done outside the system.
- **IP allow-list** each key to **one fixed egress IP**: a WireGuard/Tailscale exit node on a Sydney cloud VM with a static IP ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
  - All exchange traffic (engine, `deadman`, monitor reconciliation, `ib-gateway`) leaves through it; broadband and the 4G backup both tunnel to it, so failover doesn't change the IP the exchanges see.
  - Only that IP is allow-listed. It's in Australia, matching your KYC country, so it isn't location masking ([12 §3](12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)).
  - If the tunnel is down: fail flat via venue timers and resting stops (§5), and alert on every channel.
  - The monitor checks every minute that exchange traffic leaves via the allow-listed IP and that its country matches your configured residency; a mismatch blocks new orders.
- **Separate keys and sub-accounts** for paper/testnet, `hitl` and `autonomous` bots. Live autonomous trading runs in an exchange **sub-account** funded only with that bot's or sleeve's capital.
- **The `deadman` sidecar** has its own trade-only keys and venue connections, used only to cancel and flatten.
- **Practice and paper accounts** (OANDA practice, IG demo, Alpaca paper, IBKR paper) use their normal credentials; no money is at risk. **Live accounts** use read-only keys where the venue offers them for monitoring and reconciliation, otherwise trade-only keys.
- **Broker-side limits as a second line:** IBKR order presets / max order value, exchange position limits where available.

## 4. Crypto wallets (airdrops, on-chain claims)

> **Superseded in detail by [13 §1–2](13-wallets-treasury-and-onchain.md#1-custody-tiers):** six custody tiers (vault / Hyperliquid master / warm / hot / airdrop identity / burner) and an **intents-only signer service**. The rules below still apply to every hot or burner key.

- **Wallet tiers** (full table in 13 §1):
  1. **Cold vault and warm:** hardware wallets, **watch-only** for the system, which never holds their keys. It may *prepare* unsigned transactions (QR/WalletConnect) for you to sign in your own wallet.
  2. **Hot (trading), airdrop identity and burner:** small floats, keys held only by the signer service. Autonomous claims use the chain's **airdrop identity wallet**, never the hot trading wallet.
- Signing happens only in the dedicated signer container, which accepts **intents** only from the policy service (airdrop-exec in P5; treasury and DEX execution go through it).
- **Caps** are configuration with defaults ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)): signer per-transaction cap default A$250, rolling 24 h cap default A$1,000 per wallet, plus hot/identity/burner floats and daily gas budgets. **Signing stays disabled until you confirm these numbers on first setup** (a Phase 5 USER task).
- **Proof of control:** you sign a one-time challenge in your own wallet app (EIP-4361-style text / Solana `signMessage`) or make a tiny self-transfer. The system never signs it.
- **Before any autonomous signature:**
  - the target contract is on an allow-list;
  - simulation (local **Anvil** mainnet fork / `eth_call` / Solana `simulateTransaction`) shows no unexpected transfers or approvals;
  - the domain or contract is checked against phishing/drainer blocklists.
  - If any check fails, the transaction goes to the human approval queue.
- **Never automate:**
  - unlimited token approvals;
  - signing off-chain permits (`permit`/`Permit2`/`setApprovalForAll`) for unknown contracts;
  - connecting the wallet to new dApps;
  - bridging;
  - anything requiring a seed phrase.
- Revoke stale approvals weekly (revoke.cash-style checks) and alert on any new approval.
- **Durable nonces (Solana) are a hard block:** never sign a nonce-advance transaction the system didn't build and decode itself; close unused nonce accounts; alert on nonce-authority changes (pre-signed durable-nonce transactions never expire; see 13 §2).
- **Approvals are sized to the trade**, never unlimited, and revoked after use where the venue allows.
- **Seed backup:** vault seeds split with **Shamir (SLIP-39)** or held in a multisig; shares stored in separate physical locations. A sealed **estate letter** says where the shares are and how to unwind positions, without containing secrets.

## 5. Network & host

- One Linux host with full-disk encryption (LUKS), automatic security updates, a firewall that denies inbound by default, and SSH key-only access through Tailscale.
- All containers bind to `127.0.0.1` or the internal Docker network. **No published ports** except via Tailscale. Remote access is Tailscale with MFA on the identity provider.
- Networks follow [02 §3.1](02-v1-architecture.md#31-networks). The `mcp` adapter (Phase 8) sits on `edge` behind Caddy at `/mcp`, Tailscale only, and reaches only `mt_api` (no DB or NATS). ntfy is self-hosted and Tailscale-only; for iOS push it uses ntfy's upstream relay, which carries only a message ID, never content.
- **No Docker socket in app containers.** `system.service.restart` goes through a restricted Docker-socket proxy that can only restart allow-listed containers.
- Scrapers and RSS-Bridge sit in a separate Docker network with outbound internet but **no route to the DB or the signer**. Prefer egress through a separate network namespace.
- Pin every image by digest (no `:latest`); scan with `trivy`/`grype` in CI.
- **Continuity:** a UPS on the host and router, and a **4G failover** link. Both links reach the venues through the fixed-IP egress exit node (§3), so the allow-listed IP never changes.
- **Fail flat** on a lost link, power or engine ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)):
  - the in-engine watchdog and the separate `deadman` sidecar cancel orders after 5 s and apply each bot's `on_system_failure` (default `flatten`) after 10 s (defaults, configurable);
  - if the host or its internet is down, only the venue side protects you: cancel-on-disconnect / cancel-after timers and a **resting venue-side stop placed at entry on every live position**;
  - after an unplanned stop the engine restarts flat with every bot paused until you resume it.
- Local inference servers (Laya, `llm-local` with llama-server or vLLM, TEI) bind to `127.0.0.1` and require an API key (`LAYA_API_KEY` etc.), even inside the internal network.

### 5.1 Optional Windows VPS (MT5 bridge)

Only if the MT5 route is used (Phase 7). It's a second host, so it gets its own baseline:
- hardened Windows, automatic security updates, inbound deny-all;
- reachable **only over Tailscale**; no RDP or other port open to the internet;
- holds only the **MT5 trade-only login**, no other secrets (the sops file stays the source of truth);
- where the broker supports IP allow-listing, only the VPS's static IP is allow-listed (§3).

## 6. Application controls

- **Risk manager is authoritative.** Default-deny; kill switch; daily-loss limits and two-stage sleeve and system drawdowns; per-venue (default ≤ 25% of equity), per-instrument and portfolio limits; inline data-age check on every order (spec M11, [16 §2.1–2.2](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
- **One command layer (`mt_api`).** The UI, Telegram and (later) MCP all issue typed, audited commands; none talks to brokers directly.
- **Confirmation levels are enforced by the server** ([02 §7.2](02-v1-architecture.md#72-commands-rest-write)): C1 needs a confirm token from the preview call; C2 a risk-preview hash bound to the exact command and a session re-authenticated within 12 h; C3 = C2 + Telegram approve + TOTP + cool-down.
- **Settings and risk limits** are layered L0 hard ceilings → L4 bot, and the strictest value wins ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)):
  - Tightening is immediate (bot-level settings take a C1 confirm).
  - **Loosening any setting, or switching a bot to `autonomous`, is C3:** a Telegram button plus a TOTP code, with a cool-down (default 15 min, configurable) before it takes effect.
  - **L0 hard ceilings** are edited in the ceilings section of the agent/bot strategy settings, which applies to every bot. Tightening is immediate; loosening is C3 like every other loosening. A lower layer can never exceed them.
  - Every change is a WORM version row (`risk.change`, `audit.command`); rollback is a new row.
  - **Before Telegram C3 exists (P0–P1):** C3 completes through a host-only break-glass CLI (`mtctl approve <id>` + TOTP over SSH on Tailscale), audited. It is retired once Telegram C3 works.
- **Telegram `/kill` without mt-api:** the bot's NATS credentials can publish only `kill.set`; the engine records the kill in WORM with source `telegram`.
- **MCP server (Phase 8, optional; [16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)):**
  - Streamable HTTP at `/mcp` behind Caddy on Tailscale/TLS, or stdio locally; OAuth 2.1 (PKCE, resource indicators) for clients that support it.
  - **Tokens:** opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped, revocable instantly, last use and client identity recorded. Expiry is chosen per token (1 day to 1 year, custom, or indefinite); indefinite shows a red warning, needs C3 and reminds you monthly.
  - It *can* place, modify and cancel orders and adjust or close positions, but only through `mt_api` → risk manager, like any other source.
  - **MCP orders always need your approval card** (Telegram/web, TTL default 5 min, expiry = reject). There is no "skip approval" option, and **MCP can never approve** anything itself.
  - **Never exposed:** withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key and token management, `approval.*`, `mcp.*`, restore/delete, audit writes. Loosening risk is never a scope.
  - **Response guard:** every `source = mcp` response is filtered like any model input: no Telegram text, no `model_input_ok = false` rows, tax PII (TFN, addresses, statements) redacted, secrets scrubbed, untrusted text wrapped and marked.
  - Every MCP call, reads included, is a WORM row in `audit.mcp_call`. Default limits: 60 reads/min and 10 writes/min per token.
  - Treat Claude conversations as able to be influenced by prompt injection (e.g. a pasted news article). That's why confirmation and risk checks don't rely on the model.
- **Dead-man's switch** (three layers, [16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)): the in-engine watchdog and the external `deadman` sidecar cancel open orders when a heartbeat is missing for 5 s and apply each bot's `on_system_failure` (default `flatten`) at 10 s (defaults, configurable); venue cancel-after timers and resting stops cover a dead host. Then alert.
- **WORM integrity:** a verify mismatch sets `audit.integrity`; by default (`block_new_entries`) no new entries, exits continue, and no loosening until you acknowledge with `audit.integrity.ack` (C3) after investigating (§8).
- **LLM safety:**
  - Scraped content is wrapped and marked untrusted.
  - Telegram text never reaches any model, RAG index or training set; it becomes deterministic postures only.
  - Agents have read-only data tools; their only output is a structured `Signal`.
  - Generated strategy code runs in a no-network, no-secrets sandbox (gVisor/`--network none`).
- **Idempotent orders:** the client order ID is `{bot}-{engine_epoch}-{seq}`, and a signal hash is stored separately and checked before submit, so retries or restarts can't duplicate orders.

## 7. Supply chain

- **Vendored code:**
  - Lives in `third_party/` with a pinned commit and its licence.
  - Every upstream bump is a reviewed diff.
  - Grep for telemetry, referral/broker IDs, `eval`/`exec`, network calls.
  - Known items from vetting:
    - Hummingbot metrics + broker IDs;
    - nofx GA telemetry + builder fees;
    - OpenMagpie PostHog;
    - RSS-Bridge default `enabled_bridges = *`;
    - MiroFish open CORS / default secret.
- **LiteLLM:** releases 1.82.7/1.82.8 were malicious (PyPI compromise, March 2026). Use ≥ 1.83, pinned by hash or image digest; give it only the API keys it needs; keep it on the internal network.
- **Python:** `uv lock` with hashes; Dependabot/Renovate on the private repo; `pip-audit` in CI.
- No `curl | sh` installers; build from source or pinned images.
- **Rust components** (Nautilus extensions, signer): `cargo vet` + `cargo deny` (licences, advisories, duplicate crates).
- **Malicious-repo awareness:** check new trading-bot / wallet repos against the SlowMist and similar malicious-repo lists before cloning; fake "arbitrage bot" repos with drainer payloads are common. Never run cloned bot code outside the sandbox.

## 8. Data protection, backups & audit

- **Postgres:**
  - Encrypted at rest (disk) and in backups.
  - pgBackRest: continuous WAL archive, nightly incremental, weekly full, to an off-site encrypted target (e.g. Backblaze B2 / another box via restic). No separate `pg_dump`: the monthly immutable WORM export covers logical exports.
  - **Restore tested monthly** by an automated job.
- **WORM records** ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)): offline `worm_owner`, INSERT/SELECT-only app roles, blocking triggers, per-row hash chain, daily Merkle seal anchored to object-locked storage (+ optional OpenTimestamps, Telegram witness), immutable backups and monthly immutable exports.
- **On a verify mismatch** ([16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)): `audit.verify` sets `audit.integrity` in NATS KV, which M11 reads before every trade. The default action is `block_new_entries` (critical alert on every channel; no new entries; exits and protective orders continue; no risk loosening); options are `alert_only` and `halt_all`. You clear it with `audit.integrity.ack` (C3) after investigating. Every incident and ack is a WORM row (`audit.integrity_incident`).
- **The audit log is append-only:**
  - `audit.*` (e.g. `audit.order`, `audit.fill`, `audit.command`), `risk.change` and `journal.*` use insert-only DB roles; names follow [02 §4](02-v1-architecture.md#4-logical-components).
  - A per-row hash chain plus daily seals lets edits be detected.
  - Acknowledgements and corrections are new rows (e.g. `audit.dq_ack`), never updates.
  - Tax records need ≥ 5-year retention (Australia), so retention is set to 7 years.
- **Tax-sensitive data** (TFN, addresses, statements) is encrypted at column level (`pgcrypto`) and excluded from LLM prompts and MCP responses.
- **Key rotation without breaking WORM:** envelope encryption. Each year has its own data key, wrapped by a master key; rows record which key encrypted them. Rotation re-wraps the data keys in a non-WORM key table and never re-encrypts or updates rows.

## 9. Monitoring & incident response

- **One alert path:** Grafana/Alertmanager alerts go by webhook to the single `alert.*` consumer, which fans out to Telegram, ntfy, email and the UI ([02 §6](02-v1-architecture.md#6-messaging-nats)).
  - P0 has no fan-out yet, so Alertmanager sends straight to Telegram until P1-T045 replaces that route.
  - The consumer's own egress allow-list adds only the Telegram Bot API and your SMTP host; the `obs` network has no Telegram egress once the fan-out exists ([02 §3.1](02-v1-architecture.md#31-networks)).
- **Email:** sent through your own mail provider's SMTP (TLS) with an app password kept in the secrets file; or turn email off (Telegram + ntfy remain).
- **ntfy:** self-hosted, Tailscale-only; iOS push goes via ntfy's upstream relay, which carries only a message ID.
- **Alerts (Telegram + email + self-hosted ntfy push as the second, independent channel; Twilio SMS is an optional paid upgrade):**
  - kill-switch trigger; dead-man action;
  - risk breach; drawdown stage reached;
  - WORM verify mismatch;
  - egress IP/country mismatch or tunnel down;
  - feed stale / data-quality failure;
  - unusual order rate;
  - new wallet approval;
  - login to the host;
  - key-age expiry;
  - backup failure.
- **Runbook in `docs/runbooks/`:**
  - "Keys leaked": revoke keys at the exchange, rotate, check withdrawals.
  - "Server down with open positions": check the venue timers cancelled orders and the resting stops are in place; broker web UI → flatten if needed; kill switch; restart flat with bots paused.
  - "Bad data": downgrade autonomous bots to `hitl` or pause them, switch feeds.
  - "Wallet drained": hot, identity and burner wallets are isolated and capped, so revoke approvals and sweep what's left to the vault.
  - "WORM verify mismatch": find the cause (corruption, bad restore, tampering) before `audit.integrity.ack`.

## 10. Social & scraping accounts

- **Separate identities:**
  - Telegram: a dedicated number (landline or prepaid), 2FA password, encrypted session file.
  - Discord: a bot application in your own server.
  - Reddit, if approved: a dedicated account.
- Read-only behaviour, slow joins, no posting or engagement automation. Airdrop social tasks are **queued for the user**, never botted.
