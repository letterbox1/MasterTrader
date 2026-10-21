# CLAUDE.md

@AGENTS.md

## Claude Code specifics

- **Hooks** (`.claude/settings.json`) run the kanban tool automatically in cloud and local sessions:
  - **SessionStart:** logs the session to `tracking/SESSIONS.md` and prints the resume brief (what's in progress, checkpoints, doc sync pending, next ready). Act on it before anything else.
  - **PostToolUse:** when item files change, re-triages and rebuilds every board, `KANBAN.md`, `kanban.html` and the roadmap status blocks.
  - **Stop:** if an item was completed and its docs haven't been synced, it asks you **once per item** to update the docs listed in its `doc_sync` field, then run `./kanban docsync <ID> --done`. Do it before ending the turn unless the user says otherwise.
- **Bulk edits** to many item files (re-planning): run `./kanban pause` first and `./kanban pause --off` + `./kanban build` after, so triage doesn't rewrite files mid-edit.
- **Sub-agents** working on a phase must stay inside `tracking/phase-N/` and the code for their item, and follow `tracking/PLANNING_BRIEF.md` when (re)planning.
- **Before the session ends or context runs low:** checkpoint every in-progress item, then commit and push, so nothing is lost if the session dies.
