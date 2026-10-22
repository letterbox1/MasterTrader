---
name: MasterTrader — Autonomous Quant Terminal
version: 2.0
supersedes: ui-examples/stitch-DESIGN.original.md
colors:
  # Ground & surfaces (dark is the default theme)
  ink: '#07090D'               # canvas / background
  graphite: '#11151C'          # level 1 tiles, docks
  graphite-2: '#161B24'        # level 2 sub-panels, inputs
  graphite-3: '#1D232F'        # level 3 modals, flyouts, sheets
  line: '#232A35'              # solid dividers
  border-subtle: 'rgba(238, 242, 246, 0.07)'
  border-medium: 'rgba(238, 242, 246, 0.12)'
  border-strong: 'rgba(238, 242, 246, 0.20)'
  # Text
  paper: '#EEF2F6'             # primary text on dark
  text-secondary: '#B6C0CE'
  text-muted: '#8B95A5'        # minimum for any readable text on ink (≥ 4.5:1)
  text-disabled: '#4F5969'     # disabled / decorative only, never body text
  # Brand & semantic
  mint: '#2BE4A7'              # primary, positive delta, live/running, bids
  mint-on-light: '#0E8F69'
  cobalt: '#3A7BFF'            # secondary, routing, models, info
  cobalt-on-light: '#2A5FE0'
  flare: '#FF6B4A'             # negative delta, asks, risk, errors, kill switch ONLY
  warn: '#F5B83D'              # degraded / elevated (not red, not green)
  # Tints
  mint-tint: 'rgba(43, 228, 167, 0.12)'
  cobalt-tint: 'rgba(58, 123, 255, 0.12)'
  flare-tint: 'rgba(255, 107, 74, 0.15)'
  warn-tint: 'rgba(245, 184, 61, 0.14)'
  # Light theme (data-theme="light")
  light-bg: '#F4F6F9'
  light-surface: '#FFFFFF'
  light-surface-2: '#EEF2F6'
  light-text: '#0E131A'
  light-text-secondary: '#4A5565'
  light-border: '#D5DBE3'
typography:
  display-lg: { fontFamily: Space Grotesk, fontSize: 'clamp(28px, 2.2vw + 16px, 48px)', fontWeight: '700', lineHeight: '1.15', letterSpacing: -0.03em }
  headline-lg: { fontFamily: Space Grotesk, fontSize: 'clamp(22px, 1.2vw + 14px, 32px)', fontWeight: '600', lineHeight: '1.25', letterSpacing: -0.02em }
  headline-md: { fontFamily: Space Grotesk, fontSize: 'clamp(18px, 0.6vw + 14px, 22px)', fontWeight: '600', lineHeight: '1.3', letterSpacing: -0.01em }
  headline-sm: { fontFamily: Space Grotesk, fontSize: 'clamp(16px, 0.3vw + 14px, 18px)', fontWeight: '500', lineHeight: '1.35' }
  body-lg: { fontFamily: Space Grotesk, fontSize: 16px, fontWeight: '400', lineHeight: '1.5' }
  body-md: { fontFamily: Space Grotesk, fontSize: 14px, fontWeight: '400', lineHeight: '1.45' }
  body-sm: { fontFamily: Space Grotesk, fontSize: 12px, fontWeight: '400', lineHeight: '1.35' }
  data-mono-xl: { fontFamily: JetBrains Mono, fontSize: 'clamp(22px, 1.6vw + 12px, 34px)', fontWeight: '600', lineHeight: '1.15', letterSpacing: -0.02em }
  data-mono-lg: { fontFamily: JetBrains Mono, fontSize: 'clamp(16px, 0.5vw + 13px, 20px)', fontWeight: '600', lineHeight: '1.3', letterSpacing: -0.02em }
  data-mono-md: { fontFamily: JetBrains Mono, fontSize: 14px, fontWeight: '500', lineHeight: '1.45' }
  data-mono-sm: { fontFamily: JetBrains Mono, fontSize: 12px, fontWeight: '400', lineHeight: '1.35' }
  label-code: { fontFamily: JetBrains Mono, fontSize: 11px, fontWeight: '500', lineHeight: '1.3', letterSpacing: 0.06em }
  label-caps: { fontFamily: Space Grotesk, fontSize: 11px, fontWeight: '700', lineHeight: '1.3', letterSpacing: 0.08em }
rounded: { xs: 2px, sm: 4px, DEFAULT: 8px, lg: 12px, xl: 16px, full: 9999px }
spacing: { unit: 4px, space-xs: 4px, space-sm: 8px, space-md: 12px, space-lg: 20px, space-xl: 32px, gutter-mobile: 8px, gutter-tablet: 12px, gutter-desktop: 16px, margin-xxs: 8px, margin-mobile: 12px, margin-tablet: 16px, margin-desktop: 24px }
breakpoints: { xxs: 240px, xs: 320px, sm: 375px, ph: 480px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1440px, 3xl: 1920px, 4xl: 2560px }
---

# MasterTrader Design System (v2)

This is the authoritative design spec for every MasterTrader UI surface: the web app, the Telegram mini-views and any future desktop shell.

- **Starting point:** v1 was generated with Stitch ([ui-examples/stitch-DESIGN.original.md](ui-examples/stitch-DESIGN.original.md)).
- **Brand:** the "Signal M" brand ([brand/README.md](brand/README.md)).
- **Reference screens:** [ui-examples/](ui-examples/README.md).

**What changed from v1:**
1. **Tokens reconciled.** v1's frontmatter used generated Material tones (`#0f141a` surfaces) that contradicted its own prose and the brand. v2's tokens match the brand: Ink, Graphite, Mint, Cobalt, Flare.
2. **A full responsive system** from **1920px+ desktops down to 240px** screens (e.g. foldable cover screens), covering portrait and landscape, laptops, tablets and in-between devices (§6).
3. **Accessibility rules:**
   - contrast floor for muted text;
   - a non-colour cue for every up/down signal;
   - reduced motion;
   - touch targets.
4. **Content rules.** Mock data must match the product spec: free sources, risk rules, the MCP scope and tax rules (§10).

---

## 1. Brand & style

The interface is a **sovereign quant cockpit**, not a retail broker app. It should feel calculated, dense and calm, and it leaves out gamification.

**Visual language:** Deep Minimalist Terminal Architecture + Precision Quant Glassmorphism.
- **Background:** ultra-dark canvases.
- **Tiles:** 1px hairline borders, small tonal step-ups between surface levels.
- **Glow:** reserved for **live** states only (active agent, fill, decision node).

**Brand anchor:** the **Signal M** mark (two candlesticks + a price path with one decision node). Charts echo it: decision points render as a circular node centred on the candle.

## 2. Colour

| Role | Dark | Light | Use |
|---|---|---|---|
| Canvas | Ink `#07090D` | `#F4F6F9` | Page background |
| Level 1 | Graphite `#11151C` | `#FFFFFF` | Tiles, sidebar, docks |
| Level 2 | `#161B24` | `#EEF2F6` | Inputs, sub-panels, table headers |
| Level 3 | `#1D232F` | `#FFFFFF` + shadow | Modals, sheets, popovers |
| Primary | Mint `#2BE4A7` | `#0E8F69` (text) / `#12B886` (fills) | Primary action, positive delta, bids, running |
| Secondary | Cobalt `#3A7BFF` | `#2A5FE0` | Routing, models, info, focus ring |
| Danger | Flare `#FF6B4A` | `#D9482A` | Negative delta, asks, risk breach, errors, kill switch. **Never decorative.** |
| Warning | `#F5B83D` | `#A86F00` | Degraded / elevated / pending |
| Text | Paper `#EEF2F6` → `#B6C0CE` → `#8B95A5` | `#0E131A` → `#4A5565` | Primary → secondary → muted |

**Rules:**
- **Contrast:** body text ≥ 4.5:1 and large text (≥ 24px) ≥ 3:1. `#8B95A5` on Ink is the lowest grey allowed for readable text; `#4F5969` is for disabled/decorative only. The v1 screens use `text-[9px]`/`text-[10px]` labels in dim greys that fail this, so fix them when implementing.
- **Up/down never relies on colour alone.** Always pair it with ▲/▼, a +/− sign, or a text label (`BUY`/`SELL`, `PASS`/`VETO`), for colour-blind safety.
- **Mint vs Flare:** these are also separated by lightness, not just hue.
- **Gradient:** Cobalt → Mint (bottom-left → top-right) is reserved for the brand mark and at most one hero element per screen.

## 3. Typography

**Two engines:**
- **Space Grotesk** (human layer): headings, navigation, labels.
- **JetBrains Mono** (machine layer): every price, size, P&L, ticker, timestamp, hash, latency and JSON payload.
- **Material Symbols Outlined** for icons, as in v1.

**Number formatting:**
- All numbers use `font-variant-numeric: tabular-nums` so streaming updates don't jitter.
- Right-align numeric columns.
- Fixed decimal places per instrument (from instrument metadata).

**Type scale:**
- Display and headline sizes are **fluid** (`clamp()` in the frontmatter) between 320px and 1920px viewports.
- Body and data sizes are fixed for density.
- **Minimum rendered size is 11px** at any breakpoint. v1 used 9–10px labels; raise them to 11px.

**Labels:** uppercase + tracked (`0.06–0.08em`), used for micro-labels only, never for sentences.

## 4. Shape & elevation

**Radii:**
- 8px tiles.
- 4px nested controls, chips and inputs.
- 12–16px modals and sheets.
- Full circle for status dots and decision nodes.

**Elevation levels:**
| Level | Surface | Border | Extra |
|---|---|---|---|
| L0 | Ink | — | — |
| L1 | Graphite | `1px border-subtle` | Optional `backdrop-filter: blur(12px)` on translucent docks |
| L2 | `#161B24` | `border-medium` | — |
| L3 | `#1D232F` | `1px rgba(58,123,255,.35)` | Shadow `0 8px 32px -4px rgba(0,0,0,.75)` |

**Glows** (live only):
- Mint node: `0 0 12px rgba(43,228,167,.45)`.
- Flare alert pulse: `0 0 14px rgba(255,107,74,.5)`.
- Remove all glows and pulses under `prefers-reduced-motion`.

## 5. Spacing & density

- **Base unit:** 4px (v1 mixed rem values; normalise to 4px multiples).
- **Density modes** (user setting, persisted per device):

| Mode | Table row | Order-book row | Tile padding | Default on |
|---|---|---|---|---|
| Compact | 28px | 20px | 12px | Desktop ≥ 1440 |
| Comfortable | 36px | 24px | 16px | Laptop / tablet |
| Touch | 44px | 32px | 16px | Any `pointer: coarse` device |

## 6. Responsive system (1920px+ → 240px, portrait & landscape)

### 6.1 Device tiers & breakpoints

These are **mobile-first `min-width` breakpoints**. They replace Tailwind's defaults (Tailwind's `sm` is 640px, ours is 375px), so always use these names.

| Tier | Range | Typical devices | Shell layout | Content grid |
|---|---|---|---|---|
| **xxs** | 240–319 | Foldable cover screens (Galaxy Z Fold/Flip outer ~260–300), tiny Android, split-screen slivers, zoomed browsers | Compact top bar (logo mark only) + **bottom nav with 4 icons + "More"** | 1 col, 8px margins |
| **xs** | 320–374 | iPhone SE (1st gen), small Android | Top bar + bottom nav (5 items) | 1 col, 12px margins |
| **sm** | 375–479 | iPhone 12–17, Pixel, Galaxy S (portrait) | Same | 1 col; KPI rows 2-up |
| **ph** | 480–767 | Large phones, phones landscape, small tablets portrait, Fold inner (folded-open portrait) | Bottom nav **or** side rail when landscape (§6.2) | 2 cols |
| **md** | 768–1023 | iPad mini / iPad portrait, Android tablets | **Icon rail (64px)** + top bar; no bottom nav | 8 cols (tiles span 4 or 8) |
| **lg** | 1024–1279 | iPad landscape, iPad Pro 11" portrait (834→1024), small laptops, Surface | Icon rail + collapsible secondary dock (drawer) | 12 cols |
| **xl** | 1280–1439 | 13–14" laptops (1280×800, 1366×768) | **Full sidebar (240px, collapsible to rail)** + top bar | 12 cols |
| **2xl** | 1440–1919 | 15–16" laptops, iPad Pro 13" landscape, 1440p/1680 monitors | Sidebar + top bar + optional right dock (order book / agent feed, 320px) | 24 cols |
| **3xl** | 1920–2559 | Full HD desktops (the **primary design target**) | Sidebar + right dock both pinned | 24 cols, `max-width: none` |
| **4xl** | ≥ 2560 | QHD/4K/ultrawide | Same, with **multi-workspace** (two dashboards side by side) or a content cap of 2400px centred | 24 cols ×2 |

**Floor:** the minimum supported width is **240px**. Below that (e.g. smartwatches) we don't design, but the page must still not break: no horizontal page scroll, and controls remain operable.

### 6.2 Orientation & height rules (landscape)

Width alone isn't enough. Phones in landscape are wide but very short. Add these **raw media queries**:

| Query | Name | Rule |
|---|---|---|
| `(orientation: landscape) and (max-height: 500px)` | `landscape-short` | Phone landscape (568×320 → 932×430). **Hide the bottom nav and use a 56px left icon rail.** Top bar shrinks to 40px. KPI strip becomes one horizontal scroller. Charts get `height: calc(100dvh - 40px - 16px)`. Modals become full-height side sheets. |
| `(orientation: portrait) and (min-width: 768px)` | `tablet-portrait` | Tablet portrait: stack the right dock **below** the main content as tabs. |
| `(orientation: landscape) and (min-width: 1024px) and (max-height: 820px)` | `tablet-landscape` / short laptops | Sticky headers ≤ 48px; collapse non-critical tile headers; prefer two-column tile layouts over tall stacks. |
| `(max-height: 400px)` | `very-short` | Any device: drop decorative headers, keep top bar + content only. |
| `(hover: none) and (pointer: coarse)` | `touch` | Touch density (44px targets); show hover-only actions persistently; enlarge drag handles. |
| `(prefers-reduced-motion: reduce)` | — | No pulses, tick flashes become a 1-frame colour change, no smooth scroll. |
| `(prefers-color-scheme: light)` / `[data-theme]` | — | Theme (dark is the default; light uses the tokens above). |

Foldables/dual-screen: respect `env(safe-area-inset-*)`, and test both folded (cover) and unfolded (≈ 7.6–8" near-square) states. Treat unfolded as `md` portrait/landscape.

### 6.3 Tailwind configuration (use in every implementation and mock-up)

```js
tailwind.config = {
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    screens: {
      xxs: '240px', xs: '320px', sm: '375px', ph: '480px', md: '768px',
      lg: '1024px', xl: '1280px', '2xl': '1440px', '3xl': '1920px', '4xl': '2560px',
      'landscape-short': { raw: '(orientation: landscape) and (max-height: 500px)' },
      'tablet-portrait': { raw: '(orientation: portrait) and (min-width: 768px)' },
      'tablet-landscape': { raw: '(orientation: landscape) and (min-width: 1024px) and (max-height: 820px)' },
      'very-short': { raw: '(max-height: 400px)' },
      touch: { raw: '(hover: none) and (pointer: coarse)' },
    },
    extend: { /* colours, fonts, radii from the frontmatter */ },
  },
  plugins: [require('@tailwindcss/container-queries'), require('@tailwindcss/forms')],
}
```

**Production:** build Tailwind locally (CLI/PostCSS). **Never use the `cdn.tailwindcss.com` script in the product.** It's a dev-only runtime compiler; it's also blocked in sandboxed and locked-down environments, and it doesn't work offline.

### 6.4 App shell by tier

```
3xl/2xl  ┌ top bar 56 ─────────────────────────────────────────────┐
         │ sidebar 240 │ main (24-col grid)          │ right dock 320 │
         └ status bar 28 ──────────────────────────────────────────┘
xl       sidebar 240 (collapsible→rail) │ main 12-col │ dock as drawer
lg       rail 64 │ main 12-col │ dock as drawer/tab
md       rail 64 │ main 8-col (dock stacked below as tabs)
ph/sm/xs top bar 48 / main 1–2 col / bottom nav 56 (+safe-area)
xxs      top bar 44 (mark only) / main 1 col / bottom nav 4 + More
landscape-short: rail 56 │ main │ (no bottom nav), top bar 40
```

**Shell rules:**
- **Viewport height:** use `100dvh` / `min-h-dvh`, **never `100vh`/`h-screen`** for full-height layouts (mobile browser bars). The v1 screens use `h-screen`.
- **Bars:**
  - The **top bar, status bar and bottom nav** are sticky in normal flow, or fixed with a reserved spacer.
  - Fixed bars must not overlap content. The v1 risk-hub and tax screens' fixed status bar paints over content mid-page.
  - The sidebar must span the full height (it ends mid-page in v1).
- **Global safety controls:** **Emergency Halt / Kill switch** and the **mode badge** (bot modes `paper` / `hitl` / `autonomous`, with a LIVE marker for real money) are visible on every tier.
  - xxs–sm: in the top bar as an icon button with a text label in its accessible name.
  - Kill switch: always one tap from anywhere, with a confirm sheet (never a browser `alert()`/`confirm()`).
- **Navigation overflow:**
  - Below `xl`, the horizontal module tabs (v1 cockpit) become a **scrollable tab strip with edge fade + overflow menu**.
  - Below `md` they move into the bottom nav plus a "More" sheet.

### 6.5 Grid & tiles

- **Tiles are container-query components** (`@container`), so they adapt to the width they're given, not the viewport. A KPI tile in a 1/4 column on 1920 and a full-width tile on 375 use the same component.
- **Tile spans by tier (examples):**

| Tile | 3xl/2xl (24) | xl/lg (12) | md (8) | ph (2) | ≤ sm (1) |
|---|---|---|---|---|---|
| KPI card | 4 | 3–4 | 4 | 1 | 1 (KPIs 2-up inside a strip ≥ 375; 1-up < 375) |
| Main chart | 16 | 12 | 8 | 2 | 1 |
| Order book / dock | 8 (right dock) | drawer | tab | tab | tab |
| Agent consensus | 8–12 | 12 | 8 | 2 | 1 |
| Blotter / tables | 24 | 12 | 8 | 2 | 1 (card list) |

- **No unprefixed multi-column grids.** `grid-cols-12`, `grid-cols-6` or `grid-cols-5` without a breakpoint prefix crush content on phones. Always start at `grid-cols-1` and add columns at `ph`/`md`/`lg`.
- **Min tile width:** 260px. Below that, the tile goes full width.

### 6.6 Component behaviour across tiers

| Component | ≥ xl | md–lg | ≤ ph | xxs |
|---|---|---|---|---|
| **Data tables / blotters** | Full columns, sticky header, compact rows | Hide P3 columns (keep a column chooser) | **Card list**: each row becomes a card (primary: instrument, side, size, price, status; details expand) | Card list with 2 fields per line |
| **Order book ladder** | 20px rows, 20–25 levels each side | 15 levels | 10 levels; tap to expand | 5 levels + spread |
| **Charts** | Full toolbar | Toolbar collapses to a menu | Min height 220px (portrait) / fill height (landscape-short); pinch-zoom; timeframe chips scroll horizontally | Sparkline + last price; tap opens full-screen chart |
| **Agent debate / chat** | Side-by-side agent columns | 2 columns | Single thread with agent avatars | Same; collapsed rationale |
| **Forms / risk policy editor** | 2–3 column form | 2 columns | 1 column; steppers ≥ 44px | 1 column; labels above inputs |
| **Modals** | Centred dialog (max 640px) | Dialog | **Bottom sheet** (portrait) / side sheet (landscape-short) | Full-screen sheet |
| **KPI strip** | Grid | Grid | Horizontal snap scroller with page dots | Vertical stack |
| **Kill switch / approvals** | Tile + top-bar button | Same | Top-bar button + sticky approval bar | Same; confirm sheet full screen |
| **Hover tooltips** | Hover | Hover + long-press | Long-press / tap info icon | Tap info icon |
| **Sidebar module list** | Full labels (truncate with tooltip; v1 truncates "Strategy Lab & Nautil…") | Rail icons + tooltips | Bottom nav + More sheet | 4 icons + More |

- **Text never overflows its container.**
  - Use `min-w-0` on flex children, `truncate` with a full-text tooltip, or wrapping.
  - Long numbers wrap only at defined points.
  - A button label must never be clipped: the v1 cockpit "Authorize Mesh Vector (0.85 BTC)" is clipped, so allow wrapping or shorten the label.
- **No horizontal page scroll at any width ≥ 240px.** Wide tables scroll inside their own `overflow-x-auto` box with a visible scroll shadow.

### 6.7 Touch & input

- **Touch targets:** ≥ 44×44px on `touch`, ≥ 32px on desktop, with spacing ≥ 8px between destructive and safe actions.
- **Gestures:** swipe actions on mobile card lists (e.g. cancel order) need a confirm step for anything that trades.
- **Keyboard:** full support on desktop (`⌘/Ctrl+K` command palette, `/` search, `Esc` closes sheets). Visible focus ring: 2px Cobalt + 2px offset.
- **Form controls:** inputs use `inputmode="decimal"` for prices and sizes on mobile.

### 6.8 Test matrix (every screen must pass)

| Class | Viewports (CSS px) |
|---|---|
| Desktop | 2560×1440, **1920×1080**, 1680×1050, 1536×864, 1440×900 |
| Laptop | 1366×768, 1280×800, 1280×720 |
| Tablet landscape | 1366×1024 (iPad Pro 13), 1194×834 (iPad Pro 11), 1180×820 (iPad Air), 1024×768 (iPad mini/older) |
| Tablet portrait | 1024×1366, 834×1194, 820×1180, 768×1024 |
| Foldable | 884×1104 (unfolded), 280×653 / ~300×750 (cover) |
| Phone portrait | 430×932, 412×915, 390×844, 375×667, 360×780, 320×568 |
| Phone landscape | 932×430, 844×390, 667×375, 568×320 |
| Floor | 240×320 |

**Pass criteria at each viewport:**
1. no horizontal page scroll;
2. no clipped or overlapping text or controls;
3. kill switch and mode visible within one tap;
4. touch targets meet §6.7;
5. contrast meets §2;
6. no fixed element covers content;
7. works at 200% browser zoom (WCAG 1.4.4/1.4.10 reflow at 320 CSS px).

**Automate it:** Playwright screenshot + overflow check across this matrix in CI (`document.documentElement.scrollWidth <= innerWidth`, plus element-overlap checks for fixed bars).

## 7. Components (carried over from v1, unchanged unless noted)

**Buttons:**
- **Primary** (Buy / Start / Confirm): Mint fill, Ink text, 600 weight; hover brighten + 8px mint bloom.
- **Secondary** (Route / Backtest): Cobalt fill, Paper text.
- **Emergency** (Cancel all / Halt): Flare tint + 1px Flare border; hover = solid Flare + Ink text.
- **Ghost:** borderless, Graphite hover.
- **Heights:** 32px desktop / 44px touch.

**Tiles:**
- Graphite surface, `border-subtle`, 8px radius.
- 32px header with an 11px uppercase title, a live-stream dot and window controls.
- Window controls are hidden on ≤ ph.

**Status chips** (JetBrains Mono 11px):
| Status | Background | Text | Extra |
|---|---|---|---|
| Running | mint-tint | Mint | Pulsing 6px node |
| Idle/synced | cobalt-tint | Cobalt | — |
| Degraded | warn-tint | Warn | — |
| Breach | flare-tint | Flare | — |

Every chip has a text label (never a dot alone).

**Order book:**
- Depth bars behind prices: mint-tint (bids) and flare-tint (asks).
- Row height follows the density mode.
- The spread row is always visible.

**Logs:** alternating Graphite/transparent rows, muted timestamps, virtualised lists for > 200 rows.

**Inputs:**
- Inset `#161B24` fields with `border-medium`; Cobalt focus ring.
- Steppers and leverage sliders use Paper grips and Mint fill tracks.
- Any value that loosens risk shows the **confirmation flow** (Telegram + TOTP) inline, per the build spec M11. This includes L0 hard ceilings.
- Every configurable setting shows its effective value, the layer that set it (L0–L4) and its default from [16](docs/16-configuration-and-safety-model.md) ([ui §3.7](docs/ui/README.md#37-settings-show-configurable-defaults-and-their-layer)). Mock-ups never present a default as a fixed rule.

**Candlesticks:**
- Wicks are 1px hairlines; bodies are 4px wide at default zoom.
- Decision nodes are a centred circle (Signal M).

**Wordmark:** `MASTER` (600) + `TRADER` (300, Mint). At ≤ xs only the mark is shown (use `brand/mark-small.svg` below 24px).

## 8. Motion

- **Easing and duration:** `cubic-bezier(0.4,0,0.2,1)`; 150–200ms for UI, 0ms for data.
- **Ticks:** price flashes are a 300ms background tint in mint-tint/flare-tint, at most one per cell per 250ms.
- **Reduced motion:** see §6.2.
- **No decorative animation on trading surfaces.** "Simulated" countdowns and random pulses in the v1 mock-ups are for demonstration only.

## 9. Accessibility

- **Standard:** WCAG 2.2 AA.
- **Markup:**
  - real `<button>`/`<a>`/`<input>` elements;
  - icon-only buttons have `aria-label`;
  - live price regions use `aria-live="off"` by default (an opt-in announcer for watched symbols).
- **Behaviour:**
  - focus order follows the visual order at every tier;
  - the kill switch is reachable by keyboard within 2 tabs of the top bar.
- **Localisation:** numbers and dates follow the user locale (default `en-AU`, AEST/AEDT shown with UTC on hover); currency defaults to AUD.

## 10. Content rules for mock-ups and the product

Mock data must reflect the actual product spec, so designs don't promise things the system won't do.

- **Data sources:** free sources only. Don't show paid feeds (e.g. Trading Economics, CME FedWatch API, CoinGlass, colocation, VIP-tier venue accounts) as live sources.
- **Latency:** show measured values with units (µs for Decision One tier A, ms for tier B and feeds). Avoid "0.00ms" claims.
- **Models:** label them as in the spec: Claude via the gateway for research/debate; local decision models (SemIf / own Qwen-LoRA head) for tier B; compiled trees for tier A.
- **MCP:** every MCP-originated order creates an **approval card** you approve on Telegram/web (TTL default 5 min, [16 §2.3](docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); MCP can never approve anything itself. Loosening risk shows Telegram + TOTP confirmation (C3). Withdrawals, keys, mandates, approvals and MCP self-admin are never MCP tools ([16 §2.12](docs/16-configuration-and-safety-model.md#212-mcp-phase-8)).
- **Airdrops:** no "sybil task pipelines" or automated social tasks. Social and quest tasks appear in the **manual user-task queue**. Auto-claims show the simulation result and mandate.
- **Tax:**
  - Australian FY labels (FY2025-26) and the 12-month discount rule.
  - Lot method shown as *specific identification → FIFO fallback*.
  - Cite real ATO references only, or none (v1 cites unverified rulings).
  - "Not tax advice" footers on tax screens.
- **Risk:** every order surface shows the risk-manager status (pass / veto / needs approval).
- **Modes:** use `Paper` / `Approve (HITL)` / `Autonomous` (set per bot); never `APPROVE` / `LIVE AUTO`.
- **Telegram:** shown only as postures (numbers); never Telegram message text.
