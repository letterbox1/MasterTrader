_Raw notes from the research agents (2026-10-21). They back up [../09-journal-and-tax.md](../09-journal-and-tax.md). **Not tax advice.** WebFetch couldn't reach ato.gov.au or aph.gov.au, so most legal points come from search summaries with official URLs; (U) = unverified._

# Journal / tax research notes

## Australian CGT reform (reported)
- **The Act:** Treasury Laws Amendment (Tax Reform No. 1) Act 2026, Act No. 49 of 2026, Royal Assent 26 June 2026.
  - https://www.ato.gov.au/law/view/pdf/acts/20260049.pdf
  - Bills Digest: https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2526/26bd067
- **From 1 July 2027, for individuals, trusts and partnerships:**
  - the 50% discount is replaced by CPI indexation for assets held ≥ 12 months;
  - a 30% minimum tax on real gains accruing after 1 July 2027 (Div 119 (U));
  - gains accrued before then keep the 50% discount;
  - reportedly via a deemed disposal and reacquisition at market value on 30 June 2027, Subdiv 112-E (U).
- **Commentary:**
  - https://www.pwc.com.au/tax/tax-alerts/2026-27-federal-budget-cgt-changes-is-30-june-2027-a-transaction-deadline.html
  - https://www.moore-australia.com.au/news/federal-budget-series-cgt-discount-reform/
- **ATO:** not applicable to Tax Time 2026. https://ato.gov.au/individuals-and-families/investments-and-assets/capital-gains-tax/cgt-discount

## Repo vetting
| Repo | Licence | Stars | Last commit | Notes | Verdict |
|---|---|---|---|---|---|
| eprbell/rp2 | Apache-2.0 | 403 | 2026-01-26 | Crypto only. FIFO/LIFO/HIFO/LOFO (universal application; per-wallet unfinished, #135). Countries: generic/US/JP/ES/IE. Long-term period in days, so it can't express the ATO "exclude both days" rule; no discount maths. ODS in/out. Decimal; ~151 tests; CodeQL CI. Event types cover airdrop/staking/mining/fork/gift/fee/move. | Borrow algorithms + plugin pattern |
| eprbell/dali-rp2 | Apache-2.0 | 81 | — | Loaders (Binance.com, Coinbase, Kraken REST; many CSVs); `native_fiat`; Frankfurter/exchangerate.host/CSV FX | Reference |
| BittyTax | AGPL-3.0 | 508 | 2026-10-05 | UK same-day / B&B / s104 pooling hard-wired; ~90 crypto CSV parsers; calls api.bitty.tax, CoinGecko, CoinPaprika, Frankfurter | Reference only |
| isaacrowntree/ledger | MIT | 3 | 2026-09-07 | ~3.25k LOC, ~359 tests. `etl/cgt.py` gets the ATO details right (discount if disposed > acquired + 1 year; brokerage in the cost base; losses to non-discount gains first). AU FY; ATO return sections; ABS CPI fetch (`etl/cpi.py`). Floats; FIFO only; CommSec PDFs; FX inferred from bank transactions. | Borrow small pieces |
| miladtm94/Investment-Portfolio-Tracker (InvestIQ) | MIT | 7 | 2026-05-29 | FastAPI/Postgres/Redis/Celery/Next.js. FIFO/LIFO/HIFO TaxLot, Decimal. Importers: CommSec, IBKR Flex, Kraken, Stake, CMC, MooMoo. **Bugs in `backend/services/ato_tax_engine.py`:** `holding_days >= 365` is one day early; old 19%/32.5% brackets; "no wash-sale equivalent" comment. AI advisor uses Gemini/Claude/OpenAI or Ollama. | Reference |
| vas3k/TaxHacker | MIT | 6.8k | 2026-09-21 | Next.js/Prisma/LangChain; receipts and invoices. LLM: OpenAI/Gemini/Mistral/OpenAI-compatible (local OK). Sentry hooks (DSN from env), Stripe SaaS code, FX via xe.com scraping, fawazahmed0 API and Frankfurter. | Avoid as tax engine; optional receipts sidecar |
| Librefolio/LibreFolio | AGPL-3.0 | 27 | 2026-10-15 | FastAPI/SQLite; REST `/api/v1/transactions`; ~20 broker importers; FX from ECB/BoE/Fed/SNB (no RBA); FIFO/WAC for performance only | Reference |

### Other tools
| Tool | Licence / stars | Notes | Verdict |
|---|---|---|---|
| hledger | GPL-3.0 | 1.99.x lot tracking (FIFO/LIFO/HIFO/AVERAGE) and automatic capital gains | Audit export candidate |
| Beancount v3 + Fava | GPL-2.0 / MIT (U) | Booking STRICT/FIFO/LIFO/AVERAGE; Python API | Audit export candidate |
| Rotki | AGPL-3.0, ~4.1k★ | Local encrypted crypto/DeFi accounting; FIFO/LIFO/HIFO/ACB; German defaults | Decoder sidecar only |
| Ghostfolio | AGPL-3.0, ~9.5k★ | `POST /api/v1/import`; no tax | Optional UI |
| Wealthfolio | AGPL-3.0, ~9.2k★ | Tauri/Rust/SQLite; no tax | Skip |
| Portfolio Performance | EPL-1.0, ~4.1k★ | Strong PDF/IBKR Flex importers; no AU tax | Reference |
| tax-report topic | — | cdump/investments (RU focus (U)); Gemma41/Onchain-Accounting (new, unvetted) | Nothing for AU/AE/EG/CY |

## Australia (current law)
- **Investor vs trader-in-business:** ATO factors are repetition, volume, organisation, records, a business plan and profit intent. A trader holds trading stock, so gains/losses are income or deductions (non-commercial loss rules apply) and there's no CGT discount. The suggested ruling number is (U).
  - https://www.ato.gov.au/individuals-and-families/investments-and-assets/capital-gains-tax/shares-and-similar-investments/share-investing-versus-share-trading
  - https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/income-and-deductions-for-business/crypto-assets-and-business/crypto-assets-used-in-business
- **CGT discount:** the asset must be held ≥ 12 months **excluding the acquisition and disposal days** (e.g. bought 2 Feb 2018 → eligible from 3 Feb 2019). Losses are applied before the discount.
  - https://www.ato.gov.au/general/capital-gains-tax/working-out-your-capital-gain-or-loss/working-out-your-capital-gain/the-discount-method-of-calculating-your-capital-gain/
- **Parcel identification:** specific identification where records allow; FIFO as fallback (U for the ATO citation).
- **Crypto:**
  - Every disposal, including crypto↔crypto, is a CGT event valued at AUD market value (reputable exchange rate).
  - Staking rewards are ordinary income at receipt value, which becomes the cost base.
  - Established airdrops are income at receipt; initial allocations have a $0 cost base (U on current wording).
  - https://www.ato.gov.au/Individuals/Investments-and-assets/Crypto-asset-investments/Transactions---acquiring-and-disposing-of-crypto-assets/Crypto-to-crypto-exchange-or-swap/
  - https://www.ato.gov.au/individuals-and-families/investments-and-assets/crypto-asset-investments/transactions-acquiring-and-disposing-of-crypto-assets/staking-rewards-and-airdrops
- **CFDs:** revenue account under TR 2005/15. https://www.ato.gov.au/law/view/pdf/pbr/tr2005-015.pdf
- **Futures:** revenue / s15-15 likely (U).
- **Forex:**
  - Div 775 covers gains/losses on holding foreign currency; Subdiv 960-C sets the translation rules (TR 2007/5).
  - The $250 threshold and limited-balance election are (U).
  - The ATO uses RBA rates (since 1 Jan 2020); crypto may use reputable exchange rates.
  - https://www.ato.gov.au/law/view/pdf/pbr/tr2007-005.pdf
- **Wash sales:** TR 2008/1 (Part IVA); the ATO data-matches.
  - https://www.ato.gov.au/law/view/pdf/pbr/tr2008-001.pdf
  - https://www.ato.gov.au/media-centre/wash-sales-the-ato-is-cleaning-up-dirty-laundry
- **Records and data matching:**
  - Keep records 5 years.
  - The crypto data-matching program runs FY2014-15 to FY2025-26.
  - https://www.oaic.gov.au/privacy/privacy-registers/data-matching-exemptions-register/crypto-assets-2014-15-to-2025-26-financial-years-data-matching-program
- **myTax:** items 18 (G/H/A/V + crypto question), 20, 24, 11, 10; business schedule if trading (labels (U)).
- **GST/BAS:**
  - No ABN/GST/BAS for a private investor.
  - Securities and crypto trades with residents are input-taxed financial supplies; with non-residents, GST-free. Input-taxed supplies are excluded from GST turnover.
  - The likely statement is a **PAYG instalment** notice: you're entered automatically when instalment income ≥ $4,000, tax ≥ $1,000 and notional tax ≥ $500 (capital gains are excluded from instalment income).
  - https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/in-detail/your-industry/gst-and-crypto-assets/gst-and-trading-digital-currency

## UAE
- No personal income tax or CGT.
- **Residency** (Cabinet Decision 85/2022): 183 days, or 90 days + conditions, or principal residence. Evidence comes from an ICP entry/exit report.
  - https://taxsummaries.pwc.com/united-arab-emirates/individual/residence
- **Corporate tax** applies to natural persons only above AED 1m business turnover; personal investment income is excluded unless the activity needs a licence (Cabinet Decision 49/2023).
  - https://mof.gov.ae/wp-content/uploads/2023/05/Cabinet-Decision-No.-49-of-2023.pdf
- **VAT:** virtual-asset transfers exempt (Cabinet Decision 100/2024; retroactivity (U)).
- AU-UAE DTA status (U).

## Egypt
- **Listed securities:** CGT replaced by stamp duty; a 2026 amendment reports 0.05% per side and gains exempt (U).
  - https://www.dailynewsegypt.com/2026/08/03/egypt-exempts-listed-securities-capital-gains-from-income-tax-to-boost-stock-market/
- **Crypto:** prohibited without a CBE licence (Law 194/2020 Art. 206; no licences issued).
  - https://eg.andersen.com/legality-cryptocurrency-in-egypt/
- **Personal income tax:** progressive up to 27.5% above EGP 1.2m.
- **Residency:** 183 days or a permanent abode; foreign-income rule (U).

## Cyprus
- CGT applies to Cyprus immovable property only; securities gains are exempt.
- **2026 reform** (Law 207(I)/2025): 8% flat tax on net crypto gains under Art. 20E; losses offset same-year crypto gains only (enactment (U)).
  - https://cy.andersen.com/news/cyprus-news-cyprus-tax-reform-comprehensive-update-effective-from-1-january-2026/
- **SDC:**
  - Non-doms are exempt for 17 of 20 years (an extension option is reported).
  - Domiciled residents: dividends 17%→5% from 2026; interest 17%.
  - GeSY 2.65%.
- **Residency:** 183 days or the 60-day rule.
  - https://cy.andersen.com/news/the-60-day-tax-residency-rule-for-individuals/

## Cross-border
- **CGT event I1** on ceasing AU residency: a deemed disposal of non-TAP assets. The s104-165 election defers it for all assets.
  - https://legalvision.com.au/moving-overseas-exit-tax
- **Interaction with the 2027 reform** (U).
- **CARF/CRS 2.0:** first exchanges in 2027; Australia possibly in the 2028 group (U).
  - https://www.regnology.net/en/resources/regulatory-topics/crypto-asset-reporting-framework-carf/
