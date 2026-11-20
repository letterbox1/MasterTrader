# MasterTrader — `.env` setup guide

Step-by-step instructions for every block of [`.env.example`](../.env.example), in the same order and with the same headings. Work through it service by service, and the whole system has every key it needs, from Phase 0 to the end.
- Order of the human steps overall: [OWNER-SETUP.md](OWNER-SETUP.md).
- Where secrets live and why: [07 §2](07-security-notes.md#2-secrets).

## The flow

```bash
cp .env.example .env          # .env is git-ignored; .env.example stays in git
# ... fill .env using this guide ...
just secrets-generate         # fills the MT_* values; copy the four ★ ones to your password manager
just secrets-seal             # encrypts .env → ~/.config/mastertrader/secrets.sops.env, shreds .env
just secrets-check            # set/missing per name; never prints a value
```

- **Adding keys later:** `just secrets-edit`, or a fresh `.env` with only the new lines plus `just secrets-seal --merge`.
- **Leave anything blank you don't use:** the matching feature stays off and its live check is skipped.
- **Before the agent's first run:** `just` and the sealing commands don't exist yet (P0-T022 builds them on day one). Fill `.env` anyway and keep it on the workstation only; the first `just secrets-seal` takes it from there.
- **Agents never see values:** they only see names (`just secrets-check`, `./kanban preflight`).
- Never paste a value into chat, an issue, a commit or a screenshot.

**General rules for every account you open:**
- Turn on 2FA with an authenticator app.
- Use a password-manager-generated password.
- Where a provider offers it, give each key the **narrowest scope** and lock it to your **IP**. Before go-live that's the workstation's public IP (`curl -s https://ifconfig.me`); for live keys it's `EGRESS_STATIC_IP`.

**Naming:** `<SERVICE>_<ENVIRONMENT>_<ROLE>_<FIELD>`, explained at the top of `.env.example`. Facts marked (U) are unverified: provider screens change. If a step doesn't match what you see, follow the provider's current page; the variable names stay the same.

---

## 1. You and your login

| Variable | How |
|---|---|
| `OWNER_EMAIL` | The email you'll sign in with. On first start the agent runs `mtctl auth create-owner`, which emails or prints a set-password link to this address (local Supabase shows it in Inbucket at `http://127.0.0.1:54324`). Then enrol TOTP (P0-T062). |

## 2. LLM providers

| Variable | How |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com → **Settings → API keys → Create key**. Then **Settings → Limits** and set a monthly spend limit (default budget US$40/month, [16 §2.10](16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)). |
| `CUSTOM_LLM_BASE_URL`, `CUSTOM_LLM_API_KEY`, `CUSTOM_LLM_MODEL` | Only if you run or rent an OpenAI-compatible endpoint. Paste its base URL (ending in `/v1`), its key and the model name. Blank = the `research-custom` route is off. |
| `HUGGINGFACE_TOKEN` | Only if a model you pick is gated. huggingface.co → **Settings → Access Tokens → New token**, type **Read**. The default models (bge, Qwen) don't need it (U). |

## 3. Telegram

You need a **dedicated Telegram identity** (prepaid SIM or a landline that can take a voice code), not your personal account (P0-T002).

| Variable | How |
|---|---|
| `TELEGRAM_BOT_TOKEN` | In your **personal** Telegram, open **@BotFather** → `/newbot` → name it (e.g. *MasterTrader Alerts*) → copy the token. Then `/setjoingroups` → Disable, and `/setprivacy` → Enable. |
| `TELEGRAM_OWNER_CHAT_ID` | Open your new bot and send `/start`. On the workstation run `curl -s "https://api.telegram.org/bot<token>/getUpdates"` and copy `message.chat.id`. Only this chat can approve or `/kill`. |
| `TELEGRAM_ALERTS_CHAT_ID` | Same value as the owner chat, or create a private group, add the bot, send a message and read the group's id (negative number) the same way. |
| `TELEGRAM_READER_API_ID`, `TELEGRAM_READER_API_HASH` | Log in at **my.telegram.org** with the **dedicated** account → **API development tools** → create an app (any title, platform *Desktop*). Copy `api_id` and `api_hash`. The Telethon session is created later, once, by a login script (P4-T006). |

## 4. Email alerts (optional)

Leave the whole block blank to keep email off; Telegram and ntfy carry every alert.

| Variable | How |
|---|---|
| `SMTP_HOST`, `SMTP_PORT` | Your provider's SMTP server, e.g. Gmail `smtp.gmail.com` / `587`, Fastmail `smtp.fastmail.com` / `465`, Outlook `smtp-mail.outlook.com` / `587`. |
| `SMTP_USERNAME` | Usually your full email address. |
| `SMTP_APP_PASSWORD` | An **app password**, never your main password. Gmail: myaccount.google.com/apppasswords (needs 2FA on). Fastmail: **Settings → Privacy & Security → App passwords**. |
| `ALERT_EMAIL_FROM`, `ALERT_EMAIL_TO` | Sender (usually the same as the username) and where alerts go. After the first test, check spam once and allow the sender. |

## 5. Discord feeds server

| Variable | How |
|---|---|
| `DISCORD_APPLICATION_ID`, `DISCORD_BOT_TOKEN` | discord.com/developers/applications → **New Application** (copy the Application ID) → **Bot → Reset Token** (copy it) → turn on **Message Content Intent**. **OAuth2 → URL Generator:** scope `bot`, permissions *View Channels* + *Read Message History* only; open the URL and add the bot to your server. |
| `DISCORD_FEEDS_SERVER_ID`, `DISCORD_INBOX_CHANNEL_ID` | Create a private server *MasterTrader Feeds* with a `#mt-inbox` channel. Turn on **User Settings → Advanced → Developer Mode**, then right-click the server → **Copy Server ID**, and the channel → **Copy Channel ID**. |

Following announcement channels into it is P4-T002; no variables for that.

## 6. Off-site backups

Backblaze B2 with Object Lock is the default. The free alternative is a second box running `restic rest-server --append-only`: fill only `RESTIC_REST_SERVER_URL`.

1. backblaze.com → sign up for **B2 Cloud Storage** → turn on MFA.
2. **Buckets → Create a Bucket** three times, all **Private** with **Object Lock enabled**: e.g. `mt-pgbackrest`, `mt-restic`, `mt-worm-seal`. Default retention from P0-T006 (compliance mode).
3. Copy the **Endpoint** shown on any bucket into `B2_S3_ENDPOINT` (prefix `https://`).
4. **Application Keys → Add a New Application Key** three times, each restricted to **one** bucket, *Read and Write*. Copy each **keyID** and **applicationKey** (shown once) into the matching `B2_<BUCKET>_KEY_ID` / `B2_<BUCKET>_APPLICATION_KEY`, and the bucket names into `B2_<BUCKET>_BUCKET`.

## 7. Practice, demo and testnet venues

No real money anywhere in this block.
- **Modes:** each venue gets one account (or sub-account) per mode where the venue allows it: `PAPER`, `HITL`, `AUTO`.
- **Read-only:** a `READONLY` key for reconciliation.
- **Dead-man:** a separate `DEADMAN` key used only to cancel and flatten.
- **Trade keys:** trade + read only, **withdrawals off**, IP-locked to the workstation.

| Variables | How |
|---|---|
| `OANDA_PRACTICE_API_TOKEN`, `OANDA_PRACTICE_{PAPER,HITL,AUTO}_ACCOUNT_ID` | oanda.com → open a **practice (demo)** account → fxTrade Practice → **Manage API Access → Generate** (one token per login). Create extra practice sub-accounts in the hub (U) and copy each account id (`101-011-xxxxxxx-00N`). |
| `IG_DEMO_API_KEY`, `IG_DEMO_USERNAME`, `IG_DEMO_PASSWORD`, `IG_DEMO_{PAPER,HITL,AUTO}_ACCOUNT_ID` | ig.com/au → **Demo account**. In the web platform: **Settings → API keys → Create API key** (demo). Username/password are your demo login; account ids are listed under **My IG → Accounts** (the demo has a CFD and a spread-bet account by default; use extra ones for modes if offered (U)). |
| `ALPACA_PAPER_API_KEY`, `ALPACA_PAPER_API_SECRET` | app.alpaca.markets → switch to **Paper Trading** → **API Keys → Generate New Key**. The secret is shown once. |
| `IBKR_PAPER_USERNAME`, `IBKR_PAPER_PASSWORD`, `IBKR_PAPER_ACCOUNT_ID` | Optional. IBKR paper accounts hang off a real IBKR account (U: may need a funded live application). **Client Portal → Settings → Account Settings → Paper Trading Account → configure**; it gives a separate paper username; set its password. The account id starts with `DU`. |
| `BINANCE_TESTNET_*` (10) | testnet.binance.vision → log in with GitHub → **Generate HMAC_SHA256 Key** five times, labelled `readonly`, `paper`, `hitl`, `auto`, `deadman`. The Spot testnet has no permission or IP settings (U); the real permission audit happens on live keys. |
| `BYBIT_TESTNET_*` (10) | testnet.bybit.com → register (separate from mainnet) → **API → Create New Key → System-generated**. `READONLY`: *Read-Only*. The others: *Read-Write* with **Orders + Positions** only, no Transfer or Withdraw. **IP restriction:** the workstation's IP. Create sub-accounts per mode under **Sub-Account** if offered (U). |
| `FPMARKETS_DEMO_MT5_*`, `FPMARKETS_DEMO_CTRADER_ACCOUNT_ID` | Only if MasterTradingBot will go live. FP Markets client area → open an **MT5 demo** (login, password and server name shown there) and/or a **cTrader demo** (its account id is in cTrader). |

## 8. Market and macro data

| Variable | How |
|---|---|
| `FRED_API_KEY` | fredaccount.stlouisfed.org → sign up → **API Keys → Request API Key** (describe it as personal research). |
| `EIA_API_KEY` | eia.gov/opendata → **Register**; the key arrives by email. |
| `USDA_NASS_API_KEY` | quickstats.nass.usda.gov/api → **Request API Key**; it arrives by email. |
| `MYFXBOOK_EMAIL`, `MYFXBOOK_PASSWORD` | myfxbook.com account; the API logs in with these (no separate key). Use a unique password. |
| `COINGECKO_DEMO_API_KEY` | coingecko.com → **Developers Dashboard → Demo plan → + Add New Key**. Attribution required (shown in the UI). |
| `CRYPTORANK_API_KEY` | cryptorank.io → **Public API** → sandbox/free key (U: plan names change). |
| `FINNHUB_API_KEY` | finnhub.io/register → the key is on the dashboard. Read its ML clause (P4-T005). |
| `FMP_API_KEY` | Optional. site.financialmodelingprep.com → sign up → dashboard key (250 calls/day free (U)). |
| `TWELVEDATA_API_KEY` | Optional backup bars. twelvedata.com → sign up → **API Keys**. |
| `SEC_EDGAR_USER_AGENT` | No account. Type `MasterTrader you@example.com` with your real contact email; the SEC requires it on every request. |
| `THE_GRAPH_API_KEY` | thegraph.com/studio → connect a wallet or email → **API Keys → Create** (free monthly query allowance). |
| `JUPITER_API_KEY` | Optional (P6 DEX quotes). portal.jup.ag → create a key (U: free tier terms). |

## 9. News, events and social sources

Bluesky, Mastodon, GDELT, USGS, GDACS, NOAA, ReliefWeb, UCDP, Polymarket, Kalshi and RSS need **no key**.

| Variable | How |
|---|---|
| `CRYPTOPANIC_API_KEY` | cryptopanic.com/developers/api → sign up → copy the auth token. Attribution required. |
| `NASA_FIRMS_MAP_KEY` | firms.modaps.eosdis.nasa.gov/api/map_key → enter your email; the MAP_KEY arrives by email. |
| `ACLED_EMAIL`, `ACLED_API_KEY` | acleddata.com → register a research account → **Access Key** (U: ACLED has been moving to OAuth with your username/password; if so, put your password in `ACLED_API_KEY`). Personal, non-commercial use; never used for AI training (P4-T005). |
| `YOUTUBE_DATA_API_KEY` | Optional. console.cloud.google.com → new project → **APIs & Services → Library → YouTube Data API v3 → Enable** → **Credentials → Create credentials → API key** → **Restrict key** to the YouTube Data API v3. |
| `OPENSANCTIONS_API_KEY` | Optional. opensanctions.org/api → request a non-commercial key. Bulk data needs no key. |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` | **Only if Reddit approves** your 2026-10-29 request (P4-T004). reddit.com/prefs/apps on the dedicated account → the **script** app → client id (under the app name) and secret. |

## 10. On-chain reads and token risk

Read-only keys only. **Wallet seeds and private keys never go in `.env`.**

| Variable | How |
|---|---|
| `HELIUS_API_KEY` | dashboard.helius.dev → sign up → copy the API key (Free plan). |
| `ALCHEMY_API_KEY` | dashboard.alchemy.com → **Create new app** (Ethereum + the L2s you use) → **API key**. Under the app's **Security**, add the workstation IP to the allowlist. |
| `CHAINSTACK_SOLANA_RPC_URL` or `QUICKNODE_SOLANA_RPC_URL` | One Solana fallback is enough. Chainstack: console.chainstack.com → **Add node → Solana mainnet** → copy the HTTPS endpoint. QuickNode: dashboard → **Create endpoint → Solana mainnet** → copy the HTTPS URL. The key is inside the URL, so treat the URL as a secret. |
| `INFURA_API_KEY` | Optional EVM fallback. app.infura.io → **Create API key** → allowlist your IP under **Settings**. |
| `GOPLUS_APP_KEY`, `GOPLUS_APP_SECRET` | gopluslabs.io → developer console → create an app (U: the free tier may work without a key; blank = keyless mode with lower limits). |
| `TALLY_API_KEY` | tally.xyz → sign in → **Settings → API → Create key**. |

## 11. Statements for the journal

| Variable | How |
|---|---|
| `IBKR_FLEX_TOKEN`, `IBKR_FLEX_QUERY_ID` | IBKR Client Portal → **Performance & Reports → Flex Queries**. Create an **Activity Flex Query** (trades, cash transactions, positions, all accounts) → note its **Query ID**. Then **Flex Web Service Configuration → Generate token** (read-only statements). |

Other venues' statements are files you export into the journal inbox (P3-T003); no variables.

## 12. Go-live shift (Phase 7, optional parts)

| Variable | How |
|---|---|
| `TAILSCALE_AUTH_KEY` | login.tailscale.com/admin/settings/keys → **Generate auth key**: not reusable, **pre-approved**, tag `tag:mt-host`, 90-day expiry. Used once to join the runtime host or exit-node VM. |
| `EGRESS_STATIC_IP` | The static public IP of the exit-node VM (P7-T065) or of a static-IP runtime VM. Every live key is locked to this IP. |
| `SUPABASE_ACCESS_TOKEN`, `SUPABASE_CLOUD_PROJECT_REF`, `SUPABASE_CLOUD_DB_PASSWORD` | Only if you chose Supabase cloud (P7-T071). supabase.com/dashboard/account/tokens → **Generate new token**. **New project** in Sydney (`ap-southeast-2`): set and save its database password; the project ref is in the dashboard URL. |
| `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` | Only if the web app goes on Vercel. vercel.com/account/tokens → **Create token** (scope: your account). The agent runs `vercel link`, which writes the org and project ids; copy them here. |
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_MT_API_URL` | Public build values. **Local:** the agent fills them from `supabase status`. **Cloud:** **Project Settings → API keys → publishable key** (never the secret/service-role key). `VITE_MT_API_URL` is the tailnet URL of `mt-api` (e.g. `https://mt.<tailnet>.ts.net`). |
| `FPMARKETS_MT5_VPS_ADMIN_PASSWORD` | Only for the MT5 route. Set when you create the Windows VPS (P7-T005). |

## 13. Live venues (Phase 7, real money)

Fill **only** the venues the venue checks (P7-T003) allow and you'll trade. For every key:
- **trade + read only**;
- **withdrawals and transfers OFF**;
- **IP allow-list = `EGRESS_STATIC_IP` only**;
- one sub-account per mode (`HITL`, `AUTO`), plus a `DEADMAN` key per sub-account and a `READONLY` key for reconciliation.

P7-T047 audits every one of these before funding.

| Venue | Where to create keys |
|---|---|
| Independent Reserve | **Settings → API Keys → Generate**, access level *Full Trading* without withdrawal; use the whitelist-only withdrawal role; IP whitelist (U). |
| BTC Markets | **Account → API Key → Create**: permissions *Trade* + *Read*; add the IP whitelist. |
| Kraken AU | **Settings → API → Create key**: *Query Funds*, *Query Open/Closed Orders & Trades*, *Create & Modify Orders*, *Cancel/Close Orders*; no Withdraw or Deposit; IP allow-list. `READONLY` = Query permissions only. |
| Binance AU | **Profile → API Management → Create API → System generated**: enable *Spot & Margin Trading* only; **Restrict access to trusted IPs only**. |
| OKX AU | **Profile → API → Create V5 API key**: set a passphrase (into `_API_PASSPHRASE`), permission *Trade* (*Read* for `READONLY`), IP whitelist (required for trade keys). |
| OANDA live | fxTrade → **Manage API Access → Generate**; create sub-accounts per mode and copy their ids. |
| IG live | **Settings → API keys** (live); live login and account ids per mode. |
| IBKR live | Live username and password for IB Gateway via IBC. IBKR's 2FA (IBKR Mobile) needs a periodic tap (U: weekly re-auth). Account ids per mode. |
| Alpaca live | Live dashboard → **API Keys → Generate**, one key per account. |
| FP Markets | MT5: login, password and server from the client area. cTrader: openapi.ctrader.com → **Applications → Add new app** → client id and secret; then `just ctrader-auth` once (browser sign-in) to fill `MT_FPMARKETS_CTRADER_REFRESH_TOKEN`. |

Hyperliquid has no variables: it stays read-only until professional advice (P7-T002), and any API wallet it ever uses lives in the signer, not here.

## 14. Generated values

Leave them blank and run `just secrets-generate`. Copy these four into your password manager straight away; without them backups and encrypted journal columns can't be restored:
- `MT_JOURNAL_ENCRYPTION_KEY`
- `MT_RESTIC_PASSWORD`
- `MT_PGBACKREST_CIPHER_PASSWORD`
- `MT_MCP_TOKEN_PEPPER` (Phase 8)

Per-service database role passwords and NATS credentials are generated into the sealed file automatically and never appear in `.env`.
