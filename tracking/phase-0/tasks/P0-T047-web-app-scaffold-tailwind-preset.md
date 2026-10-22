---
id: P0-T047
kind: task
title: Scaffold the web app with the DESIGN.md v2 Tailwind preset
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.11]
roadmap_todos: [T0.26]
modules: [M15]
dashboards: []
tools: [git, node>=20, pnpm]
mcp: []
env: []
services: []
branch: p0/P0-T047-web-app-scaffold-tailwind-preset
pr: ""
doc_sync: [DESIGN.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T047 · Scaffold the web app with the DESIGN.md v2 Tailwind preset

## Goal / expected outcome

`apps/web` is a React 18 + TypeScript + Vite PWA with TanStack Router/Query, Zustand, Radix primitives and a **locally built** Tailwind configured from the DESIGN.md v2 preset (tokens, the ten breakpoints, raw orientation/height queries, container queries, forms), self-hosted fonts, and a CI job running typecheck, lint, Vitest and build; Caddy serves the build.

## Context & references

- [Roadmap P0 R0.11](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.26](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §10 frontend](../../../docs/02-v1-architecture.md#10-frontend-architecture)
- [DESIGN §6.3 Tailwind preset](../../../DESIGN.md#63-tailwind-configuration-use-in-every-implementation-and-mock-up)
- [DESIGN §6](../../../DESIGN.md#6-responsive-system-1920px--240px-portrait--landscape)
- [DESIGN §2 colour](../../../DESIGN.md#2-colour)
- [mobile & Telegram](../../../docs/ui/mobile-and-telegram.md#1-pwa) (PWA)
- `tablet-landscape` is now in the DESIGN §6.3 config ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B013, closed).
- Depends on: P0-T014

## Requirements

- Node LTS pinned (`.nvmrc`), pnpm with lockfile; `vite`, `react@18`, `@tanstack/react-router`, `@tanstack/react-query`, `zustand`, `@radix-ui/*`, `vite-plugin-pwa`, `vitest`, `@testing-library/react`, `eslint`, `typescript --strict`.
- Tailwind **3.4.x** (matches the JS config in DESIGN §6.3; v4 migration later) with `tailwind.preset.cjs` generated from DESIGN.md front matter (colours, typography, radii, spacing) and `screens` exactly: xxs 240, xs 320, sm 375, ph 480, md 768, lg 1024, xl 1280, 2xl 1440, 3xl 1920, 4xl 2560, plus raw `landscape-short`, `tablet-portrait`, `tablet-landscape`, `very-short`, `touch`; `darkMode: ['selector', '[data-theme="dark"]']`; plugins container-queries + forms.
- A test asserts preset values equal the DESIGN.md front matter (parse YAML) so drift fails CI.
- Fonts: Space Grotesk, JetBrains Mono, Material Symbols Outlined self-hosted (woff2 in `public/fonts`, OFL/Apache licences recorded); **no CDN** (no `cdn.tailwindcss.com`, no Google Fonts URLs); CSP-compatible.
- Global CSS: `min-h-dvh` shell, `tabular-nums` utility, reduced-motion overrides, focus ring 2px Cobalt + 2px offset, default theme dark.
- PWA: manifest (name, icons from `brand/app-icon.svg`), service worker caches the shell only — never API responses.
- `openapi-typescript` generation from `packages/mt_api/openapi.json` into `src/lib/api/types.ts` (CI fails if stale).

## ToDo

- [ ] Create the Vite app, routes folder, `src/components`, `src/tiles`, `src/lib/api`, `src/lib/ws`.
- [ ] Write the preset generator script + drift test.
- [ ] Add fonts and licences; global CSS.
- [ ] Configure PWA plugin.
- [ ] Fill the CI `web` job (typecheck, eslint, vitest, build, OpenAPI type freshness).
- [ ] Caddy route serving `apps/web/dist`.

## Verification

### Tests
- Unit: preset drift test; a component renders with tokens.
- Build: `pnpm build` produces < 300 kB gzipped initial JS (budget logged).
- Static check: grep build output for `cdn.tailwindcss.com`, `fonts.googleapis.com` → none.

### Scenarios
- Given the device is offline, when the PWA opens, then the shell renders with a 'Disconnected' banner instead of a blank page.

### Stress / failure injection
- n/a: scaffold; performance budget checked in build.

## Acceptance criteria

- [ ] App builds and serves via Caddy
- [ ] Preset matches DESIGN.md (drift test)
- [ ] No CDN references; fonts self-hosted with licences
- [ ] CI `web` job green
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Tailwind v4 would change config format; stay on 3.4.x until a deliberate migration.

## Cardinal rules (do NOT)

- Do NOT use the Tailwind CDN script or external font CDNs.
- Do NOT cache API data in the service worker.
- Do NOT add analytics or telemetry SDKs.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `DESIGN.md` §6.3: no change expected (the preset is generated from it); `docs/02-v1-architecture.md` §10: note Tailwind 3.4 and pnpm.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T047-web-app-scaffold-tailwind-preset`
- PR title: `P0-T047: Scaffold the web app with the DESIGN.md v2 Tailwind preset`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (P0-B013 closed (tablet-landscape in DESIGN §6.3); run fields added)
