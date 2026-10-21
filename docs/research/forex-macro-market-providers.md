_Raw notes from the research agents. They back up [../06-aggregators-and-market-providers.md](../06-aggregators-and-market-providers.md). Checked 2026-10-21: library versions and licences come from the PyPI JSON API; GitHub stars weren't collected (API blocked); (U) = unverified._

# Additional forex / multi-asset providers & OSS aggregators

## 1. Forex data & brokers
| Provider | What it gives | Free / limits | Python lib (PyPI ver/date/licence) | Verdict / module |
|---|---|---|---|---|
| OANDA v20 (+ orderBook/positionBook) | Prices, candles, trading, retail positioning books | Free practice account | oandapyV20 0.7.2/2021/MIT (stale); v20 3.0.25/2018/MIT. **Book endpoints still live? test it (U)** | M1, M12, M6 |
| FXCM ForexConnect/fxcmpy | — | REST phased out after Q1 2023; vendor reports public API deprecated 2026 | forexconnect 1.6.43/2022/proprietary | **SKIP** |
| IG REST + Lightstreamer | CFD/spot FX, indices, commodities, trading, **client sentiment** | Free demo; weekly historical allowance (U) | trading-ig 0.0.25/2026-08-25/BSD-3 | M1, M12, M6 |
| Saxo OpenAPI | Multi-asset broker API | SIM free, 24h token, $100k sim; live by contacting Saxo | saxo_openapi 0.6.0/2019 stale → thin httpx client | M12 optional |
| cTrader Open API / FIX (Spotware) | Works with any cTrader broker; FIX free per account | Free demo | ctrader-open-api 0.9.2/2024-06/MIT (official) | M12, M1 |
| Dukascopy | Free historical ticks (bi5); JForex | Free | duka 0.2.0/2016 dead → dukascopy-node (npm, MIT, U) or own bi5 parser | M1 |
| TrueFX | Free top-of-book interbank ticks | Free w/ registration (U); 2026 availability unconfirmed | none | M1 cross-check |
| HistData.com | Free M1 bars/ticks FX + metals | Manual download | scrapers | M1 cross-validation |
| FOREX.com/GAIN (StoneX) | REST + Lightstreamer | Live account; AppKey via support (~3 days) | unofficial libs | M12 low priority |
| IBKR IDEALPRO | Interbank FX | FX top-of-book free for funded accounts (U) | ib_async 2.1.0/2025-12/BSD | M12, M1 |
| MT5 | Terminal IPC, Windows only | Free w/ broker | MetaTrader5 5.0.6231/2026-09-27/MIT | M12, M1 |
| MT4 ZMQ (DWX) | — | Unmaintained; MT4 EOL | — | SKIP |
| TradingView / tvdatafeed | No official data API; ToS bans extraction (U) | — | not on PyPI | SKIP (lightweight-charts for UI only) |
| ECB reference rates (Data Portal) | ~30 ccy vs EUR daily | Free no key | sdmx1 2.28.0/2026-10-18/Apache-2.0 | M1, M6 |
| Frankfurter (OSS) | JSON over ECB rates since 1999; self-hostable Docker | Free | frankfurter 2.0.0/2025-01/MIT | M1 self-hosted |
| exchangerate.host | — | 100 req/month | — | Skip |
| Open Exchange Rates | 170+ fiat | 1,000 req/month, USD base | — | Optional exotics |
| Alpha Vantage FX | — | 25/day, 5/min | alpha_vantage 3.0.0/MIT | Skip |
| Twelve Data FX | FX/crypto/US equities | 8/min, 800/day; individual plans personal only | twelvedata 1.4.0/2026-04/MIT | M1 backup bars |
| Polygon → Massive | FX separate subscription; free basic likely stocks-only (U) | — | massive 2.9.0/2026-10/MIT | Paid only |
| Tiingo FX | FX top-of-book | Free tier (numbers U) | tiingo 0.16.1/MIT | Optional |
| Finage | — | unknown | — | Skip |

## 2. Economic calendars & central banks
- **FRED/ALFRED release dates** (`fred/releases/dates`): US calendar backbone, point-in-time. fredapi 0.5.2.
- **ForexFactory weekly JSON** (`nfs.faireconomy.media/ff_calendar_thisweek.json`) (U): the only practical free source of consensus forecasts; ToS-grey, personal use, cache it.
- Investing.com / investpy (2022) / investiny (2022): **dead** + ToS. Trading Economics: paid (~$149/mo+, U). Myfxbook calendar / FXStreet / DailyFX: skip.
- Fed RSS (statements, minutes, speeches) + FOMC calendar; **ECB Data Portal** SDMX (rates, FX, SPF); **BoE IADB** CSV; **BoC Valet** JSON (no key, U); BoJ/SNB/RBA/RBNZ CSV/API (U).
- **IMF** SDMX 3.0 (legacy dataservices.imf.org decommissioned 2025); imfp 2.1.0/2026-09/Apache. **OECD**, **BIS** (REER/NEER, credit gaps), **Eurostat** via sdmx1; **World Bank** via wbgapi 1.0.14/MIT; ONS API.
- **DBnomics**: one API over 80+ providers; Python lib is AGPL (fine for private use).
- Use **sdmx1** (2.28.0, active), not pandasdmx (stale since 2023).

## 3. Reports & forecasts
| Source | Access | Notes | Module |
|---|---|---|---|
| CFTC COT | Socrata API + zips; cot-reports 0.1.3 (stale) | Public domain | M6, M5 |
| IMF WEO, OECD EO | SDMX | Free | M6, M3 |
| Fed SEP / dot plot | HTML/PDF; FRED median series (U) | Public domain | M6, M3 |
| CME FedWatch | Official paid API (~$25/mo EOD, U); **don't scrape** | Free alternative: compute from ZQ futures | M6 |
| ECB SPF | ECB Data Portal | Free | M6 |
| Atlanta Fed GDPNow | XLSX; FRED GDPNOW (U) | Free | M6 |
| NY Fed Staff Nowcast | Page + FRBNY-RG/New-York-Nowcast | Free | M6 |
| Cleveland Fed inflation nowcast | Website | Free | M6 |
| **LBMA gold/silver** | **IBA licence required, incl. historical** | SKIP; use spot XAU/XAG (OANDA/Dukascopy/IBKR) + COMEX GC/SI | — |
| World Gold Council Goldhub | Registration; reuse limited | Manual | M6 |
| Kitco | No API; scraping ToS-risky | SKIP | — |
| Baker Hughes rig count | Weekly XLSX (U) | Free | M6, M5 |
| EIA STEO, USDA WASDE / NASS QuickStats | APIs/XML | Public domain | M6, M5 |
| Cboe VIX history | CSV; FRED VIXCLS | Free | M6 |

## 4. OSS aggregators & libs
| Project | PyPI | Status | Use |
|---|---|---|---|
| OpenBB | 5.0.0/2026-09-29/Apache | Active | M1/M6 umbrella |
| **FinanceToolkit** | 2.2.3/2026-10-12/MIT | Active | M6 ratios/models |
| **FinanceDatabase** | 2.5.1/2026-10-12/MIT | Active | Symbol master |
| investpy / investiny | 2022 | Dead | Skip |
| pandas-datareader | 0.11.1/2026-06/BSD-3 | Mostly broken/redundant | Skip |
| **akshare** | 1.19.1/2026-09-30/MIT | Very active | China/Asia futures, FX, SHFE/DCE/ZCE; M1 secondary |
| pyqlib | 0.9.7/2025-08/MIT | Active-ish | M6 research |
| yahooquery | 2.4.1/MIT | Maintained | yfinance alternative |
| finvizfinance | 1.5.0/2026-08/MIT | Active | Optional screener (ToS grey) |
| **sdmx1** | 2.28.0/2026-10-18/Apache | Very active | ECB/IMF/OECD/BIS/Eurostat |
| Ghostfolio | AGPL (U) | Active | Optional portfolio UI |
| lightweight-charts | JS Apache (U); py wrapper 2.1/MIT | Active | UI charts |
| ccxt | 4.5.89/2026-10-20/MIT | Very active | M1/M12 |
| CoinGecko | pycoingecko 3.2.0 | Demo 10k calls/month; 100 RPM since 2026-05-17 | M1 |
| CryptoCompare/CCData | — | Free tier reportedly retired 2026-05-21 (U) | Skip |
| CoinPaprika | lib dead 2019 | Free API (U) | Optional fallback |
| Messari | — | Free tier conflicting (U) | Low |
| Glassnode | — | No free API | Skip |
| CoinGlass | — | Paid; Hobbyist $29/mo, 30 req/min, personal | Optional |
| **Binance data.binance.vision** | python-binance 1.0.37/MIT | Free bulk klines/trades/futures metrics incl. long/short (U) | **M1 backfill top pick** |
| Tardis.dev | tardis-dev 5.0.2/MPL-2.0 | First day of month free (U) | Order-book samples |

## 5. Retail sentiment & positioning
- **Myfxbook Community Outlook**: free 100 req/24h (all symbols in one call), session bound to IP, 1-month TTL. **Yes**; poll every 15–30 min.
- **IG Client Sentiment** (`/clientsentiment/{marketId}`, U) via trading-ig. **Yes.**
- **OANDA order/position books**: yes, if the live test passes (U).
- Dukascopy SWFX: web only, 30-min updates; optional low-frequency scrape (ToS grey).
- FXSSI: skip. CoinGlass long/short: paid; Binance futures long/short free (U). COT: yes.

## 6. Prediction markets
| Platform | Access | Notes |
|---|---|---|
| **Kalshi** | `api.elections.kalshi.com/trade-api/v2`; public reads need no auth | CFTC-regulated; Fed/CPI/NFP/GDP markets; official lib is proprietary, so use httpx |
| **Polymarket** | Gamma + CLOB, no auth for reads | py-clob-client 0.34.6/MIT; CLOB V2 2026-04-28 (U); some fields are JSON-encoded strings |
| Manifold | Public reads (U) | Play money; weak |
| Metaculus | Token; ToS restricts commercial / AI training (U) | Personal research only |

## Open checks before building
- OANDA book endpoints
- TrueFX downloads
- IMF SDMX 3.0 base URL
- IG sentiment endpoint path
- Tardis free samples
- Messari free tier
- BoC Valet / BoJ keyless access
