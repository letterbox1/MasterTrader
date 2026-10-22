---
name: pm-triage
description: Turn incoming work into well-formed kanban items and keep the board honest - bug reports and requests from chat, issue trackers, CI failures, review findings and TODOs become deduplicated items with kind, severity, phase, priority and links; stale, blocked and mis-prioritised items get resolved. Use when the human reports a bug or asks for something new, when CI or a review fails, when the brief shows stale or blocked items, or for "triage", "groom the backlog", "file this".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-triage

Triage decides **what** an incoming thing is and **where** it goes. It doesn't fix anything; fixing is **pm-execute**.

## 1. Collect

Take what's in front of you, plus whatever sources you can reach:
- the human's message (a bug, a request, a change of mind);
- failing CI runs, test output, review findings (**pm-review**);
- the project's issue tracker, if a tool for it is available;
- `TODO`/`FIXME` notes added in recent commits (`git log -p --since=… | grep -n "TODO\|FIXME"`).

## 2. De-duplicate

Before creating anything, search: `./kanban list --grep "<2-3 key words>"` (add `--kind bug` or `--phase N` to narrow).
- **Same problem already filed:** add the new evidence to that item's progress log (`./kanban checkpoint <ID> "…"` or edit the log), raise its severity or priority if warranted. Don't file a twin.
- **Related but different:** file it and mention the related ID in *Context & references*.

## 3. Classify

| Decide | Rule |
|---|---|
| **kind** | `bug`: worked as specified, now broken. `gap`: the spec or plan is wrong, missing or contradictory. `task`: new work. `chore`: upkeep with no behaviour change |
| **severity** (bugs/gaps) | S1 data loss, security, money or safety at risk, or nothing works · S2 a core flow broken, no workaround · S3 broken with a workaround · S4 cosmetic |
| **phase** | The phase whose exit criteria it affects. For a defect in finished work, the current open phase |
| **type** | `USER` if only the human can do it (accounts, keys, money, approvals, decisions); otherwise BUILD/OPS/VERIFY/DOC/RESEARCH/… |
| **priority** | critical for S1, high for S2 or a critical-path blocker, otherwise medium/low |
| **found_in** | The item ID or area where it showed up |

## 4. File

`./kanban new --phase N --kind bug|gap|task --severity S? --found-in <ID> --title "…"`, then fill the body:
- **bugs:** reproduce steps, expected, actual, environment, evidence (log lines, commit, screenshot path);
- **gaps:** what's wrong, what's expected, suggested fix, which docs and tasks it touches;
- **tasks:** the full task template (goal, requirements, ToDo, verification, acceptance, tools/mcp/env/services).

Never paste secrets or personal data into items. Reference where they live instead.

## 5. Groom what's already there

- **Stale in progress** (the brief or `./kanban doctor` lists them): read the checkpoint and log. Either resume it (**pm-execute**), or record why it stopped with `./kanban checkpoint`, or release it (`./kanban block <ID> --reason …`, or `reopen` it to `ready`).
- **Blocked:** check each `blocked_reason`. If the blocker is gone, `./kanban unblock <ID>`. If it needs the human, make sure a USER item exists and is linked.
- **Priorities:** S1/S2 bugs and gaps above everything else in their phase; critical-path items above parallel ones.

## 6. Escalate and report

- **S1/S2 gaps** or anything needing a decision → **pm-reconcile** (ask the human with a recommendation).
- Tell the human in a few lines: what was filed (IDs), what was merged into existing items, what needs them.
- Commit: `triage: <n> filed, <m> merged`.
