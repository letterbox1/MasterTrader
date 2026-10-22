# CeraNova PM brand assets (the board only)

These style the **kanban board** (`kanban.html`, and the small signature in `KANBAN.md`). They don't touch your project's own design: design-system, UI and branding work for your product lives in your docs and follows your brand.

| File | Use |
|---|---|
| `ceranova-mark.png` / `ceranova-mark-128.png` | The CeraNova mark: board header, favicon, footer credit, `KANBAN.md` signature |
| `ceranova-logo.png` | Full CeraNova logo (README) |
| `fonts/*.woff2` | Bebas Neue, DM Sans, Space Mono (SIL Open Font License 1.1, see `fonts/OFL-*.txt`), embedded in the board so it works offline |

**Your project on the board:** its name (`project` in `tracking/kanban.config.json`) and its logo, auto-detected from `brand/logo.svg`, `logo.svg`, `assets/logo.png` and similar, or set with `brand.logo` (`false` hides it).

**Options** (`brand` in the config): `attribution: false` hides the footer credit and the `KANBAN.md` signature; `fonts: false` skips the embedded fonts (smaller file, system fonts); `accent` / `accent2` override the red and gold accents.

The CeraNova name and mark are trademarks of CeraNova (https://ceranovaai.com); the code is under the repository licence.
