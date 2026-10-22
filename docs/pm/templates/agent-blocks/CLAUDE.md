<!-- pm-kit:start (managed by CeraNova PM install.sh; edit outside this block for project-specific rules) -->
@AGENTS.md

## CeraNova PM: Claude Code specifics

- **First run:** if `tracking/kanban.config.json` doesn't exist and `tracking/` has no `phase-*` folders, invoke the **pm-bootstrap** skill before any other project work. Then follow the lifecycle:
  - **pm-intake** → (**pm-doc-ingest**, **pm-research**, **pm-scope**) → **pm-roadmap**;
  - **pm-plan** / **pm-delegate** → **pm-reconcile**;
  - **pm-execute** → **pm-review** → **pm-doc-sync** / **pm-status**; **pm-triage** whenever bugs, requests or failures come in.
- **What's next:** the session-start brief's **"Lifecycle next"** line (and `./kanban doctor`) names the next skill; act on it. If anything about the setup misbehaves, use **pm-doctor** (`./kanban doctor --fix`). Use **pm-lifecycle** if unsure.
- **Hooks** (`.claude/settings.json`) run whatever model this harness uses:
  - **SessionStart:** enables the git hooks, logs the session to `tracking/SESSIONS.md` and prints the resume brief. Act on it first.
  - **PostToolUse:** rebuilds every board when item files change.
  - **Stop:** asks **once per completed item** for doc sync. Do it before ending the turn unless the human says otherwise.
  - The same hooks exist for Codex, Gemini CLI, Cursor and OpenCode (`./kanban agents`).
- **Bulk edits** to item files: `./kanban pause` first; `./kanban pause --off && ./kanban build` after.
- **Sub-agents** stay inside their assigned phase folder or doc set and follow the matching brief in `tracking/briefs/`.
- **Reconciling with the human:**
  - explain gaps plainly with a recommendation;
  - record decisions in the decisions register and configuration doc;
  - align the docs, then the tasks;
  - close gaps with evidence (**pm-reconcile**).
- **Before the session ends or context runs low:** checkpoint in-progress items, commit, push.
<!-- pm-kit:end -->
