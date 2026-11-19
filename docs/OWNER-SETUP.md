# MasterTrader — Owner setup sheet

Every remaining thing only you can do, in the order to do it. Each line links to its task file, which has the exact steps.
- Plan: [18 platform & deployment](18-platform-and-deployment.md) (workstation first, test, then shift) and [17 §G](17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19).
- Generated 2026-11-19 from the kanban. `./kanban list --type USER` shows the live state.

## How this works

- **Agents build everything without you.** No build task in Phases 0–6 waits on anything here. Code is built and tested against fixtures, testnets and paper venues; anything that would be a "setting" (risk values, sleeves, watchlist, keywords, budgets, wallet limits, token scopes) is seeded from the documented defaults.
- **What you give in week one feeds three things:**
  - real data for the 8-week paper clock;
  - the late live checks ("build first, keys last");
  - the long-lead outside parties, such as your tax agent.
- **One review of all settings, at go-live:** the go-live pack ([P7-T070](../tracking/phase-7/tasks/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl.md)). Until then you can change anything in settings whenever you like, but you're never asked to.
- **Secrets:** never paste a key into chat, issues or git.
  - Keep each value in your password manager until the agent has created the encrypted secrets file ([P0-T022](../tracking/phase-0/tasks/P0-T022-sops-age-secrets-tmpfs.md), its first day). Then add them all in one `sops` session; the agent prints the exact key names.
  - Tasks list only the names, never values.

**Reddit:** [P0-T001](../tracking/phase-0/tasks/P0-T001-reddit-api-decision.md) is waiting on Reddit's reply to your 29 Oct 2026 request. When it comes, do [P4-T004](../tracking/phase-4/tasks/P4-T004-reddit-decision.md) (5 min). Nothing else waits on it.

---

## 1. Week one: one sitting (about 3–4 hours) plus a few things that take days

Do these in this order; most are sign-ups.

| # | Do | Why | Time | Task |
|---|---|---|---|---|
| 1 | Make the GitHub repo private (it is), turn on 2FA, secret scanning, push protection and Dependabot; protect `main` | Stops a leaked key ever reaching git | 10 min | [P0-T004](../tracking/phase-0/tasks/P0-T004-github-private-secret-scanning.md) |
| 2 | Open the **demo/paper/testnet accounts**: OANDA practice, IG demo, Alpaca paper, IBKR paper (optional; IBKR may need a live application), Binance Spot testnet, Bybit testnet. 2FA on each | Real market streams and paper trading for the 8-week clock | 45 min | [P0-T009](../tracking/phase-0/tasks/P0-T009-demo-practice-accounts.md) |
| 3 | Register the **free data keys**: FRED, EIA, USDA NASS, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Helius, Alchemy, GoPlus, Finnhub, CryptoPanic | Free macro, crypto and news data | 45 min | [P0-T010](../tracking/phase-0/tasks/P0-T010-free-data-api-keys.md) |
| 4 | Free **event-source keys** (NASA FIRMS, ACLED) and read three terms pages (Finnhub ML clause, CryptoPanic attribution, OpenSanctions licence); YouTube key optional | Events layer; provenance flags set correctly | 20 min | [P4-T005](../tracking/phase-4/tasks/P4-T005-event-keys-and-terms.md) |
| 5 | **Tally** API key; request **FinMMEval** data access (or decline) | DAO monitor; model benchmark data | 10 min | [P6-T002](../tracking/phase-6/tasks/P6-T002-external-access-tally-finmmeval-weights.md) |
| 6 | **LLM keys**: Anthropic API key with a monthly spend limit in the console; your custom endpoint URL/key if you have one | The research and agent routes | 10 min | [P0-T007](../tracking/phase-0/tasks/P0-T007-llm-gateway-credentials.md) |
| 7 | **Telegram**: a dedicated identity (prepaid SIM or landline voice code), 2-step password, `api_id`/`api_hash` from my.telegram.org, an alert bot from @BotFather; send `/start` to it from your personal account | Alerts, approvals, the seal witness; Telegram postures | 30 min | [P0-T002](../tracking/phase-0/tasks/P0-T002-telegram-account-and-bot.md) |
| 8 | **Discord**: private "MasterTrader Feeds" server + a bot application (Message Content intent); then follow the announcement channels you care about into it | Discord announcement ingest | 20 min + follows when you like | [P0-T008](../tracking/phase-0/tasks/P0-T008-discord-server-and-bot.md) → [P4-T002](../tracking/phase-4/tasks/P4-T002-discord-follows.md) |
| 9 | **Off-site backup**: Backblaze B2 with Object Lock (three buckets, restricted keys) or a second box running restic append-only | Immutable off-site backups and WORM seals | 20 min | [P0-T006](../tracking/phase-0/tasks/P0-T006-offsite-object-lock-backup-target.md) |
| 10 | Email alerts: an SMTP **app password** from your mail provider, or say "email off" | Third alert channel (optional) | 5 min | [P1-T068](../tracking/phase-1/tasks/P1-T068-smtp-app-password-or-email-off.md) |
| 11 | **Engage a registered tax agent** and send the 12 questions from doc 09; include the 2027 CGT reform questions in the same email | Investor-vs-trader answer is required before any live trade; agents take weeks | 30 min + their turnaround | [P3-T001](../tracking/phase-3/tasks/P3-T001-engage-tax-agent.md), [P3-T002](../tracking/phase-3/tasks/P3-T002-confirm-2027-reform-status.md) |
| 12 | **Export your historical statements** (IBKR Flex, OANDA, IG, exchanges, wallets) into the journal inbox | Opening balances and lots with real cost bases | 30–60 min | [P3-T003](../tracking/phase-3/tasks/P3-T003-export-historical-statements.md) |
| 13 | Calendar: 30 June 2027 snapshot reminders | A hard tax date | 5 min | [P3-T004](../tracking/phase-3/tasks/P3-T004-diary-30-june-2027-snapshot.md) |
| 14 | Export your **MasterTradingBot** rules and historical signals/trades (MT5) into the git-ignored fixtures folder | Golden files so the port matches your bot exactly | 30–60 min | [P2-T002](../tracking/phase-2/tasks/P2-T002-mastertradingbot-golden-inputs.md) |
| 15 | *Optional:* check your AU venues on the AUSTRAC register | Refines the agent's venue seed (paper works without it) | 30 min | [P0-T011](../tracking/phase-0/tasks/P0-T011-venue-austrac-checks.md) |
| 16 | *Long lead, optional until go-live:* order a UPS and a 4G failover router | Needed only for live money on the workstation | 15 min | [P0-T012](../tracking/phase-0/tasks/P0-T012-ups-and-4g-failover.md) |

**Right after the agent's first run** (it posts on Telegram when the secrets file exists):
- Put every value from rows 2–10 into the secrets file in one `sops` session ([P0-T022](../tracking/phase-0/tasks/P0-T022-sops-age-secrets-tmpfs.md) prints the names).
- **Read-only keys** on the practice/testnet accounts, IP-locked to your workstation's IP (10 min, [P1-T002](../tracking/phase-1/tasks/P1-T002-read-only-recon-keys.md)).
- **Trade-only testnet keys** per mode, withdrawals off, IP-locked, plus the dead-man key (20 min, [P2-T001](../tracking/phase-2/tasks/P2-T001-testnet-trade-only-keys.md)).
- Open the app on the workstation, **set your password and enrol TOTP**, ideally with a second device as backup (2 min, [P0-T062](../tracking/phase-0/tasks/P0-T062-set-password-enrol-totp.md)).

After this, the agents don't need you to keep building.

---

## 2. When the agent pings you (a few minutes each, on your schedule)

These depend on things the agents build first. They notify you on Telegram, and nothing in the build waits on them.

| Do | When | Task |
|---|---|---|
| Register your real accounts and tag each `investment` or `trading` | When the journal's account page exists (P3) | [P3-T042](../tracking/phase-3/tasks/P3-T042-register-accounts-and-tags.md) |
| Enter your residency timeline | Same time | [P3-T043](../tracking/phase-3/tasks/P3-T043-enter-residency-timeline.md) |
| List the Telegram channels you want watched (postures only, ≤ 500) and log in the Telethon session once | When the login script exists (P4) | [P4-T001](../tracking/phase-4/tasks/P4-T001-telegram-channel-list.md) |
| Set up the **vault** (cold) and **warm** hardware wallets yourself, offline; public addresses only | Before P5 live checks; only if you'll use on-chain features | [P5-T001](../tracking/phase-5/tasks/P5-T001-vault-warm-hardware-wallets.md) |
| Back up the vault seed with Shamir shares and write the sealed estate letter | After the wallets | [P5-T002](../tracking/phase-5/tasks/P5-T002-shamir-seed-backup-estate-letter.md) |
| Add fallback RPC provider accounts and restrict the keys | P5 | [P5-T003](../tracking/phase-5/tasks/P5-T003-rpc-provider-accounts.md) |
| Register every address you own with proof of control | P5, after the wallets | [P5-T005](../tracking/phase-5/tasks/P5-T005-register-all-addresses.md) |

**Optional, whenever you feel like it** (agents use silver labels and defaults otherwise):
- [P4-T049](../tracking/phase-4/tasks/P4-T049-label-200-docs.md): label ~200 documents to tune the relevance gate.
- [P6-T044](../tracking/phase-6/tasks/P6-T044-work-labelling-queue.md): work the D10 labelling queue.
- [P5-T008](../tracking/phase-5/tasks/P5-T008-work-task-queue.md): do airdrop social tasks yourself.
- [P6-T049](../tracking/phase-6/tasks/P6-T049-approve-social-drafts.md): social drafts (off by default).
- [P5-T066](../tracking/phase-5/tasks/P5-T066-sell-claimed-airdrop-tokens-yourself-when-the-di.md): sell claimed airdrop tokens yourself.

---

## 3. Before go-live (Phase 7): the only stage that needs you in person

The agents prepare each item (instructions, comparisons, the preflight) before it reaches you. In order:

1. **Choose where live runs** ([P7-T071](../tracking/phase-7/tasks/P7-T071-choose-the-go-live-runtime-host-and-cloud-option.md)): stay on the workstation (default, free), a home server, or a Sydney static-IP VM; optionally Vercel for the web app and Supabase cloud (paid). The agent writes a cost and latency comparison first.
2. **Hardware key** ([P7-T072](../tracking/phase-7/tasks/P7-T072-move-the-age-identities-onto-a-yubikey-before-li.md)): buy a YubiKey (and a spare); move the secret-file keys onto it (about 20 min with the agent's commands).
3. **Tailscale** ([P0-T003](../tracking/phase-0/tasks/P0-T003-tailscale-mfa-and-age-hardware-key.md)) and **ntfy on your phone** ([P1-T003](../tracking/phase-1/tasks/P1-T003-ntfy-app-and-email.md)): phone access and the second alert channel.
4. **UPS and 4G installed** ([P7-T009](../tracking/phase-7/tasks/P7-T009-ups-and-4g-failover.md)) if live runs on the workstation; **Sydney exit-node VM** with a static IP ([P7-T065](../tracking/phase-7/tasks/P7-T065-provision-the-sydney-egress-exit-node-vm-with-a-.md)) unless the runtime host is itself a static-IP VM.
5. **WORM owner ceremony** ([P0-T013](../tracking/phase-0/tasks/P0-T013-worm-owner-offline-credential.md)): generate the offline `worm_owner` credential (15 min).
6. **Drills** (30–60 min each; they prove the safety paths with paper positions):
   - first-bot walkthrough + one HITL approval ([P2-T066](../tracking/phase-2/tasks/P2-T066-user-first-bots-hitl.md));
   - kill switch from your phone ([P2-T064](../tracking/phase-2/tasks/P2-T064-user-kill-drill-phone.md));
   - a C3 loosening with TOTP ([P2-T065](../tracking/phase-2/tasks/P2-T065-user-approve-c3-loosening.md));
   - pull the plug ([P7-T053](../tracking/phase-7/tasks/P7-T053-pull-the-plug-drill.md)).
7. **Tax and legal:**
   - record the tax agent's investor-vs-trader answer ([P7-T001](../tracking/phase-7/tasks/P7-T001-tax-agent-regime-decision.md));
   - close or defer the lawyer items ([P7-T002](../tracking/phase-7/tasks/P7-T002-lawyer-advice-items.md)).
8. **Venues:** AUSTRAC re-check and terms for the venues you'll trade live ([P7-T003](../tracking/phase-7/tasks/P7-T003-venue-checks-before-live.md)). If MasterTradingBot goes live: read FP Markets' algo clauses and pick MT5 or cTrader ([P7-T004](../tracking/phase-7/tasks/P7-T004-fp-markets-terms-and-route.md)), then the Windows VPS ([P7-T005](../tracking/phase-7/tasks/P7-T005-windows-vps-for-mt5.md)).
9. **Live accounts and keys** (the "bearer tokens"):
   - KYC'd live accounts with one sub-account per mandate ([P7-T006](../tracking/phase-7/tasks/P7-T006-live-accounts-and-sub-accounts.md));
   - **trade-only, no-withdrawal, IP-locked live keys** ([P7-T007](../tracking/phase-7/tasks/P7-T007-live-trade-only-keys.md));
   - withdrawal addresses pre-registered with proof of control ([P7-T008](../tracking/phase-7/tasks/P7-T008-travel-rule-addresses.md)).
10. **On-chain money (only if you want it):**
    - confirm the signer limits and fund the minimal floats ([P5-T004](../tracking/phase-5/tasks/P5-T004-approve-hot-identity-burner-keys.md));
    - sign the first claim mandates ([P5-T006](../tracking/phase-5/tasks/P5-T006-sign-first-mandates.md));
    - approve the treasury policy ([P6-T034](../tracking/phase-6/tasks/P6-T034-approve-treasury-policy.md)).
11. **Approve the go-live pack** ([P7-T070](../tracking/phase-7/tasks/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl.md)): one page with every seeded value (risk limits and ceilings, sleeves, strategy manifests, watchlist, budgets). Change anything you want, then approve once (C3).
12. **Fund the first bot** ([P7-T057](../tracking/phase-7/tasks/P7-T057-fund-micro-live.md)): default A$2,000, one sleeve, HITL mode, only after the preflight, gate report and stress replay are green.

## 4. After go-live (recurring)

| Do | How often | Task |
|---|---|---|
| Sign off the weekly review pack | Weekly, 30–45 min | [P7-T060](../tracking/phase-7/tasks/P7-T060-weekly-review-signoffs.md) |
| Approve bot promotions HITL → autonomous | When a bot's checklist is green | [P7-T058](../tracking/phase-7/tasks/P7-T058-approve-bot-promotions.md) |
| Approve capital steps (+25%) | After 4 clean weeks | [P7-T061](../tracking/phase-7/tasks/P7-T061-approve-capital-steps.md) |
| Pre-commit the 12-month keep criteria and diary the review | Once, then yearly | [P7-T063](../tracking/phase-7/tasks/P7-T063-precommit-12-month-review.md) |
| AUSTRAC register re-check | Quarterly reminder | [P1-T069](../tracking/phase-1/tasks/P1-T069-quarterly-austrac-register-check.md) |
| Decide whether to build MCP (Phase 8, optional), then connect your Claude client | After 4 weeks of daily use | [P8-T001](../tracking/phase-8/tasks/P8-T001-decision-gate.md), [P8-T018](../tracking/phase-8/tasks/P8-T018-configure-mcp-client.md) |

## Totals

- **Week one:** about 3–4 hours of sign-ups, plus the tax agent's and Telegram's lead times.
- **During the build:** a handful of 5–15 minute items when pinged; nothing blocks the agents.
- **Go-live:** about a day of your time spread over Phase 7, mostly drills, accounts and keys.
