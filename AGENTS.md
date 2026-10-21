# AGENTS.md: how any coding agent works in this repo

This applies to every CLI agent: Claude Code (cloud or local), Codex, Gemini CLI, Cursor and similar. `CLAUDE.md` imports this file.

**MasterTrader** is a private, single-user, self-hosted AI trading platform.
- Start with [README.md](README.md) and [SPEC.md](SPEC.md); the phased plan is in [docs/roadmap/](docs/roadmap/README.md).
- **All work is tracked on the kanban** in [`tracking/`](tracking/README.md) and rolled up into [`KANBAN.md`](KANBAN.md) / `kanban.html`.

## 1. Session protocol (do this every time)

**1. Sync and resume:**
- `git pull` (or fetch your branch), then run `./kanban resume`.
- The SessionStart hook does this automatically in Claude Code.
- If anything is `in_progress`, **resume it first**: read its `checkpoint` and the last lines of its `## Progress log`, then check out its branch.

**2. Pick work:**
- `./kanban next [--phase N]` lists ready items, most important first.
- Items with `owner: user` are the human's. **Never do them for the user**: no creating accounts, no handling keys or money, no approvals. You may prepare instructions or code that supports them.

**3. Claim:**
- `./kanban start <ID> [--git]` sets `in_progress` and `claimed_by`, logs it, and optionally switches to the item's branch.
- If your session requires a fixed branch (e.g. a cloud session's designated branch), work there and record that branch in the item.

**4. Work the item file as the spec.**
- Follow its *Requirements*, *ToDo*, *Verification*, *Exceptions* and *Cardinal rules*.
- Tick ToDo boxes as you go (`./kanban tick <ID> <n|text>`, or edit the file).

**5. Checkpoint often:** `./kanban checkpoint <ID> "where I am, what's next"`.
- Do this after each meaningful step and **always before you stop**.
- Commit + push the item file with your code, so another machine (or you after a crash) can continue.

**6. Verify:** run the item's tests, scenarios and stress checks. Record what you ran and the result in the progress log.

**7. Bugs found along the way:**
- `./kanban new --phase N --kind bug --severity S1|S2|S3|S4 --found-in <ID> --title "…"`, then fill in reproduce / expected / actual.
- Don't silently fix unrelated things.

**8. Finish:**
- `./kanban review <ID> --pr <url>` when a PR is open.
- After merge (or when verified on the designated branch): `./kanban done <ID> --evidence "commands run + results"`.
- `done` refuses if any ToDo or acceptance box is unticked or there's no evidence.

**9. Doc sync.** Completing an item marks its `doc_sync` docs as pending (`tracking/DOC_SYNC.md`).
- Update those docs so they match what was built: spec (`docs/03`), architecture (`docs/02`), roadmap phase doc (**tick the matching roadmap ToDo**), UI docs, `SPEC.md`.
- Then run `./kanban docsync <ID> --done`.
- In Claude Code the Stop hook reminds you once per completed item.

**10. End of session:**
- `./kanban session handoff --note "…"`, then commit and push, so the next session (cloud or local) picks up cleanly.

## 2. Phase completion

**A phase completes automatically** when:
- all its tasks are `done`/`cancelled`;
- no S1/S2 bug is open;
- every `## Exit criteria` box in `tracking/phase-N/PHASE.md` is ticked.

Tick exit criteria only with evidence: link the run, log or commit in the progress log of the phase's exit-demo item.

On completion `PHASE.md` becomes `status: done` with `doc_sync_status: pending`. Then:
1. Update `docs/roadmap/README.md` and `docs/04-plan-of-action.md` to mark the phase done.
2. Run `./kanban docsync P<N> --done`.

The next phase opens by itself (its `opens_after`).

## 3. Never edit generated files

These are rebuilt by `./kanban build`, the hooks and CI:
- `KANBAN.md`, `kanban.html`;
- `tracking/phase-N/BOARD.md`, `tracking/DOC_SYNC.md`;
- blocks between `<!-- kanban:… -->` markers in `docs/roadmap/README.md`.

Edit the item files, `PHASE.md` or the roadmap phase docs instead. **Never delete an item:** cancel it with `./kanban cancel <ID> --reason …`.

## 4. Cardinal rules (apply to all work)

- **Secrets:** never commit secrets or paste them into chats, issues or logs. Secrets live in the sops/age file ([07 §2](docs/07-security-notes.md#2-secrets)).
- **No bypasses:** every order goes through the risk manager (M11) via `mt_api`; research reads data only through `pit(as_of)`.
- **WORM:** audit/journal records are write-once ([15 §2](docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)). Never UPDATE or DELETE them; corrections are new rows.
- **Data terms:**
  - free data only;
  - no scraping against terms, no self-bots or user tokens, no sybil or fake engagement;
  - **no Telegram text in any model, RAG index or training set** ([12 §4–5](docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- **Money safety:**
  - keys are trade-only, IP-locked, withdrawals disabled;
  - no live money before the Phase 7 gates;
  - loosening risk, autonomous mode and mandates are C3;
  - protective exits never wait for approval.
- **Tests:** never skip, weaken or delete a test to get green; risk, `pit`, WORM and tax golden tests are mandatory.
- **Supply chain:** pin images by digest; no telemetry or referral IDs in vendored code; review every third-party bump.

## 5. Git conventions

- **Branches:** `p<N>/<ID>-<slug>`, one item per branch and PR. PR title `<ID>: <title>`.
- **Commits:** mention the item ID; include the updated item file with the code.
- **Don't push to `main` directly.** Session-specific branch instructions override this.
- **Hooks for non-Claude agents and humans:** `./kanban install-hooks`.
  - **pre-commit:** validate + rebuild boards.
  - **post-merge / post-checkout:** print the resume brief.
- **CI** (`.github/workflows/kanban.yml`) validates items, runs the kanban tool tests and checks the generated boards are current.

## 6. Commands

```
./kanban resume | next [--phase N] | list [--phase N --status S --type T] | show <ID>
./kanban start <ID> [--git] | tick <ID> <n|text> | checkpoint <ID> "note"
./kanban review <ID> --pr URL | done <ID> --evidence "…" | block <ID> --reason … | unblock <ID>
./kanban new --phase N --title "…" [--kind task|bug|gap|chore] [--type BUILD] [--severity S2]
./kanban docsync <ID|P<N>> --done | validate [--phase N] | build | open | serve
./kanban session handoff --note "…" | pause [--off] | install-hooks
```
