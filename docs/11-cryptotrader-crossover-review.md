# CryptoTrader Spec Review: Crossover Vetting

_Reviewed 2026-10-21._

**Inputs:**
- *CryptoTrader — Build Spec v0.1* (28 Sep–1 Oct 2026, spec only, no code).
- Its *Integration catalogue*.

CryptoTrader is a sibling project (airdrops, hold-and-earn, memecoin/majors trading, cross-exchange arbitrage) intended to merge into the unified platform. MasterTrader is that unified platform, so its useful parts are folded in here.

**Method:**
- Every section was compared against MasterTrader's docs (01–10, `docs/ui/`, DESIGN.md).
- **Direct crossover** (same idea, already specified here) was **dropped**.
- **New specs or systematic approaches** were **added**, either to new docs 12–14 or as edits to existing docs.
- **Conflicts** were resolved, with the reasoning recorded.
- Claims from CryptoTrader keep their own verification labels (vendor / secondary / UNVERIFIED). They're **not re-verified** in this session unless noted.

---

## 1. Dropped: already covered in MasterTrader

| CryptoTrader item | Where MasterTrader already has it |
|---|---|
| Event bus + append-only store as the training set | Architecture §5–6 (NATS, append-only audit/journal, teacher logs) |
| NautilusTrader as the core, pinned; Freqtrade research-only; ccxt; Hummingbot as reference/sidecar | 01 vetting report, 03 M12/M13 |
| "Code computes → model judges → code decides → risk veto" | Architecture §1 principle 2; 10 §4 Decision One |
| Gradient-boosted trees for numeric data; decision models for text; no model in the latency path | 10 §4 (tier A / tier B) |
| Laya assessment (weak zero-shot, over-confident, fine-tune + calibrate) | 10 §4, research/decision-models-system-one.md |
| Point-in-time data, raw payload retention, stale feed disables dependants | 03 §4, M16 |
| Deflated Sharpe, walk-forward, look-ahead checks, paper before live | 03 §8, M7 |
| Kill switch, dead-man's heartbeat, idempotent order IDs, reconciliation | 03 M11/M16, 07 §6 |
| Trade-only, no-withdraw, IP-allow-listed keys; secrets out of `.env`; pinned digests | 07 §2–3, §7 |
| Discord: own server + followed announcement channels + own bot; no self-bots | 06, 08 curation queue |
| Quest platforms manual; no sybil/multi-wallet; no fake engagement | 08 principles |
| Airdrop tax: ordinary income vs initial allocation; 5-year records | 09 |
| Telegram bot alerts/approvals; Tailscale; Postgres/Timescale; Prometheus/Grafana; restic | Architecture §3, 07 |
| Rug checks (mint/freeze authority, LP, concentration), GoPlus/RugCheck/Honeypot.is, phishing lists | 08 |
| X: "verify, never discover" and pay-per-use (deferred here) | 06 §0 (X deferred) |

## 2. Added: new specs and systematic approaches

| Topic | Added where | Why it matters |
|---|---|---|
| **Telegram API terms ban using Telegram data to train, fine-tune or deploy AI** (per CryptoTrader research, Telegram API ToS §1.5) | 12 §4; 03 M2; 06; 10 | MasterTrader was sending Telegram text through FinBERT, decision models and RAG. **Changed:** Telegram feeds deterministic **postures** only (regex contract addresses, mention velocity, channel counts). No model sees Telegram text. |
| **Row-level data-provenance tagging + training filters** | 12 §5; 03 §1 | One mechanism enforces every data-terms restriction (Telegram, Birdeye, Etherscan, non-commercial datasets). A future SaaS becomes a retrain, not a redesign. |
| **Australian regulatory boundary + venue access registry** (ASIC 2:1 retail crypto CFD cap, AU derivatives access by venue, AUSTRAC VASP register checks, Travel Rule, Digital Assets Framework, Polymarket ISP block) | 12 §1–3; 03 M12 | MasterTrader listed Bybit/OKX/Bitget/Hyperliquid perps and Polymarket without an AU access check |
| **Per-platform do/don't table** (CoinGecko ≤ 24h cache, DefiLlama API-only, DexScreener no competing screener, Etherscan not a decision input, Birdeye excluded, GoPlus no proxies, Jupiter keys, Jito tip-in-tx) | 12 §4 | These terms bind us even for private use |
| **Explicit self-trade prevention (STP) on every order**, per venue | 12 §3; 03 M12 | Multiple strategies per account plus exchange conduct rules |
| **Custody tiers + signer service** (vault / Hyperliquid master / warm / hot / burner / airdrop identity; intents-only signer; sized approvals; **durable-nonce hard block**) | 13 §1–2; 07 §4 | Concrete wallet architecture beyond "hot claim wallet" |
| **Hyperliquid key model** (master key on a hardware signer via EIP-712; agent keys trade-only, rotated, `valid_until`) | 13 §2 | Hyperliquid is in our venue list |
| **Unified wallet view** (address registry, read-only aggregation, rotki reconciliation) | 13 §3; UI D18 | MasterTrader had no portfolio view of self-custody wallets |
| **Hold-and-earn / treasury module (new M22)**: staking, LSTs, lending allow-list, Pendle PTs, HLP capped, nodes/validators net-earnings model, yield allocator, DAO monitoring, depeg/exploit/bridge policies, sweeps | 13 §4–6; 03 M22; UI D18 | A whole capability that was missing |
| **On-chain cost gate** (Solana/EVM fee formulas, AMM impact, all-in round-trip, `allow / wait / reject`) + DEX execution (Jupiter, Jito, 1inch free, Flashbots Protect) | 13 §7; 03 M12/M16 | MasterTrader's cost model covered CEX venues only |
| **Social participation (new M23)**: drafts in your voice, you approve, X web-intent post (no API cost), holdings disclosure; account credibility scoring; shill-burst posture | 13 §8; 03 M23; UI D13 | Fills the "social engagement" part of the airdrop goal without automation that breaks the rules |
| **Airdrop module upgrades**: corroboration score, EV formula, burner-first, one identity wallet per chain, genuine-use on-chain tasks under mandate, disposal rule, campaign record, project dossier, entity blacklist with funding-graph links, own wallet-cluster detection (MemeTrans), default-reject fresh launches, datasets | 08 (edited) | Systematic vetting/EV that 08 lacked |
| **Strategy evidence & realism**: viability verdict, Sydney-operator edge analysis, ranked strategy catalogue (P1/P2/P3/X/Never), "name the counterparty" rule | 14 §1–3; 03 M0 | Templates now carry evidence and priority; the never-build list is enforced |
| **Trading methods**: regime filters, vol-targeting, correct Kelly (quarter, capped), drawdown de-risking, ATR stops, maker-first execution, TWAP above 1% of 1-min volume | 14 §4; 03 M11 | Concrete sizing/execution defaults |
| **Risk fallback ladder (6 rungs)**, decision deadlines, API-error pause, exchange concentration cap, per-sleeve capital/kill, per-asset netting | 14 §5; 03 M11; UI D06 | Formalises degraded behaviour |
| **Validation harness extensions**: per-year **and** per-regime profitability, 2× / 3× cost stress, auto trial counter, worst-fold judging, LLM-assisted leakage review gate, survivorship-free universes, decay monitoring (rolling 5th percentile + CUSUM), daily health check, written kill criteria, capital steps per phase | 14 §6–7; 03 §8; 04 Phase 7 | Stricter promotion gates |
| **Decision-model operations**: per-question thresholds from measured disagreement, 5% shadow checks, **labels from outcomes or you, never from a shadow model**, monthly fine-tune, Kev-4B as challenger, Laya server auth, AMD 7900 XTX notes | 10 (edited) | Operational rules for tier B |
| **Sentiment & regime engine per market type** + macro layer; Fear & Greed, liquidations/OI; Finnhub (free, personal) + FMP calendar (free tier) as extra sources | 03 M6/M5; 06 | Keeps market types' signals separate |
| **MasterTradingBot integration** (your existing deterministic MT5 system on FP Markets): shared pure-function indicator/sizing libraries with golden tests; keep FP Markets MT5 execution; cTrader Open API as the Linux route; TradFi → crypto porting pitfalls | 14 §8; 03 M12 | Brings an existing asset into the plan |
| **Production checklist items**: UPS + 4G failover (fail flat), second alert channel, Shamir/multisig seed backup, sealed estate letter, venue-health monitor (AUSTRAC status, withdrawal delays), stablecoin depeg auto-reduce | 07 (edited); 13 §6 | Continuity and custody hygiene |

## 3. Conflicts and how they were resolved

| Conflict | MasterTrader said | CryptoTrader says | Resolution |
|---|---|---|---|
| **Telegram data in models** | Telegram text → FinBERT, decision models, RAG | Banned by Telegram API ToS §1.5 | **Adopt the CryptoTrader stance** (stricter, safer): Telegram → postures/regex only |
| **Tenderly** | Free tier, 120K simulations/month | Free plan has **no API** | **Use local simulation:** Anvil fork (EVM) and `simulateTransaction` (Solana). Tenderly is dropped. |
| **Etherscan** | Enrichment source in the airdrop pipeline | Terms bar use "as a basis for financial gain"; free tier dropped Base/OP/BNB | **Blockscout + own RPC** for decisions; Etherscan for manual lookups only |
| **Discord Message Content intent** | Self-serve under 100 servers | Since 11 Jun 2026: self-serve for apps under 10,000 users | Newer fact adopted (either way it's self-serve for us). Also added: **~10–15 follow webhooks per receiving channel**, so follows are spread across channels. |
| **Polymarket** | Optional Nautilus adapter; probability source | ACMA warning + ISP block for Australians (Interactive Gambling Act) | **No trading.** Read-only probability data only where lawfully reachable; never via VPN. Kalshi likewise read-only. |
| **AU derivatives venues** | Bybit/OKX/Hyperliquid perps listed as venues | Offshore perps unlicensed for AU retail; Binance AU none; Kraken AU wholesale-only; OKX AU unresolved; ASIC 2:1 cap | **Venue access registry** (12 §2). Perps/CFDs only via venues that are lawfully available to you; leverage capped at **2×** by default; Hyperliquid only after professional advice. |
| **AU 2027 CGT reform** | Reported law (Act No. 49 of 2026, Royal Assent 26 Jun 2026) | "Budget proposal, not law" (as of 28 Sep 2026) | **Unresolved:** sources disagree. Keep the `AU_2027_REFORM` plugin behind a flag; the tax agent confirms before use. |
| **Base currency** | AUD at event time (RBA rate per event) | USD base; batch RBA conversion at tax time | **Store both:** native + USD + AUD per event (RBA daily rate). The base currency is a user setting (default AUD), and tax always uses AUD via RBA. |
| **Second alert channel** | Telegram + email | Telegram + Twilio SMS (paid, ~US$13/month) | **Free-only:** Telegram + email + self-hosted **ntfy** push. Twilio is an optional paid upgrade. |
| **Infrastructure** | One self-hosted box | k3s + KEDA, AWS Tokyo/Singapore/Sydney node pools, Redis hot tier | **Keep the single box.** Latency-race strategies are on the never-build list for a Sydney operator (14 §2). NATS KV replaces Redis. A remote "execution edge" VM stays a documented future option, gated on a measured, proven edge. |
| **Tax software** | Own engine + Beancount export | Syla (A$249/yr) export | **Own engine stays primary;** Syla/Koinly CSV export is optional (paid tools aren't required) |

## 4. Not adopted (and why)

- **Memecoin sniping, copy-trading, listing/news latency trading, Solana atomic arbitrage, JIT liquidity, millisecond cross-market arbitrage, Polymarket bots:** rated **X** (no edge from Sydney / blocked in AU).
- **Sandwiching:** **Never** (harms users; potential market manipulation).
- These are enforced as non-available strategy templates (14 §3).
- **k3s/KEDA multi-region topology, Redis hot tier, AWS region pools:** out of scope for a single private box (see §3).
- **Paid providers** (Chainstack/QuickNode paid tiers, LunarCrush, Bitquery, CryptoRank Pro, Twilio, Syla, Ledger/Trezor purchase):
  - listed in 13/06 as optional upgrades only, in line with the free-only rule;
  - the hardware signer for Hyperliquid is the exception: it's recommended **only if** Hyperliquid is ever used.
- **Bootstrapping from $0 (bounties/grants):** career advice, not platform scope.
- **Ellipal Titan specifics:** these depend on your hardware. The custody design in 13 is device-agnostic and notes Ellipal's limits (no EIP-712, MetaMask-QR only).
