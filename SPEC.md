# MasterTrader — Specification (summary)

**Usage:**
- Private, single-user, personal use.
- GPL/AGPL is allowed, because nothing is distributed or served to others.
- **Free data and free tiers only.**
- Australian tax resident, with a possible later move to the UAE, Egypt or Cyprus.

**Detailed docs:**
- [docs/03-build-spec.md](docs/03-build-spec.md): full module spec M0–M23.
- [docs/04-plan-of-action.md](docs/04-plan-of-action.md): phased plan.
- [docs/07-security-notes.md](docs/07-security-notes.md)
- [docs/08-airdrops-and-token-launches.md](docs/08-airdrops-and-token-launches.md)
- [docs/09-journal-and-tax.md](docs/09-journal-and-tax.md)
- [docs/12-policy-and-compliance.md](docs/12-policy-and-compliance.md), [docs/13-wallets-treasury-and-onchain.md](docs/13-wallets-treasury-and-onchain.md), [docs/14-strategy-evidence-and-validation.md](docs/14-strategy-evidence-and-validation.md): added from the CryptoTrader review ([docs/11](docs/11-cryptotrader-crossover-review.md)).
- [docs/02-v1-architecture.md](docs/02-v1-architecture.md): architecture overview.
- [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md) and [docs/06](docs/06-aggregators-and-market-providers.md): justify the component choices.
- [docs/05](docs/05-saas-legal-and-licensing.md): what a SaaS would require.

## Core decisions

| Area | Decision |
|---|---|
| Platform stance | **Strategy-agnostic, any timeframe** (tick/L2 → 1D+). Strategies, risk limits and preferences are user inputs (M0) |
| Execution / backtest core | **NautilusTrader**: the same code runs backtest, paper and live. Custom adapters for Alpaca, OANDA, IG (optional cTrader/Saxo/MT5) |
| Risk | Built-in **risk manager** (M11): default-deny; multi-level limits; sizing models; kill switch; dead-man's switch; tighten instantly, loosen with Telegram + TOTP |
| Market-making sidecar | **Hummingbot** (telemetry off) |
| AI decision layer | **TradingAgents** debate pattern on LangGraph + **FinRobot V2** valuation operators |
| Research lab | Nautilus truth backtests with **measured costs**; Vibe-Trading-style screener and validation; vendored freqtrade look-ahead analysers; Optuna; **MLflow** experiment tracking |
| Live monitoring | **M16:** always-on data-quality and cost/TCA monitor with venue reconciliation. It feeds the risk manager and the backtest cost models |
| Storage | **Postgres + TimescaleDB + pgvector** (system of record, bars at every size); **Nautilus Parquet catalog + DuckDB** (raw ticks/L2) |
| Observability & audit | **Grafana + Loki + Prometheus + Vector + OpenTelemetry**; append-only, hash-chained audit tables (orders, fills, LLM calls, risk changes, commands) |
| Journal & tax | In-house jurisdiction-pluggable engine (rp2/ledger ideas): **AU_2026**, **AU_2027_REFORM**, AE, EG, CY; PAYG-instalment estimator; Beancount/hledger audit export |
| Memory / RAG | **Hindsight** (self-hosted, our Postgres, local TEI embedder bge-small + reranker) + hybrid document RAG in Postgres (pgvector + tsvector, RRF, rerank, point-in-time); LightRAG optional later |
| Decision One & models | **Tier A:** in-process compiled GBDT (~10–50 µs) in the order path. **Tier B: decision models** (no text generation; SemIf readout → own Qwen3 + LoRA + classification head, ~2–12 ms on GPU) for text/context judgements, feeding tier A. Jev / Microsoft-Decision-1 excluded (closed, paid); Laya and Clef-flash benchmarked. Big-model decisions distilled into both. Research/chat via the **LiteLLM gateway** (Claude / custom endpoint / local fallback, budgets) |
| News & social | RSS + RSS-Bridge, GDELT, Telegram (Telethon + Bot API, **postures only**: Telegram API ToS bars AI on Telegram data), Discord (own server + followed announcement channels), Bluesky, Mastodon, Farcaster, CryptoPanic. **Reddit optional; X deferred** |
| Policy & compliance | AU retail boundary; **venue access registry** (AUSTRAC check quarterly, products per residency); **2× crypto-derivatives cap**; explicit **STP** on every order; Travel Rule pre-registered addresses; Polymarket/Kalshi read-only. See [12](docs/12-policy-and-compliance.md) |
| Data provenance | Every row tagged `train_ok` / `model_input_ok` / `display_ok` / `retention_days` / `commercial_ok`; training and inference refuse disallowed rows |
| Wallets & treasury | Custody tiers (vault / HL master / warm / hot / identity / burner), **intents-only signer**, durable-nonce hard block, unified wallet view, **M22 hold-and-earn**, on-chain cost gate, Anvil simulation, Blockscout for decisions. See [13](docs/13-wallets-treasury-and-onchain.md) |
| Strategy evidence | Evidence-ranked catalogue (P1/P2/P3/X/never) with the counterparty rule, sleeves, fallback ladder, extended validation, capital steps and kill criteria; MasterTradingBot shares libraries. See [14](docs/14-strategy-evidence-and-validation.md) |
| Social participation | **M23** (optional): drafts only, approved by you, posted via web intent from your own account |
| Global events | GDELT/USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP + Kalshi/Polymarket probabilities |
| Airdrops / launches | Vet (GoPlus, RugCheck, Honeypot.is, blocklists, rug-pull heuristics) → auto-claim only for eligible claims on a mandate-bound hot wallet → everything else becomes user tasks |
| Curation | **One task queue** for social tasks, Discord/Telegram servers and channels to follow, manual claims, and approvals; daily and weekly digests with Telegram buttons |
| Command layer | **`mt_api`**: every action (UI, Telegram, later MCP) is a typed, audited command |
| MCP | **Last (Phase 8), optional.** A thin adapter over `mt_api`: read/analyse, talk to agents, **trade and adjust positions**, strategies, risk, curation. Orders go through the risk manager and default to approve mode |
| Rejected | VibeTradingLabs/vibetrading, nofx as a platform, threads-scraper, log, Spacebar, Graylog, OpenObserve, TDengine, ArcticDB, Soda Core, paid data |

## Non-negotiable requirements

1. **Point-in-time data:** `event_time` + `ingest_time`; research reads only via `pit(as_of)`.
2. **Every order passes through the risk manager,** whatever its source (strategy, agent, UI, Telegram, MCP).
3. **No trading on bad data:** a DQ failure pauses the affected strategies.
4. **Sandboxed generated code** (no network, no secrets).
5. **Exchange keys:**
   - withdrawals disabled;
   - IP allow-listed;
   - separate sub-accounts per mode.
6. **Hot wallet only for autonomous claims:**
   - signed mandates;
   - simulation before every signature;
   - never permits/approvals.
7. **Append-only audit and journal,** kept ≥ 7 years, with tested backups.
8. **No telemetry or referral tags** in vendored components; the repo stays private.
9. **Promotion gates** before live capital: out-of-sample after measured costs, robustness statistics, a clean look-ahead check, a paper/approve period.
10. **Data terms are enforced by provenance tags:** no Telegram text (or any `model_input_ok = false` row) reaches a model, RAG index or training set.
11. **Only `allowed` venues/products** for your current residency; explicit STP on every order; no wash trading, spoofing, VPNs or multiple KYC accounts.

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
| 7 | Prove it, then go small-live |
| 8 | MCP control plane (optional, last) |
