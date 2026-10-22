# {{PROJECT}} Roadmap

One scoped document per phase. Each has requirements with IDs, ToDos split by **who or what does the work**, deliverables, exit criteria and risks. Execution is tracked per phase on kanbans in [`tracking/`](../../tracking/README.md).

<!-- pm:fill Table: Phase | Document | Weeks | Indicative dates. One row per docs/roadmap/phase-N-*.md. -->

**Live status** (auto-updated by `./kanban build`; open [`kanban.html`](../../kanban.html) or [`KANBAN.md`](../../KANBAN.md) for the boards):

<!-- kanban:phase-status:start -->
<!-- kanban:phase-status:end -->

## 1. How to read the phase documents

**IDs:**
- `R<phase>.<nn>`: a requirement. `R<phase>.N<n>` is non-functional.
- `T<phase>.<nn>`: a ToDo. It points (`→`) at the requirement(s) it satisfies and the doc section it comes from.

**ToDo types:**

| Tag | Who / what |
|---|---|
| `USER` | **The human only:** accounts, credentials, money, hardware, decisions, approvals, reviews, external advice |
| `BUILD` | Making the thing: code, content, assets, configuration-as-code |
| `OPS` | Infrastructure, environments, pipelines, schedules |
| `VERIFY` | Tests, checks, drills, benchmarks, reviews that prove a requirement |
| `RUN` | Elapsed-time work: soaks, trials, observation windows |
| `DOC` | Documentation, runbooks |
| `RESEARCH` | Investigations with a written report as the deliverable (`skills/pm-research`) |

## 2. Work mix per phase

<!-- kanban:roadmap-counts:start -->
<!-- kanban:roadmap-counts:end -->

## 3. Timeline & dependencies

<!-- pm:fill Mermaid gantt + flowchart of phase dependencies; critical path; what runs in parallel. -->

## 4. Fixed external dates

<!-- pm:fill Deadlines outside your control (contracts, releases, regulation, events). | Date | Event | Affects | Source | -->

## 5. Cross-phase tracks

<!-- pm:fill Security / compliance / UI / testing / docs tracks across phases. -->

## 6. `USER` action register (all phases)

<!-- kanban:user-register:start -->
<!-- kanban:user-register:end -->

## 7. Traceability

<!-- pm:fill Spec non-negotiables → requirement IDs; goal capabilities → phases; modules/components → phases; docs → phases. -->

## 8. Definition of done (every phase)

1. All requirements verified and the exit demo runs.
2. All checks green.
3. Every user action is recorded where the project keeps its audit trail.
4. Docs and runbooks updated for what changed.
5. The phase's `USER` items are done or deferred with a reason.
