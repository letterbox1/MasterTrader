# Phase 0 · Foundations & Security Baseline

| | |
|---|---|
| **Goal** | A secure, reproducible single-box stack with the system of record, the audit chain, the `mt_api` command layer and the web shell, so every later phase plugs into it. |
| **Duration** | Weeks 1–2 (plus the "do now" account actions, which run in parallel and gate later phases) |
| **Depends on** | Nothing |
| **Unlocks** | Every other phase |
| **Modules** | `mt_core`, `mt_store`, `mt_api`, M17 observability & audit, M21 gateway pieces (LiteLLM, TEI), M15 shell |
| **Containers** | `caddy`, `mt-api`, `postgres`, `nats`, `prefect-*`, `grafana`/`loki`/`prometheus`/`vector`/`alertmanager`, `mlflow`, `litellm`, `tei` ([02 §3.2](../02-v1-architecture.md#32-containers)) |
| **Dashboards** | App shell + [D16](../ui/dashboards/D16-system.md) System |
| **Primary docs** | [03 §3](../03-build-spec.md#3-repository-layout) · [03 §4](../03-build-spec.md#4-data-model-overview) · [03 M17](../03-build-spec.md#m17-observability--audit--mt_obs) · [02 §7](../02-v1-architecture.md#7-api-contract-mt_api) · [07](../07-security-notes.md) · [DESIGN §6](../../DESIGN.md#6-responsive-system-1920px--240px-portrait--landscape) · [ui §2](../ui/README.md#2-app-shell-all-routes) |

## 1. Scope

**In:** host hardening, the Compose stack, schemas and migrations (including provenance columns and the venue registry table), `pit(as_of)`, the append-only audit chain, secrets, backups and restore tests, the `mt_api` skeleton (auth, commands, confirmation levels, WebSocket), the model gateway and embedder, the web shell and the System dashboard, CI.

**Out (later phases):** any market data (P1), strategies and risk logic (P2), Telegram bot features (alerts P1, commands P2).

## 2. Entry criteria

- The host hardware exists (T0.01). Everything else can start on a laptop and move over.

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R0.01 | `uv` workspace monorepo with the package layout of 03 §3; ruff, mypy, pytest, pre-commit with gitleaks | [03 §3](../03-build-spec.md#3-repository-layout) | CI green |
| R0.02 | Compose stack with every image **pinned by digest**; all services healthy on `docker compose up` | [03 §2](../03-build-spec.md#2-target-environment), [07 §5](../07-security-notes.md#5-network--host) | Health checks |
| R0.03 | Postgres schemas `market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops` via Alembic | [03 §4](../03-build-spec.md#4-data-model-overview), [02 §5.1](../02-v1-architecture.md#51-stores) | Migration test |
| R0.04 | Every fact carries `event_time` + `ingest_time`; research reads only via `mt_store.pit(as_of)`; **CI fails on bypass** | [SPEC NN1](../../SPEC.md#non-negotiable-requirements), [03 §4](../03-build-spec.md#4-data-model-overview) | `pit` CI test |
| R0.05 | Ingest tables carry provenance columns `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok` (populated from P1) | [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) | Schema test |
| R0.06 | `ops.venue_registry` table exists and is seeded from your venue checks | [12 §2](../12-policy-and-compliance.md#2-venue-access-registry) | Seed present |
| R0.07 | **WORM** audit/journal tables: offline `worm_owner`, INSERT/SELECT-only app roles, UPDATE/DELETE/TRUNCATE blocked by triggers, **per-row hash chain**, daily Merkle seal anchored outside the DB (object-locked/append-only storage, optional OpenTimestamps, Telegram witness), corrections as new rows; verify mismatch halts trading | [15 §2](../15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many), [03 M17](../03-build-spec.md#m17-observability--audit--mt_obs), [07 §8](../07-security-notes.md#8-data-protection-backups--audit) | WORM test suite |
| R0.08 | `mt_api`: Argon2 login + **TOTP**, session cookie, `POST /commands/{command}` with idempotency key, every command written to `audit.command`; **C0–C3/Kill enforced server-side**; WebSocket envelope `{topic, seq, ts, data}` | [02 §7](../02-v1-architecture.md#7-api-contract-mt_api), [02 §7.2](../02-v1-architecture.md#72-commands-rest-write) | API tests |
| R0.09 | LiteLLM ≥ 1.83 pinned by digest (Claude, your custom endpoint, a local model), per-role budgets; TEI with bge-small-en-v1.5 + bge-reranker-v2-m3 | [10 §5](../10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21), [10 §2](../10-memory-rag-and-models.md#2-local-embedders--rerankers) | Smoke calls |
| R0.10 | Structured logs (structlog) with `trace_id`; Loki/Prometheus/Grafana showing host, DB and NATS health | [03 M17](../03-build-spec.md#m17-observability--audit--mt_obs) | Grafana board |
| R0.11 | Web shell (top bar, nav, status bar, kill-switch placeholder) and D16 System on the DESIGN.md v2 Tailwind preset | [ui §2](../ui/README.md#2-app-shell-all-routes), [D16](../ui/dashboards/D16-system.md), [DESIGN §6.3](../../DESIGN.md#63-tailwind-configuration-use-in-every-implementation-and-mock-up) | Playwright |
| R0.N1 | **Secrets:** `sops` + `age` decrypted into tmpfs; age key off the backup disk; no secret in git | [07 §2](../07-security-notes.md#2-secrets) | gitleaks, review |
| R0.N2 | **Host:** LUKS, deny-inbound firewall, SSH keys only, **Tailscale-only access**, chrony | [07 §5](../07-security-notes.md#5-network--host) | Host checklist |
| R0.N3 | **Network segmentation:** scrapers/RSS-Bridge network has no route to the DB or signer | [02 §3.1](../02-v1-architecture.md#31-networks) | Port scan |
| R0.N4 | **Backups:** pgBackRest + restic to an encrypted off-site target; automated restore test | [07 §8](../07-security-notes.md#8-data-protection-backups--audit), [02 F11](../02-v1-architecture.md#8-end-to-end-flows) | Restore test passes |
| R0.N5 | Vendored code under `third_party/` with pinned commit + `LICENSES.md`; images scanned (trivy/grype) | [07 §7](../07-security-notes.md#7-supply-chain), [03 §9](../03-build-spec.md#9-future-proof-hygiene) | CI scan |
| R0.N6 | Responsive shell passes the viewport matrix 240 → 2560 px, portrait + landscape | [DESIGN §6.8](../../DESIGN.md#68-test-matrix-every-screen-must-pass) | Playwright matrix |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T0.01** `USER` Provision the host: 8–16 cores, 32–64 GB RAM, 2–4 TB NVMe + HDD; decide on a **16–24 GB GPU** now (it shapes P4/P6 speed). → R0.02 · [03 §2](../03-build-spec.md#2-target-environment)
- [ ] **T0.02** `USER` Order a **UPS** and a **4G failover** router (needed before live, cheap to set up early). → [07 §5](../07-security-notes.md#5-network--host)
- [ ] **T0.03** `USER` Create the Tailscale account with MFA on the identity provider; buy/assign a YubiKey (or OS keychain) for the age key. → R0.N1, R0.N2
- [ ] **T0.04** `USER` Open the off-site backup target with **Object Lock** (e.g. Backblaze B2 compliance mode) or a second box running restic `rest-server --append-only`; store credentials in the secrets file. → R0.N4, R0.07
- [ ] **T0.05** `USER` Keep the GitHub repo **private**; turn on secret scanning. → [SPEC NN8](../../SPEC.md#non-negotiable-requirements)
- [ ] **T0.06** `USER` **Telegram:** dedicated number (landline voice code or prepaid SIM), `api_id`/`api_hash`, 2-step password, bot via @BotFather. → gates P1 alerts, P4 ingest · [07 §10](../07-security-notes.md#10-social--scraping-accounts)
- [ ] **T0.07** `USER` **Discord:** private "MasterTrader Feeds" server with `#mt-inbox` + category channels; bot app with Message Content intent; start following announcement channels you already know. → gates P4 · [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)
- [ ] **T0.08** `USER` ⚠️ **Reddit (optional): apply before 2026-10-31.** X stays deferred. → [06 §0](../06-aggregators-and-market-providers.md#0-️-time-sensitive-actions)
- [ ] **T0.09** `USER` Free demo/practice accounts: OANDA practice, IG demo, Alpaca paper, IBKR paper, Binance + Bybit testnets. → gates P1/P2
- [ ] **T0.10** `USER` Free API keys: FRED, EIA, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Helius, Alchemy, GoPlus, Finnhub, CryptoPanic. → gates P1/P4/P5 · [06](../06-aggregators-and-market-providers.md)
- [ ] **T0.11** `USER` **Venue checks:** look up each AU venue you may use on the AUSTRAC register by ABN; note products available to you as a retail client; send the results for the registry seed. → R0.06 · [12 §2](../12-policy-and-compliance.md#2-venue-access-registry)
- [ ] **T0.12** `USER` Set your login password and enrol TOTP on first boot. → R0.08

### B. Build (`BUILD`, code)
- [ ] **T0.20** `BUILD` Monorepo skeleton: `uv` workspace, all packages from 03 §3 as stubs, `third_party/LICENSES.md`, ruff/mypy/pytest/pre-commit (gitleaks). → R0.01, R0.N5
- [ ] **T0.21** `BUILD` `mt_core` types: Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent; config, clock, logging. → R0.01
- [ ] **T0.22** `BUILD` `mt_store`: schemas + Alembic migrations incl. provenance columns and `ops.venue_registry`; `pit(as_of)` API; Parquet catalog helpers. → R0.03–R0.06
- [ ] **T0.23** `BUILD` WORM layer: `worm_owner` role + grants, blocking triggers, per-row hash-chain trigger, correction rows, daily Merkle seal + external anchoring, `audit.verify` command and incident path. → R0.07 · [15 §2](../15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- [ ] **T0.24** `BUILD` `mt_api` skeleton (FastAPI): auth (Argon2 + TOTP), command bus with idempotency + `audit.command`, confirmation-level engine (C0–C3, Kill; C3 = approve + TOTP + cool-down), problem+json errors, OpenAPI, WebSocket hub with `seq` gap detection. → R0.08 · [02 §7.2](../02-v1-architecture.md#72-commands-rest-write)
- [ ] **T0.25** `BUILD` `mt_obs`: structlog JSON with `trace_id`, Prometheus metrics helpers, OpenTelemetry setup. → R0.10
- [ ] **T0.26** `BUILD` Web app: React + TS + Vite PWA, TanStack Router/Query, typed WS client, Tailwind **DESIGN.md v2 preset**, component library v0 (shell, tiles, data states), app shell, D16 System (health, services, backups, keys metadata, settings). → R0.11 · [02 §10](../02-v1-architecture.md#10-frontend-architecture) · [comp](../ui/components.md)

### C. Ops & config (`OPS`)
- [ ] **T0.40** `OPS` Host hardening: LUKS, firewall, SSH keys, auto security updates, Tailscale, chrony. → R0.N2
- [ ] **T0.41** `OPS` `docker-compose.yml` with digests: Postgres 16 + TimescaleDB (TSL) + pgvector + pg_trgm, NATS JetStream, Prefect, Grafana/Loki/Prometheus/Vector/Alertmanager, MLflow, Caddy, LiteLLM, TEI. → R0.02
- [ ] **T0.42** `OPS` Docker networks per 02 §3.1 (internal, scrapers, signer isolated). → R0.N3
- [ ] **T0.43** `OPS` `sops` + `age` secrets file → tmpfs at container start; per-service secret scoping. → R0.N1
- [ ] **T0.44** `OPS` pgBackRest + WAL archiving + restic off-site; Prefect flow for the monthly restore test. → R0.N4
- [ ] **T0.45** `OPS` LiteLLM config: model list (research-primary, research-custom, local-advisor, local-embed), per-role virtual keys and budgets. → R0.09 · [10 §5](../10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [ ] **T0.46** `OPS` Grafana provisioning: host, Postgres, NATS, container dashboards; Loki retention 30–90 days. → R0.10

### D. Verify & test (`VERIFY`)
- [ ] **T0.60** `VERIFY` `pit` bypass test in CI (a module reading raw tables fails the build). → R0.04
- [ ] **T0.61** `VERIFY` WORM test suite: app-role UPDATE/DELETE/TRUNCATE fail; a direct edit as `worm_owner` is caught by `audit.verify`; seal mismatch → incident + trading halt; restore from immutable backup re-verifies. → R0.07
- [ ] **T0.62** `VERIFY` Confirmation-level tests: a C3 command cannot apply without approval + TOTP + cool-down; Kill ON is never blocked. → R0.08
- [ ] **T0.63** `VERIFY` First restore test from the off-site backup to a scratch DB. → R0.N4
- [ ] **T0.64** `VERIFY` Playwright viewport matrix + axe on the shell and D16. → R0.N6
- [ ] **T0.65** `VERIFY` trivy/grype scan; external port scan shows nothing exposed outside Tailscale. → R0.N2, R0.N3, R0.N5

### E. Run / soak (`RUN`)
- [ ] **T0.80** `RUN` 72-hour idle soak: no restarts, backups ran, alerts quiet.

### F. Docs
- [ ] **T0.90** `BUILD` `docs/runbooks/`: backup & restore, host rebuild, secret rotation. → [07 §9](../07-security-notes.md#9-monitoring--incident-response)

## 5. Deliverables

Running stack · migrations · `mt_api` with OpenAPI · web shell + D16 · CI (lint, types, tests, `pit`, Playwright, scans) · first runbooks · seeded venue registry.

## 6. Exit criteria (demo)

1. `docker compose up` → all services healthy; Grafana shows host/DB/NATS health and logs in Loki.
2. Log in with password + TOTP; a test command appears in `audit.command` with a valid hash chain.
3. A restore from the off-site backup succeeds.
4. The shell passes the viewport matrix from 240 px to 2560 px.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| GPU decision delayed | Tier B and local models fall back to CPU (slower); decide by P4 |
| Hardware lead time | Start on a laptop/VM; the stack is portable |
| Reddit deadline (2026-10-31) | Optional; nothing in the plan depends on Reddit |
