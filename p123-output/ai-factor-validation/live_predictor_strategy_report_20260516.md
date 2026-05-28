---
title: "Portfolio123 Live Predictor Strategy Report - 2026-05-16"
created_at: 2026-05-16 10:56 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-16
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for Portfolio123 Live Predictor Strategy Report - 2026-05-16."
---

# Portfolio123 Live Predictor Strategy Report - 2026-05-16

## Objective

Test the prior best AI Factor strategy configuration through the latest available Portfolio123 data using the live predictor branch:

```text
AIFactor("AI Factor Base 87 Features Andreas 2", "extra trees medium 4")
```

This is a distinct branch from the earlier exact validation model:

```text
AIFactorValidation("AI Factor Base 87 Features Andreas 2", "extra trees medium 4", "2")
```

## Platform Constraint Found

P123 did not allow the live predictor to be backtested over the requested full available account history.

The predictor dialog warned that live predictor backtests are limited to the latest 5 years, but native simulation rejected the 5-year window with this stricter rule:

```text
Predictions may only be made using data from dates with which the predictor was not trained.
Predictor was trained until 06/21/2025.
```

Rejected native windows:

- `05/16/2021 - 05/16/2026`
- `06/22/2025 - 05/16/2026`
- `06/23/2025 - 05/16/2026`

The first accepted native window was:

```text
01/19/2026 - 05/16/2026
```

## Created P123 Objects

- Ranking system: `codex_ranking_ai_base87_live_v1`, P123 id `545009`
- Simulated strategy: `codex_strategy_ai_base87_live_v1_5y_conc10`, P123 id `1941664`

## Configuration

| Field | Value |
|---|---|
| AI Factor | `AI Factor Base 87 Features Andreas 2` |
| Live predictor | `extra trees medium 4` |
| Ranking formula | `AIFactor("AI Factor Base 87 Features Andreas 2", "extra trees medium 4")` |
| Universe | `No OTC Exchange + min 10 mil No Finance2` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Position sizing | Static weight |
| Target positions | 10 |
| Rebalance | Every Week |
| Commission | `0.005 USD Per Share` |
| Slippage | Variable |
| Transaction price | Average of Next High, Low, and 2X Close |
| PIT Method - Prelim | Exclude |
| Buy rules | `Rank > 95`; `Close(0) > 1`; `AvgDailyTot(20) > 100000` |
| Sell rules | `Rank < 85` |
| Accepted period | `01/19/2026 - 05/16/2026` |

## Native P123 Result

| Metric | Result |
|---|---:|
| Total return | 0.53% |
| Benchmark return | 7.16% |
| Active return | -6.63% |
| Annualized return | 1.67% |
| Sharpe ratio | 0.43 |
| Max drawdown | -18.32% |
| Benchmark max drawdown | -8.88% |
| Annual turnover | 65.98% |
| Overall winners | 8/17, 47.00% |
| Risk samples | 3 |
| Correlation with SPY | 0.98 |

## Conclusion

The requested full-history-through-today test is not available for this live predictor in native P123. The longest accepted native live-predictor simulation currently found was only `01/19/2026 - 05/16/2026`.

That accepted test performed poorly: `1.67%` annualized return, `0.43` Sharpe, `-18.32%` max drawdown, and `-6.63%` active return versus SPY.

The live predictor branch therefore does not rescue the prior AI strategy. It also cannot answer the original full-history question without retraining/configuring a validation method that saves predictions across a longer historical window.

## Recommended Next Step

Use a new Rolling Time Series CV or Time Series CV validation setup with saved validation predictions if the goal is a defensible multi-year AI Factor backtest. For the current predictor, native P123 only supports a short post-predictor-update out-of-sample window.

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
