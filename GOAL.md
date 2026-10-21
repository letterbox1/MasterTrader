# Goal

Build **MasterTrader**: a private, single-user, self-hosted AI trading **platform**. It combines the best parts of leading open-source trading projects into one system, running on **free data sources and free tiers only**.

MasterTrader is a platform, not a strategy. It should let the user set up, experiment with and run **any type of strategy** (scalping, intraday, EMA/MA, mean-reversion, breakout, swing, position, grid/DCA, market making, pairs, event-driven, ML or LLM-driven) on **any timeframe**, from tick/order-book level up to daily and longer. Strategies come after the platform works.

## The platform must

- **Ingest:**
  - market data (ticks to daily);
  - macro, fundamental, news, social (Telegram, Discord, Bluesky…) and calendar data;
  - global-event data (disasters, conflicts, geopolitics);
  - all from free and open sources.
- **Research:**
  - build, backtest, simulate, validate, optimise and paper-trade strategies with **realistic, measured costs**;
  - track every experiment.
- **Decide** with AI agents: multi-agent debate, valuation tools, RAG memory with reflection.
- **Manage risk** through a built-in, user-configurable risk manager: limits, sizing, kill switch, dead-man's switch.
- **Monitor live, autonomously:**
  - data quality (stale feeds, gaps, bad ticks, cross-source divergence);
  - real trading costs (spreads, fees, funding, swaps, slippage);
  - anomalies.
- **Execute** through broker and exchange connectors, from paper to live, always behind the risk manager.
- **Record everything automatically:**
  - an append-only audit trail;
  - a trading journal;
  - tax records with Australian EOFY and PAYG-instalment output now, and pluggable rules for the UAE, Egypt, Cyprus or anywhere else later.
- **Curate airdrops, token launches and ICOs:**
  - vet them against rug-pull and scam signals;
  - participate autonomously only where that's safe and permitted;
  - otherwise queue step-by-step instructions and the social-engagement tasks you need to do.
- **Curate communities:** tell the user which Discord servers, announcement channels and Telegram channels to join or follow, on a daily or weekly cadence.
- **Later, optionally:** let the user talk to and control the system through Claude via MCP (analysis, trade adjustments, risk changes). This is built last.

## Asset and market scope

- **Trading:** crypto (spot/perps), forex, commodities and precious metals (via CFDs/perps where futures data isn't free), stocks, ETFs, bonds (via ETFs/futures), IPOs.
- **Tracked:** ICOs/token launches, crypto airdrops, social engagement requirements, forex and index reports, forecasts and nowcasts, retail positioning, prediction-market probabilities, global events.

## Non-goals

- Guaranteed profitability claims.
- Hard-coding a trading style, timeframe, capital amount or loss tolerance. Those are user inputs.
- Unattended live trading without user-set mandates and risk limits.
- Self-bots, fake engagement, sybil farming, or scraping that breaks a platform's terms.
- Paid data or APIs, including Reddit and X unless free and permitted.
