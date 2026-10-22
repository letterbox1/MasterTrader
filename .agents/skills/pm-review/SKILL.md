---
name: pm-review
description: Independently verify a kanban item before it is marked done - re-run its Verification steps, check every Acceptance criterion and the evidence against the actual code or content, look for regressions and spec drift, then record a pass or fail verdict with findings. Use when an item is in review (PR open), before `./kanban done`, when the brief says items wait for review, or for "review P2-T014", "check this task is really done".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.2"
---

# pm-review

A review is only worth something if it doesn't trust the builder. Ideally run it as a **separate agent or session** from the one that built the item (with **pm-delegate**, give it this skill and the item ID only).

## 1. Load the item

`./kanban show <ID>`. Note its Requirements, ToDo, Verification, Acceptance criteria, Exceptions, Cardinal rules and `doc_sync` list. Find the change: its branch or PR (`branch`, `pr` fields) and the commits mentioning the ID (`git log --oneline --grep <ID>`).

## 2. Re-run, don't re-read

- Run every command under **Verification** yourself: tests, scenarios, stress/failure checks. Use the item's preflight (`./kanban preflight <ID>`) to confirm you have what they need.
- If a check can't run here (needs hardware, a paid service, the human), say so explicitly; don't count it as passed.
- Compare what you got with the evidence in the progress log. Different results are a finding.

## 3. Check the substance

For each **Acceptance criterion**, point at the code, content or output that satisfies it. Then look for:
- **Spec drift:** the change does something the spec, roadmap or decisions register doesn't say (or contradicts it);
- **Regressions:** related tests or flows that now fail; run the wider suite if it's affordable;
- **Exceptions & edge cases** listed in the item that aren't handled or tested;
- **Cardinal rules** broken (secrets committed, tests weakened or skipped, guard rails bypassed);
- **Config:** values that should come from the configuration doc but are hard-coded;
- **Doc sync:** docs listed in `doc_sync` that will need updating (that happens after `done`; note anything already wrong).

## 4. Verdict

- **Pass:** `./kanban reviewed <ID> --pass --note "ran <commands>: <results>; checked <criteria>"`. The builder (or you, if asked) then runs `./kanban done <ID> --evidence "…"`.
- **Fail:** `./kanban reviewed <ID> --fail --note "<the findings, most serious first>"`. The item goes back to `in_progress` with the findings as its checkpoint.
  - Defects outside the item's scope become bugs (**pm-triage**): `./kanban new --kind bug --found-in <ID> …`.
  - A spec problem becomes a gap and, if S1/S2, goes to **pm-reconcile**.

`require_review: true` in `tracking/kanban.config.json` makes a passing review a condition of `done` for tasks.

## Don't

- Don't fix the code during a review; report it. A reviewer who fixes things is reviewing their own work.
- Don't pass on "looks fine": every pass names what was run and what it showed.
- Don't fail for style preferences the project hasn't adopted; mention them as optional notes.
