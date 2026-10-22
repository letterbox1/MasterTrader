<!-- pm-kit:start (managed by CeraNova PM install.sh; edit outside this block for project-specific rules) -->
# Agent protocol (CeraNova PM)

This applies to every coding agent and any model: Claude Code (cloud or local), Codex, Gemini CLI, Cursor, OpenCode and similar.

**All work is tracked on per-phase kanbans** in [`tracking/`](tracking/README.md), rolled up into [`KANBAN.md`](KANBAN.md) / `kanban.html`. The phased plan is in `docs/roadmap/`. Lifecycle guide: [`docs/pm/LIFECYCLE.md`](docs/pm/LIFECYCLE.md).

## 1. Session protocol

1. **Sync and resume.** `git pull`, then `./kanban resume` (its **"Lifecycle next"** line names the next step; `./kanban doctor` shows the full list). If anything is `in_progress`, finish it first: read its `checkpoint` and progress log, check out its branch.
2. **Pick.** `./kanban next [--phase N]`. Items with `owner: user` are the human's (accounts, credentials, money, approvals, decisions). **Never do them for the user.** Prepare instructions or supporting work instead.
3. **Claim.** `./kanban start <ID> [--git]`. A session-designated branch overrides the item's branch name (`start` logs the branch). Put the item ID in every commit message so `./kanban trail <ID>` reconciles item → branch → PR → commits. `start` runs a **preflight** of the tools, MCP servers, env var names and services the item lists; if something only the human can provide is missing, block the item and raise a USER task.
4. **Work the item file as the spec:** Requirements, ToDo, Verification, Exceptions, Cardinal rules. Tick boxes as you go (`./kanban tick <ID> <n|text>`).
5. **Checkpoint often.** `./kanban checkpoint <ID> "where I am, what's next"` after each step and **always before stopping**. Commit and push the item file with the work.
6. **Verify.** Run the item's tests, scenarios and stress checks; record commands and results in the progress log.
7. **Bugs found along the way.** Search first (`./kanban list --grep "…"`), then `./kanban new --phase N --kind bug --severity S1|S2|S3|S4 --found-in <ID> --title "…"` (**pm-triage**). Don't silently fix unrelated things.
8. **Finish.** `./kanban review <ID> --pr <url>`, then an independent check (**pm-review**, ideally another agent: `./kanban reviewed <ID> --pass|--fail --note "…"`). After merge or verification, push, then `./kanban done <ID> --evidence "commands + results"` (it records the item's commits). `done` refuses on unticked boxes or missing evidence (and on a missing passing review when `require_review` is on).
9. **Doc sync.** Completing an item queues its `doc_sync` docs (`tracking/DOC_SYNC.md`). Update them to match what was built, **tick the roadmap ToDo**, then `./kanban docsync <ID> --done`.
10. **End of session.** `./kanban session handoff --note "…"`, then commit and push.

## 2. Phase completion

A phase completes automatically when all its tasks are done or cancelled, no S1/S2 bug is open, and every `## Exit criteria` box in `tracking/phase-N/PHASE.md` is ticked (with evidence). Then:
1. Mark the phase done in the roadmap and plan docs.
2. Run `./kanban docsync P<N> --done`.

The next phase opens by itself.

## 3. Generated files: never edit

- `KANBAN.md`, `kanban.html`
- `tracking/phase-N/BOARD.md`, `tracking/DOC_SYNC.md`
- the blocks between `<!-- kanban:… -->` markers

Never delete items; cancel them instead (`./kanban cancel <ID> --reason …`).

## 4. Universal cardinal rules

- Never commit secrets or paste them into chats, issues or logs.
- Never skip, weaken or delete a test to get green.
- Nothing a user may want to change is hard-coded; it goes in the configuration doc as a default.
- Respect the project-specific rules below this block.

## 5. Git

- **Branches:** `p<N>/<ID>-<slug>`, one item per branch/PR. PR title `<ID>: <title>`. Commits mention the item ID.
- **Git hooks** run locally for every tool and model. Claude Code sessions enable them automatically; otherwise run `./kanban install-hooks` once per clone.
  - **pre-commit:** validate + rebuild boards.
  - **pre-push:** block if invalid or stale.
  - **post-merge / post-checkout:** resume brief.
- CI is a manual backstop only.

## 6. Skills (open Agent Skills format) and commands

Skills (`SKILL.md`, open Agent Skills format) are installed in `.claude/skills/` (Claude Code; OpenCode reads it too) and `.agents/skills/` (Codex, Gemini CLI and other open-standard agents):
- **pm-lifecycle** (router), **pm-doctor** (setup check, repair, next step)
- **pm-bootstrap**, **pm-intake**, **pm-doc-ingest**, **pm-research**, **pm-scope**, **pm-roadmap**, **pm-plan**
- **pm-delegate**, **pm-reconcile**, **pm-execute**, **pm-review**, **pm-triage**, **pm-doc-sync**, **pm-status**

Agents that don't load skills automatically can read the same `SKILL.md` files as step-by-step playbooks. Write a project skill only for a procedure you'll repeat (`.agents/skills/<project>-<name>/`; `./kanban doctor --fix` mirrors it).

**Session hooks** (resume brief, board rebuild, doc-sync prompt) exist for Claude Code, Codex, Gemini CLI, Cursor and OpenCode: `./kanban agents` shows them, `./kanban agents --add <agent>` installs one. Without them, run `./kanban resume` first; the git hooks still guard every commit and push.

```
./kanban resume | next [--phase N] | list [--phase N --status S --type T --kind gap --include-bugs] | show <ID>
./kanban start <ID> [--git] | preflight [<ID>… | --ready] | tick <ID> <n|text> | checkpoint <ID> "note"
./kanban review <ID> --pr URL | reviewed <ID> --pass|--fail --note "…" | done <ID> --evidence "…"
./kanban block <ID> --reason … | unblock <ID> | list --grep "words" | trail [<ID>…] | agents [--add …|all] | version
./kanban new --phase N --title "…" [--kind task|bug|gap|chore] [--type BUILD] [--severity S2]
./kanban init --project "…" [--phases "A,B,C" --roadmap] | phase-add --title "…" [--roadmap]
./kanban docsync <ID|P<N>> --done | validate [--phase N] | build | open | serve | doctor [--fix]
./kanban session handoff --note "…" | pause [--off] | install-hooks
```
<!-- pm-kit:end -->

# MasterTrader specifics

**MasterTrader** is a private, single-user, self-hosted AI trading platform.
- Start with [README.md](README.md) and [SPEC.md](SPEC.md); the phased plan is in [docs/roadmap/](docs/roadmap/README.md).
- Decisions and configurable defaults: [16 configuration and safety model](docs/16-configuration-and-safety-model.md) and [17 decisions register](docs/17-decisions-register.md). Numbers are configurable defaults from 16, never hard-coded.
- Agent briefs: [`tracking/briefs/`](tracking/briefs/) (planning, execution, doc alignment, task alignment, doc ingest).

## Cardinal rules (apply to all work)

- **Secrets:** never commit secrets or paste them into chats, issues or logs. Secrets live in the sops/age file ([07 §2](docs/07-security-notes.md#2-secrets)).
- **No bypasses:** every order goes through the risk manager (M11) via `mt_api`; research reads data only through `pit(as_of)`.
- **WORM:** audit/journal records are write-once ([15 §2](docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)). Never UPDATE or DELETE them; corrections are new rows.
- **Data terms:**
  - free data only;
  - no scraping against terms, no self-bots or user tokens, no sybil or fake engagement;
  - **no Telegram text in any model, RAG index or training set** ([12 §4–5](docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- **Money safety:**
  - keys are trade-only, IP-locked, withdrawals disabled;
  - no live money before the Phase 7 gates;
  - loosening risk, autonomous mode and mandates are C3;
  - protective exits never wait for approval.
- **Tests:** never skip, weaken or delete a test to get green; risk, `pit`, WORM and tax golden tests are mandatory.
- **Supply chain:** pin images by digest; no telemetry or referral IDs in vendored code; review every third-party bump.

## Doc sync targets

- Spec (`docs/03`), architecture (`docs/02`), the roadmap phase doc (**tick the matching roadmap ToDo**), UI docs (`docs/ui/`), `SPEC.md`.
- On phase completion: update `docs/roadmap/README.md` and `docs/04-plan-of-action.md` to mark the phase done, then `./kanban docsync P<N> --done`.
- Tick `PHASE.md` exit criteria only with evidence: link the run, log or commit in the progress log of the phase's exit-demo item.

## What tasks need to run

Each task lists `tools`, `mcp`, `env` and `services` in its front matter (checked by `./kanban preflight` and `./kanban start`):
- `env` holds variable **names** only; values live in the sops/age secrets file ([07 §2](docs/07-security-notes.md#2-secrets)) and never in item files.
- Exchange keys, accounts, paid plans and anything with money are USER tasks the item depends on.

## Git

- **Don't push to `main` directly.** Session-specific branch instructions override this.
- Commits mention the item ID and include the updated item file with the code.
- **CI** (`.github/workflows/kanban.yml`) is **manual only**; day-to-day checking happens in the local git hooks.
