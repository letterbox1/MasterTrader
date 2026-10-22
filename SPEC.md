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
- [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md) and [docs/06](docs/06-aggregators-and-market-providers.md): justify the component choices.
- [docs/05](docs/05-saas-legal-and-licensing.md): what a SaaS would require.

## Core decisions

| Area | Decision |
|---|---|
| Platform stance | **Strategy-agnostic, any timeframe** (tick/L2 → 1D+). Strategies, risk limits and preferences are user inputs (M0) |
| Execution / backtest core | **NautilusTrader**: the same code runs backtest, paper and live. Custom adapters for Alpaca, OANDA, IG (optional cTrader/Saxo/MT5) |
| Risk | Built-in **risk manager** (M11): default-deny; tighten-only configuration layers L0–L4 with defaults ([16](docs/16-configuration-and-safety-model.md)); sizing models; two-stage drawdowns; kill switch; **three-layer dead-man's switch** (in-engine, external `deadman` sidecar, venue-side timers + resting stops); tighten instantly, loosen C3 (Telegram + TOTP + cool-down) |
| Market-making sidecar | **Hummingbot** (telemetry off) |
| AI decision layer | **TradingAgents** debate pattern on LangGraph + **FinRobot V2** valuation operators |
| Research lab | Nautilus truth backtests with **measured costs**; Vibe-Trading-style screener and validation; freqtrade look-ahead analysers (GPL, vendored under `third_party/`, isolated in `mt_lab`; personal use); Optuna; **MLflow** experiment tracking |
| Live monitoring | **M16:** always-on data-quality and cost/TCA monitor with venue reconciliation. It feeds the risk manager and the backtest cost models |
| Storage | **Postgres + TimescaleDB + pgvector** (system of record, bars at every size); **Nautilus Parquet catalog + DuckDB** (raw ticks/L2) |
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
| Command layer | **`mt_api`**: every action (UI, Telegram, later MCP) is a typed, audited command |
| Trading bots | A **bot** = strategy version × market scope (instrument, list or dynamic selection) × venue/sleeve × mode. Modes `paper` / `hitl` / `autonomous` per bot: paper → HITL is C2; **autonomous** is C3, gates required, auto-downgrade on decay/DQ; **HITL** sends Telegram approval cards (TTL, protective exits automatic). See [15](docs/15-bots-hitl-and-worm-audit.md) |
| MCP | **Last (Phase 8), optional.** A thin adapter over `mt_api`: read/analyse, talk to agents, **trade and adjust positions**, strategies, risk, curation. Orders go through the risk manager and **always** need your approval card; MCP can never approve, and the never-exposed list is in [16 §2.12](docs/16-configuration-and-safety-model.md#212-mcp-phase-8) |
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
| 7 | Prove it, then go small-live (opens after Phase 3; hard-gated) |
| 8 | MCP control plane (optional, last; hard-gated) |

Tasks run in parallel by dependency across phases, each claimed by one agent and independently reviewed before it's done; Phases 7 and 8 wait for their prerequisite phases ([17 §E](docs/17-decisions-register.md#e-ratification-2026-10-22)).
