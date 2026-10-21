# MasterTrader

A **private, proprietary, single-user** AI trading **platform** built from open-source parts, using **free data sources and free tiers only**. Currently in the **planning / research stage**.

MasterTrader is a platform, not a strategy. You set up and experiment with **any strategy type on any timeframe**, from tick/order-book level to daily and beyond. Under the hood it combines:
- NautilusTrader's execution and backtesting engine;
- a built-in, user-configurable risk manager;
- TradingAgents-style AI agents with FinRobot valuation tools;
- Vibe-Trading-style research tooling;
- Hummingbot market making.

Around that it adds:
- live data-quality and trading-cost monitoring;
- an automatic audit trail, trading journal and tax records (Australia now; UAE/Egypt/Cyprus pluggable);
- news, social (Telegram/Discord/Bluesky) and global-event feeds;
- vetted airdrop/launch tracking with a user task queue;
- optional Claude/MCP control, built last.

## Documents

| File | Contents |
|---|---|
| [GOAL.md](GOAL.md) | What we're building and why |
| [DESIGN.md](DESIGN.md) | **Design system v2:** tokens, type, components, and the full responsive system (1920px+ → 240px, portrait/landscape, laptops, tablets, foldables) |
| [docs/ui/](docs/ui/README.md) | **Frontend scope:** information architecture & routes, app shell, component library, 17 dashboard specs (widgets, data shown, actions + confirmation levels, states, acceptance criteria, backend contract), mobile/PWA/Telegram |
| [ui-examples/](ui-examples/README.md) | 13 Stitch reference screens (screenshots + HTML) with a responsive audit and content corrections |
| [brand/](brand/README.md) | Signal M logo, app icon, palette |
| [SPEC.md](SPEC.md) | v1 specification and core decisions |
| [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md) | Vetting of 10 open-source repos: licenses, code audit, reputation, overlap and redundancy, verdicts, and the supporting free data/memory/quant ecosystem |
| [docs/02-v1-architecture.md](docs/02-v1-architecture.md) | **End-to-end architecture v3:** deployment topology, networks & containers, module ownership, data stores, NATS subjects, `mt_api` REST/WS contract + confirmation levels + command catalogue, end-to-end flows, SLOs, degraded modes, frontend stack, phase-by-phase build plan |
| [docs/03-build-spec.md](docs/03-build-spec.md) | **Build spec v2:** ground rules (free only), stack, repo layout, modules M0–M20 (strategy framework, risk manager, live monitor, observability, journal/tax, curation, MCP), timeframes per asset class, gates |
| [docs/04-plan-of-action.md](docs/04-plan-of-action.md) | Phases 0–8 with checklists and a demo per phase (platform first, strategies second, MCP last) |
| [docs/05-saas-legal-and-licensing.md](docs/05-saas-legal-and-licensing.md) | What would change licence-, data- and regulation-wise if this ever became a SaaS |
| [docs/06-aggregators-and-market-providers.md](docs/06-aggregators-and-market-providers.md) | Aggregators, social sources and forex/macro providers: RSS-Bridge, Spacebar, threads-scraper, listeningkit, log, the social-scraping landscape, IG/cTrader/Saxo, calendars, central banks, nowcasts, retail sentiment, prediction markets. **Reddit and X are deferred; Telegram and Discord are the free social feeds** |
| [docs/07-security-notes.md](docs/07-security-notes.md) | Threat model, secrets, exchange keys (no withdrawals), wallet tiers, network, application controls (risk changes, MCP), supply chain, backups, incident runbooks |
| [docs/08-airdrops-and-token-launches.md](docs/08-airdrops-and-token-launches.md) | Airdrop/ICO/launch pipeline, rug-pull and scam vetting, what may run autonomously vs user tasks, Discord/community curation queue |
| [docs/09-journal-and-tax.md](docs/09-journal-and-tax.md) | Automatic journal and tax engine: AU EOFY/PAYG (incl. the reported 2027 CGT reform), UAE/Egypt/Cyprus plugins, residency timeline, tax-tool vetting |
| [docs/10-memory-rag-and-models.md](docs/10-memory-rag-and-models.md) | Hindsight self-hosted memory, local embedders/rerankers, hybrid RAG in Postgres, **Decision One** (µs tree tier + System One decision models: SemIf, own Qwen-LoRA head; Jev/Laya/Clef assessed), LiteLLM routing to Claude / custom endpoint |
| [docs/research/](docs/research/) | Raw per-repo research notes with file-level evidence |

## Licensing stance

This is a private project for personal use only. GPL obligations start only when software is distributed, and AGPL obligations only when others use it over a network. Neither happens here, so GPL/AGPL code may be used directly. The verdicts below reflect what is **best**, not just what is licence-safe. See [docs/05](docs/05-saas-legal-and-licensing.md) for the SaaS picture. **Keep this repo private.**

## Repos vetted

| Repo | License | Verdict |
|---|---|---|
| nautechsystems/nautilus_trader | LGPL-3.0 | Adopt as core engine |
| hummingbot/hummingbot | Apache-2.0 | Adopt as a module (market making, DEX) |
| TauricResearch/TradingAgents | Apache-2.0 | Borrow its pattern and components (AI decision layer) |
| HKUDS/Vibe-Trading | MIT | Borrow components (research lab, order guard) |
| AI4Finance-Foundation/FinRobot | Apache-2.0 | Borrow components (valuation) |
| freqtrade/freqtrade | GPL-3.0 | Reference only (redundant as an engine) |
| NoFxAiOS/nofx | AGPL-3.0 | Avoid the code; borrow ideas |
| VibeTradingLabs/vibetrading | No LICENSE file | Avoid (redundant) |
| 666ghj/MiroFish | AGPL-3.0 | Reference only / experiment |
| simplifaisoul/osiris | MIT | Reference only |
| RSS-Bridge/rss-bridge | Unlicense | Adopt (internal sidecar for feedless sites) |
| spacebarchat | AGPL-3.0 | Avoid (a chat server, not a data source) |
| the-ai-entrepreneur-ai-hub/threads-scraper | None | Avoid (unlicensed paid Apify actor) |
| matthewdonsemail-lab/listeningkit | Apache-2.0 (fork of obris-dev/openmagpie) | Reference only |
| matthewdonsemail-lab/log | MIT | Avoid (cookie-harvesting lead-gen) |
| eprbell/rp2 | Apache-2.0 | Borrow (lot-matching algorithms, country-plugin pattern) |
| isaacrowntree/ledger | MIT | Borrow (ATO CGT details, AU FY, ABS CPI fetch) |
| Librefolio/LibreFolio | AGPL-3.0 | Reference (broker importers, provider registry) |
| miladtm94/Investment-Portfolio-Tracker | MIT | Reference (importers; its ATO engine has bugs) |
| BittyTax/BittyTax | AGPL-3.0 | Reference (UK pooling rules; crypto CSV parsers) |
| vas3k/TaxHacker | MIT | Optional sidecar (expense receipts, local LLM) |
| degenfrends/solana-rugchecker | No LICENSE (package.json says MIT) | Ideas only (Solana rug heuristics) |
| CRPWarner/RugPull | None (Gigahorse BSD-3) | Concepts + optional sandboxed EVM deep scan |
| dianxiang-sun/rug_pull_dataset | None | Private evaluation labels only |
| jattin1/rug-pull-detector-extension | None | Reject (non-functional) |
| N8python/rugpull | CC0 | Reject (not crypto) |

> Nothing here is financial advice. No reviewed system has shown durable, cost-adjusted, out-of-sample profitability.
