# Trading Journal & Tax Records (Module M18)

_Raw evidence: [research/tax-journal.md](research/tax-journal.md). **Not tax advice:** rules marked (U) are unverified against primary sources, and everything here should be confirmed by a registered Australian tax agent (plus a local adviser if you move)._

## Goals

1. **Record everything automatically.** Every fill, fee, funding/swap payment, deposit, withdrawal, transfer, airdrop, staking reward, dividend, interest payment and FX conversion lands in an append-only journal without manual entry.
2. **Produce Australian EOFY output** (1 July–30 June), and the activity-statement output that actually applies to you (see the BAS section below).
3. **Pluggable jurisdictions:** Australia now; UAE, Egypt and Cyprus (or anywhere else) later, driven by a **residency timeline**.
4. **Independent audit trail:** an hledger/Beancount export an accountant can read and diff.
5. **Three currencies on every event:** native amount, **USD** and **AUD** (RBA daily rate, with the rate source and timestamp stored), so a later change of base currency or residency doesn't need a re-price.
6. **Wallet registry:** every exchange account and on-chain address you own is registered (M22 unified wallet view, [13 §3](13-wallets-treasury-and-onchain.md#3-unified-wallet-view)). Transfers between your own wallets are tagged **internal** and are never disposals.
7. **Investment vs trading segregation:** wallets/sub-accounts are tagged `investment` or `trading`, so long-term holdings can be argued as capital even if active trading is treated as revenue (ask your tax agent).
8. **Optional export** to Syla / Koinly-style CSV so a tax agent can cross-check with their usual tool. Our engine stays primary.

## ⚠️ Key findings that shape the design

| Finding | Design impact |
|---|---|
| **Australian CGT reform from 1 July 2027** (Treasury Laws Amendment (Tax Reform No. 1) Act 2026, Royal Assent 26 June 2026, reported). For individuals, the 50% discount is replaced by **CPI indexation** plus a **30% minimum tax** on gains accruing after 1 July 2027. Pre-reform gains keep the 50% discount, reportedly via a deemed market-value disposal on **30 June 2027** (mechanism (U)). | Rules are **versioned by date** (`AU_2026`, `AU_2027_REFORM`). **Market-value snapshot of every open lot at 30 June 2027** (end of day AEST, price source recorded). ABS CPI series ingested. Per-lot split into pre- and post-reform portions. |
| **No existing OSS tool fits.** None handles AU CGT + revenue-account CFD/FX/futures + Div 775 forex + crypto income + the 2027 regime + multiple jurisdictions. Every tool hard-codes "50% if held ≥ 12 months". | **Build the rules engine in-house.** Borrow algorithms from rp2 (Apache) and isaacrowntree/ledger (MIT). |
| A **high-volume autonomous system may count as "carrying on a business"** (ATO tests). If so, gains are revenue (ordinary income), with no CGT discount. | The tax regime (investor vs trader-in-business vs revenue instrument) is a **per-FY, per-activity setting**, and the engine reports both ways until your tax agent decides. |
| **BAS:** a private investor needs no ABN, GST or BAS. Share and crypto trades are input-taxed financial supplies, excluded from GST turnover. The statement you're most likely to get is a **PAYG instalment notice**. | "BAS module" = **PAYG-instalment estimator** (quarterly). A GST/BAS mode stays dormant behind a flag in case you later trade through a company or business structure. |
| **Sources conflict on the 2027 reform's status** (the CryptoTrader research calls it a proposal, not law). | `AU_2027_REFORM` stays **behind a flag** until your tax agent confirms; reports show both regimes side by side. See [11 §3](11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved). |
| **Airdrop classification turns on what you did to earn it.** Tasks, staking or genuine protocol use point to ordinary income on receipt; a pure initial allocation points to a $0 cost base with CGT on disposal (U). | The campaign record ([08](08-airdrops-and-token-launches.md)) is linked to each airdrop journal event, so the evidence of "activity done to earn it" is attached. |
| **Egypt: crypto is effectively banned** (CBE Law 194/2020 Art. 206; no licences issued). | A **hard compliance flag**: block crypto mandates while the residency timeline says "Egypt". |
| **Wash sales:** no mechanical rule, but TR 2008/1 lets the ATO apply Part IVA to sell-and-rebuy losses. | Flag any loss disposal re-entered within N days (especially May–July). The AI must not tax-loss-harvest with reacquisition. |

## Tools vetted

| Repo | Licence | Verdict | What we take |
|---|---|---|---|
| [eprbell/rp2](https://github.com/eprbell/rp2) (+ dali-rp2) | Apache-2.0 | **Borrow** | Country-plugin pattern (`AbstractCountry`); FIFO/LIFO/HIFO/LOFO lot-matching plugins; Decimal arithmetic; crypto event types (airdrop, staking, mining, fork…); "transparent computation" report. **No AU plugin; no specific ID.** |
| [isaacrowntree/ledger](https://github.com/isaacrowntree/ledger) | MIT | **Borrow** | Correct ATO details: 12-month test excluding both days, per-parcel discount, brokerage in the cost base, losses applied to non-discount gains first. Also AU FY handling, myTax section mapping and the ABS CPI fetcher. Floats → convert to Decimal; FIFO-only; bank/CommSec focused. |
| [Librefolio/LibreFolio](https://github.com/Librefolio/LibreFolio) | AGPL-3.0 | Reference | Portfolio tracker (SQLite), not tax. ~20 broker importers and a provider-plugin registry are worth copying. **No RBA FX.** |
| [miladtm94/Investment-Portfolio-Tracker](https://github.com/miladtm94/Investment-Portfolio-Tracker) | MIT | Reference | Data model and IBKR Flex / CommSec / Kraken importers. **Don't trust its ATO engine:** its 365-day test is one day early, it uses old tax brackets, and it assumes no wash-sale rule. |
| [BittyTax/BittyTax](https://github.com/BittyTax/BittyTax) | AGPL-3.0 | Reference | **UK pooling rules**, which are wrong for Australia. ~90 crypto exchange CSV parsers are useful as format references. Its default price lookups call external APIs. |
| [vas3k/TaxHacker](https://github.com/vas3k/TaxHacker) | MIT | Optional sidecar | Receipt and expense capture only (deductible expenses: data, VPS, subscriptions). Run with a **local LLM**, Sentry DSN unset and external FX lookups disabled. Not investment tax. |
| [topics/tax-report](https://github.com/topics/tax-report) | — | Nothing for AU/AE/EG/CY | Country-specific (DE/IT/RU) tools only |
| **hledger** or **Beancount v3 + Fava** | GPL | **Adopt as the audit export** | Yearly double-entry ledger export with lot tracking: an independent second opinion and accountant hand-off. Choose Beancount (Python-native) unless you prefer hledger. |
| **Rotki** | AGPL-3.0 | Optional sidecar | Local on-chain/DeFi event decoding (airdrops, staking, LP). Ingest its decoded events; **don't** use its P&L (German defaults). |
| Ghostfolio | AGPL-3.0 | Optional sidecar | Portfolio dashboard via `POST /api/v1/import`. Not tax. |

**On log stores (Loki, Graylog, OpenObserve):** these are operational logs, not the journal of record. The journal lives in **Postgres** (append-only, hash-chained); Loki holds the operational logs. See [03-build-spec §5 M17](03-build-spec.md#m17-observability--audit--mt_obs).

## Architecture

```
NautilusTrader fills/positions ─┐
Broker statements (IBKR Flex, CommSec, OANDA, IG…) ─┤→ Ingestion adapters (own code; importer formats from InvestIQ/LibreFolio/BittyTax)
Exchange REST (ccxt ledgers) / on-chain (own indexer or Rotki sidecar) ─┤
Airdrop module (M4) / staking / funding / swaps ─┘
        ↓
Append-only JOURNAL (Postgres `journal` schema; raw payload + normalised event; hash chain; corrections via supersedes_event_id)
        ↓
FX & price service (RBA F11 daily for AUD; reputable-exchange rate for crypto; ECB / CBE / CBUAE for other homes; source recorded per event)
        ↓
LOT ENGINE (rp2-style; SPECIFIC_ID primary, FIFO fallback; Decimal; lots for every asset AND every non-AUD cash balance (Div 775);
            snapshots: 30-Jun-2027 reform, residency change (CGT event I1))
        ↓
JURISDICTION RULES ENGINE (plugins, versioned by date) + RESIDENCY TIMELINE
        ↓
REPORTS: myTax worksheet · CGT schedule · revenue/trading P&L · PAYG-I estimate · wash-sale & compliance flags · CY 8% crypto ledger · EG stamp duty
        ↓
EXPORTS: Beancount/hledger ledger · CSV/PDF accountant pack · CARF reconciliation (venue-reported vs journal)
```

### Journal event (captured per transaction)

- **Identity:**
  - `event_id` (UUIDv7) and `source` (nautilus / broker_stmt / chain / manual / airdrop);
  - `source_ref` (exec ID, order ID, tx hash + log index);
  - `ingested_at`, `supersedes_event_id`, `raw_payload_hash`.
- **Time:**
  - `ts_utc` (ns precision);
  - venue timezone and local time;
  - **taxpayer-local date**, which drives the FY and the "exclude both days" day count.
- **Venue and account:**
  - venue, account, venue country, custodial or self-custody;
  - wallet address and chain, counterparty address;
  - whether the counterparty is resident (for GST classification).
- **Instrument:** ID, ISIN/ticker/contract, asset class (equity, ETF, crypto spot, perp, future, option, CFD, FX spot, metal, cash), multiplier, expiry, settlement currency.
- **Economics:**
  - side, quantity, price, gross amount;
  - fees split by type: commission, exchange, regulatory, gas, funding, borrow/overnight financing, spread markup;
  - **home-currency equivalents** (AUD now; AED/EGP/EUR later) with `fx_rate`, `fx_rate_source`, `fx_rate_ts`.
- **Classification:** `event_type`, one of:
  - trade open/close, crypto↔crypto swap;
  - deposit, withdrawal, internal transfer;
  - staking reward, airdrop (established), airdrop (initial allocation), mining;
  - interest, dividend (franking credits, withholding);
  - funding payment, borrow fee, CFD financing, futures variation margin, expiry settlement;
  - fork, gift, loss/theft, fee-only, corporate action.
- **Lots:**
  - a `lot_id` on every acquisition, including income receipts and FX cash inflows;
  - match records showing which lots each disposal used, with the method and reason;
  - cost-base elements;
  - flags: taxable Australian property, pre-2027 snapshot value, I1 snapshot value.
- **Tax context:**
  - residency at that moment (from the timeline);
  - activity regime (investor / trader-in-business / revenue instrument);
  - wash-sale flag;
  - `strategy_id`.

### Jurisdiction plugin interface

```python
class JurisdictionRules(Protocol):
    code: str; valid_from: date; valid_to: date | None      # e.g. AU_2026, AU_2027_REFORM
    home_currency: str
    def tax_year(self, local_date) -> TaxYear                 # AU 1 Jul–30 Jun; CY/EG calendar year
    def is_resident(self, timeline, tax_year) -> ResidencyResult
    def classify(self, event, regime) -> Treatment            # CAPITAL | REVENUE | INCOME | EXEMPT | STAMP_DUTY | CRYPTO_FLAT
    def lot_policy(self, asset_class) -> LotPolicy            # AU: SPECIFIC_ID → FIFO
    def fx_policy(self) -> FxPolicy                           # AU: RBA daily; crypto: reputable exchange
    def compute(self, events, lots, tax_year) -> TaxComputation
    def on_residency_change(self, from_, to_, at) -> list[DeemedEvent]   # AU CGT event I1 (+ s104-165 election, modelled both ways)
    def reports(self) -> list[ReportGenerator]
    def compliance_flags(self, events) -> list[Flag]
```

| Plugin | Rules (summary) |
|---|---|
| **AU_2026** (through FY2026-27) | **Investor:** CGT with the 50% discount for lots held ≥ 12 months excluding acquisition and disposal days; capital losses applied before the discount, to non-discount gains first; carried forward. **Crypto:** every disposal including crypto↔crypto is a CGT event; staking rewards and established airdrops are ordinary income at AUD value (that value becomes the cost base); initial-allocation airdrops have a $0 cost base. **CFDs:** revenue account (TR 2005/15). **Futures:** revenue by default, with a per-instrument override (U). **Forex:** Div 775 gains/losses on foreign-currency cash balances (U on the thresholds and elections). **Trader-in-business mode:** all trading gains are ordinary income. **Wash-sale flags. myTax mapping:** items 18 (capital gains), 20 (foreign income), 24 (other income), 10/11 (interest/dividends), business schedule if trading (labels (U)). **PAYG-instalment estimator. Record retention:** ≥ 5 years (we keep everything). |
| **AU_2027_REFORM** (FY2027-28 onward) | 30 June 2027 snapshot split; CPI indexation of the cost base (ABS CPI); 30% minimum tax on post-reform real gains (U on the exact mechanism) |
| **AE** (UAE) | No personal income tax or CGT. **Corporate-tax monitor:** personal investment income is excluded unless the activity needs a licence or is business-like (AED 1m turnover threshold for natural persons). Virtual-asset transfers are VAT-exempt (Cabinet Decision 100/2024). Residency: 183 days, or 90 days + conditions, or principal residence. |
| **EG** (Egypt) | Listed securities: stamp duty per trade (reported 0.05% per side from 2026 (U)); gains on listed securities exempt; other income at progressive rates up to 27.5%. **Crypto hard-flag (prohibited).** Residency: 183 days. |
| **CY** (Cyprus) | Securities gains exempt; **8% flat tax on net crypto gains** (Art. 20E from 1 Jan 2026; losses offset same-year crypto gains only; enactment (U)); SDC on dividends/interest by domicile, with non-dom exemption for 17 years; GeSY 2.65%. Residency: 183 days or the 60-day rule. |
| **GENERIC** | Home currency + FIFO/HIFO capital report for unsupported countries |

**Cross-border events:**
- **Leaving Australia:**
  - Australia applies **CGT event I1**: a deemed sale of non-TAP assets at market value.
  - You can elect under **s104-165** to defer it; the engine models both outcomes.
  - After departure, it tracks each lot's TAP status.
- **CARF / CRS 2.0:** exchanges report crypto activity to tax authorities (Australia from 2027/28 (U)). The engine reconciles your journal against the venue's reported totals, and stores each venue's tax-residency declaration.

**Residency timeline:**
- A table of entries and exits per country. It can be fed manually or from passport-stamp/ICP reports.
- It also records domicile, permanent home, employment and centre-of-interests evidence.
- Each plugin evaluates its own tests from this timeline.
- **Where two countries could tax you,** tie-breakers come from the tax treaty between them (DTA status for AU-UAE/CY/EG is (U)).

### Quality

- **Golden-file tests** from ATO worked examples (e.g. bought 2 Feb 2018 → discount eligible from 3 Feb 2019) and each jurisdiction's published examples.
- **Property tests:**
  - lots are conserved;
  - matched quantity = disposed quantity;
  - journal balances reconcile to venue balances daily.
- **Corrections append:** supersedes events, never edits.
- **Every report records** which rule version and which FX/price source produced it.

### Questions for your tax agent (tracked as tasks)

1. Is the autonomous activity "carrying on a business"? This decides revenue vs capital for everything.
2. How are futures treated?
3. The exact 2027 transitional mechanism, and how it applies to crypto.
4. Div 775 thresholds and elections for broker cash balances.
5. Which tax treaties (DTAs) apply to AU-UAE/CY/EG?
6. Egypt's final stamp-duty rates; whether Cyprus Art. 20E is enacted, and how it interacts with non-dom status.
7. Australia's CARF start date.
