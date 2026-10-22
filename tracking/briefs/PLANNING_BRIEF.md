# Phase Planning Brief (for planning agents)

Use this brief to (re)plan a phase into kanban items. It keeps every phase board uniform, so they all roll up into the root board (`KANBAN.md` / `kanban.html`).

## 1. Your scope

- You own **one phase**: `tracking/phase-N/` only (plus `PHASE.part-*.md` if the phase is split between planners).
- **Don't edit any other file in the repo.** Problems you find elsewhere become **gap/bug items** in your phase (§5).
- You plan; you don't implement product code. Every item must be **ready for branch + PR work**: a developer or agent can pick it up cold and finish it from the file alone, plus the docs it links.

## 2. Read first

1. `tracking/SCHEMA.md`, `tracking/templates/{task,bug,phase}.md`. These are the exact formats.
2. Your roadmap phase doc `docs/roadmap/phase-N-*.md` (primary) and `docs/roadmap/README.md`.
3. Every doc your roadmap phase links to: `docs/02`, `03`, `07`, `09`–`15`, `docs/ui/**` dashboards, `DESIGN.md` §6.8, and `SPEC.md` (non-negotiables) and `GOAL.md`.
4. Cross-reference neighbouring phases' roadmap docs so you don't duplicate or orphan work at the boundaries.

## 3. What to produce

**A. `tracking/phase-N/PHASE.md`** (from `templates/phase.md`):
- Front matter exactly as in the template, with the `opens_after` you were given; `status: not_started`; dates `2026-10-21`.
- **Summary** and **Entry criteria** checklist.
- **Exit criteria** checklist: the roadmap §6 items, plus "all tasks done/cancelled" and "no open S1/S2 bugs".
- **Workstreams** table and **Critical path**.
- **Traceability:** every roadmap requirement `R<N>.xx` → tasks, and every roadmap ToDo `T<N>.xx` → tasks. **Every one must be covered.**
- **Planning notes & risks**, and **Cross-phase prerequisites** (other phases' roadmap IDs your tasks rely on).

**B. Task items** `tracking/phase-N/tasks/P<N>-T<nnn>-<slug>.md` (from `templates/task.md`):
- **Decompose every roadmap ToDo** into implementable tasks: one branch and one PR each, sized **XS–L** (XS ≈ < 2 h, S ≈ half a day, M ≈ 1–2 days, L ≈ 3–5 days of evenings). **No XL**; split instead.
- **Every task has all required headings** with specific content:
  - **Goal / expected outcome:** concrete end state.
  - **Context & references:** relative links (from a task file the repo root is `../../../`) to roadmap requirement(s), spec sections, flows, dashboards, related tasks.
  - **Requirements:** functional + non-functional, with the real numbers from the docs (SLOs, caps, limits, retention).
  - **ToDo:** `- [ ]` steps covering code, config, tests and docs.
  - **Verification:**
    - **Tests:** unit / integration / golden / property.
    - **Scenarios:** given/when/then, including unhappy paths.
    - **Stress / failure injection:** load, fault, chaos, latency, or "n/a: reason".
  - **Acceptance criteria:** `- [ ]` measurable.
  - **Exceptions & edge cases:** degraded modes (02 §9.3), restarts, clock, partial failure.
  - **Cardinal rules (do NOT):** task-specific prohibitions **plus** the relevant global ones (§6).
  - **Doc sync on completion:** which docs change when it lands. Always include the roadmap phase doc, because completing a task ticks the matching roadmap ToDo box.
  - **Branch & PR:** branch `p<N>/<ID>-<slug>`, PR title `<ID>: <title>`, PR checklist.
  - **Progress log:** one line, `- 2026-10-21 00:00 · planner · created`.
- **Front matter:**
  - `status: backlog` (triage promotes it); `created`/`updated: 2026-10-21`.
  - `type` is one of USER / BUILD / OPS / VERIFY / RUN / DOC; `owner: user` for USER items, otherwise `agent`.
  - `requirements` and `roadmap_todos` use the roadmap IDs; `modules` and `dashboards` as relevant.
  - `doc_sync` lists repo-relative paths.
  - **What the task needs to run:** `tools` (CLIs on PATH, e.g. `[docker, uv, pnpm]`), `mcp` (MCP servers the agent will call), `env` (variable **names** only, e.g. `[BINANCE_TRADE_KEY]`; values stay in the sops file), `services` (e.g. `[timescaledb, redis]`). Anything only the user can provide is a USER task this one depends on. Don't assign skills.
  - **`depends_on` only references items in your own phase.** Cross-phase prerequisites are handled by the phase's `opens_after` and are named in text under *Context & references*.
- **USER items** (only the human can do them): exact step-by-step instructions, where outputs go (secrets → the sops secrets file, **never** chat or git), how to confirm, and what it unblocks.
- **Verification coverage:**
  - every BUILD/OPS item carries its own tests;
  - add dedicated **VERIFY** items for each roadmap VERIFY ToDo, end-to-end **scenario** items for the phase's flows, **stress/failure-injection** items where the roadmap has SLOs or degraded modes;
  - **one final "Phase exit demo" VERIFY item** that runs every exit criterion and depends on everything it needs.
- **RUN items that would outlast the phase** (e.g. an 8-week paper clock) are modelled as "start X" here; completion is checked in the phase that needs it. This keeps phases closable.
- Number items in a sensible build order (T001, T002, …), using the ID range you were given.

**C. Gap/bug items** in `tracking/phase-N/bugs/P<N>-B<nnn>-<slug>.md` (from `templates/bug.md`, `kind: gap` or `bug`):
- File one for each inconsistency, missing spec detail, conflicting numbers, broken link or unaddressed requirement you find while cross-referencing.
- Severity: **S1** blocks the phase · **S2** major · **S3** minor · **S4** trivial.
- `found_in` = the doc path (and section).
- *Requirements* holds what's wrong / expected / suggested fix.

## 4. Quality bar

- Specific beats generic: name the files, packages (`packages/mt_risk/...`), tables, NATS subjects, commands, endpoints and numbers from the docs.
- No invented paid services or data; free tiers only (03 §1).
- Plain English, concise. A task file is typically 70–150 lines.
- Before finishing, run `python3 tools/kanban/kanban.py validate --phase N`. It must show **0 errors**, and no warnings about missing roadmap IDs or headings. **Don't** run `build` (the main agent does).

## 5. Final report (≤ 300 words)

- Tasks by type and total.
- A requirement and ToDo coverage statement (any uncovered → why).
- The gaps/bugs filed (ID, severity, one line each).
- Cross-phase prerequisites.
- Anything uncertain.

## 6. Global cardinal rules (copy the relevant ones into each task)

- Never commit secrets, or paste them into chats/issues; secrets live in the sops/age file (07 §2).
- Never bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- **Never update or delete WORM rows**; corrections are new rows (15 §2).
- No paid data/APIs; no scraping that breaks terms; no self-bots or user tokens; no sybil/multi-wallet/fake engagement.
- **No Telegram text in any model, RAG index or training set** (12 §4–5).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates.
- Never skip, weaken or delete a test to get green. Pin images by digest. No telemetry or referral IDs in vendored code.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
