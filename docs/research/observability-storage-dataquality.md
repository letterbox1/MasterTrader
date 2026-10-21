_Raw notes from the research agents (2026-10-21). They back up [../03-build-spec.md](../03-build-spec.md). (U) = unverified: either the docs site was unreachable from the research sandbox, or the claim is from secondary sources._

# Observability, tick storage, data quality, live costs, free tick data, MCP

## Recommended stack
| Layer | Pick | Licence |
|---|---|---|
| System of record (orders, fills, fees, decisions, LLM audit, risk-config history, tax lots, DQ/cost incidents) | Postgres 16 + TimescaleDB (TSL Community image, not `-oss`) + pgvector | PostgreSQL / TSL (free for own internal use) |
| Bars 1s→1d+, cost/DQ metrics | Timescale hypertables + hierarchical continuous aggregates; `time_bucket` for arbitrary sizes | TSL |
| Raw ticks/trades/quotes/L2 | **Nautilus ParquetDataCatalog** on disk + DuckDB (MIT) | LGPL / MIT |
| Optional live tick SQL | QuestDB (only if needed) | Apache-2.0 |
| Logs | **Grafana Loki** single binary + **Vector** (MPL-2.0) or Alloy | AGPL (fine privately) |
| Metrics/alerts | Prometheus + Grafana Alerting → Telegram | Apache / AGPL |
| Traces | OpenTelemetry SDK (+ optional Tempo) | Apache |
| LLM tracing | Postgres `audit.llm_calls` + optional **Arize Phoenix** UI (ELv2); Langfuse (MIT core) is heavier (ClickHouse + Redis + S3) | — |
| Data quality | Custom streaming checks on NATS + **Pandera** (MIT) for batches + **Evidently** (Apache) for drift | — |
| MCP | Official `mcp` SDK 2.3.0 (MIT) or FastMCP 4.1.3 (Apache-2.0); stdio or localhost/Tailscale only | — |

**Split between the database and the logs:**
- Postgres holds anything you may need to prove: append-only, hash-chained, with `trace_id` linking to the logs.
- Loki holds operational text, kept 14–90 days.
- Never let Loki be the only copy of a trade.
- No Postgres multi-tenancy for a single user; use schemas `audit` / `market` / `journal` / `ops` plus least-privilege roles.

## Logging options
| Tool | Licence | Footprint | Notes |
|---|---|---|---|
| Grafana Loki | AGPL-3.0 (Apache exceptions) | Low | Native in Grafana; LogQL; label-first |
| Graylog Open | **SSPL v1** (not OSI) | Heavy (JVM + OpenSearch + MongoDB, 4–8 GB+) | Not chosen |
| OpenObserve | **AGPL-3.0** (moved from Apache) + Enterprise | Low–medium; Rust single binary | Good all-in-one, but duplicates Grafana |
| Vector / Fluent Bit | MPL-2.0 / Apache-2.0 | Very low | Shippers |
| Langfuse | MIT except `/ee` | Heavy (v3) | Best LLM UI |
| Arize Phoenix | **ELv2** | Light | LLM trace UI |

Logging rules:
- Structured JSON logs (structlog) carrying `trace_id`, `strategy_id`, `instrument_id`, `venue`.
- Loki labels stay low-cardinality: service, venue, level.

## Tick storage
**"TenentDB"** most likely means **TDengine** (AGPL-3.0, IoT-focused, no finance ecosystem) → not recommended. TencentDB (Tencent's managed cloud DB) is out of scope.

| Store | Licence | Verdict |
|---|---|---|
| TimescaleDB | Apache core + TSL features | Bars, business and audit data |
| QuestDB | Apache-2.0 | Optional live tick SQL |
| ClickHouse | Apache-2.0 | Overkill for one user |
| ArcticDB | **BSL 1.1** (production use needs a licence) | Excluded |
| DuckDB + Parquet | MIT | Research queries |
| Nautilus ParquetDataCatalog | LGPL | Raw ticks/L2; read natively by backtests |

### Storage estimates per symbol (calculated, U)
| Data | Volume |
|---|---|
| BTCUSDT trades | 12–50 MB/day in Parquet (5–18 GB/yr) |
| 1-second bars | 0.4–0.7 GB/yr |
| L1 bookTicker | 18–70 GB/yr |
| L2 top-20 @100 ms | 36–73 GB/yr (keep out of Postgres) |
| L2 top-20 @1 s | 4–7 GB/yr |

Rule of thumb: about 10 liquid crypto symbols with trades + L1 + L2@1s comes to **0.3–1 TB/yr**. Budget 2–4 TB of NVMe, with cold partitions moved to HDD.

### Hot / cold flow
1. Venue WebSocket → Nautilus data client → NATS.
2. From NATS:
   - the strategy (in-process);
   - a Parquet recorder (rolled every 1–5 min, compacted daily);
   - a bar builder writing 1s/1m bars into Timescale, with continuous aggregates for 5m–1d.
3. Backtests read the Parquet catalog.

## Data quality (streaming `dq-monitor` service on NATS JetStream)
| Check | How |
|---|---|
| Stale feed | Session-aware timeout per instrument and venue |
| Gaps | Sequence IDs (Binance U/u, Bybit seq, trade-id continuity); expected bar counts |
| Outliers | Robust z-score (median/MAD); price outside the spread band; crossed or locked book |
| Cross-source divergence | Mid-price difference in bps (Binance vs Bybit/OKX/Coinbase; OANDA vs Dukascopy/IG) |
| Clock skew | `recv_ts − exchange_ts` p99; chrony offset via node_exporter |
| Book integrity | Venue checksums (OKX, Kraken; U) + periodic REST snapshot reconciliation |

- Incidents go to `audit.dq_events`; metrics go to Prometheus/Grafana alerts → Telegram.
- **The risk engine auto-pauses any strategy whose feed is stale.**
- Nightly: Pandera checks on the day's Parquet + Evidently drift report.

Other tools:
- **Soda Core** has moved to **ELv2** ("Proprietary" on PyPI), so it's not used.
- Great Expectations is optional.

## Live cost monitoring
| Cost | Free source |
|---|---|
| Crypto commissions | ccxt `fetchTradingFees` and per-fill fees; Binance `/api/v3/account/commission` |
| Funding | ccxt `fetchFundingRate(s)` / `fetchFundingRateHistory`; Bybit v5 tickers (fundingRate, interval, bid/ask); realised funding via `fetch_ledger` / `fetchFundingHistory` (U) |
| Borrow | ccxt `fetchCrossBorrowRate(s)` / `fetchIsolatedBorrowRate(s)` |
| OANDA swaps | v20 `InstrumentFinancing` longRate/shortRate via account instruments (U, high confidence); realised financing transactions. Price stream capped at 4 quotes/s per instrument |
| IG overnight funding | No API field found (U); measure realised funding from account history |
| IBKR | TWS `commissionAndFeesReport` per execId (`ib_async` 2.1.0, BSD); persist as fills arrive; Flex Queries for statements |
| Alpaca | Stocks commission-free; crypto 15/25 bps down to 0/10 bps; reg fees on sells (U) |
| Spreads | `spread_bps` series per instrument × hour-of-week; alert at > 3× rolling median |

**TCA (implementation shortfall):**
- **Formula:** IS bps = side × (fill VWAP − decision mid) / decision mid × 1e4 + fees bps.
- **Breakdown:** delay, spread/impact, fees.
- **Alert:** when realised/modelled cost exceeds 1.5×.
- **Feedback:** measured costs feed back into Nautilus fill and fee models.

## Free smallest-timeframe data
| Asset class | Real-time | History | Limits |
|---|---|---|---|
| Crypto | Binance/Bybit/OKX/Coinbase public WebSockets (trades, L1, L2 diff 100 ms); no key needed | data.binance.vision trades/aggTrades/klines down to 1s (next day, with checksums) | Free L2 history only exists if you record it yourself |
| FX | OANDA v20 stream (4 quotes/s); IG Lightstreamer (U); TrueFX (U) | Dukascopy ticks (1600+ instruments); TrueFX since 2009 (U) | No true L2 for FX |
| US stocks/ETFs | Alpaca Basic: **IEX only, 30 symbols** over WebSocket | Alpaca historical (IEX; SIP delayed 15 min, U) | IEX ≠ NBBO; fine for swing trading, poor for scalping cost measurement |
| Futures/commodities | IBKR real-time needs paid data; delayed is free (U) | Free daily only | Use crypto perps / FX / CFDs for exposure instead |

## MCP security
1. **Transport:** stdio preferred; otherwise Streamable HTTP on localhost/Tailscale with OAuth 2.1/bearer auth. No token passthrough.
2. **Tools:**
   - Read tools are separate from a small, typed (Pydantic) set of write tools.
   - Annotations (readOnlyHint/destructiveHint) are hints only, not security.
3. **Asymmetric changes:**
   - Tightening, pausing or killing applies immediately.
   - **Loosening needs an out-of-band Telegram approval + TOTP, with an expiry.**
4. **Hard ceilings** live in a file the MCP server can't write; the Nautilus RiskEngine and pre-trade checks enforce them regardless.
5. **Audit:** every call goes to `audit.risk_config_changes`, configs are versioned, and every write sends a Telegram notification.
6. **Limits:** rate limits and cool-downs; the server's DB role can only INSERT.
7. **Never exposed via MCP:** order placement, withdrawals, key management.

## Sources
- https://github.com/grafana/loki
- https://github.com/graylog2/graylog2-server
- https://github.com/openobserve/openobserve
- https://github.com/vectordotdev/vector
- https://github.com/langfuse/langfuse
- https://github.com/Arize-ai/phoenix
- https://github.com/timescale/timescaledb/blob/main/tsl/LICENSE-TIMESCALE
- https://github.com/questdb/questdb
- https://pypi.org/project/arcticdb/
- https://pypi.org/project/duckdb/
- https://pypi.org/project/nautilus-trader/
- https://pypi.org/project/pandera/
- https://github.com/sodadata/soda-core
- https://pypi.org/project/evidently/
- https://github.com/ccxt/ccxt/wiki/Manual
- https://bybit-exchange.github.io/docs/v5/market/tickers
- https://async-v20.readthedocs.io
- https://www.interactivebrokers.com/docs/tws-api/doc/order-management/commission-and-fees-report
- https://docs.alpaca.markets/docs/crypto-fees
- https://docs.alpaca.markets/docs/about-market-data-api
- https://github.com/binance/binance-public-data/
- https://pypi.org/project/mcp/
- https://pypi.org/project/fastmcp/
- https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices
