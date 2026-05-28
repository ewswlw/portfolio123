---
title: "Native Strategy Book Read-Only Inventory"
created_at: 2026-05-22 15:20 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/strategy-books
  - work/native-validation
  - work/generated-artifacts
created: 2026-05-22
updated: 2026-05-28
description: "Generated native Portfolio123 Strategy Book validation artifact for Native Strategy Book Read-Only Inventory."
---

# Native Strategy Book Read-Only Inventory

This artifact records read-only Portfolio123 platform observations for the promoted dynamic Strategy Book validation plan. No Portfolio123 objects were created, edited, copied, deleted, saved, submitted, or run during this pass.

## Validation Context

- Plan: `docs/plans/2026-05-22-004-native-p123-strategy-book-validation-plan.md`
- Requirements: `docs/brainstorms/2026-05-22-native-p123-strategy-book-validation-requirements.md`
- Candidate package: `p123-output/native_validation_package_20260522.md`
- Candidate trial: `386`
- Candidate optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: `20.68%`
- API-estimated Sharpe: `2.00`
- API-estimated max drawdown: `-12.81%`
- Corrected local timing-panel start: `2007-06-26`

## Close Native Books

All inspected native books below are existing Portfolio123 simulated books. They are useful references, but none is a clean replication of the promoted candidate.

| Native book | Port ID | Period | Assets | Rebalance | Annualized return | Sharpe | Max drawdown | Correlation to SPY |
|---|---:|---|---:|---|---:|---:|---:|---:|
| `BookSim - Copy` | `1930094` | `01/03/06 - 04/02/26` | 4 | Every 4 Weeks | 22.90% | 1.90 | -25.52% | 0.71 |
| `BookSim - Copy(2)` | `1930095` | `01/03/06 - 04/02/26` | 4 | Every 4 Weeks | 26.55% | 1.84 | -31.92% | 0.73 |
| `BookSim - Copy(3)` | `1930104` | `01/03/06 - 04/02/26` | 4 | Every 4 Weeks | 21.99% | 1.86 | -25.18% | 0.70 |
| `BookSim(6)` | `1930097` | `01/03/06 - 04/02/26` | 5 | Every 4 Weeks | 23.60% | 1.85 | -27.13% | 0.75 |

Interpretation:

- `BookSim - Copy` is the closest visible native book by combined Sharpe and drawdown, but it still misses the strict target: Sharpe is below 2.0 and max drawdown is slightly worse than -25%.
- `BookSim - Copy(2)` and `BookSim(6)` have higher returns but much larger drawdowns.
- `BookSim - Copy(3)` has drawdown close to the gate, but return and Sharpe are lower than the promoted API-estimated candidate.

## Asset Mixes

### `BookSim - Copy` / `1930094`

| Asset | Weight |
|---|---:|
| iShares 20+ Year Treasury Bond ETF | 14.44% |
| SPDR Gold Shares | 15.36% |
| Advisor Small Cap Focus (P123) With Risk Reduction | 40.85% |
| Wes Gray Momentum Microcaps Hedged | 29.36% |

### `BookSim - Copy(2)` / `1930095`

| Asset | Weight |
|---|---:|
| iShares 20+ Year Treasury Bond ETF | 9.52% |
| SPDR Gold Shares | 10.26% |
| Advisor Small Cap Focus (P123) With Risk Reduction | 51.58% |
| Wes Gray Momentum Microcaps Hedged | 28.64% |

### `BookSim - Copy(3)` / `1930104`

| Asset | Weight |
|---|---:|
| iShares 20+ Year Treasury Bond ETF | 24.07% |
| SPDR Gold Shares | 5.27% |
| Advisor Small Cap Focus (P123) With Risk Reduction | 41.71% |
| Wes Gray Momentum Microcaps Hedged | 28.95% |

### `BookSim(6)` / `1930097`

| Asset | Weight |
|---|---:|
| Advisor Small Cap Focus (P123) With Risk Reduction | 35.99% |
| SAMCF + Quality Filter Group | 9.04% |
| Wes Gray Momentum Microcaps Hedged | 24.93% |
| SPDR Gold Shares | 14.98% |
| iShares 20+ Year Treasury Bond ETF | 15.05% |

## Structural Observations

- The inspected books use `Static Weight` sizing.
- The inspected books show `Last Rebalanced (Every 4 Weeks)`.
- The inspected books use `S&P 500 (SPY:USA)` as benchmark.
- The visible review page for `BookSim - Copy` showed:
  - Currency: `USD`
  - Starting capital: `100,000.00`
  - Asset rebalance slippage: `0.25%`
  - Minimum rebalance transaction: `0.5%`
  - Asset tolerance: `2.0%`
  - Gross exposure: `1.0`
  - Net exposure: `1`
  - Allocation algorithm: `Fixed Weight`
  - Allocation: TLT 15%, GLD 15%, Advisor Small Cap Focus 40%, Wes Gray Momentum Microcaps Hedged 30%
  - Period: `01/03/2006 - 04/02/2026`

## Timing-Surface Inspection

Read-only inspection of `BookSim - Copy` included:

- Summary page: `https://www.portfolio123.com/port_summary.jsp?portid=1930094`
- Trading-system/review page: `https://www.portfolio123.com/port_wiz.jsp?editUid=1930094`
- General page attempt: `https://www.portfolio123.com/port_wiz.jsp?editUid=1930094&st=0`
- Assets & Rebalance direct page attempt: `https://www.portfolio123.com/port_wiz.jsp?editUid=1930094&st=1`
- Period & Restrictions direct page attempt: `https://www.portfolio123.com/port_wiz.jsp?editUid=1930094&st=7`
- Review page attempt: `https://www.portfolio123.com/port_wiz.jsp?editUid=1930094&st=8`

Observed outcome:

- The review page exposed General, Assets & Rebalance, and Period & Restrictions settings.
- The visible review text did not expose a Strategy Book-level timing rule, formula rule, conditional allocation rule, or hedge/timing rule surface.
- Direct navigation to the Assets & Rebalance and Period & Restrictions wizard steps returned an internal server error in this read-only session.

Conclusion:

- Book-level conditional timing was not confirmed from the read-only inspection.
- The safer native replication assumption remains: if the user proceeds, separate timed simulated strategy components may be required.
- This is not proof that book-level timing is impossible; it means the read-only surface did not confirm it.

## Candidate Replication Implication

The existing close books are structurally different from the promoted candidate:

- Existing close books use a small number of static allocations to existing PTF/ETF assets.
- The promoted candidate requires five 200-day timed strategy components at 16% each plus a 20% defensive proxy.
- The visible close books do not appear to contain all five promoted source strategies, nor do they expose the 200-day timing overlay.

Therefore:

- Existing books are useful benchmarks/reference points.
- They should not be treated as validation of trial `386`.
- A clean native validation still requires either:
  - a confirmed book-level timing mechanism, or
  - separate `codex_` timed simulated strategy components.

## Still Open Before Any Native Run

1. Choose the native book rebalance cadence:
   - Every 4 weeks to match inspected close books, or
   - annual book-level rebalance per general Strategy Book guidance.
2. Choose defensive proxy policy:
   - primary validation with `SHY` only, or
   - separate pre-registered `SHY`, `IEF`, and `AGG` variants.
3. Confirm the native mechanism for 200-day timing:
   - book-level timing if a supported UI/API surface is found, or
   - separate timed simulated strategy components if not.

## Validation Tier

This artifact is read-only platform inventory. It is not a native Strategy Book validation result and does not prove the target was met.

---

## Tags

#algo-trading/portfolio123 #algo-trading/strategy-books #work/native-validation #work/generated-artifacts
