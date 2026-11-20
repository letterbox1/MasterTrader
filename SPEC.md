# MasterTrader — Specification (summary)

**Usage:**
- Private, single-user, personal use.
- GPL/AGPL is allowed, because nothing is distributed or served to others.
- **Free data and free tiers only.**
- Australian tax resident, with a possible later move to the UAE, Egypt or Cyprus.

**Detailed docs:**
- [docs/03-build-spec.md](docs/03-build-spec.md): full module spec M0–M23.
- [docs/04-plan-of-action.md](docs/04-plan-of-action.md): phased plan; detailed per-phase scope, ToDos and traceability in [docs/roadmap/](docs/roadmap/README.md); execution tracked on per-phase kanbans in [tracking/](tracking/README.md), rolled up in [KANBAN.md](KANBAN.md).
- [docs/07-security-notes.md](docs/07-security-notes.md)
- [docs/08-airdrops-and-token-launches.md](docs/08-airdrops-and-token-launches.md)
- [docs/09-journal-and-tax.md](docs/09-journal-and-tax.md)
- [docs/12-policy-and-compliance.md](docs/12-policy-and-compliance.md), [docs/13-wallets-treasury-and-onchain.md](docs/13-wallets-treasury-and-onchain.md), [docs/14-strategy-evidence-and-validation.md](docs/14-strategy-evidence-and-validation.md): added from the CryptoTrader review ([docs/11](docs/11-cryptotrader-crossover-review.md)).
- [docs/15-bots-hitl-and-worm-audit.md](docs/15-bots-hitl-and-worm-audit.md): trading bots (paper / HITL / autonomous) and WORM records.
- [docs/16-configuration-and-safety-model.md](docs/16-configuration-and-safety-model.md): configuration layers, **every default value**, failure safety. Where another doc quotes a number, 16 is the reference.
- [docs/17-decisions-register.md](docs/17-decisions-register.md): the decision for every planning gap.
- [docs/02-v1-architecture.md](docs/02-v1-architecture.md): architecture overview.
- [docs/18-platform-and-deployment.md](docs/18-platform-and-deployment.md): **platform and deployment (canonical for the stack):** Rust first, Python where necessary, Supabase Postgres, the web app served locally or on Vercel, deployment modes, regions, workstation-first build path. Where 02 or 03 differ on the stack, 18 wins.
- [docs/19-third-party-register.md](docs/19-third-party-register.md): **third-party register:** every outside component with its language, licence, how we use it, and what an open-source or commercial release would need (copyleft items flagged ⚑).
- [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md) and [docs/06](docs/06-aggregators-and-market-providers.md): justify the component choices.
- [docs/05](docs/05-saas-legal-and-licensing.md): what a SaaS would require.

## Core decisions

| Area | Decision |
|---|---|
| Platform stance | **Strategy-agnostic, any timeframe** (tick/L2 → 1D+). Strategies, risk limits and preferences are user inputs (M0) |
| Languages | **Rust for everything we write**, including the designs we borrow from other projects ([17 §H](docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)): services, strategies (Rust by default), agents, NLP, features, the model runtime, data connectors, the job scheduler, the lab harness and the simulator (Cargo workspace in `crates/`, crate list in [18 §2.1](docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)). **Python only where absolutely required:** ML training and exploration (`mt_research`), trafilatura extraction (`mt_extract`), the Telethon reader (`mt_telegram_reader`), ccxt ledger import (`mt_ledger_import`) and the MT5 bridge (uv workspace in `packages/`). Python never places orders, signs or sits on the live decision path ([18 §2](docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary)). Third-party services run unmodified, whatever their language ([19](docs/19-third-party-register.md)) |
| Deployment | **Workstation first:** Phases 0–6 build, test and paper-trade on your workstation (Mode 1, free). Before live money, Phase 7 shifts to the runtime host you choose (default: stay on the workstation) and can optionally move the web app to **Vercel** and the database to **Supabase cloud** (Mode 2). Always-on trading services never run on Vercel. One region (Sydney) by default ([18 §5–9](docs/18-platform-and-deployment.md#5-deployment-modes)) |
| Execution / backtest core | **NautilusTrader** (Rust core): the same code runs backtest, paper and live. Rust live node where the venue's Rust adapter is production-ready (U, per venue), otherwise the Python node; `mt-risk` is linked in either way. Custom adapters for Alpaca, OANDA, IG (optional cTrader/Saxo/MT5) |
| Risk | Built-in **risk manager** (M11): default-deny; tighten-only configuration layers L0–L4 with defaults ([16](docs/16-configuration-and-safety-model.md)); sizing models; two-stage drawdowns; kill switch; **three-layer dead-man's switch** (in-engine, external `deadman` sidecar, venue-side timers + resting stops); tighten instantly, loosen C3 (Telegram + TOTP + cool-down) |
| Market-making sidecar | **Hummingbot** (telemetry off), run unmodified and driven from Rust (`mt-mm-adapter`) through the Hummingbot API |
| AI decision layer | **TradingAgents**-style debate and a **FinRobot**-style valuation desk, rebuilt in Rust: `mt-agents` on `rig-core` (explicit state-machine graph, Postgres checkpoints; prompts adapted with their NOTICE). Every model call goes through the LiteLLM gateway |
| Research lab | **Production harness in Rust** (`mt-lab-core`: walk-forward and validation, gate reports, cost models, clean-room look-ahead/recursive bias analysers, setup odds) driving Nautilus truth backtests with **measured costs**; **exploration and training in Python** (`mt_research`: notebooks, Optuna, MLflow client) through a PyO3 binding; Vibe-Trading-style screener and a sandboxed LLM generator that emits Rust strategies; **MLflow** experiment tracking |
| Scenario & crowd simulator | **M14 `mt-crowdsim`** (clean-room Rust, no MiroFish/OASIS code): persona crowds turn an event into simulated price, volatility, spread and liquidity shocks. A **scenario twin** paper engine runs the same bots under them during the paper period (weekly report per bot), and they join the pre-live stress tests. It never trades; its synthetic data never reaches features, training or RAG ([18 §2.4](docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool)) |
| Live monitoring | **M16:** always-on data-quality and cost/TCA monitor with venue reconciliation. It feeds the risk manager and the backtest cost models |
| Storage | **Supabase Postgres + pgvector** (system of record; local via the Supabase CLI or self-hosted on the workstation, optionally Supabase cloud; SQL migrations in `supabase/`). Bars at every size in monthly native partitions, no TimescaleDB ([18 §4.3](docs/18-platform-and-deployment.md#43-bars-without-timescaledb)); **Nautilus Parquet catalog + DuckDB** (raw ticks/L2, older bars) |
| Observability & audit | **Grafana + Loki + Prometheus + Vector + OpenTelemetry**; WORM audit tables (`audit.order`, `audit.fill`, `audit.command`, `audit.llm_call` from P0, `audit.mcp_call`, …) |
| Journal & tax | In-house jurisdiction-pluggable engine (rp2/ledger ideas): **AU_2026**, **AU_2027_REFORM**, AE, EG, CY; PAYG-instalment estimator; Beancount/hledger audit export |
| Memory / RAG | **Hindsight** (self-hosted, our Postgres, local TEI embedder bge-small + reranker) + hybrid document RAG in Postgres (pgvector + tsvector, RRF, rerank, point-in-time); LightRAG optional later |
| Decision One & models | **Tier A:** in-process compiled GBDT (~10–50 µs) in the order path. **Tier B: decision models** (no text generation; SemIf readout → own Qwen3 + LoRA + classification head, ~2–12 ms on GPU) for text/context judgements, feeding tier A. Jev / Microsoft-Decision-1 excluded (closed, paid); Laya and Clef-flash benchmarked. Big-model decisions distilled into both. Research/chat via the **LiteLLM gateway** (Claude / custom endpoint / local fallback, budgets) |
| News & social | RSS + RSS-Bridge, GDELT, Telegram (Telethon + Bot API, **postures only**: Telegram API ToS bars AI on Telegram data), Discord (own server + followed announcement channels), Bluesky, Mastodon, Farcaster, CryptoPanic. **Reddit optional; X deferred** |
| Policy & compliance | AU retail boundary; **venue access registry** (AUSTRAC check quarterly, products per residency); **2× crypto-derivatives cap**; explicit **STP** on every order; Travel Rule pre-registered addresses; Polymarket/Kalshi read-only. See [12](docs/12-policy-and-compliance.md) |
| Data provenance | Every row carries seven columns: `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`; training and inference (incl. MCP responses) refuse disallowed rows |
| Wallets & treasury | Custody tiers (vault / HL master / warm / hot / identity / burner), **intents-only signer**, durable-nonce hard block, unified wallet view, **M22 hold-and-earn**, on-chain cost gate, Anvil simulation, Blockscout for decisions. See [13](docs/13-wallets-treasury-and-onchain.md) |
| Strategy evidence | Evidence-ranked catalogue (P1/P2/P3/X/never) with the counterparty rule, sleeves, fallback ladder, extended validation, capital steps and kill criteria; MasterTradingBot shares libraries. See [14](docs/14-strategy-evidence-and-validation.md) |
| Social participation | **M23** (optional): drafts only, approved by you, posted via web intent from your own account |
| Global events | GDELT/USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP + Kalshi/Polymarket probabilities |
| Airdrops / launches | Vet (GoPlus, RugCheck, Honeypot.is, blocklists, rug-pull heuristics) → auto-claim only for eligible claims from the chain's mandate-bound **airdrop identity wallet** → everything else becomes user tasks |
| Curation | **One task queue** for social tasks, Discord/Telegram servers and channels to follow, manual claims, and approvals; daily and weekly digests with Telegram buttons |
| Command layer | **`mt-api`** (Rust, axum, OpenAPI): every action (UI, Telegram, later MCP) is a typed, audited command. Login is **Supabase Auth** (password + TOTP; commands need the MFA level `aal2`); the browser never reads the database directly ([18 §4.5–4.6](docs/18-platform-and-deployment.md#45-access-rules)) |
| Web app | React + TypeScript SPA (`apps/web`), built once; served locally by Caddy or deployed to Vercel (`web.host`, [16 §2.15](docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)) |
| Trading bots | A **bot** = strategy version × market scope (instrument, list or dynamic selection) × venue/sleeve × mode. Modes `paper` / `hitl` / `autonomous` per bot: paper → HITL is C2; **autonomous** is C3, gates required, auto-downgrade on decay/DQ; **HITL** sends Telegram approval cards (TTL, protective exits automatic). See [15](docs/15-bots-hitl-and-worm-audit.md) |
| MCP | **Last (Phase 8), optional.** A thin adapter (`mt-mcp`, Rust) over `mt-api`: read/analyse, talk to agents, **trade and adjust positions**, strategies, risk, curation. Orders go through the risk manager and **always** need your approval card; MCP can never approve, and the never-exposed list is in [16 §2.12](docs/16-configuration-and-safety-model.md#212-mcp-phase-8) |
| Rejected | VibeTradingLabs/vibetrading, nofx as a platform, threads-scraper, log, Spacebar, Graylog, OpenObserve, TDengine, ArcticDB, Soda Core, paid data |

## Non-negotiable requirements

1. **Point-in-time data:** `event_time` + `ingest_time`; research reads only via `pit(as_of)`.
2. **Every order passes through the risk manager,** whatever its source (strategy, agent, UI, Telegram, MCP).
3. **No trading on bad data:** a DQ failure pauses the affected bots, and M11 checks data age inline on every order.
4. **Sandboxed generated code** (no network, no secrets).
5. **Exchange keys:**
   - withdrawals disabled;
   - IP allow-listed to one fixed AU egress IP;
   - separate sub-accounts per mode.
6. **Autonomous claims only from the airdrop identity wallet** (never the hot trading wallet):
   - signed mandates;
   - simulation before every signature;
   - never permits/approvals.
7. **WORM audit and journal** (write-once: offline owner role, blocking triggers, per-row hash chain, externally anchored daily seals, immutable backups), kept ≥ 7 years, verified daily; a verify mismatch blocks new entries by default until you acknowledge it (C3).
8. **No telemetry or referral tags** in vendored components; the repo stays private.
9. **Promotion gates** before live capital: out-of-sample after measured costs, robustness statistics (deflated Sharpe ≥ 0.95), a clean look-ahead check, a paper/HITL period (default ≥ 8 weeks and ≥ 50 trades), safety drills ([03 §8](docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)).
10. **Data terms are enforced by provenance tags:** no Telegram text (or any `model_input_ok = false` row) reaches a model, RAG index or training set.
11. **Only `allowed` venues/products** for your current residency; explicit STP on every order where the venue supports it; no wash trading, spoofing, VPNs or multiple KYC accounts.
12. **Settings, not constants:** every limit, threshold, allocation and timer is a default you change in settings ([16](docs/16-configuration-and-safety-model.md)); tightening is immediate, loosening is C3.
13. **Fail flat:** a down engine, host or network leaves no unprotected exposure (three-layer dead-man, resting venue stops, restart flat with bots paused).

## Phases

| # | Phase |
|---|---|
| 0 | Foundations & security baseline |
| 1 | Market data, recording & live monitoring |
| 2 | Strategy framework, risk manager & research lab |
| 3 | Journal & tax |
| 4 | News, social, events & calendars |
| 5 | Airdrops, launches & curation queue |
| 6 | AI decision layer, memory & anomalies |
| 7 | Prove it, then go small-live (opens after Phase 3; hard-gated). Includes the go-live pack approval and the shift to the runtime host before any live money |
| 8 | MCP control plane (optional, last; hard-gated) |

Tasks run in parallel by dependency across phases, each claimed by one agent and independently reviewed before it's done; Phases 7 and 8 wait for their prerequisite phases ([17 §E](docs/17-decisions-register.md#e-ratification-2026-10-22)). Everything up to Phase 7 builds and runs on your workstation: no dedicated host, LUKS, Tailscale, YubiKey or GPU is needed before then ([18 §9](docs/18-platform-and-deployment.md#9-workstation-first-build-path)).
