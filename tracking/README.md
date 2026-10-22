# Tracking: per-phase kanbans and the project board

Every phase of the roadmap (`docs/roadmap/`) has its own kanban. All of them are built the same way and roll up into one project board.

## 1. Where to look

| View | What it shows | How |
|---|---|---|
| **`kanban.html`** (repo root) | Interactive board: overall and per-phase **progress bars**, columns Backlog → Ready → In progress → Review → Blocked → Done, filters (type, priority, owner, search), item details, bugs, doc-sync queue, recent sessions | `./kanban open` (builds and opens it), or `./kanban serve` and visit `http://127.0.0.1:8765/kanban.html` |
| **`KANBAN.md`** (repo root) | The same summary in Markdown: phase table with bars, in progress, blocked, next up, S1/S2 bugs, doc sync | Readable on GitHub |
| **`tracking/phase-N/BOARD.md`** | One phase's kanban with its progress bar | Linked from `KANBAN.md` |
| **`tracking/phase-N/PHASE.md`** | Phase plan: entry/exit criteria, workstreams, critical path, traceability | Hand-maintained |
| **`docs/roadmap/README.md`** | Phase status block (auto-updated) | — |

## 2. Where the data lives

```
tracking/phase-N/tasks/P<N>-T<nnn>-<slug>.md   ← one file per task (the spec for a branch + PR)
tracking/phase-N/bugs/P<N>-B<nnn>-<slug>.md    ← bugs and gaps found along the way
```

The format is in [SCHEMA.md](SCHEMA.md) and the templates are in [templates/](templates/). Everything else is generated from these files by `./kanban build`, so the boards can't drift from the items.

## 3. Life of a task

1. `backlog` → **ready**: automatic once its dependencies are done and its phase is open.
2. `./kanban start P2-T014`: **in progress**, claimed by this session.
3. Tick ToDo boxes and `./kanban checkpoint P2-T014 "…"` as you go.
4. `./kanban review P2-T014 --pr <url>`: **review**.
5. `./kanban done P2-T014 --evidence "pytest -k risk: 48 passed; drill ok"`: **done**.
   - `done` refuses while ToDo or acceptance boxes are unticked, or without evidence.
6. Its `doc_sync` docs are queued in `DOC_SYNC.md`. Update them, then `./kanban docsync P2-T014 --done`.

**Bugs:** `./kanban new --phase 2 --kind bug --severity S2 --found-in P2-T014 --title "…"`. Open **S1/S2** bugs block phase completion.

## 4. Automation

| Trigger | What happens |
|---|---|
| Claude Code **SessionStart** hook | Logs the session (cloud/local, host, branch, active items) to `SESSIONS.md`; prints the resume brief into the agent's context |
| Claude Code **PostToolUse** hook | If any item file changed: triage (backlog ↔ ready, auto-unblock, doc-sync flags, phase status) + rebuild all boards |
| Claude Code **Stop** hook | Once per newly completed item with pending doc sync: asks the agent to update the spec/roadmap/docs and mark doc sync done |
| git **pre-commit** | Validate + rebuild + stage generated files into the same commit, for any agent or human |
| git **pre-push** | Refuse the push if items are invalid or boards are stale (rebuilds them and tells you to commit); notes pending doc sync |
| git **post-merge / post-checkout** | Print the resume brief after pulling another machine's work or switching branches |
| **CI** (`.github/workflows/kanban.yml`) | **Manual only** (Actions → Run workflow). A backstop for edits made outside a hooked clone (e.g. the GitHub web editor); costs no minutes day to day |

**Phase completion** is automatic: all tasks done/cancelled, no open S1/S2 bugs, and all `PHASE.md` exit criteria ticked. The phase is then marked `done` and its doc sync queued; the next phase unlocks via `opens_after`.

**Which hooks run where:**
- **Git hooks** run on whatever machine makes the commit or push, for every tool (Claude Code with any model, Codex, Gemini CLI, Cursor, a human in a terminal). They're the universal layer.
- Git doesn't copy hooks when cloning. The Claude Code SessionStart hook switches them on automatically (`core.hooksPath`); elsewhere, run `./kanban install-hooks` once per clone.
- **Agent session hooks** add the resume brief, live rebuilds and doc-sync prompts: `.claude/settings.json` (Claude Code, whatever model it runs), `.codex/hooks.json` (Codex), `.gemini/settings.json` (Gemini CLI), `.cursor/hooks.json` (Cursor), `.opencode/plugins/ceranova-pm.js` (OpenCode). `./kanban agents` shows and adds them.
- Other CLIs have their own (or no) hook systems. They read `AGENTS.md` / `GEMINI.md` and rely on the git hooks.
- **Hooks never push for you.** The pre-commit hook puts the rebuilt boards into your commit, and your normal `git push` carries them. `git commit --no-verify` or edits on github.com skip hooks; that's what the manual CI backstop is for.

## 5. Cloud ↔ local, and crash recovery

Nothing lives only in a session. Every item's status, checkpoint and append-only progress log are in git.

| Situation | What to do |
|---|---|
| **Moving machines** | Push from one machine, then `git pull && ./kanban resume` on the other. The resume brief lists in-flight items with their checkpoint, last log lines and branch. |
| **A session crashed or ran out of usage** mid-task | The item is still `in_progress` with its last checkpoint. Run `./kanban resume`, check out the item's branch, read the progress log, and carry on. |
| **Ending a session cleanly** | `./kanban session handoff --note "…"`, then commit + push. |
| **Bulk edits** (e.g. re-planning a phase) | `./kanban pause`, edit, then `./kanban pause --off && ./kanban build`. |

## 6. Planning a phase

Planning agents follow [briefs/PLANNING_BRIEF.md](briefs/PLANNING_BRIEF.md): one phase each, every roadmap requirement and ToDo covered, every task with tests, scenarios, stress checks, exceptions and cardinal rules, and gaps filed as items.

## 7. Skills and the full lifecycle

The pm-* skills (open Agent Skills format, installed in `.claude/skills/` and `.agents/skills/`) package the whole lifecycle:
- bootstrap, intake, doc ingest, research, scope, roadmap, plan;
- delegate, reconcile, execute, review, triage;
- doc sync, status, doctor.

See [`docs/pm/LIFECYCLE.md`](../docs/pm/LIFECYCLE.md) and [`docs/pm/SKILLS.md`](../docs/pm/SKILLS.md). Agent briefs live in [`briefs/`](briefs/).
