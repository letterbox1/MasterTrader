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
| HLP vault, capped | Hyperliquid traders | Any; ≤ 10% of stables **and** ≤ 5% of total portfolio, whichever is smaller (default, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)) | — | Past-month APR ~4% (late Sep 2026) | **P1 capped**, if Hyperliquid is approved |
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
| Hold-and-earn (HLP ≤ 10% of stables and ≤ 5% of portfolio) | 10% | 20–30% |
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
| Starting live allocation | Set per bot when it goes live: **default A$2,000** (suggested A$2–5k micro-live), only after paper passes ([16 §2.5](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)). It grows toward A$10–25k only through capital steps (§7) |

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
- **Drawdown de-risking (two stages, before the halt):** at **10%** below the sleeve's peak, new position sizes are halved; at **15%** the sleeve halts (§5). Both are defaults, configurable, with stage 1 always below stage 2 ([16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
- **Per-trade risk:**
  - directional strategies: default 1% of sleeve equity (UI range 0.1–2%; 0.5–1% is the evidence-based band);
  - memecoin positions: ≤ 0.25–0.5% of total equity, with the sleeve ≤ 5–10% of the book;
  - from the stop: `units = capital × risk% ÷ |entry − stop|`.
- **Leverage:** trend 1–1.5× gross; carry hedged at 1×; **2× hard cap** for crypto derivatives (12 §1), an L0 ceiling set in the bot strategy settings ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance); loosening is C3).

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
- **No discretionary overrides.** The only manual trading action outside HITL approvals is **flatten-and-halt with a required reason** (`position.close` with `halt: true` and a reason). Manual tickets in D05 are their own `manual` sleeve with their own limits and journal tag.
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

**Default limits** (per sleeve unless noted). These are defaults, not fixed rules: the reference values live in [16 §2](16-configuration-and-safety-model.md#2-default-values-all-configurable); tightening is immediate, loosening is C3:

| Limit | Default | On breach |
|---|---|---|
| Risk per trade | 1% of sleeve | Reject |
| Max position | 10% of sleeve (memecoins 2%) | Reject |
| Daily loss | 3% of sleeve | Sleeve halts until the next day (Sydney time) |
| **Sleeve drawdown, stage 1** | 10% below sleeve peak | **Halve new position sizes** |
| **Sleeve drawdown, stage 2** | 15% below sleeve peak | **Halt the sleeve:** cancel orders, close per the sleeve's exit rule, alert; restart is C3 |
| **System drawdown, stage 1** | 10% below portfolio peak | **No new entries anywhere**; exits and protective orders continue, positions keep their stops; restart is C3 |
| **System drawdown, stage 2** | 25% below portfolio peak | **Flatten** to stablecoins/AUD + 30-day review lock (§7) |
| Open positions | 10 per sleeve | Reject new entries |
| Stale data | Per bot: 2 s (fast), 60 s (slow); data age = now − our receive time; closed sessions aren't stale | M11 checks age **inline on every order** → reject; the ladder holds ([16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)) |
| **Decision deadline** | Per bot: scalping 1 s · intraday 10 s · swing 5 min · position 1 h | Drop the decision (never act late) |
| Price collar | 2% from last trade (crypto majors) · 0.5% (FX majors) · 1% (ETFs) | Reject |
| API/RPC errors | 5 in 60 s | That venue's orders pause 10 min |
| Cost blow-out | Realised ÷ modelled cost > 1.5× over the last 20 fills | Pause the bot, alert |
| Calendar blackout | 15 min before to 15 min after high-importance events (CB decisions, CPI, NFP, …), for bots marked `event_sensitive` (scalping/intraday by default) | Block new entries; exits and protective orders continue ([16 §2.8](16-configuration-and-safety-model.md#28-calendar-blackouts)) |
| Venue concentration | ≤ 25% of total equity per venue (range 10–30%) | Block deposits/new exposure there |
| Leverage | 1× until you approve more; crypto derivatives ≤ 2× (L0 ceiling) | Reject |
| Dead-man | Three layers: engine/component heartbeat missing 5 s → cancel orders; 10 s → each bot's `on_system_failure` (default `flatten`); venue cancel-after timers + resting venue stops ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) | Restart flat, bots paused until you resume |

**Drawdown notes:**
- Stage 1 must be below stage 2 (rejected at save time otherwise). If you prefer "15% then a further 15%", set sleeve stage 1 = 15% and stage 2 = 30%.
- The system stage-1 stop keeps positions under their resting stops, so gaps can still carry drawdown towards stage 2; that's why stage 2 flattens.
- Equity basis for the system stages: trading equity, excluding the vault and hold-and-earn, adjusted for deposits/withdrawals ([16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).

**Fallback ladder** (shown live in D06):
1. Healthy, high confidence → normal size.
2. Healthy, low confidence → half size or observe only.
3. Decision late or feed stale → **hold** (never act on old state).
4. Model service down → deterministic rules only: manage exits, no new entries.
5. Hard limit breached → halt the sleeve, cancel open orders, close per the sleeve rule, alert.
6. Kill switch (you, from your phone) → stops all new trading, cancels open orders, applies each bot's `on_system_failure` policy, freezes new treasury/earn moves, and (from Phase 5, default on) **sweeps hot trading balances to the vault address**. The protective sweep is exempt from the freeze. In Phase 2 there are no hot wallets yet, so the sweep is a logged no-op hook.

**Daily health check (per bot):** the bot halts pending your review if either ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)):
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
   - Any "present" blocks the strategy until fixed or waived by you (`lab.leakage.waive`, C2, with the waiver audited).
   - This runs alongside the freqtrade look-ahead/recursive analysers, vendored under `third_party/` with their GPL-3.0 licence and isolated in `mt_lab` (fine for personal, never-distributed use, [03 §1](03-build-spec.md#1-ground-rules); a SaaS would need a clean-room rewrite, [05](05-saas-legal-and-licensing.md)).
2. **Deflated Sharpe (DSR):**
   - DSR is a **probability** (0–1) that the strategy's true Sharpe is above zero, given all variants tried.
   - Inputs: per-period (not annualised) Sharpe, observation count, skew/kurtosis, variance of Sharpe across trials (the trial counter).
   - **Pass at DSR ≥ 0.95** (95% confidence; default, configurable, [16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)). "DSR > 0" in older text was an error.
3. **Walk-forward:** judged on the **share of positive folds and the worst fold**, not the average. Default: ≥ 60% of folds positive **and** worst fold ≥ −(sleeve halt drawdown).
4. **Per-year and per-regime:**
   - Profitable in **each year** and **each regime** (bull/bear/chop), across several assets, not just in aggregate.
   - Regimes are price-based, per asset, daily (`regime_v1`, [16 §2.4.1](16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results)): **bull** = above the 200-day average and 90-day return > +10%; **bear** = below it and 90-day return < −10%; **chop** = everything else. Sentiment-based regimes (P4) can only become later versions.
   - Single-regime edges are labelled and only run in that regime.
5. **Cost stress:** results must stay profitable at **2× measured costs**; **3×** is reported.
6. **Benchmark:** beats the asset-class passive benchmark (§1) after costs.
7. **Paper then small money:**
   - Paper/HITL through the real policy, risk and execution path before autonomous mode or a capital step: default **≥ 8 weeks and ≥ 50 trades**. Class overrides: P1 sleeves ≥ 8 weeks; memecoins ≥ 300 trades; low-frequency bots that can't reach the trade count use a ≥ 26-week window ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)).
   - Live results must sit within the backtest's expected range before capital steps up.
8. **Monte Carlo permutation:** p < 0.05.
9. **Safety drills:** kill switch, dead-man and restart drills passed on the bot's venue.

Gate values are defaults, configurable per strategy. **Loosening any gate is C3**; tightening is free.

**Decay monitoring (live): one meaning per signal** ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)):

| Signal | Action |
|---|---|
| A bot's rolling 60-trade Sharpe or hit rate below the backtest's **5th percentile** (low-frequency bots: a 26-week window) | Alert + **downgrade autonomous → HITL**; the week isn't clean |
| **CUSUM** break on P&L residuals | Alert + downgrade to HITL |
| Daily health check fails (§5) | **Halt the bot** pending your review |
| Kill criteria (§7) | **Halt the sleeve** + capital step-down |

Built in Phase 2 for paper bots; Phase 7 extends it to live with the kill criteria. Models retrain on schedule and are promoted only if they beat a frozen baseline on unseen data **on the worst fold and calibration**.

## 7. Phase capital steps & kill criteria (refines 04 Phase 7)

| Phase | Capital at risk | Exit / kill criteria |
|---|---|---|
| Paper (all P1 sleeves ≥ 8 weeks) | A$0 | Every P1 sleeve passes its gate profile (§6): walk-forward **DSR ≥ 0.95** with measured costs, paper ≥ 8 weeks and ≥ 50 trades by default |
| Micro-live | Starting allocation set per bot: default A$2,000 (suggested A$2–5k) | **Kill (halt the sleeve) if:** live implementation shortfall > 2× modelled; the sleeve's live Sharpe, once it has 60 live trades, < the backtest 5th percentile; **any reconciliation mismatch unexplained within 24 h halts everything** ([16 §2.9](16-configuration-and-safety-model.md#29-reconciliation)) |
| Scale P1, add P2 | **+25% of the current allocation** (A → 1.25A) after **4 consecutive clean weeks**, up to the sleeve's target cap (e.g. A$10–25k); each step is C3 | **Memecoin kill:** sleeve DD > 30%; negative expectancy after 200 live trades; rug rate among entries > 5%; any single loss > 1% of total equity |
| 12-month review | Decided at review | Keep only sleeves with positive live net P&L, live Sharpe > 0.5 over 12 months, and beating the benchmark. **System drawdown stage 2 (default 25% below portfolio peak) → flatten to stablecoins/AUD + a 30-day review lock; two such events end the trading programme** and capital moves to hold-and-earn. |

**Capital steps** (defaults, configurable, [16 §2.5](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)):
- **Clean week:** a calendar week (Mon–Sun, Sydney) with no kill-criterion breach, no unexplained reconciliation mismatch, no S1/S2 incident on that bot, live implementation shortfall ≤ 1.5× modelled, and weekly P&L inside the backtest's 5th–95th percentile band.
- **Step up:** after 4 consecutive clean weeks, +25% of the **current** allocation, up to the sleeve's target cap. Each step needs your approval (C3).
- **Step down:** a kill-criterion warning → back one step. A halt → back to the starting allocation after your review.

**Notes:**
- The 12-month review is a **scheduled recurring review** (a calendar task), not a phase item; Phase 7 closes once micro-live is stable.
- If hold-and-earn (M22, Phase 6) isn't built yet when capital must leave trading, the fallback is stablecoins on the venue plus a USER task to move them.
- The "Kill" column above refines the general signal table in §6; the per-bot rolling 60-trade window there only downgrades.

## 8. MasterTradingBot integration

You have an existing **deterministic** system (EMA, scalping and rule-based strategies on ETFs, gold/commodities, FX and metals via **FP Markets on MT5**).

1. **Shared libraries, not merged engines.**
   - A pure-function **indicator/signal library** (EMA, ATR, scalper triggers; no I/O), tested with **golden files** against MasterTradingBot's historical outputs.
   - A **sizing/risk library** (vol-targeting, per-asset caps, correlation buckets).
   - These live in `mt_core`/`mt_strategy` as our own licence-clean code.
2. **Execution stays on FP Markets** at first:
   - **Primary:** the MT5 Python API on a Windows VPS near FP's MT5 servers (LD4 vs NY4 is settled by your client-area server name). The VPS is hardened, reachable over Tailscale only, holds only the MT5 trade-only login and no other secrets ([07](07-security-notes.md)).
   - **Linux route:** FP Markets' **cTrader Open API**, the M12 cTrader adapter to prototype.
   - NautilusTrader has no official MT5/cTrader adapter, and the community ones are immature, so **none touches live money until tested in paper**.
3. **Merging:** once merged, MasterTradingBot strategies appear as M0 strategies (template "deterministic rule-based"). They share the risk manager, journal, tax and UI, and their execution adapter is MT5 or cTrader.
4. **Open items:** FP Markets FIX availability for retail; client-agreement clauses on algo trading/scalping/hedging; cTrader Open API limits (tracked in 12 §6).
