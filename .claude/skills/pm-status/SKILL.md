---
name: pm-status
description: Report project progress and keep sessions recoverable - per-phase progress bars, what's in flight, blocked, next up, open S1/S2 gaps, doc sync; open or serve the HTML board; produce a handoff before ending or switching cloud/local. Use for "where are we", "status", "show me the board", "hand off", "I'm switching machines", or when a session is about to end.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.1"
---

# pm-status

## Report

1. `./kanban build` (fast), then read `KANBAN.md`. Optionally `./kanban next -n 10`, `./kanban list --status blocked`.
2. **Tell the human, briefly:**
   - overall % and per-phase %, with status;
   - what's in progress, each with its checkpoint;
   - what's blocked and why;
   - the next 3–5 ready items, and **which need them** (`owner: user`);
   - open S1/S2 gaps;
   - pending doc sync.
3. **Board:**
   - local: `./kanban open` (or `./kanban serve` → http://127.0.0.1:8765/kanban.html);
   - on GitHub: `KANBAN.md` and `tracking/phase-N/BOARD.md`.

## Handoff / end of session / switching cloud ↔ local

1. `./kanban checkpoint <ID> "<where I am, what's next>"` for every in-progress item you touched.
2. `./kanban session handoff --note "<summary>"`, then commit and push. The pre-push hook checks the boards are current.
3. On the other machine: `git pull`, then `./kanban resume`. Agents with session hooks (e.g. Claude Code) do this automatically and also switch the git hooks on.

## Health

`./kanban doctor` checks Python, git hooks, agent session hooks (Claude Code, Codex, Gemini CLI, Cursor, OpenCode), the CLAUDE.md/AGENTS.md merge blocks, config, phases and validation.
