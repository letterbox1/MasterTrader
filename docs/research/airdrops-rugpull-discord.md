_Raw notes from the research agents (2026-10-21). They back up [../08-airdrops-and-token-launches.md](../08-airdrops-and-token-launches.md). WebFetch was blocked, so web facts come from search snippets; (U) = unverified._

# Airdrop / token-launch module: repo vetting, free sources, Discord facts

## Repos
| Repo | Reality | Licence | Verdict |
|---|---|---|---|
| degenfrends/solana-rugchecker | TypeScript lib (npm v0.0.16) that scores SPL tokens on Raydium AMM v4 only; "under development". Last commit 2024-06-14. | No LICENSE file; package.json says MIT (ambiguous) | **Ideas only.** Reimplement the feature list in Python; use RugCheck.xyz + GoPlus as the data feeds |
| jattin1/rug-pull-detector-extension | Non-functional MV3 extension stub (hard-coded example data, broken fetch). Not malicious. | None | **Reject** |
| N8python/rugpull | **Not crypto**: a local RAG/UMAP document visualiser ("Retrieval yoU Generate…"). Has path-traversal routes. | CC0 | **Reject** (name false-positive) |
| CRPWarner/RugPull | Academic Datalog rules on the Gigahorse EVM decompiler: hidden mint, limiting sell order, leaking token. Paper: IEEE TSE 2024, arXiv:2403.01425 (P 91.8% / R 85.9%). Blind to proxies. | Top level has none; vendored gigahorse is BSD-3 | **Concepts + optional sandboxed offline worker** (build from upstream Gigahorse; no `$HOME` mount; no vendored .deb) |
| dianxiang-sun/rug_pull_dataset | 2,391 labelled ETH/BSC rug-pull contracts (2020–23), 14 types. Matches the SoK paper arXiv:2403.16082 / ISSTA 2025. Attribution (U). | None | **Private evaluation labels only**; cite the paper; don't redistribute |

### solana-rugchecker signals (worth reimplementing)
- **Scored signals:**
  - mint authority (+80);
  - freeze authority (+65);
  - mutable metadata (+50);
  - top-20 holder share ≥50/35/20% (+80/60/50), excluding the Raydium authority;
  - LP < 95% burned (+80);
  - individual large holders.
- **Gaps:**
  - no Token-2022 extensions;
  - no LP lockers;
  - no insider clustering;
  - no creator history;
  - no sell simulation.

## Free / free-tier token-risk sources
| Service | Free tier | Use |
|---|---|---|
| **GoPlus Security** | 150K CU/month, 30K/day, 150/min | **Primary EVM risk feed**: honeypot, mintable, balance-changeable, taxes, blacklist, proxy, LP locks, phishing sites, approval security; Solana beta |
| **Honeypot.is** | Free (U on limits) | EVM buy/sell simulation, second opinion |
| **RugCheck.xyz** | Read endpoints free (U) | **Primary Solana risk feed** (score, flags, LP lock, insiders) |
| TokenSniffer | Paid ($99/mo) | Skip |
| De.Fi | Free UI only | Manual link |
| **DexScreener** | Free, no key; ~300/min pairs, 60/min profiles (U) | Market enrichment + new pairs |
| GeckoTerminal | Free (U) | Top pools |
| Birdeye | $0 plan: 30K CU, 1 rps | Marginal |
| **Helius** | 1M credits/month, 10 RPC rps | **Solana RPC** |
| Solscan | Free tier quota unpublished | Optional |
| QuickIntel / Forta / Bubblemaps API | Paid or unclear | Manual links (Bubblemaps) |
| **Etherscan V2** | 3–5 calls/s, 100K/day, shared per chain | Verified source, proxy, creator |
| Slither | AGPL-3.0 OSS | Optional CLI on verified source |

## Discovery sources
- **DefiLlama `/protocols`:** gives "tokenless protocols with rising TVL", a legitimate airdrop-candidate signal. The airdrops page sits behind Cloudflare, so don't scrape it.
- **CoinGecko Demo** (~30/min, 10K/month): new listings, categories, and `links` (`chat_url`, `twitter`, `announcement_url`). This is the legitimate source of Discord/Telegram links.
- **CryptoRank Sandbox** (10/min, 10K credits/month): ICO/IDO calendars, launchpads, funding rounds.
- **Galxe GraphQL:** read-only campaign and eligibility checks. **Never automate task completion.** Zealy/Layer3: manual links.
- **Snapshot GraphQL, governance forums** (Discourse `/latest.json`), project docs.
- airdrops.io / earndrop / DropsTab: manual or low-volume only. No maintained OSS tracker exists, and many "checker" repos are phishing.

## Safety sources
- **Blocklists:**
  - MetaMask eth-phishing-detect (DBAD licence, U; repo says it has moved, U).
  - ScamSniffer scam-database (GPL-3.0, U; possibly delayed vs the paid API).
  - polkadot-js/phishing.
  - Chainabuse API (5,000 calls/hour).
- **Simulation:** Tenderly free tier (120K simulations/month) for EVM; Solana `simulateTransaction`.
- **Approvals:** revoke.cash (core free); or DIY by indexing Approval logs + GoPlus approval security.
- **Threat context:** 2025 drainer losses ≈ $84M; forged Permit signatures and fake eligibility checkers dominate.

## Discord facts
1. **Bots can't join servers on their own.** They need an OAuth `bot` install by a user with Manage Server (U on exact wording).
2. **Follow Announcement Channel** (`POST /channels/{id}/followers`) needs MANAGE_WEBHOOKS on the **target** channel, and the bot must see the source channel. A bot that isn't in the project server can't follow it.
3. **Self-bots / user-account automation are prohibited**, as is scraping member data.
4. **Message Content intent:** a toggle under 100 servers; verification required at 100+.

So the user clicks "Follow" in the project's announcement channel and targets a channel in their own server, where the bot ingests everything.

## Tax flag (Australia)
- General airdrops are ordinary income at market value on receipt, which becomes the cost base.
- Initial-allocation airdrops are not income on receipt (cost base is usually $0); CGT applies on disposal.

Source: secondary, (U).

Sources:
- https://arxiv.org/abs/2403.01425
- https://arxiv.org/abs/2403.16082
- https://gopluslabs.io/zh/security-api
- https://tokensniffer.readme.io/reference/pricing
- https://docs.birdeye.so/docs/pricing
- https://www.helius.dev/docs/billing/plans
- https://docs.etherscan.io/etherscan-v2/rate-limits
- https://cryptorank.io/public-api/pricing
- https://docs.galxe.com/quest/graphql-api/overview
- https://tenderly.co/pricing
- https://docs.trmlabs.com/guides/chainabuse/welcome-to-chainabuse-api
- https://github.com/MetaMask/eth-phishing-detect
- https://github.com/polkadot-js/phishing
- https://support.discord.com/hc/articles/115002192352
- https://discord.com/blog/the-future-of-bots-on-discord
- https://cryptotaxcalculator.io/au/blog/new-guidance-airdrop-tax-australia
