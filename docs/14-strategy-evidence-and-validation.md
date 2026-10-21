# Strategy Evidence, Trading Methods & Validation Harness

_Adopted from the CryptoTrader spec ([review](11-cryptotrader-crossover-review.md)), generalised from crypto to all asset classes. MasterTrader stays strategy-agnostic ([03 M0](03-build-spec.md)): this doc supplies **evidence-ranked defaults, guardrails and promotion gates**, not a fixed strategy. Evidence labels from the source are kept; figures are as of Sep 2026. Not financial advice._

## 1. Viability verdict (set expectations before building)

- **What the evidence supports:** a small, disciplined, multi-sleeve system, **not a money printer**. Run well, it could plausibly earn **~10–30% a year** on capital, with **15–30% drawdowns**, if strategies hold up out of sample.
- **Retail reality:**
  - BIS WP 1049: 73–81% of retail investors likely lost money on their initial bitcoin investment.
  - pump.fun: 0.4% of ~13.4M wallets realised $10k+.
  - Copy-trading: ~48% of followers profitable (vendor-adjacent study).
  - Alpha Arena S1: 4 of 6 frontier LLMs lost real money. **LLMs aren't a proven alpha source**, which is why they're advisors and teachers here, never the order path.
- **The benchmark rule:**
  - Every strategy must beat the **passive alternative for its asset class after all costs** over its evaluation window. For crypto that's holding BTC + stablecoin yield; for FX/indices it's buy-and-hold or carry; for equities it's an index ETF.
  - One that doesn't is switched off, and its capital goes to hold-and-earn (M22).
- **Your time:** labelling (~500 posts to start tier-B fine-tunes), approving drafts and votes, a weekly worst-five-trades review, and monthly calibration checks. Budget these hours.

## 2. Where a solo operator in Sydney has an edge

| Edge source | Solo? | Why |
|---|---|---|
| Speed (sniping, atomic arb, sandwiching, latency arb, prediction-market latency) | **No** | Sydney is ~100–250 ms from most matching engines; Solana arb bots pay 50–60% of profit in tips (avg US$1.58/arb) |
| Slow, capacity-limited premia (trend, carry, event drift) | **Yes** | Funds skip small, slow trades; small size is an advantage |
| Patience (2–30 day holds) | **Yes** | No redemption pressure |
| Rug/scam filtering in illiquid niches | Partial | Mostly avoids losses |
| Australian frictions (AUD premium) | Small | Thin; onshore fees 0.5–0.85% |

**Consequence:** strategies whose edge is latency are **not offered as templates** (§3, X/Never). A remote execution VM (Tokyo/Singapore) is a future option **only** after a measured, proven edge.

## 3. Strategy catalogue (evidence-ranked templates)

**Priorities:**
- **P1:** build now.
- **P2:** after P1 validates.
- **P3:** research/paper only.
- **X:** don't build.
- **Never:** prohibited.

**The counterparty rule:** each strategy must name its counterparty in one sentence (who loses to it and why). If it can't, it's noise. This is a required field in the M0 manifest.

| Strategy | Counterparty | Capital worth it | Latency | Evidence | Priority |
|---|---|---|---|---|---|
| Trend on majors (BTC/ETH/SOL; also FX majors, gold, indices), daily/4h, vol-targeted | Under-/over-reacting speculators; hedgers | A$2–5k | Minutes–hours | SSRN walk-forward: net Sharpe 1.41 vs 0.70 buy-and-hold, max DD −44.6% vs −84.4%; but trend adds ~0.05 Sharpe over pure vol-scaling (independent) | **P1** |
| Funding carry (long spot / short perp, same venue) | Leveraged longs paying funding | A$10k per venue | Minutes | Only ~40% of top spreads profitable after costs (MDPI 2026) | **P1, regime-gated** (AU derivatives access permitting, 12 §2) |
| Hold-and-earn (LSTs, blue-chip lending, Pendle PTs) | Borrowers, fixed-rate buyers | Any | — | On-chain dashboards | **P1 base layer** (M22) |
| HLP vault, capped | Hyperliquid traders | Any; ≤ 10% of stables | — | Past-month APR ~4% (late Sep 2026) | **P1 capped**, if Hyperliquid is approved |
| Cross-sectional momentum, top-20 liquid | Attention flows | A$10k+ | Hours | SSRN (survivorship-free rotation, Sharpe > 1.5) | **P2** |
| Cross-venue funding/basis | Fragmented price discovery | A$20k+ | Seconds–minutes | Most spreads revert before costs | **P2** |
| Memecoin momentum with rug filtering (enter 5–60 min after launch, not first slot) | Late retail buyers | A$1–5k sleeve; A$20–200 per trade | Seconds–minutes | Realised-PnL data bot-contaminated; small, concentrated gains | **P2, paper first** (≥ 300 paper trades) |
| Token-unlock pre-positioning (short into large team cliffs) | Recipients selling new supply | A$5k+, needs a perp | Days | Keyrock: ~90% of 16k+ unlocks show negative pressure from ~30 days before | **P2** |
| Event/macro drift (rates, CPI, central banks) on FX/indices/gold | Slow repricing | Varies | Minutes–days | Literature on post-announcement drift (to replicate) | **P2** (MasterTrader addition) |
| Community-coin rotation | Buyers chasing the coin that just ran | A$5k+ | Hours | Source article only | **P3** |
| Dated futures basis; mean-reversion/pairs; liquidation-cascade fading; intraday breakouts | Various | A$5–20k+ | Seconds–hours | Weak/anecdotal after fees | **P3** |
| Market-making (Hummingbot / Hyperliquid quote gate) | Takers | A$20k+ | Low ms | HLP is the benchmark; severe adverse selection for a remote maker | **P3** (must beat HLP on the same capital) |
| AUD premium arbitrage | Local on-ramp imbalance | A$20k+ | Minutes | No rigorous data; fees 0.5–0.85% | **P3 monitor** |
| Memecoin sniping; copy-trading KOL/smart-money wallets (wallets OK as **features**); listing/news latency trading; Solana atomic arb/backruns; JIT/active concentrated liquidity; millisecond CEX–CEX/CEX–DEX latency arb; Polymarket bots (blocked in AU) | — | — | Sub-second/colocated | Won by colocated firms; leaders dump on copiers | **X**: no template; the manifest validator rejects these patterns |
| **Sandwiching** / any user-harming MEV | Ordinary users | — | — | Potential market manipulation/fraud | **Never** |

**Portfolio allocation** (after validation; allocate by **risk**, not capital):

| Sleeve | Risk budget | Capital share |
|---|---|---|
| Trend on majors (vol-targeted, long-biased) | 40% | 30–40% |
| Funding carry (regime-gated, hedged) | 15% | 20–30% |
| Hold-and-earn (HLP ≤ 10% of stables) | 10% | 20–30% |
| Memecoin engine | 25% | ≤ 5–10% |
| Unlock/event sleeve | 10% | 5–10% |

**Stress-testing:**
- Trend and carry are both long crypto beta in bull markets, so stress-test against **May 2022, Nov 2022, Aug 2024 and Feb–Mar 2026**.
- Keep a 20–40% stable/AUD reserve.

**Minimum capital (after fees):**
| Strategy | Minimum |
|---|---|
| Trend | A$2–5k |
| Single-venue carry | A$10k |
| Cross-venue arbitrage | A$20k+ |
| Memecoin | A$1k (learning only) |
| Sensible first live allocation | **A$10–25k, only after paper passes** |

## 4. Trading methods (enforced in code; defaults, user-editable in D06)

**Trade selection:**
- **Validated signals only** (§6).
- **Regime filters:**
  - trend long only above a slow MA or with positive 30–90d momentum, with shorts capped;
  - carry only when the trailing 7-day annualised funding > fees + buffer (start 8%);
  - memecoins only when launchpad volume and graduation rate > their 30-day median.
- **Prefer slow, explainable premia.**

**Sizing:**
- **Volatility targeting first:** e.g. 15–20% annualised for trend, from 30–60d realised vol.
- **Kelly:** `f = (p·b − q)/b`, with b = measured average win ÷ average loss. **Quarter-Kelly is a ceiling, never a target.** Never the `(2p − 1)` shortcut, and never stack Kelly on a vol-targeted sleeve.
- **Drawdown de-risking:** halve exposure when a sleeve is > 15% below its peak.
- **Per-trade risk:**
  - directional strategies: ≤ 0.5–1% of sleeve equity;
  - memecoin positions: ≤ 0.25–0.5% of total equity, with the sleeve ≤ 5–10% of the book;
  - from the stop: `units = capital × risk% ÷ |entry − stop|`.
- **Leverage:** trend 1–1.5× gross; carry hedged at 1×; **2× hard cap** for crypto derivatives (12 §1).

**Stops and exits:**
- ATR-scaled trailing stops (2–4× daily ATR for swing/trend).
- Memecoins: time stops, partial profits into strength, **never average down**.
- The exit plan is fixed and logged at entry.

**Execution:**
- **Maker first:** post-only with a timeout, then escalate to taker. Implementation shortfall is logged per order (M16).
- **Large orders:** TWAP/slice anything > ~1% of 1-minute volume.
- **DEX:** tight slippage + private submission (13 §7).
- **Costs:** fees, spread, slippage and funding per venue are re-measured monthly, and backtests use those measured figures.

**Discipline:**
- **No discretionary overrides.** The only manual trading action outside approve-mode is **flatten-and-halt with a required reason**. Manual tickets in D05 are their own `manual` sleeve with their own limits and journal tag.
- **Review:** weekly review of the five worst trades.

**TradFi → 24/7 crypto porting pitfalls** (also for MasterTradingBot strategies):
- No session close, so daily bars need a fixed UTC cut, and weekends are thin.
- AU venue fees and spreads are far above FX ECN costs, so pip-sized scalper edges rarely survive.
- Perp funding every few hours must be in the backtest.
- Replace fixed-pip stops and lot sizing with ATR/vol scaling.
- Scalpers only on deep books.
- Explicit STP when strategies share an account.

## 5. Risk engine additions (M11)

**Sleeves:**
- Capital is split into **sleeves (engines)**, each with its own capital, limits and kill switch, so one sleeve's bad week can't drain another.
- The risk engine **nets exposure per asset across sleeves** and enforces a total per-asset cap.

**Default hard limits** (per sleeve unless noted; user-editable, loosening = C3):

| Limit | Default | On breach |
|---|---|---|
| Risk per trade | 1% of sleeve | Reject |
| Max position | 10% of sleeve (memecoins 2%) | Reject |
| Daily loss | 3% of sleeve | Sleeve halts until the next day |
| Drawdown from peak | 15% sleeve / **10% whole system** | Halt + alert + manual restart |
| Open positions | 10 per sleeve | Reject new entries |
| Stale data | 2 s (fast sleeves), 60 s (slow) | Hold, no new orders |
| **Decision deadline** | Per sleeve | Drop the decision (never act late) |
| API/RPC errors | 5 in 1 min | Sleeve pauses 10 min |
| Exchange concentration | 25–30% of total capital per venue | Block deposits/new exposure there |
| Leverage | 1× until approved; then ≤ 2× on majors | Reject |

**Fallback ladder** (shown live in D06):
1. Healthy, high confidence → normal size.
2. Healthy, low confidence → half size or observe only.
3. Decision late or feed stale → **hold** (never act on old state).
4. Model service down → deterministic rules only: manage exits, no new entries.
5. Hard limit breached → halt the sleeve, cancel open orders, close per the sleeve rule, alert.
6. Kill switch (you, from your phone) → everything halts, and hot balances sweep to the vault address.

**Daily health check (per sleeve):** the sleeve halts pending review if either:
- the live 30-day Sharpe is < ½ the validated figure; or
- drawdown is > 1.5× the backtest maximum.

**Kill criteria are written down before deployment** (stored in the manifest).

## 6. Validation harness (extends 03 §8)

**Backtest engine requirements:**
- **Signals:** act on the next bar/event.
- **Costs:** real fees, AMM/book impact at your size, gas and tips. **No fixed-bps slippage for illiquid assets.**
- **Fills:** only at prices that existed at that time and size.
- **Universe:** **delisted, rugged and dead instruments stay in the universe.**
- **Conventions:** one timezone and bar-close convention.
- **Trial counter:** every run records its parameter set and a **trial counter, incremented automatically on every tweak** (it feeds deflated Sharpe).

**Gates (all must pass):**
1. **Leakage review:**
   - An adversarial checklist is run on the strategy code: look-ahead, survivorship, repainting indicators, costs, fill realism, full-sample fitting, regime coverage, alignment.
   - A model (via the gateway) answers present/absent per item, **quoting the exact line**.
   - Any "present" blocks the strategy until fixed or waived by you, with the waiver audited.
   - This runs alongside the vendored freqtrade look-ahead/recursive analysers.
2. **Deflated Sharpe:**
   - The probability that the best Sharpe is real, given all variants tried.
   - Inputs: per-period (not annualised) Sharpe, observation count, skew/kurtosis, variance of Sharpe across trials.
   - **Pass at > 0.95.**
3. **Walk-forward:** judged on the **share of positive folds and the worst fold**, not the average.
4. **Per-year and per-regime:**
   - Profitable in **each year** and **each regime** (bull/bear/chop), across several assets, not just in aggregate.
   - Single-regime edges are labelled and only run in that regime.
5. **Cost stress:** results must survive **2× and 3× measured costs**.
6. **Benchmark:** beats the asset-class passive benchmark (§1) after costs.
7. **Paper then small money:**
   - Paper through the real policy, risk and execution path (≥ 2–4 weeks; ≥ 8 weeks for P1 sleeves; ≥ 300 trades for memecoins).
   - Live results must sit within the backtest's expected range before capital steps up.

**Decay monitoring (live):**
- Alert when the rolling 60-trade Sharpe or hit rate falls below the backtest's **5th percentile**.
- Run a **CUSUM** test on P&L residuals.
- Models retrain on schedule and are promoted only if they beat a frozen baseline on unseen data **on the worst fold and calibration**.

## 7. Phase capital steps & kill criteria (refines 04 Phase 7)

| Phase | Capital at risk | Exit / kill criteria |
|---|---|---|
| Paper (all P1 sleeves ≥ 8 weeks) | A$0 | Every P1 sleeve has a walk-forward deflated Sharpe > 0 at 95% with measured costs |
| Micro-live | A$2–5k | **Kill if:** live implementation shortfall > 2× modelled; live Sharpe after 60 trades < the backtest 5th percentile; **any reconciliation mismatch unexplained within 24h halts everything** |
| Scale P1, add P2 | Up to A$10–25k in **25% steps after 4 clean weeks each** | **Memecoin kill:** sleeve DD > 30%; negative expectancy after 200 live trades; rug rate among entries > 5%; any single loss > 1% of total equity |
| 12-month review | Decided at review | Keep only sleeves with positive live net P&L, live Sharpe > 0.5 over 12 months, and beating the benchmark. **Portfolio DD > 25% → flatten to stables + a 30-day review; two such events end the trading programme** and capital moves to hold-and-earn. |

## 8. MasterTradingBot integration

You have an existing **deterministic** system (EMA, scalping and rule-based strategies on ETFs, gold/commodities, FX and metals via **FP Markets on MT5**).

1. **Shared libraries, not merged engines.**
   - A pure-function **indicator/signal library** (EMA, ATR, scalper triggers; no I/O), tested with **golden files** against MasterTradingBot's historical outputs.
   - A **sizing/risk library** (vol-targeting, per-asset caps, correlation buckets).
   - These live in `mt_core`/`mt_strategy` as our own licence-clean code.
2. **Execution stays on FP Markets** at first:
   - **Primary:** the MT5 Python API on a Windows VPS near FP's MT5 servers (LD4 vs NY4 is settled by your client-area server name).
   - **Linux route:** FP Markets' **cTrader Open API**, the M12 cTrader adapter to prototype.
   - NautilusTrader has no official MT5/cTrader adapter, and the community ones are immature, so **none touches live money until tested in paper**.
3. **Merging:** once merged, MasterTradingBot strategies appear as M0 strategies (template "deterministic rule-based"). They share the risk manager, journal, tax and UI, and their execution adapter is MT5 or cTrader.
4. **Open items:** FP Markets FIX availability for retail; client-agreement clauses on algo trading/scalping/hedging; cTrader Open API limits (tracked in 12 §6).
