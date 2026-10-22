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
| **Capital gains** | CGT events: asset, acquired, disposed, holding days, discount eligibility (12-month rule, both days excluded), cost base, proceeds, gain/loss, method used (specific ID / FIFO fallback), wash-sale flag (re-acquisition within 30 days either side of a loss disposal; flag only, default window configurable) | `/tax/summary?fy=&section=cgt` |
| **Income** | Ordinary income items: staking, airdrops (general vs initial allocation), interest, dividends (franking), CFD/futures results, funding/financing | `/tax/summary?fy=&section=income` |
| **PAYG** | Quarterly instalment estimates computed **both ways**: the ATO instalment-amount method and the instalment-rate method (your notice decides which applies (U), tax agent to confirm); due dates; instalment income basis (excluding capital gains); history | `/tax/summary?fy=&section=payg` |
| **Lots** | `LotTable`: open lots per asset (incl. foreign-currency cash lots), unrealised gains, discount-eligible date countdown; **30 Jun 2027 snapshot** status with each price's source and method ([16 §4.2](../../16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change)); I1 snapshot (if residency changed) | `/journal/lots` |
| **Residency** | Timeline of residency periods (country, from/to, evidence notes); active plugin per period; CGT event I1 modelling (elect s104-165 vs not, both shown) | `/tax/residency` |
| **Reports** | Generated outputs: myTax worksheet (item mapping), CGT schedule, income schedule, PAYG workings, accountant pack (CSV/PDF), Beancount ledger export, CARF reconciliation (venue-provided statements vs journal, where a venue provides them; otherwise not applicable); generation history with hashes | `/tax/reports` |
| **Questions** | Open questions for the tax agent (from the spec: business vs investor, futures treatment, perps treatment (default revenue (U)), 2027 transition, Div 775, DTAs…) with status and answers (`task.answer`); answers can set the regime. Stored in the minimal `curation.task` table from Phase 3 | `/tasks?type=TAX_QUESTION` |

## Actions

| Control | Command | Level |
|---|---|---|
| Generate report | `tax.report.generate` | C1 |
| Export (CSV/PDF/Beancount) | `tax.export` | C0 |
| Add/edit residency period | `tax.residency.add` | C1 (re-computation preview first); **C3** if the change loosens risk (e.g. removing a period that blocks crypto). Saving emits `tax.residency.changed`; the venue registry recomputes, and any loosening that results is C3 |
| Set regime (per FY/activity) | `tax.regime.set` | C1 (after an agent answer) |
| Override lot selection (specific ID) for a disposal, before FY close | `tax.lot.select` | C1 (audited; only where records allow) |
| Answer a tax-agent question | `task.answer` | C1 |
| Lock / unlock an FY | `tax.fy.lock` / `tax.fy.unlock` | C3 (unlock needs a reason) |

## Rules & states

- **Locked FYs:** after a report is marked "lodged", the FY is locked (`tax.fy.lock`), and changes need explicit unlocking (`tax.fy.unlock`, C3 + reason).
- **Wash-sale warnings:** shown inline. The system never suggests tax-loss harvesting with reacquisition.
- **Egypt residency:** a red compliance flag on any crypto activity; the venue registry blocks crypto products for that period (fail-closed). Removing the block is a loosening (C3).
- **Valuation:** non-trade events show their value method ([16 §4.1](../../16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)): fill price → VWAP of our recorded trades → on-chain pool price; aggregators are a cross-check only.
- **Accounts:** registering and tagging accounts in Phase 3 happens in D16 Settings → Accounts.

## Acceptance criteria

1. **Traceability:** every number drills down to journal events.
2. **Repeatable reports:** reports are reproducible (same inputs give the same hash).
3. **Discount boundary:** the 12-month discount boundary matches the ATO example (bought 2 Feb → eligible from 3 Feb next year) in a golden test surfaced in the UI's "rule check" panel.

## Backend contract

- **Queries:** `/tax/summary` (+ sections), `/tax/reports`, `/tax/residency`, `/journal/lots`, `/tasks?type=TAX_QUESTION`.
- **WebSocket topics:** `journal`.
- **Commands:** `tax.report.generate`, `tax.export`, `tax.residency.add`, `tax.regime.set`, `tax.lot.select`, `tax.fy.lock`, `tax.fy.unlock`, `task.answer` _(added to architecture §7.2)_.
