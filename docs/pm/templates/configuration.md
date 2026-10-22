# Configuration & Defaults

**Rule: anything a user might reasonably want to change is configuration, not code.** This includes limits, thresholds, timers, budgets and behaviour on failure. Numbers here are **defaults**. Other docs link here instead of repeating numbers.

## 1. Layers (tighten-only inheritance)

| Layer | Holds | Who edits | Changing it |
|---|---|---|---|
| L0 Hard ceilings | <!-- pm:fill absolute limits nobody can exceed from the app --> | Owner only, outside the app | Manual + restart |
| L1 System | <!-- pm:fill --> | <!-- --> | <!-- e.g. tighten: immediate; loosen: needs confirmation --> |
| L2 … | | | |

The effective value is the strictest across layers. Every change is versioned and recorded.

## 2. Defaults

<!-- pm:fill One table per area: | Setting | Layer | Default | Range | Notes |. Mark unverified values (U). -->

## 3. Failure behaviour

<!-- pm:fill What happens when each dependency fails, and the default action (with configurable alternatives). -->

## 4. Live inputs instead of constants

<!-- pm:fill Values fetched at runtime (prices, fees, quotas, rates) and their sources. -->
