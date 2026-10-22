# Adding CeraNova PM to an existing project

## Option A: installer (recommended)

```bash
git clone https://github.com/letterbox1/project-manager.git /tmp/ceranova-pm
/tmp/ceranova-pm/install.sh /path/to/your/project            # add --init "Name" --phases "A,B,C" to initialise too
```

**What it touches:**

| Path | Behaviour |
|---|---|
| `tools/kanban/`, `kanban`, `skills/pm-*` → `.claude/skills/` and `.agents/skills/` (choose with `--agents`), `tracking/{README,SCHEMA}.md`, `tracking/briefs/`, `docs/pm/*.md` | Copied (updated on re-run) |
| `tracking/templates/`, `docs/pm/templates/` | Copied only if missing (`--force-templates` to refresh) |
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | A `<!-- pm-kit:start --> … <!-- pm-kit:end -->` block is **appended** (or replaced on update). Your text is untouched |
| Agent session hooks | **Added next to** your existing hooks: `.claude/settings.json` always; `.codex/hooks.json`, `.gemini/settings.json`, `.cursor/hooks.json`, `.opencode/plugins/ceranova-pm.js` when that agent's folder exists (choose with `--hooks auto\|all\|claude,codex,gemini,cursor,opencode`; later: `./kanban agents --add <agent>`) |
| `.gitignore` | Adds `tracking/.state/` |
| `.github/workflows/kanban.yml` | Created only if missing (manual trigger, costs no CI minutes) |
| Git hooks | `core.hooksPath = tools/kanban/githooks` if you don't use `core.hooksPath` already. Your `.git/hooks/*` scripts keep running (they're chained first) |
| Your tracking data | Never touched (phases, tasks, bugs, `kanban.config.json`) |

**Updating:** re-run the installer, or `install.sh /path --update`. Use `--dry-run` to preview.

## Option B: by hand

1. Copy these into the project root:
   - `tools/kanban/`
   - `kanban`
   - `skills/pm-*` → into `.claude/skills/` (Claude Code) and/or `.agents/skills/` (Codex and other open-standard agents)
   - `tracking/` (without any `phase-*` folders)
   - `docs/pm/`
2. **Merge** `CLAUDE.md` and `AGENTS.md`: paste the kit's CeraNova PM block (between the `pm-kit:start` and `pm-kit:end` markers) into yours (top or bottom). Do the same for `GEMINI.md` if you use Gemini CLI.
3. **Session hooks:** run `./kanban agents --add claude` (plus `codex`, `gemini`, `cursor`, `opencode` as you use them). It merges the entries next to your existing hooks.
4. Add `tracking/.state/` to `.gitignore`.
5. Run `./kanban install-hooks`, or chain the hooks (below).
6. On the next prompt, an agent that reads `CLAUDE.md`/`AGENTS.md` runs **pm-bootstrap**. Or run `./kanban init --project "Name"` yourself.

## Projects that already manage git hooks

| Hook manager | What to do |
|---|---|
| **`.git/hooks/*` scripts** | Nothing. CeraNova PM's shims run them first and stop if they fail |
| **husky** (`core.hooksPath=.husky`) | Add `python3 tools/kanban/kanban.py git-hook pre-commit "$@"` to `.husky/pre-commit`, and the same for `pre-push`, `post-merge`, `post-checkout` |
| **pre-commit framework** | Add a local hook running `python3 tools/kanban/kanban.py git-hook pre-commit`; for `pre-push` add `stages: [pre-push]` with `git-hook pre-push` |
| **lefthook / others** | Call the same `git-hook <name>` command from the matching hook |

## Agent session hooks: what to expect

The same three behaviours (resume brief at session start, board rebuild after edits, one doc-sync prompt per completed item at end of turn) are wired into each agent's own hook system. All of them call `python3 tools/kanban/kanban.py hook <event> --agent <name>`, which formats the reply the way that agent expects.

| Agent | Config | Notes |
|---|---|---|
| Claude Code | `.claude/settings.json` | May ask you to trust the project's hooks once. Runs whatever model Claude Code uses, cloud or local |
| Codex | `.codex/hooks.json` | Project hooks load when the project is trusted; review them with `/hooks` |
| Gemini CLI | `.gemini/settings.json` | Project hooks need approval the first time (`/hooks`) |
| Cursor | `.cursor/hooks.json` | `sessionStart` context injection has been unreliable in some Cursor versions; `AGENTS.md` still tells the agent to run `./kanban resume` |
| OpenCode | `.opencode/plugins/ceranova-pm.js` | A small plugin (Bun) that calls the same command |

`./kanban agents` shows which are installed. Any other agent is covered by `AGENTS.md` (run `./kanban resume` first) and the git hooks.

## Removing CeraNova PM

1. Delete:
   - `tools/kanban/`, `kanban`
   - `.claude/skills/pm-*`, `.agents/skills/pm-*`
   - `.opencode/plugins/ceranova-pm.js` and the kanban entries in `.codex/hooks.json`, `.gemini/settings.json`, `.cursor/hooks.json`
   - `tracking/`, `docs/pm/`
   - `KANBAN.md`, `kanban.html`
2. Remove the `pm-kit:start` … `pm-kit:end` blocks and the kanban hook entries.
3. Run `git config --unset core.hooksPath`.
