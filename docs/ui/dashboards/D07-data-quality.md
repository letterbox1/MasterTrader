# D07 · Data & Quality

| | |
|---|---|
| **Route** | `/data` (tabs: Feeds · Quality · Costs · Quotas · Reconciliation · Storage) |
| **Modules** | M1 ingestion, M16 monitor, M2/M3 source health |
| **Phase** | 1 |
| **Mock-up reference** | `live-free-data-pipeline-feed-quality-sentinel.png` |

## Purpose

Prove that the data feeding decisions is fresh, correct and within free-tier limits, and that trading costs are what we think they are.

**What "stale" means** ([16 §2.2](../../16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)): data age = now (host monotonic clock) − the time **we received** the last update for that instrument stream, not the exchange timestamp (that gap is shown separately as clock skew). Thresholds are set per bot (defaults 2 s fast / 60 s slow, configurable); closed sessions show `closed`, not stale. M11 checks data age inline on every order, so no order acts on stale data whatever the UI shows.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | KPI strip (feeds ok/degraded/stale/bad, incidents 24h, cross-source divergence max, quota headroom min, recon mismatches, storage used) + tabs |
| xl–md | Tabs; tables with priority columns |
| ≤ ph | Segmented tabs; feed cards with status chips |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Feeds** | Every connector (venue WebSockets, OANDA/IG streams, Alpaca IEX, Dukascopy/backfills, macro/central banks, text and event sources). Per feed: status, data age vs threshold (and the bots using it), msgs/s, latency p50/p99, reconnects 24h, gaps 24h, licence tag (personal/commercial_ok), cost tag (free). Sparkline of msg rate. | `/data/feeds`, WS `dq.status` |
| **Quality** | Incident list (stale, gap, bad tick, crossed book, divergence, clock skew, book checksum), each with instrument, venue, observed value, threshold (default or overridden), duration, auto-action (bots paused), resolved time, acknowledgement (a separate WORM `audit.dq_ack` row; the incident row is never updated). Cross-source divergence chart per instrument pair. Clock-skew chart (`recv_ts − exchange_ts` p99, chrony offset). Nightly Pandera validation results; Evidently drift report links. | `/data/dq-events`, WS `dq.status` |
| **Costs** | Spread (bps) by instrument × hour-of-week heatmap; current fee tiers per venue; funding rates (predicted/realised) and swap/financing rates; borrow rates; alerts when spread > 3× normal (default, configurable); cost blow-out (realised ÷ modelled > 1.5× over the last 20 fills → bot paused; default) | `/data/costs`, WS `cost` |
| **Quotas** | Per free API: limit, used (rolling), headroom %, throttle state, next reset; history chart; warnings at 80% (default) | `/data/quotas` |
| **Reconciliation** | Positions and balances vs each venue: last run, mismatches (instrument, ours, venue's, difference), status, explanation (matched journal event) or "unexplained" with the time left before it halts everything (24 h). Defaults ([16 §2.9](../../16-configuration-and-safety-model.md#29-reconciliation), configurable): positions and open orders every 60 s, balances every 5 min, full reconciliation at end of day (Sydney); quantities must match exactly, balances within 0.01% or dust | `/data/recon`, WS `recon` |
| **Storage** | Parquet catalog size by venue/type, hot/cold tiers, Timescale compression stats, backfill jobs and their progress | `/data/feeds?storage=1`, `/lab/jobs?kind=backfill` |

## Actions

| Control | Command | Level |
|---|---|---|
| Pause / resume feed | `data.feed.pause` / `data.feed.resume` | C1 (shows which strategies depend on it) |
| Run backfill (source, instrument, range) | `data.backfill.run` | C1 |
| Run reconciliation now | `data.recon.run` | C1 |
| Acknowledge incident | `data.incident.ack` (appends an `audit.dq_ack` WORM row referencing the incident) | C0 |
| Adjust DQ thresholds | Link to D06 policy (data freshness, blackouts) / `system.settings.update` (DQ thresholds): tightening C1; loosening C3. Before Telegram C3 exists (Phase 1), loosening completes via the break-glass CLI (`mtctl approve <id>` + TOTP), audited | C1 / C3 |

## Acceptance criteria

1. **Speed:** the monitor flips `dq.status` to `stale` within 250 ms (p99) of the threshold being crossed ([16 §2.2](../../16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)); the UI shows it within the live-update lag (p95 < 500 ms), along with the bots it paused.
2. **Licence tags:** every feed shows its licence/cost tag. A paid feed can't be enabled (UI blocks it, server rejects it).
3. **Quotas:** quota warnings appear before throttling starts.

## Backend contract

- **Queries:** `/data/feeds`, `/data/dq-events`, `/data/costs`, `/data/quotas`, `/data/recon`, `/lab/jobs?kind=backfill`.
- **WebSocket topics:** `dq.status`, `cost`, `recon`, `lab.job`.
- **Commands:** `data.feed.pause|resume`, `data.backfill.run`, `data.recon.run`, `data.incident.ack`, `system.settings.update`.
