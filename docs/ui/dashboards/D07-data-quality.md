# D07 · Data & Quality

| | |
|---|---|
| **Route** | `/data` (tabs: Feeds · Quality · Costs · Quotas · Reconciliation · Storage) |
| **Modules** | M1 ingestion, M16 monitor, M2/M3 source health |
| **Phase** | 1 |
| **Mock-up reference** | `live-free-data-pipeline-feed-quality-sentinel.png` |

## Purpose

Prove that the data feeding decisions is fresh, correct and within free-tier limits, and that trading costs are what we think they are.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | KPI strip (feeds ok/degraded/stale/bad, incidents 24h, cross-source divergence max, quota headroom min, recon mismatches, storage used) + tabs |
| xl–md | Tabs; tables with priority columns |
| ≤ ph | Segmented tabs; feed cards with status chips |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Feeds** | Every connector (venue WebSockets, OANDA/IG streams, Alpaca IEX, Dukascopy/backfills, macro/central banks, text and event sources). Per feed: status, last message age, msgs/s, latency p50/p99, reconnects 24h, gaps 24h, licence tag (personal/commercial_ok), cost tag (free). Sparkline of msg rate. | `/data/feeds`, WS `dq.status` |
| **Quality** | Incident list (stale, gap, bad tick, crossed book, divergence, clock skew, book checksum), each with instrument, venue, observed value, threshold, duration, auto-action (strategies paused), resolved time. Cross-source divergence chart per instrument pair. Clock-skew chart (`recv_ts − exchange_ts` p99, chrony offset). Nightly Pandera validation results; Evidently drift report links. | `/data/dq-events`, WS `dq.status` |
| **Costs** | Spread (bps) by instrument × hour-of-week heatmap; current fee tiers per venue; funding rates (predicted/realised) and swap/financing rates; borrow rates; alerts when spread > 3× normal | `/data/costs`, WS `cost` |
| **Quotas** | Per free API: limit, used (rolling), headroom %, throttle state, next reset; history chart; warnings at 80% | `/data/quotas` |
| **Reconciliation** | Positions and balances vs each venue: last run, mismatches (instrument, ours, venue's, difference), status, auto-resolution notes | `/data/recon`, WS `recon` |
| **Storage** | Parquet catalog size by venue/type, hot/cold tiers, Timescale compression stats, backfill jobs and their progress | `/data/feeds?storage=1`, `/lab/jobs?kind=backfill` |

## Actions

| Control | Command | Level |
|---|---|---|
| Pause / resume feed | `data.feed.pause` / `data.feed.resume` | C1 (shows which strategies depend on it) |
| Run backfill (source, instrument, range) | `data.backfill.run` | C1 |
| Run reconciliation now | `data.recon.run` | C1 |
| Acknowledge incident | `system.settings.update` (incident ack) | C0 |
| Adjust DQ thresholds | Link to D06 policy (blackouts) / `system.settings.update` (DQ thresholds; loosening thresholds = C3) | C1 / C3 |

## Acceptance criteria

1. **Speed:** a stale feed shows in the UI within 2 s of detection, along with the strategies it paused.
2. **Licence tags:** every feed shows its licence/cost tag. A paid feed can't be enabled (UI blocks it, server rejects it).
3. **Quotas:** quota warnings appear before throttling starts.

## Backend contract

- **Queries:** `/data/feeds`, `/data/dq-events`, `/data/costs`, `/data/quotas`, `/data/recon`, `/lab/jobs?kind=backfill`.
- **WebSocket topics:** `dq.status`, `cost`, `recon`, `lab.job`.
- **Commands:** `data.feed.pause|resume`, `data.backfill.run`, `data.recon.run`, `system.settings.update`.
