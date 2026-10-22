# Customising CeraNova PM

Everything is optional. The defaults suit a software project.

## `tracking/kanban.config.json`

```json
{
  "project": "Acme Game",
  "roadmap_dir": "docs/roadmap",
  "roadmap_index": "docs/roadmap/README.md",
  "types": ["USER", "BUILD", "OPS", "VERIFY", "RUN", "DOC", "RESEARCH"],
  "project_type": "software",
  "sizes": {"XS": 1, "S": 2, "M": 3, "L": 5, "XL": 8},
  "required_headings": ["## Goal / expected outcome", "## Context & references", "## Requirements", "## ToDo",
                        "## Verification", "## Acceptance criteria", "## Exceptions & edge cases",
                        "## Cardinal rules (do NOT)", "## Doc sync on completion", "## Branch & PR", "## Progress log"],
  "stale_days": 7,
  "brand": {"logo": "brand/logo.svg", "attribution": true, "fonts": true},
  "requires_defaults": {"*": {"tools": ["git"]}, "BUILD": {"tools": ["node", "pnpm"]}, "OPS": {"env": ["CLOUD_API_TOKEN"]}},
  "env_files": [".env", ".env.local"],
  "require_review": false,
  "phase_gating": "dependencies",
  "branch_per_task": true
}
```

| Key | Effect |
|---|---|
| `project` | Name on `KANBAN.md`, `kanban.html`, resume briefs |
| `roadmap_dir` / `roadmap_index` | Where roadmap phase docs live and which file gets the auto-generated status blocks |
| `types` | Allowed task types (validated). Keep `USER` for human-only work |
| `sizes` | Size labels and their progress weights |
| `required_headings` | Headings every item must have (validated); match your templates |
| `stale_days` | When an in-progress item is flagged stale |
| `project_type` | `greenfield`, `software`, `data-ml`, `media-video`, `media-audio`, `game`, `docs`, `research`, `design` or `mixed`. Set by `init` from `./kanban detect`; picks the research agenda (`skills/pm-research/references/research-agendas.md`) |
| `brand.logo` | Your project logo next to the project name on the board (SVG/PNG/JPG/WebP ≤ 300 KB). Auto-detected from `brand/logo.svg`, `logo.svg`, `assets/logo.*`, `public/logo.*`, `.github/logo.*` and similar if omitted; `false` hides it |
| `brand.attribution` | The "Powered by CeraNova PM" footer credit and the `KANBAN.md` signature. `false` hides both |
| `brand.fonts` | Embed the board fonts (Bebas Neue, DM Sans, Space Mono; ~70 KB) so the board looks the same offline. `false` uses system fonts |
| `brand.accent` / `brand.accent2` | Optional overrides of the board's red and gold accents |
| `requires_defaults` | Tools, MCP servers, env var names and services every task of a type needs (`"*"` = all types), merged with each item's own `tools`/`mcp`/`env`/`services`. Checked by `./kanban preflight` and `./kanban start` |
| `env_files` | Files whose variable **names** count as available to the preflight (values are never read out) |
| `require_review` | `true`: `./kanban done` refuses a task without a passing `./kanban reviewed` (the **pm-review** skill) |
| `phase_gating` | `"phases"` (default): a phase's tasks wait for its `opens_after` phases. `"dependencies"`: tasks become ready when their own `depends_on` are done, so independent work in later phases runs in parallel; phases with `hard_gate: true` in `PHASE.md` (e.g. go-live) still wait |
| `branch_per_task` | `true`: `./kanban start` switches to (or creates) the item's branch without `--git`. Leave `false` where a session must stay on one designated branch |

## Project-type presets

| Project | `types` suggestion | Notes |
|---|---|---|
| Software / services | default | Verification = unit/integration/e2e tests, load and failure injection |
| Data / ML | add `DATA`, `EVAL` | `RUN` for training/soak windows; VERIFY = evaluation reports with thresholds from the configuration doc |
| Film / video / audio | `USER, ASSET, EDIT, REVIEW, RENDER, DOC` | Branches per shot/sequence; Git LFS for media; VERIFY = review/approval checklists, render specs; exit demo = cut review |
| Games | add `ART`, `DESIGN`, `PLAYTEST` | RUN = playtest windows; VERIFY = performance budgets per platform |
| Docs / books / courses | `USER, WRITE, EDIT, REVIEW, PUBLISH, DOC` | "Tests" = link checks, style lint, reviewer sign-off |
| Research | `USER, READ, EXPERIMENT, ANALYSE, WRITE, VERIFY` | Experiments carry hypotheses and pre-registered success criteria |

**Changing types or headings:** update `tracking/templates/task.md` to match, then run `./kanban validate`.

## Phases

- **Add phases:** `./kanban init --phases "A,B,C" --roadmap` (first time) or `./kanban phase-add --title "…" --roadmap [--opens-after 2,3] [--number 7]`.
- **Phase numbers** can go past 9 (`P12-T004`).
- **Order** is controlled by `opens_after` in each `PHASE.md`. Set `force_open: true` to work a phase early.

## Item templates

Edit `tracking/templates/{task,bug,phase}.md` freely: add sections, change checklists, add project cardinal rules. The validator only enforces `required_headings` and the front-matter schema (`tracking/SCHEMA.md`).

## Project rules for agents

Add project-specific cardinal rules **below** the CeraNova PM block (`pm-kit:start` … `pm-kit:end`) in `AGENTS.md`. Examples:
- "never bypass the payment service";
- "all audio at 48 kHz/24-bit";
- "no client names in commits".

Planning agents copy the relevant ones into every task.

## Board branding

The board is a **CeraNova PM** product surface; your project is named on it:
- **Header:** the CeraNova mark and "CeraNova PM", then your project's name and logo (auto-detected or `brand.logo`).
- **Theme:** the CeraNova design system: tonal dark surfaces (or the warm `#F7F5F2` light mode), red and gold accents, Bebas Neue for numbers, DM Sans for text, Space Mono for labels, an 80px background grid and soft glows. Follows the system light/dark setting; the Theme button overrides it.
- **Status colours** (done / review / in progress / blocked) stay functional, so progress reads the same in every project.
- **Offline:** fonts and marks are embedded; the board loads nothing from the internet.
- **Scope:** this styles the kanban only. Your product's own design system, UI and branding are project work (**pm-scope**, your design docs) and follow your brand, not CeraNova's.

## Research by project type

`./kanban detect` reads the repo (manifests, code, media/session files, engine projects, notebooks/models, LaTeX, design files) and reports a type. **pm-research** then uses that type's agenda:
- **greenfield:** prior art, build-vs-buy, stack, feasibility spikes, cost;
- **media:** delivery specs, toolchain, rights and clearances, platforms, accessibility;
- **game:** engine, certification, performance budgets, monetisation rules;
- **data-ml:** datasets and licences, models, evaluation, compute;
- **docs:** audience, publishing formats, style and accessibility;
- **research:** literature, methods, ethics, venues;
- **design:** users, patterns, design systems, licensing.

Pin the type with `project_type` if detection guesses wrong.
