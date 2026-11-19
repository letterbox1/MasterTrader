# Re-platform Brief (wave 3, 2026-11-19): Rust + Python, Supabase, Vercel, workstation-first

The stack changed. [`docs/18-platform-and-deployment.md`](../../docs/18-platform-and-deployment.md) is canonical; the decisions are [`docs/17 §G`](../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) and the defaults [`docs/16 §2.15`](../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions). Read all three first.

**Behaviour doesn't change.** Modules M0–M23, risk (M11), WORM, `pit(as_of)`, HITL, C0–C3, the dead-man, the data and Telegram rules and every number in 16 stay as they are. Only the language, the paths, the database technology, the deployment and who blocks whom change.

## 1. Mapping rules (docs and tasks)

| Old | New |
|---|---|
| FastAPI / uvicorn `mt_api` | Rust `mt-api` (axum, utoipa OpenAPI) in `crates/mt-api/` |
| `packages/mt_<x>/` for a module in 18 §2.1 | `crates/mt-<x>/` (Rust). Use the crate names in 18 §2.1 |
| `packages/mt_<x>/` for a module in 18 §2.2 | Unchanged (Python), `uv` |
| `mt_store.pit` | `mt-store` crate with Python bindings (`mt_store` PyO3 module); one implementation |
| Postgres 16 + TimescaleDB, hypertables, continuous aggregates, `time_bucket`, compression | Supabase Postgres; monthly native partitions (pg_partman or the `mt-store` partition job); the recorder writes standard bar sizes; rollup job for corrections; `date_bin` at read time; old bars to Parquet (18 §4.3) |
| Alembic migrations, `migrations/` | `supabase/migrations/*.sql`; `supabase db reset` / `migration up` locally, `supabase db push` to cloud; pgTAP tests (`supabase test db`) |
| Hand-built login + TOTP | Supabase Auth (password + TOTP MFA, sign-ups off); `mt-api` verifies the JWT and requires `aal2` for commands (18 §4.6) |
| python-telegram-bot | Rust `mt-telegram-bot` (teloxide). Telethon (reading channels) stays Python |
| `mt_mcp` | Rust `mt-mcp` (rmcp) |
| `mt_engine` | `mt-engine`: NautilusTrader Rust live node where the venue adapter is production-ready (U, per venue), else the Python node; `mt-risk` linked in either way |
| Host (one Linux box), LUKS, Tailscale, YubiKey as preconditions | Workstation first (18 §9): nothing before Phase 7 needs a dedicated host, LUKS, Tailscale or a YubiKey. Live hardening is P7-T073; the YubiKey is P7-T072; Tailscale (P0-T003) is optional until go-live |
| GPU decision as a gate | `models.gpu_profile: auto`; CPU profiles are the default; GPU-only checks run when a GPU is present |
| Web app served by Caddy only | Same SPA, served locally by Caddy or deployed to Vercel (`web.host`, 16 §2.15) |

**Task front matter:**
- `tools`: use `cargo` for Rust work, `uv` only for Python work, `supabase` for migrations or DB tests, `pnpm` for the web, `docker` for compose, and `vercel` only in shift tasks.
- `services`: use `supabase-postgres` instead of `postgres`, `supabase-auth` where login is involved, and `supabase-storage` where files are stored.

**Commands in ToDo/Verification:**
- Rust: `cargo test -p <crate>` and `cargo clippy`.
- Python: `uv run pytest`.
- SQL invariants: `supabase test db`.
- Web: `pnpm test` and `pnpm playwright`.
- The golden tests (risk, `pit`, WORM, tax) live in the Rust crates; `pit` is also tested through its Python binding.

## 2. USER-blocker rule (from 17 §G, kit 1.4.2)

An agent task may depend on a USER task **only** when it truly needs something only the human can provide:
- a key or account;
- money;
- a legal or tax answer;
- a fact only they know, such as their own accounts, their own MasterTradingBot files, or their tax agent.

Everything else is unblocked:
- **Configurable values** (limits, thresholds, lists of keywords or feeds, sleeves, schedules, labels used for tuning): the agent drafts them from the docs' defaults and seeds them, and the human reviews them once in the go-live pack (P7-T070). Remove any dependency on a USER task that only "sets" or "decides" such a value, and say so in the progress log.
- **Labelled data the human was asked to make** (e.g. relevance labels): use agent-made silver labels by default; the human's labels are an optional improvement that never blocks.
- **Walkthroughs, drills and "take part in" items:** keep them as USER tasks scheduled before go-live (they can feed P7-T070 or the P7 preflight), but no build or RUN task waits on them. Exit-demo tasks may still list them.
- **Live checks with real keys** stay separate, late VERIFY tasks that depend on the USER key task ("build first, keys last").

Never invent a USER task to replace one you removed; never make an agent do a USER task.

**USER tasks that only set a configurable value become agent tasks.** Convert each of these the way P2-T048/T049/T050 were converted:
- `type` BUILD/OPS and `owner: agent`;
- the title becomes "Seed …" or "Draft …";
- the agent seeds the default from the cited doc section through `mt-api` with source `seed`, idempotent, never overwriting the human's edits;
- the human reviews it in the go-live pack (P7-T070) or edits it any time.

The tasks to convert:
- **P1-T001**: starting universe/watchlist from the docs' default lists.
- **P1-T066**: the agent tunes noisy DQ thresholds from the first week's alert stats, inside the 16 ranges; tightening only.
- **P4-T003**: keywords, cashtags and trusted feeds from docs 06/12 defaults.
- **P4-T049**: becomes optional human labels on top of agent silver labels (stays USER, optional, blocks nothing).
- **P5-T007**: disposal rule and EV hurdle from 13/16 defaults.
- **P5-T065**: wallet, signer and gas limits from 16 §2.7. Enabling signing still needs P5-T004's human approval.
- **P6-T001**: LLM budgets from 16 §2.10. The custom endpoint URL and key stay in P0-T007.
- **P6-T003**: optional modules default **off** per the docs; enable any time in settings. Convert it to a short agent task that records the defaults, or cancel it with that reason.
- **P8-T019**: default token scopes read-only, expiry per 16 §2.12. Enabling write tool groups stays a C3 action.

Leave the remaining USER tasks as they are: keys, accounts, money, legal/tax, facts only the human has, drills, and approvals of real-money actions.

## 3. Doc wave (agents assigned doc sets)

- Bring your docs in line with 18 using §1.
  - Rewrite stack text: tables of services and packages, layout, migrations, the DB, auth and deploy.
  - Point to 18 for the full picture rather than duplicating it.
  - Keep **heading text unchanged** wherever possible, because tasks link to the anchors. If you must rename a heading, list the old and new anchors in your report.
- Keep the house style: short sentences, plain words, tables where they help. Mark unverified facts **(U)**.
- Edit only your assigned files; report problems in other docs instead of fixing them.

## 4. Task wave (agents assigned phases)

For every task in your phase(s):
1. Apply §1 to front matter (`tools`, `services`) and text: paths, commands, technology names, Verification commands.
2. Apply §2 to `depends_on`: remove USER dependencies that §2 says are not needed. Where a value or list was expected from the human, the task now seeds a default from the docs (cite the doc section).
3. Workstation-first: remove host, LUKS, Tailscale, YubiKey and GPU preconditions before Phase 7 (keep them in P7 shift/live tasks).
4. Add a progress-log line: `- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (<what changed>)`.
5. Keep IDs, file names and headings. Don't delete items; cancel obsolete ones with `./kanban cancel <ID> --reason "…"`. If the new stack needs work no task covers (e.g. a Supabase stack task, a partition job, a Cargo workspace skeleton, Python bindings for `pit`, a `vercel.json`), create it with `./kanban new --phase N --type … --title "…"` and fill every template heading.

**Validation:**
- The kanban hooks are **paused** for this wave. Don't run `./kanban build` or `./kanban pause --off`.
- Validate with `python3 tools/kanban/kanban.py validate --phase N`: **0 errors and 0 warnings**.
- Don't commit; the main agent commits.

## 5. Report (≤ 250 words)

Report:
- the count of files changed and the notable changes;
- new IDs;
- USER dependencies removed (`ID → dependency`);
- USER dependencies kept, with the reason;
- anchors renamed;
- contradictions found in docs you didn't own.
