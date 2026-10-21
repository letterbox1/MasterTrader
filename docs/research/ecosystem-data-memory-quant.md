_Raw notes from the research agents. They back up [../01-repo-vetting-report.md](../01-repo-vetting-report.md). File paths refer to each upstream repo at its 2026-10-21 HEAD._

# Supporting ecosystem — raw findings (2026-10-21)
Verification: stars/licenses via GitHub search API + PyPI JSON; free-tier limits mostly third-party pages; (U) = unverified. Reddit/HN unreachable.

## Top picks
- Market data: OpenBB Platform (Apache-2.0 per LICENSE + PyPI openbb 5.0.0; repo now resolves at github.com/openbq-org/OpenBB, same repo id — verify provenance), ccxt (MIT, 44.5k), FRED/ALFRED (120 req/min, vintages), SEC EDGAR via edgartools (MIT, 2.8k; 13F/Form 4), Treasury/BLS/EIA/CFTC, Databento $125 one-off credit. Free tiers: Twelve Data 800 credits/day, FMP 250/day, Alpha Vantage 25/day (U), Polygon/Massive 5/min EOD (U). Stooq needs API key since ~Mar 2026 (pandas-datareader#1012).
- Brokers: alpaca-py (old SDK archived), ib_async (BSD-2; ib_insync archived), OANDA practice (official SDK stale since 2021), MetaTrader5 Windows-only (U), Hyperliquid SDK MIT (US persons restricted, U).
- Social/news: RSS + trafilatura (Apache-2.0) / crawl4ai (Apache-2.0, 86k), FinBERT, GDELT.
- Geo/events: GDELT + USGS/GDACS/NOAA/FIRMS/ReliefWeb; Polymarket Gamma (no auth). OSIRIS MIT 11.2k; worldmonitor AGPL-3.0-only 89k (commercial licenses sold).
- Memory/storage: Hindsight (vectorize-io, MIT, 52k; facts/experiences/mental models; Postgres+pgvector; Ollama/LangGraph/MCP). Postgres+pgvector+TimescaleDB (TSL features free self-host, no DBaaS). DuckDB/Parquet. LightRAG (MIT). ArcticDB BSL 1.1 (no third-party DB service; Apache after 2y).
- Quant: Qlib (MIT), skfolio/Riskfolio, alphalens/pyfolio/empyrical-reloaded, quantstats, TA-Lib, Chronos/TimesFM/Kronos (weights license U) for vol/volume features.
- Orchestration: LangGraph (MIT), Prefect (Apache-2.0), NATS JetStream / Valkey (BSD-3), Grafana (AGPL, unmodified OK).

## Landmines
- vectorbt: Apache-2.0 + Commons Clause; dev moved to PRO.
- Copyleft: nofx AGPL, freqtrade GPL, nautilus LGPL, Firecrawl server AGPL, backtesting.py AGPL, Grafana AGPL, Redis 8 tri-license (AGPL option), Lumibot GPL; kalshi-python proprietary.
- ACLED 2025 terms: corporate license for commercial use; strict AI/LLM limits.
- Personal/non-commercial: Yahoo (yfinance, Qlib prebuilt data); Reddit new API access manual approval (U); CoinGecko Demo, Etherscan, Finnhub, Polygon free tiers.
- Prohibited scraping: X (twscrape/twikit), Discord self-bots, ForexFactory/Investing.com.
- Dead/moved: snscrape, pytrends (archived Apr 2025), pandas-ta (404 -> pandas-ta-classic / ta), StockTwits API, Telethon (Codeberg), Zep CE deprecated (Graphiti only), zipline-reloaded maintenance, py-clob-client archived, backtrader no pushes since 2024-08, Dune free view-only from Sep 2026 (U).
- Gaps: no maintained OSS airdrop/ICO/token-launch tracker; no free OSS economic calendar API.

## Stars (2026-10-21)
TradingAgents 112k, freqtrade 55.7k, Vibe-Trading 36.1k, nautilus 30.4k, hummingbot 20.6k, nofx 13.1k, FinRobot 8.3k, Kronos 42.4k, Qlib 49.6k, mem0 67.5k, LightRAG 40.2k, Graphiti 32.1k, Qdrant 35.2k, Firecrawl 193.5k.

## Community (2026 blogs, U)
vectorbt/Qlib for research, Nautilus for production (parity praised, learning curve criticised), freqtrade for crypto bots, Databento for data quality.
Sources: https://bullalert.ai/blog/best-python-backtest-engines-2026/ , https://autotradelab.com/blog/nautilus-vs-vectorbt-vs-freqtrade-20-python-quant-trading-frameworks-compared
