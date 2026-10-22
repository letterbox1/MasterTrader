---
name: pm-doctor
description: Diagnose and repair the CeraNova PM setup in this repo and find where the project is in the lifecycle - runs `./kanban doctor`, applies `--fix` for safe repairs (git hooks, agent session hooks, CLAUDE.md/AGENTS.md blocks, skill mirroring, .gitignore, config, permissions, boards), fixes what remains by hand, then hands over to the next lifecycle skill. Use when something about the kanban, hooks or boards isn't working, after cloning or moving machines, when the resume brief looks wrong, or for "check the setup", "what's next", "fix the tracking".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.2"
---

# pm-doctor

1. **Diagnose:** `./kanban doctor`. It prints:
   - **Setup:** each check as `ok` / `FIX` (python, git, git hooks, executables, agent session hooks, merge blocks, `.gitignore`, config, templates, validation);
   - **Lifecycle:** the ordered next steps, each naming a skill. For example:
     - `pm-intake: foundation docs missing`
     - `pm-plan: phases without tasks`
     - `pm-reconcile: 3 open S1/S2 gaps`
     - `pm-execute: …ready`
     - `ask the human: USER items waiting`

2. **Auto-repair the safe items:** `./kanban doctor --fix`. Repaired lines show `FIXED`; it never overwrites your text or existing hooks.

3. **Fix the rest by hand:**

   | Problem | Fix |
   |---|---|
   | `./kanban` / `tools/kanban/` missing | Re-run the kit installer (`install.sh /path/to/repo --update`) |
   | `core.hooksPath` points to husky or another manager | Add `python3 tools/kanban/kanban.py git-hook <name> "$@"` to that manager's `pre-commit`, `pre-push`, `post-merge`, `post-checkout` (`docs/pm/MERGING.md`) |
   | Validation errors | `./kanban validate` lists file + problem. Fix the item front matter or headings per `tracking/SCHEMA.md`. Never delete items; cancel them |
   | Templates missing | `install.sh --update` (or `--force-templates` to refresh customised ones) |
   | Hooks paused | If nothing is mid-edit: `./kanban pause --off && ./kanban build` |
   | Boards stale or conflicted after a merge | `./kanban build` and commit the regenerated files (never hand-merge them) |
   | Session hooks don't fire | `./kanban agents` shows each agent's status; `./kanban agents --add <agent>` adds them. Agents ask you to trust/approve project hooks once (Claude Code prompt; `/hooks` in Codex and Gemini CLI) and load them at session start, so restart the session |
   | A task won't start (preflight) | `./kanban preflight <ID>` lists what's missing. Install routine tools; for keys, accounts or paid services, block the item and raise a USER task |

4. **Re-run** `./kanban doctor` until Setup is all `ok`. Commit (`pm: doctor fixes`).

5. **Continue the lifecycle** with the first step it lists. If the first step is `ask the human`, present the waiting USER items with their instructions.
