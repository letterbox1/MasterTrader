# If MasterTrader Became a SaaS — Legal & Licensing Notes

> Not legal advice. This is a technical/licensing map to discuss with a lawyer before launching anything commercial. Financial-services rules depend heavily on your jurisdiction.

## Short answer

The personal-use freedoms **do not carry over**, but the project doesn't "go out the window" either. Three separate things change:

1. **Open-source licences:** mostly manageable if you followed the hygiene in [build spec §9](03-build-spec.md#9-minimal-future-proof-hygiene-cheap-now-saves-a-rewrite-if-you-ever-go-saas). Only the **AGPL** parts and a few source-available licences force real changes.
2. **Data licences:** the **biggest practical blocker**. Most free data is personal/non-commercial only, and serving it to paying users needs paid commercial or redistribution licences.
3. **Financial regulation:** potentially the **biggest legal blocker**. Giving other people trading signals or running automated trading on their accounts can make you an investment adviser or a broker under the law.

---

## 1. Open-source licences in a SaaS

Key facts:
- **GPL** obligations only start when you *distribute* software. Running it on your own servers for users is not distribution (the "SaaS loophole").
- **AGPL** closes that loophole: if users interact with a modified AGPL program over a network, you must offer them its source.
- **LGPL** behaves like GPL for the library itself, not for code that merely uses it.

| Component | Licence | SaaS impact | What to do |
|---|---|---|---|
| NautilusTrader | LGPL-3.0 | ✅ OK as an unmodified dependency on your servers | If you modify Nautilus itself, you only have to publish those changes if you *distribute* it (e.g., a desktop app). Simplest: don't fork it; upstream fixes. |
| freqtrade code | GPL-3.0 | ✅ OK for pure server-side SaaS (no distribution) | ⚠️ If you ever ship a desktop/on-prem/self-hosted version to customers, the whole combined program must be GPL. Keep it isolated (§9) or rewrite it clean-room. |
| Hummingbot, TradingAgents, FinRobot | Apache-2.0 | ✅ OK | Keep LICENSE/NOTICE files. **Don't use "FinRobot" in your product name** (its trademark policy). |
| Vibe-Trading, osiris, Hindsight, LightRAG, ccxt | MIT | ✅ OK | Keep copyright notices. Remove osiris's token panel and unreviewable `.pyc` files anyway. |
| **nofx** | **AGPL-3.0** | ❌ Using its code in the SaaS forces you to publish the SaaS source to users | Don't use it; re-implement ideas clean-room (already the plan). |
| **MiroFish** | **AGPL-3.0** | ❌ Same as nofx | Drop it, or rebuild on CAMEL-AI OASIS (Apache-2.0). |
| Grafana | AGPL-3.0 | ⚠️ OK if **unmodified** and internal-only; risky if you modify it and expose it to customers | Keep it as an internal ops tool; build the customer UI yourself. |
| worldmonitor, Firecrawl server, backtesting.py | AGPL-3.0 | ❌ for customer-facing use | Avoid, or use permissive alternatives (crawl4ai). |
| vectorbt (open) | Apache-2.0 + **Commons Clause** | ❌ You can't sell a product or service whose value derives substantially from it | Replace with Nautilus / your own vectorised engine, or buy vectorbt PRO's licence. |
| ArcticDB | BSL 1.1 | ⚠️ Fine as your internal DB; not as a database service offered to third parties | Fine to keep internally, or use Timescale/Parquet. |
| TimescaleDB (TSL features) | Timescale License | ✅ OK for your SaaS; ❌ only if you sell "Timescale-as-a-service" | Fine. |
| Redis 8 | RSAL / SSPL / AGPL tri-licence | ⚠️ | Use **Valkey** (BSD). |
| LLM weights (Qwen/Llama/Chronos/TimesFM/Kronos) | Varies (Apache, Llama licence, custom) | ⚠️ Check each model's licence for commercial-use and user-count clauses | Keep a model licence register. |

**Licence checklist for a SaaS launch:**
1. Generate an SBOM (e.g., `pip-licenses`, `syft`) and fail CI on AGPL, SSPL, Commons Clause or "non-commercial" licences in customer-facing services.
2. Remove or replace: nofx-derived code, MiroFish, vectorbt (open), any GPL code *if* you will ever distribute software.
3. Ship a "third-party notices" page in the product (Apache/MIT attribution).
4. Have a lawyer review the result once, before launch.

---

## 2. Data licences — the real cost centre

| Data | Personal use | SaaS (show to or use for other users) |
|---|---|---|
| Yahoo / yfinance | ✅ | ❌ Prohibited. Buy a commercial feed. |
| Exchange market data (stocks/ETFs/options) | ✅ via your broker | ❌ Redistribution needs exchange licences and per-user fees (NYSE/Nasdaq/CBOE/OPRA). Vendors like Databento, Polygon/Massive, Intrinio or Alpaca's broker data can bundle this, at a cost. |
| Crypto exchange data via ccxt | ✅ | ⚠️ Usually OK for derived analytics; check each exchange's terms for raw redistribution. |
| FRED | ✅ | ⚠️ FRED's own data is fine, but **some series are copyrighted third-party data** (marked in FRED). Filter them out. |
| SEC EDGAR, US Treasury, BLS, EIA, USDA, CFTC, USGS, NOAA, GDACS | ✅ | ✅ US public domain or open; respect rate limits and fair-access (EDGAR requires a User-Agent). |
| GDELT | ✅ | ✅ Open, with attribution. |
| ACLED | ✅ (research account) | ❌ Corporate licence required; AI/LLM use restricted. |
| ReliefWeb / UCDP | ✅ | ⚠️ Mostly open with attribution; check each item's source licence. |
| Free tiers: Finnhub, Alpha Vantage, FMP, Twelve Data, CoinGecko Demo, Etherscan, Polygon free | ✅ | ❌ Paid commercial plans required. |
| Reddit API | ✅ (approved app) | ❌ Commercial use needs a paid Reddit data agreement. |
| X/Twitter | ⚠️ (official API only) | Official paid API tiers only. |
| Telegram public channels | ✅ | ⚠️ Grey area; follow Telegram's terms and the channels' rights. |
| News article full text | ✅ (reading) | ❌ Storing or redisplaying full articles is a copyright issue. Show headline + link + your own summary/sentiment, or license a news API. |
| LLM providers (Claude, OpenAI…) | ✅ | ✅ Commercial API terms allow it; follow the usage policies on financial advice. |

Rough budget to make a multi-asset SaaS data-legal: **hundreds to thousands of US$ per month** in data licences before your first customer, scaling with user count for real-time exchange data.

---

## 3. Financial regulation — what the product *does* matters most

| Product shape | Regulatory exposure (indicative) |
|---|---|
| **Software / tools only.** Users bring their own data keys and broker keys and configure their own strategies; you give no personalised recommendations. | Lowest. Generally treated as a software vendor. Still needs clear "not financial advice" terms, no performance promises, and marketing-claims compliance. |
| **Publishing signals or research to subscribers** (same for everyone, not personalised) | Medium. May fall under "publisher" exclusions in some regions (e.g., the US *Lowe v. SEC* publisher exclusion). In the UK/EU/AU, investment-research rules and financial promotions rules can apply. |
| **Personalised recommendations** ("you should buy X") | High. Investment adviser registration: SEC/state RIA (US), FCA authorisation (UK), MiFID II licence (EU), AFSL (Australia). |
| **Auto-trading users' accounts / managing money** | Highest. Discretionary portfolio management or broker-dealer rules; custody rules; potentially CTA/CPO registration for futures/FX (CFTC/NFA in the US). |
| **Crypto specifics** | MiCA in the EU (CASP licence for certain services), FCA crypto financial-promotions regime in the UK, state money-transmitter issues in the US if you touch funds. Never custody user funds. |

Common safe-ish pattern for v1 SaaS: **"bring-your-own-keys" analytics and automation software**. Users connect their own broker accounts via the broker's official OAuth/partner programme (e.g., Alpaca Broker/OAuth, IBKR's third-party programme). They pick and approve their own strategies; you never hold funds. Plus robust terms, risk disclosures, and **no performance claims** without audited, compliant presentation.

Other SaaS obligations:
- **Privacy:** GDPR/UK GDPR/CCPA (privacy policy, DPA, data residency).
- **Security:** encrypted broker keys (KMS), SOC 2-style controls once you have B2B customers, and pen-testing.
- **Broker/exchange partner agreements:** many APIs forbid operating on *other people's* accounts without a partner agreement.
- **Company and insurance:** set up a limited company; get professional indemnity / E&O and cyber insurance.
- **Tax/VAT** on digital services.

---

## 4. What to do *now* so a SaaS flip stays cheap

1. Follow [build spec §9](03-build-spec.md#9-minimal-future-proof-hygiene-cheap-now-saves-a-rewrite-if-you-ever-go-saas):
   - keep a `third_party/LICENSES.md` manifest;
   - keep GPL/AGPL code isolated;
   - tag every data source `license: personal|commercial_ok|unknown`.
2. Keep the core (`mt_core`, `mt_store`, `mt_guard`, `mt_agents`, `mt_engine` wrapper) **your own code** or MIT/Apache-derived.
3. Design data access behind provider interfaces so yfinance can be swapped for a licensed feed with a config change.
4. Keep the repo private. Publishing it would count as distributing any GPL code inside it.

## 5. Bottom line

| Question | Answer |
|---|---|
| Can I use everything (incl. GPL/AGPL) for personal use? | **Yes.** |
| Does flipping to a SaaS make the project impossible? | **No.** |
| What must change for a SaaS? | Drop/replace the AGPL bits (nofx, MiroFish), Commons-Clause vectorbt and non-commercial data. Pay for commercial data. Choose a product shape that fits your regulatory appetite. |
| Biggest cost? | Data licences. |
| Biggest legal risk? | Financial regulation (advice / managing others' money), not GitHub licences. |
