---
name: pm-bootstrap
description: Install and initialise the CeraNova PM (kanban per phase + project board + hooks + agent protocol) in the current repository, new or existing, any project type (software, content, media, research). Use when tracking/kanban.config.json is missing, when the user says "set up the kanban / project tracking / CeraNova PM here", or after the kit files were just copied into a repo.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-bootstrap

**Goal:** a working tracking system in this repo, configured for this project, with hooks active and the agent protocol merged, without breaking anything the project already has.

## Steps

1. **Check what's here:** `./kanban doctor` if `./kanban` exists. Otherwise look for `tools/kanban/kanban.py`.
   - If the kit files are missing, ask the human to run `install.sh /path/to/this/repo` from a CeraNova PM checkout, or copy the kit (see `docs/pm/MERGING.md`).
   - Never invent the tool.

2. **Detect the project type and conventions** (don't ask what you can read):
   - languages, build/test commands, CI;
   - existing docs (`README`, `docs/`, ADRs);
   - media/content folders;
   - branch naming and commit style;
   - existing git hooks (`core.hooksPath`, `.husky/`, `.git/hooks/`, pre-commit framework);
   - existing `CLAUDE.md` / `AGENTS.md` / `.claude/settings.json`.

3. **Merge, don't overwrite** (`install.sh` already does this; verify it):
   - `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` each contain one `<!-- pm-kit:start -->…<!-- pm-kit:end -->` block; the project's own text stays outside it.
   - `.claude/settings.json` contains the three kanban hooks (SessionStart, PostToolUse, Stop) **alongside** any existing hooks. If the human uses other agents, add theirs too: `./kanban agents --add codex,gemini,cursor,opencode` (or `all`).
   - `.gitignore` contains `tracking/.state/`.
   - **Git hooks:**
     - if `core.hooksPath` is unset → `./kanban install-hooks`;
     - if the project uses husky or another `core.hooksPath` → add `python3 tools/kanban/kanban.py git-hook <name> "$@"` lines to its pre-commit/pre-push/post-merge/post-checkout scripts;
     - `.git/hooks/*` scripts are chained automatically.

4. **Configure:** run `./kanban detect` (project type from repo signals), then `./kanban init --project "<name>" [--type <type>]`. The type drives the research agendas (**pm-research**). Then edit `tracking/kanban.config.json` only if the project needs it:
   - task `types` (e.g. media: add `ASSET`, `EDIT`, `REVIEW`);
   - `sizes`, `required_headings`, `roadmap_dir`, `brand` colours.

   See `docs/pm/CUSTOMIZING.md`.

5. **Next:**
   - If foundation docs (goal/spec/architecture) are missing or thin → **pm-intake**.
   - If the human handed you docs → **pm-doc-ingest**.
   - If docs exist but there's no roadmap → **pm-roadmap**.

6. **Verify:** `./kanban doctor` all ok (or each FIX explained to the human); `./kanban build`; the board renders (`./kanban open` locally).

7. **Commit** (`pm: bootstrap`) and push. The pre-commit hook validates. Tell the human:
   - where the board is;
   - that Claude Code may ask them to trust the project hooks;
   - that other agents/clones need `./kanban install-hooks` once (agents with session hooks, e.g. Claude Code, do this automatically).

## Don't

- Don't overwrite existing hooks, CI, `CLAUDE.md` or `AGENTS.md` content.
- Don't enable CI that costs minutes. The kit's workflow is manual-only.
- Don't create tasks before a roadmap exists, except bugs/gaps.
