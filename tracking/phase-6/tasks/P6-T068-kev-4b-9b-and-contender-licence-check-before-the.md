---
id: P6-T068
kind: task
title: Kev-4B/9B and contender licence check before the bake-off
phase: 6
type: VERIFY
status: ready
priority: high
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.12]
roadmap_todos: [T6.72]
modules: [M21]
dashboards: [D10]
tools: [git, curl]
mcp: []
env: []
services: [huggingface-hub]
branch: p6/P6-T068-kev-4b-9b-and-contender-licence-check-before-the
pr: ""
doc_sync: [docs/research/decision-models-system-one.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T068 · Kev-4B/9B and contender licence check before the bake-off

## Goal / expected outcome

The unverified (U) fact behind R6.12 is settled by an agent before any weights are pulled: does a **public, licence-compatible release of Kev-4B/9B** exist? The answer, with its source, licence and weights location, is recorded; Kev is dropped from the bake-off if not. The same check confirms the self-hosting licences of Laya, Clef-flash weights and SemIf, so P6-T027 builds only cleared contenders.

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.72
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B003: Kev only if a public, licence-compatible release exists; otherwise dropped (U)) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) ((U) facts are verified by agents in research tasks before the build that relies on them)
- Spec: [10 §4.1](../../../docs/10-memory-rag-and-models.md#41-what-decision-models-are-and-the-candidates) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) bake-off · [research: decision models](../../../docs/research/decision-models-system-one.md) · [07 §7](../../../docs/07-security-notes.md#7-supply-chain)
- Gap owned: P6-B003
- Unblocks: P6-T027 (contender containers), P6-T029 (bake-off harness)

## Requirements

- For Kev-4B/9B: publisher, repository/weights URL, licence text, size/context length, serving method; or a dated "no public release found" with the places searched.
- "Licence-compatible" = free to download and self-host for private, non-distributed use with no paid tier, no telemetry and no use restriction that conflicts with trading (03 §1).
- Same record for Laya (`NandhaKishorM/laya`), Clef-flash weights, SemIf and the Qwen3-0.6B/1.7B backbones (pinned HF revisions).
- Result written as a table in the progress log and proposed for the 10 §4.1 candidate table and the research note (doc sync).
- Hosted or paid decision models (Jev, Microsoft-Decision-1) stay excluded.

## ToDo

- [ ] Search Hugging Face, GitHub and the publisher's pages for Kev-4B/9B; record URLs and dates checked.
- [ ] Read each licence; classify allowed / not allowed with the clause quoted.
- [ ] Record SHA/revision for every allowed contender's weights (no download yet beyond metadata).
- [ ] Write the decision table in the progress log; comment the outcome on P6-B003 and close it if Kev is decided either way.
- [ ] Update the docs listed under Doc sync.

## Verification

### Tests
- n/a: research check; P6-T027 smoke-tests the cleared contenders.

### Scenarios
- Given no public Kev release exists, then the table says "dropped (U resolved: no release, checked <date>)" and P6-T027 omits Kev.
- Given a Kev release exists under a non-commercial or restricted licence, then it is dropped with the clause quoted.
- Given a release under Apache-2.0/MIT, then its repo, revision and serving notes are recorded for P6-T027.

### Stress / failure injection
- n/a: desk research.

## Acceptance criteria

- [ ] Kev decision recorded with sources and date.
- [ ] Licence status recorded for every bake-off contender and backbone.
- [ ] P6-B003 updated with the outcome.

## Exceptions & edge cases

- A release appears after the bake-off: it can join a later bake-off run through the same check; the current report notes its absence.
- Ambiguous licence: treat as not allowed and record why.

## Cardinal rules (do NOT)

- Do NOT download or run weights whose licence isn't cleared here.
- Do NOT use hosted/paid model endpoints as a substitute.
- Do NOT add paid data/APIs or scraping that breaks terms.
- Do NOT commit secrets; do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/research/decision-models-system-one.md`: Kev source/licence or exclusion; contender licence table.
- `docs/10-memory-rag-and-models.md` §4.1: Kev row (or "dropped") in the candidate table.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.72 (and note this task ID).

## Branch & PR

- Branch: `p6/P6-T068-kev-4b-9b-and-contender-licence-check-before-the`
- PR title: `P6-T068: Kev-4B/9B and contender licence check before the bake-off`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T068` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T6.72 (Kev (U) check moved from the USER item P6-T002 to an agent check per 17 §E; owns P6-B003)
