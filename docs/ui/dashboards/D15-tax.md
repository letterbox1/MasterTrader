# D15 · Tax & Reports

| | |
|---|---|
| **Route** | `/tax` (tabs: Summary · Capital gains · Income · PAYG · Lots · Residency · Reports · Questions) |
| **Modules** | M18 journal & tax (jurisdiction plugins) |
| **Phase** | 3 |
| **Mock-up reference** | `vetted-launch-radar-au-eofy-tax-ledger.png` (fix: lot method, FY labels, citations, "not tax advice") |

## Purpose

Australian EOFY and PAYG instalment outputs now, with other jurisdictions (UAE, Egypt, Cyprus) available by residency period. Every figure is traceable to journal events, FX sources and rule versions. Shown in every footer: **"Not tax advice. Confirm with a registered tax agent."**

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ xl | FY selector + jurisdiction badge (from residency) + regime badge (investor / trader-in-business / both) + tabs |
| md–lg | Same; tables with priority columns |
| ≤ ph | FY selector; summary cards; tabs as a select; lots as cards |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Summary** | `TaxSummaryCard`s:<br>• net capital gain (after losses, discount/indexation);<br>• carried-forward capital losses;<br>• revenue/trading income (CFDs, futures);<br>• Div 775 forex gains/losses;<br>• crypto income (staking, general airdrops);<br>• foreign income + foreign tax paid;<br>• estimated tax impact (informational).<br>Each card shows the **rule version** (AU_2026 / AU_2027_REFORM) and **FX source** (RBA). **Regime toggle** (investor vs trader-in-business) shows both computations until the tax agent decides. | `/tax/summary?fy=` |
| **Capital gains** | CGT events: asset, acquired, disposed, holding days, discount eligibility (12-month rule, both days excluded), cost base, proceeds, gain/loss, method used (specific ID / FIFO fallback), wash-sale flag | `/tax/summary?fy=&section=cgt` |
| **Income** | Ordinary income items: staking, airdrops (general vs initial allocation), interest, dividends (franking), CFD/futures results, funding/financing | `/tax/summary?fy=&section=income` |
| **PAYG** | Quarterly instalment estimates, due dates, instalment income basis (excluding capital gains), history | `/tax/summary?fy=&section=payg` |
| **Lots** | `LotTable`: open lots per asset (incl. foreign-currency cash lots), unrealised gains, discount-eligible date countdown; **30 Jun 2027 snapshot** status; I1 snapshot (if residency changed) | `/journal/lots` |
| **Residency** | Timeline of residency periods (country, from/to, evidence notes); active plugin per period; CGT event I1 modelling (elect s104-165 vs not, both shown) | `/tax/residency` |
| **Reports** | Generated outputs: myTax worksheet (item mapping), CGT schedule, income schedule, PAYG workings, accountant pack (CSV/PDF), Beancount ledger export, CARF reconciliation (venue-reported vs journal); generation history with hashes | `/tax/reports` |
| **Questions** | Open questions for the tax agent (from the spec: business vs investor, futures treatment, 2027 transition, Div 775, DTAs…) with status and answers; answers can set the regime | `/tasks?type=TAX_QUESTION` |

## Actions

| Control | Command | Level |
|---|---|---|
| Generate report | `tax.report.generate` | C1 |
| Export (CSV/PDF/Beancount) | `tax.export` | C0 |
| Add/edit residency period | `tax.residency.add` | C1 (re-computation preview first) |
| Set regime (per FY/activity) | `tax.regime.set` | C1 (after an agent answer) |
| Override lot selection (specific ID) for a disposal, before FY close | `tax.lot.select` | C1 (audited; only where records allow) |

## Rules & states

- **Locked FYs:** after a report is marked "lodged", the FY is locked, and changes need explicit unlocking (C1 + reason).
- **Wash-sale warnings:** shown inline. The system never suggests tax-loss harvesting with reacquisition.
- **Egypt residency:** a red compliance flag on any crypto activity.

## Acceptance criteria

1. **Traceability:** every number drills down to journal events.
2. **Repeatable reports:** reports are reproducible (same inputs give the same hash).
3. **Discount boundary:** the 12-month discount boundary matches the ATO example (bought 2 Feb → eligible from 3 Feb next year) in a golden test surfaced in the UI's "rule check" panel.

## Backend contract

- **Queries:** `/tax/summary` (+ sections), `/tax/reports`, `/tax/residency`, `/journal/lots`, `/tasks?type=TAX_QUESTION`.
- **WebSocket topics:** `journal`.
- **Commands:** `tax.report.generate`, `tax.export`, `tax.residency.add`, `tax.regime.set`, `tax.lot.select` _(added to architecture §7.2)_.
