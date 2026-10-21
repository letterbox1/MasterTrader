# MasterTrader brand (draft v1: "Signal M")

Two candlesticks form the uprights of an **M**. The price path between them dips to a single data node and recovers higher than it started.

Concept canvas (three directions, app-icon sizes): https://claude.ai/artifact/KKaaX95u5UpJDvWbz5JsD5 (private)

## Files
| File | Use |
|---|---|
| `mark.svg` | Primary mark, gradient, for dark grounds |
| `mark-on-light.svg` | Primary mark, deeper gradient, for light grounds |
| `mark-mono.svg` | One colour (`currentColor`) for print, watermarks, single-colour UI |
| `mark-small.svg` | Simplified mark for ≤ 24 px: favicon, tabs, bot avatar (no wicks or node) |
| `app-icon.svg` | 1024 rounded-square app icon (iOS/desktop/PWA) |

## Palette
| Token | Hex | Role |
|---|---|---|
| Ink | `#07090D` | Primary ground |
| Graphite | `#11151C` | Surfaces |
| Line | `#232A35` | Borders |
| Paper | `#EEF2F6` | Text on dark / light ground |
| Signal Mint | `#2BE4A7` (on light `#0E8F69` text / `#12B886` graphics) | Brand primary, positive |
| Cobalt | `#3A7BFF` (on light `#2A5FE0`) | Brand secondary |
| Flare | `#FF6B4A` | Alerts / negative only, never in the logo |

Gradient: Cobalt → Mint, bottom-left to top-right (rising).

## Type
- **Space Grotesk:** wordmark (`MASTER` 600 + `TRADER` 300 in Mint, tracking 0.06em) and headings.
- **JetBrains Mono:** prices, tickers, labels.

## Rules
- Clear space around the mark is ≥ the width of one candle body.
- Below 24 px, use `mark-small.svg`.
- Don't add glows, outlines or extra colours to the mark.
