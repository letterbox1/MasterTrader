# Phase 1 · Market Data, Recording & Live Monitoring

| | |
|---|---|
| **Goal** | Free, clean, point-in-time market and macro data for every asset class at every timeframe from ticks to 1W, with an always-on data-quality and cost monitor that alerts you. |
| **Duration** | Weeks 3–6 |
| **Depends on** | P0 (stack, schemas, `pit`, provenance columns, alerts plumbing) |
| **Unlocks** | P2 (strategies need data, measured costs and DQ status), P3 (RBA FX, ABS CPI), P4 (store and monitor patterns) |
| **Modules** | M1 market & macro data, M16 live cost & data-quality monitor, quota tracker, provenance tagging, M17 alerts |
| **Containers** | `ingest-market`, `ingest-batch`, `monitor`, `ntfy`, `telegram-bot` (alerts only), `ib-gateway` (only when IBKR is used) |
| **Dashboards** | [D07](../ui/dashboards/D07-data-quality.md) Data & Quality, [D02](../ui/dashboards/D02-markets.md) Markets, notifications |
| **Primary docs** | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) · [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · [03 §6](../03-build-spec.md#6-smallest-free-timeframe-by-asset-class) · [06 §3](../06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) · [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) · [02 F1](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** real-time and historical connectors for crypto, FX/metals, stocks/ETFs, futures (daily), rates and macro, fundamentals; the Parquet recorder and bar builder; quota tracking; provenance tags + retention jobs; the DQ monitor, cost monitor and reconciliation (on practice/testnet accounts); venue-health monitoring; alert channels (Telegram, ntfy, optional email) behind one fan-out; D07 and D02.

**Out:** calendars and text (P4), TCA on real fills (P2, once orders exist), on-chain data (P5).

## 2. Entry criteria

- P0 exit criteria met.
- Practice/testnet accounts (T0.09) and free API keys (T0.10) exist; Telegram bot exists (T0.06).

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R1.01 | **Crypto real-time:** public WS trades, L1 and L2 (Binance, Bybit, OKX, Coinbase, Kraken) via Nautilus/ccxt → NATS `md.*`. L2 diffs are recorded at native speed only for symbols whose bots need order-book data (default ≤ 3 symbols, configurable); the rest get 1 s book snapshots | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [02 §6](../02-v1-architecture.md#6-messaging-nats), [17 §D](../17-decisions-register.md#d-other-decisions) | Live feed |
| R1.02 | **Recording:** Parquet recorder (1–5 min files, daily compaction); bar builder writes 1s/1m bars to Timescale; timeframes run tick → 1W with continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W; other sizes via `time_bucket` queries at read time | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [02 F1](../02-v1-architecture.md#8-end-to-end-flows), [17 §D](../17-decisions-register.md#d-other-decisions) | Bar parity test |
| R1.03 | **Crypto history:** data.binance.vision trades/aggTrades/1s klines backfill | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Backfill report |
| R1.04 | **FX & metals:** OANDA practice stream, IG demo stream, Dukascopy ticks, ECB/Frankfurter, **RBA F11** daily FX; broker XAU/XAG (no LBMA) | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [06 §3](../06-aggregators-and-market-providers.md#market-data-m1) | Live feed |
| R1.05 | **Stocks/ETFs:** Alpaca IEX real-time (30 symbols), yfinance daily, FinanceDatabase symbol master, `exchange_calendars` | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Live feed |
| R1.06 | **Futures/commodities (daily), rates & macro:** yfinance futures, EIA, USDA, CFTC COT, Baker Hughes; FRED/ALFRED vintages, US Treasury, `sdmx1`, BoE/BoC/RBA/SNB/BoJ, DBnomics, **ABS CPI** (All groups CPI, weighted average of eight capital cities, series A2325846C (U), verified in T1.60) | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Batch flows |
| R1.07 | **Fundamentals:** SEC EDGAR via edgartools (declared User-Agent, ≤ 10 req/s) | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Batch flow |
| R1.08 | **Quota tracker** per connector that throttles before each free limit | [03 §1](../03-build-spec.md#1-ground-rules) | Quota panel in D07 |
| R1.09 | **Provenance:** every ingested row tagged (`source`, `licence`, use flags); retention jobs enforce `retention_days` (e.g. CoinGecko ≤ 24 h) | [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms), [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules) | Provenance test |
| R1.10 | **DQ monitor:** stale feed, gaps, bad ticks, cross-source divergence, clock skew, book integrity, nightly Pandera + Evidently → `dq.status.*` + `audit.dq_event`; an incident acknowledgement is a new WORM row (`audit.dq_ack`), never an update; loosening a DQ threshold is C3 (via the break-glass CLI, R0.12, until Telegram C3 lands in P2) | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Fault injection |
| R1.11 | **Cost monitor:** fee tiers, funding (predicted + realised), swap/financing, `spread_bps` by instrument × hour-of-week → `cost.*` | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Cost panels |
| R1.12 | **Reconciliation:** vs each practice/testnet venue: positions and open orders every 60 s, balances every 5 min, full EOD (defaults, configurable, [16 §2.9](../16-configuration-and-safety-model.md#29-reconciliation)); mismatch = incident in `audit.recon` | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Recon report |
| R1.13 | **Venue-health monitor:** our own measured withdrawal times, PoR/incident notes, venue status pages/feeds (via the regulatory & venue watch, R4.15, once P4 lands) and a quarterly AUSTRAC register check (USER task T1.06) → `ops.venue_registry` health | [12 §2](../12-policy-and-compliance.md#2-venue-access-registry), [13 §6](../13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) | D07 panel |
| R1.14 | **Alerts, one fan-out:** Grafana alerts → webhook → the `alert.*` consumer → Telegram + **ntfy** (second independent channel; self-hosted, Tailscale only; iOS push via ntfy's upstream relay carries only a message ID) + email (your mail provider's SMTP with an app password, or turned off) | [07 §9](../07-security-notes.md#9-monitoring--incident-response), [17 §D](../17-decisions-register.md#d-other-decisions) | Test alerts |
| R1.15 | **UI:** D07 (feeds, quotas, DQ events, costs, recon) and D02 (charts, cross-asset matrix, instrument detail with **finest available resolution**; P4-fed widgets such as sentiment, positioning, nowcasts and prediction markets show an "arrives in P4" state, never placeholder data) | [D07](../ui/dashboards/D07-data-quality.md), [D02](../ui/dashboards/D02-markets.md), [03 §6](../03-build-spec.md#6-smallest-free-timeframe-by-asset-class) | Playwright |
| R1.N1 | Feed staleness: `dq.status` → stale within **≤ 250 ms (p99)** of the data-age threshold being crossed (see R1.17) | [02 §9.2](../02-v1-architecture.md#92-observability--slos) | SLO metric |
| R1.N2 | UI live update lag p95 < 500 ms; server throttles ≤ 4 Hz charts, ≤ 1 Hz tables | [02 §9.2](../02-v1-architecture.md#92-observability--slos), [02 §6](../02-v1-architecture.md#6-messaging-nats) | Client telemetry |
| R1.N3 | Storage within budget (~0.3–1 TB/year for ~10 liquid crypto symbols at trades + L1 + 1 s book snapshots, native L2 diffs only for the default ≤ 3 order-book symbols; recalculated from the soak, T1.80); cold Parquet to HDD | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Disk metrics |
| R1.16 | **Egress check:** every minute, confirm exchange traffic leaves via the allow-listed static IP and the IP's country matches your configured residency (free GeoIP DB, e.g. DB-IP Lite); mismatch blocks new orders + alerts. Safety only; never a tax input | [16 §3.2](../16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) | Fault test |
| R1.17 | **Data age definition:** age = now − our receive time per stream; per-bot thresholds (default 2 s fast / 60 s slow, configurable, session-aware); monitor flips status ≤ 250 ms p99 after crossing (M11's inline order-time check lands in P2) | [16 §2.2](../16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) | Fault injection |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T1.01** `USER` Pick the starting **universe/watchlist**: ~10 crypto pairs, FX/metal pairs, ~30 US ETFs/stocks (Alpaca IEX limit), macro series you care about. → R1.01–R1.06
- [ ] **T1.02** `USER` Create **read-only** API keys where the testnet offers them (Binance/Bybit testnets, IP-allow-listed) for reconciliation and fee-tier reads; OANDA practice, IG demo, Alpaca paper and IBKR paper use their normal credentials (no money at risk). All go in the secrets file. → R1.12 · [07 §3](../07-security-notes.md#3-broker--exchange-keys)
- [ ] **T1.03** `USER` Install the ntfy app on your phone and subscribe to the private topic; confirm the email alert address (or turn email off). → R1.14
- [ ] **T1.04** `USER` Review the first week's DQ alerts and tell us which thresholds are too noisy. → R1.10
- [ ] **T1.05** `USER` Create an SMTP app password at your own mail provider and put it in the secrets file, or turn email alerts off (Telegram + ntfy remain). → R1.14
- [ ] **T1.06** `USER` Each quarter, when the reminder arrives, check every venue you use on the AUSTRAC register and record the result (recurring). → R1.13 · [12 §2](../12-policy-and-compliance.md#2-venue-access-registry)

### B. Build (`BUILD`, code)
- [ ] **T1.20** `BUILD` `mt_data.market` crypto WS clients via Nautilus data clients/ccxt; publish `md.*`. → R1.01
- [ ] **T1.21** `BUILD` Parquet recorder + daily compaction; bar builder (1s/1m) + Timescale continuous aggregates (1m, 5m, 15m, 1h, 4h, 1D, 1W); tick/volume/value bar support. → R1.02
- [ ] **T1.22** `BUILD` Backfill flows: data.binance.vision, Dukascopy (dukascopy-node or own bi5 parser), Alpaca history, yfinance. → R1.03–R1.05
- [ ] **T1.23** `BUILD` FX/metals streaming: OANDA v20 practice, IG Lightstreamer demo; Frankfurter self-hosted; RBA F11 flow. → R1.04
- [ ] **T1.24** `BUILD` Macro/rates/fundamentals Prefect flows: FRED/ALFRED (vintages), Treasury, `sdmx1`, central banks, EIA/USDA/COT/Baker Hughes, ABS CPI, EDGAR. → R1.06, R1.07
- [ ] **T1.25** `BUILD` Quota tracker (per-connector budgets from live headers where available) shared by all connectors. → R1.08
- [ ] **T1.26** `BUILD` Provenance tagging at write time (defaults from each source's licence tag in 06) + retention job. → R1.09
- [ ] **T1.27** `BUILD` `mt_monitor` DQ service: per-instrument rolling state, checks table, `dq.status.*`, incidents, `audit.dq_ack` acknowledgement rows. → R1.10, R1.17
- [ ] **T1.28** `BUILD` `mt_monitor` cost service: fees/tiers, funding, financing, spreads by hour-of-week; TCA scaffolding for P2. → R1.11
- [ ] **T1.29** `BUILD` Reconciliation jobs (ccxt read-only, OANDA, IG, Alpaca, IBKR paper), built and tested against recorded fixtures; mismatches → `audit.recon` (live run in T1.67). → R1.12
- [ ] **T1.30** `BUILD` Venue-health collector writing to `ops.venue_registry` health fields from our own withdrawal-time measurements; quarterly AUSTRAC re-check reminder (T1.06). → R1.13
- [ ] **T1.31** `BUILD` Telegram bot (alerts only) + ntfy + email notifier behind one `alert.{severity}.{kind}` consumer; Grafana alerts reach it by webhook (single fan-out). → R1.14
- [ ] **T1.32** `BUILD` UI: D07 Data & Quality, D02 Markets (lightweight-charts, matrix, instrument detail, "arrives in P4" states for P4-fed widgets), notifications centre. → R1.15 · [D07](../ui/dashboards/D07-data-quality.md) · [D02](../ui/dashboards/D02-markets.md)
- [ ] **T1.33** `BUILD` Egress IP/country check with GeoIP DB; `egress.status` → M11 + alerts. → R1.16
- [ ] **T1.34** `BUILD` Alpaca real-time stream, FinanceDatabase symbol master and `exchange_calendars` integration; CoinGecko/DefiLlama enrichment with ≤ 24 h encrypted cache. → R1.05, R1.09

### C. Ops & config (`OPS`)
- [ ] **T1.40** `OPS` Storage layout: NVMe hot Parquet, HDD cold tier, compaction schedule, disk alerts. → R1.N3
- [ ] **T1.41** `OPS` Prefect schedules for batch flows (respecting quotas and source update times, AEST/AEDT aware). → R1.06
- [ ] **T1.42** `OPS` Grafana boards: live prices by timeframe, spreads/funding/swaps, DQ incidents, quota usage. → R1.10, R1.11
- [ ] **T1.43** `OPS` ntfy container (self-hosted, auth on, Tailscale only; upstream relay allowed for iOS push, message ID only). → R1.14
- [ ] **T1.44** `OPS` `ib-gateway` container (IBC-managed, digest-pinned, read-only API for reconciliation) when IBKR is used. → R1.12

### D. Verify & test (`VERIFY`)
- [ ] **T1.60** `VERIFY` Run the open provider checks: OANDA order/position books, TrueFX, IMF SDMX 3.0 URL, IG sentiment path, StockTwits reachability, Tardis samples, BoC/BoJ keyless, ABS CPI series ID A2325846C (U). → [06 §3 open checks](../06-aggregators-and-market-providers.md#open-checks-do-these-in-phase-1)
- [ ] **T1.61** `VERIFY` DQ fault injection: kill a feed (status stale ≤ 250 ms p99 after its data-age threshold), inject a bad tick, skew the clock, drop sequence IDs. → R1.10, R1.N1, R1.17
- [ ] **T1.62** `VERIFY` Bar parity: Timescale aggregates vs bars rebuilt from Parquet ticks for a sample day. → R1.02
- [ ] **T1.63** `VERIFY` Provenance/retention test: CoinGecko rows deleted after 24 h; untagged rows rejected. → R1.09
- [ ] **T1.64** `VERIFY` Alert path test on all three channels. → R1.14
- [ ] **T1.65** `VERIFY` Egress fault test: wrong egress IP or country → new orders blocked and alerted. → R1.16
- [ ] **T1.66** `VERIFY` Live connector check with your credentials and keys (after T0.09, T0.10, T1.02): OANDA/IG/Alpaca streams and keyed batch flows (FRED, EIA, CoinGecko Demo) deliver, and the quota tracker reads live headers. → R1.01, R1.04–R1.06, R1.08
- [ ] **T1.67** `VERIFY` Live reconciliation on practice/testnet accounts with your keys (after T1.02): a clean run, then a seeded mismatch raises an incident. → R1.12

### E. Run / soak (`RUN`)
- [ ] **T1.80** `RUN` 7-day continuous recording soak; gap report per instrument; disk growth vs budget. → R1.N3

## 5. Deliverables

Connectors + recorder + bar builder · batch flows · quota tracker · provenance + retention · DQ/cost/recon monitor · venue-health monitor · alerts on 3 channels · D07 + D02.

## 6. Exit criteria (demo)

1. Grafana and D02 show live prices at every timeframe from ticks to 1W across crypto, FX/metals and ETFs, plus daily futures and macro.
2. Live spread/funding/swap panels populate; reconciliation runs clean on practice accounts.
3. A deliberately killed feed shows stale within 250 ms (p99) of its data-age threshold and the alert reaches Telegram, ntfy and (if on) email.
4. Open provider checks are recorded in 06 (pass/fail).

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Free-tier changes or API breakage | Quota tracker + monthly ToS check (standing rule); cross-source references for every critical feed |
| Disk growth from L2 | Record L2 only for symbols that need it; compaction; HDD tier |
| IEX ≠ NBBO for US stocks | Flag in D02; avoid scalping-cost conclusions on IEX data (03 §6) |
