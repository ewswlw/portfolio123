---
title: "Native P123 Dynamic Strategy Book Replication Execution Plan"
tags:
  - algo-trading/portfolio123
  - work/plans
created: 2026-05-22
updated: 2026-05-28
description: "Portfolio123 implementation plan covering scope, workflow, validation, and deliverables for Native P123 Dynamic Strategy Book Replication Execution Plan."
---

# Native P123 Dynamic Strategy Book Replication Execution Plan

## Summary

Execute native Portfolio123 replication of promoted trial `386` using the survivor set from `docs/ideation/2026-05-22-native-p123-replication-ideation.md` and the active project-spec memory. The plan is gated: create `codex_dynamic_*` objects only when exact timing behavior is confirmed; otherwise stop and classify the result as blocked or approximation-required.

## Source Inputs

- Active memory spec: `Native P123 Dynamic Strategy Book Replication`
- Ideation: `docs/ideation/2026-05-22-native-p123-replication-ideation.md`
- Prior plan: `docs/plans/2026-05-22-004-native-p123-strategy-book-validation-plan.md`
- Read-only inventory: `p123-output/native_strategy_book_readonly_inventory_20260522.md`
- Native package: `p123-output/native_validation_package_20260522.md`
- Dynamic timing learning: `docs/solutions/workflow-issues/portfolio123-dynamic-strategy-book-timing-warmup-workflow-2026-05-22.md`

## Candidate Definition

- Trial: `386`
- Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: `20.68%`
- API-estimated Sharpe: `2.00`
- API-estimated max drawdown: `-12.81%`
- Corrected local timing start: `2007-06-26`

Primary native allocation:

| Component | Weight |
|---|---:|
| `codex_dynamic_1873038_timed_200d` | 16% |
| `codex_dynamic_1934014_timed_200d` | 16% |
| `codex_dynamic_1934023_timed_200d` | 16% |
| `codex_dynamic_1934030_timed_200d` | 16% |
| `codex_dynamic_1934037_timed_200d` | 16% |
| `SHY` defensive proxy component | 20% |

## Hard Gates

1. Use only new `codex_dynamic_*` platform objects.
2. Do not mutate existing non-`codex_dynamic_*` P123 objects.
3. First check for exact book-level conditional timing.
4. If book-level timing is absent, check exact component-level timing with defensive substitution.
5. If exact defensive substitution is impossible, stop before approximation.
6. Count every native run; maximum total run budget is 5.
7. Label every object and result as `exact`, `approximation`, `variant`, `blocked`, or `not_run`.
8. No success claim unless native Tier 1 Strategy Book result passes all three gates.

## Work Phases

### Phase 1: Browser Preflight

Goal: confirm safe starting state.

Actions:

- Connect to the in-app Browser session.
- Confirm P123 is authenticated.
- Confirm current page has no unsaved modal or blocking dialog.
- Navigate to simulated books and simulated strategies only through normal page loads.

Output:

- `iteration.md` preflight entry.

Stop condition:

- If authentication is missing or an unsafe modal blocks navigation, stop and report.

### Phase 2: Platform Capability Gate

Goal: determine whether exact timing is natively expressible.

Actions:

- Inspect Strategy Book creation/edit/review surfaces for conditional allocation, formula, hedge, or timing controls.
- Inspect a source simulated strategy edit/review surface for market-timing, hedge, buy-rule, sell-rule, or allocation-to-ETF capabilities.
- Do not save or run during inspection.

Classification:

- `exact`: P123 can express the local behavior, including risk-off substitution to `SHY`.
- `approximation`: P123 can express cash/risk-off gating but not `SHY` substitution.
- `blocked`: neither book-level nor component-level timing is available.

Output:

- Capability entry in final evidence artifact.

Stop condition:

- If only approximation is available, stop before creating/running and ask for approval.

### Phase 3: Source Strategy Mapping

Goal: verify source IDs and clone/copy route.

Source strategies:

| Source ID | Source Name |
|---:|---|
| `1873038` | `Canada Core Combo - Eddy/Kurtis` |
| `1934014` | `SAMCF + Quality Filter Group - Copy` |
| `1934023` | `Small Cap Focus - Small...erse - Small AUM - Copy` |
| `1934030` | `Small Caps + Altman in Ranking + Altman > 1 - Copy` |
| `1934037` | `Advisor TSX Mighty Mouse Momentum - Copy` |

Actions:

- Open each source strategy summary.
- Capture name, URL/object ID, period, type, benchmark, and relevant copy/edit affordances.
- Do not mutate source objects.

Output:

- Source mapping in final evidence artifact.

### Phase 4: Timed Component Creation

Goal: create exact `codex_dynamic_*` timed components when capability gate passes.

Actions:

- For each source strategy, create or copy a new component object.
- Name using `codex_dynamic_<source_id>_timed_200d`.
- Apply the 200-day timing rule:
  `Close(0,#Bench) > SMA(200,0,#Bench)`
- Configure risk-off behavior to `SHY` if exact P123 surface supports it.
- Record exact formula/setting and object ID.

Stop conditions:

- If a formula is rejected, stop and classify that component as `blocked`.
- If the only available risk-off behavior is cash, stop before running and ask whether to proceed as approximation.

Run budget:

- Component validation runs count against the 5-run limit.

### Phase 5: Component Validation

Goal: validate each component only as needed before final book construction.

Actions:

- Run each newly created timed component if required by P123 to generate usable book assets.
- Record period, annualized return, Sharpe, max drawdown, warnings, and run count.
- Mark each component status.

Stop condition:

- If any required component is `blocked`, do not build the final book.

### Phase 6: Strategy Book Construction

Goal: build the final native Strategy Book candidate.

Actions:

- Create `codex_dynamic_strategy_book_candidate`.
- Add five timed components at 16% each.
- Add `SHY` defensive proxy at 20%.
- Set static weights.
- Use every-4-weeks rebalance for the primary run.
- Confirm total weight is 100%.
- Confirm no inverse or tactical ETF sleeves are included.

Output:

- Book object ID and pre-run settings in evidence artifact.

### Phase 7: Native Strategy Book Run

Goal: obtain the Tier 1 native result.

Actions:

- Run the native Strategy Book candidate.
- Capture native period, annualized return, Sharpe, max drawdown, correlation, asset weights, and any warnings.
- Count the run against the 5-run budget.

Success criteria:

- Native annualized return > 20%.
- Native Sharpe > 2.
- Native max drawdown better than -25%.

### Phase 8: Evidence And Interpretation

Goal: document exact outcome.

Actions:

- Write `p123-output/native_strategy_book_validation_20260522.md`.
- Include replication status matrix.
- Include run ledger.
- Compare API-estimated versus native metrics.
- Update `iteration.md`.

Final labels:

- `exact`: exact native replication and final book run completed.
- `approximation`: non-exact but approved approximation ran.
- `variant`: changed cadence/proxy/formula/weights.
- `blocked`: exact replication could not be implemented or run.
- `not_run`: planned item was not executed.

## Expected Artifacts

- `docs/ideation/2026-05-22-native-p123-replication-ideation.md`
- `docs/plans/2026-05-22-005-native-p123-replication-execution-plan.md`
- `p123-output/native_strategy_book_validation_20260522.md`
- `iteration.md`

## Verification

- Confirm no secrets were written.
- Confirm every created P123 object has `codex_dynamic_` prefix.
- Confirm run count is <= 5.
- Confirm final report contains status matrix and tier labeling.
- Confirm no native success claim is made without a native Strategy Book result.

---

## Tags

#algo-trading/portfolio123 #work/plans
