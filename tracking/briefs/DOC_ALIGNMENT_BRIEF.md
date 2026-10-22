# Doc Alignment Brief (for doc agents)

Use this brief to bring a set of docs in line with the decisions taken on 2026-10-21.

## Sources of truth (read fully first)

- [`docs/16-configuration-and-safety-model.md`](../docs/16-configuration-and-safety-model.md): configuration layers, default values, failure safety, valuation and live inputs.
- [`docs/17-decisions-register.md`](../docs/17-decisions-register.md): the decision for every planning gap.
- [`docs/15-bots-hitl-and-worm-audit.md`](../docs/15-bots-hitl-and-worm-audit.md): bots, HITL/autonomous, WORM.
- The gap files themselves: `tracking/phase-*/bugs/*.md`. `grep -l "<your doc filename>" tracking/phase-*/bugs/*.md` finds the ones that concern your docs. Read their *Requirements* sections for exact locations.

## Rules

1. **Edit only the files you were assigned.** Nothing in `tracking/`, nothing in other docs.
2. **Don't rename or remove existing headings.** Other docs link to them by anchor. Add new headings or sub-sections instead.
3. **Apply every decision in 16/17 that touches your files.**
   - Replace stale numbers with the decided default and a link to the relevant 16 section.
   - Unify names: modes `paper`/`hitl`/`autonomous`, canonical audit table names, `ops.wallets`, 25% venue cap, DSR ≥ 0.95, two-stage drawdowns, three-layer dead-man, MCP rules.
   - Remove contradictions.
4. **Configurable values must read as defaults, not hard rules:** "default X, configurable (16 §n)".
5. Keep the existing style: concise, plain English, tables where they already are, `(U)` for unverified facts.
6. Where 17 says "adopt the suggested fix", use the fix in that gap file.
7. **When done:** check every relative link you touched resolves, then report (≤ 250 words):
   - which gap IDs you resolved, with file + section;
   - which gap IDs that mention your files you did **not** resolve, and why;
   - any new inconsistency you noticed in docs you don't own.
