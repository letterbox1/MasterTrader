---
name: pm-execute
description: Execute kanban tasks end to end - resume in-flight work, pick the next ready item, claim it, implement per the task file, tick ToDos, checkpoint, run the tests/scenarios/stress checks, file bugs, open a PR, mark done with evidence, and do the doc sync. Use for "work on the next task", "execute phase N", "continue", or after a crash/session move.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-execute

Follow `tracking/briefs/EXECUTION_BRIEF.md`. The loop:

1. **Resume:** `git pull` and `./kanban resume`; the SessionStart hook prints this too. Anything `in_progress` comes first:
   - read its `checkpoint` and the last progress-log lines;
   - `git switch` to its branch;
   - check what's already committed.

2. **Pick:** `./kanban next [--phase N] --owner agent`. Never take `owner: user` items; for those, prepare instructions or supporting work and tell the human.

3. **Claim:** `./kanban start <ID> --git` (or stay on the session's designated branch and record it).
   - `start` runs the **preflight**: the tools, MCP servers, env var names and services listed in the item (plus `requires_defaults`). It refuses while a tool or env var is missing on this machine.
   - Missing something? Install it if that's routine and allowed (a dev dependency, a CLI). If it needs the human (an account, a key, money, an approval): `./kanban block <ID> --reason "needs …"`, raise a USER task with exact instructions, and pick another item.
   - An MCP server marked `check` may be a user-level or hosted connector: confirm by using it, not by guessing.

4. **Do the work.**
   - Treat the item file as the spec: Requirements, ToDo, Exceptions, Cardinal rules.
   - Tick boxes as you go (`./kanban tick <ID> <n|text>`).
   - `./kanban checkpoint <ID> "done X; next Y"` after each meaningful step.
   - Commit with the ID in the message; push.

   - **Skills on the fly:** use the skills you already have (they're matched by description). Write a new skill only when the task repeats a non-obvious procedure you'll need again (in this task or the phase), such as a release recipe or a data migration routine:
     - put it in `.agents/skills/<project>-<name>/SKILL.md` (open Agent Skills format: `name` = folder name, a `description` that says when to use it), and run `./kanban doctor --fix` to mirror it into `.claude/skills/`;
     - keep it short, procedural and project-specific; never put secrets in it;
     - note it in the progress log. Most tasks need none: if the item is scoped well, just do the work.

5. **Verify:** run everything under *Verification* (tests, scenarios, stress/failure injection). Paste the commands and results into the progress log.

6. **Bugs:** `./kanban new --phase N --kind bug --severity S? --found-in <ID> --title …`, with reproduce / expected / actual. Fix them only if in scope.

7. **Finish.**
   - With a PR: `./kanban review <ID> --pr <url>`. Then get an independent check with **pm-review** (ideally a separate agent); `require_review: true` in the config makes it mandatory.
   - When merged or verified: `./kanban done <ID> --evidence "<commands + results>"`. `done` refuses on unticked boxes or missing evidence; fix the cause, don't force it.

8. **Doc sync:** the Stop hook will ask. Update the docs in the item's `doc_sync` list and **tick the roadmap ToDo** it satisfies, then `./kanban docsync <ID> --done`. See **pm-doc-sync**.

9. **Repeat**, or hand off: `./kanban session handoff --note "…"`, commit, push.

## Don't

- Don't skip, weaken or delete tests to get green.
- Don't silently fix unrelated things; file them.
- Don't end a session with uncheckpointed in-progress work.
