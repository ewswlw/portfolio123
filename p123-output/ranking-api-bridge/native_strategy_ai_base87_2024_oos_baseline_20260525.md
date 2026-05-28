---
title: "Native Strategy Result: 2024 OOS AI Factor Baseline"
created_at: 2026-05-25 14:36 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ranking-systems
  - work/generated-artifacts
  - work/api-bridge
created: 2026-05-25
updated: 2026-05-28
description: "Generated Portfolio123 ranking API bridge artifact for Native Strategy Result: 2024 OOS AI Factor Baseline."
---

# Native Strategy Result: 2024 OOS AI Factor Baseline

## Objects

- AI Factor: `codex_ai_base87_etm4_2024_oos_v1`
- Validation model: `extra trees medium 4 #2`
- Validation formula loaded into API ranking system:
  `AIFactorValidation("codex_ai_base87_etm4_2024_oos_v1", "extra trees medium 4", "2")`
- Ranking system used by native simulation: `ApiRankingSystem` (`541785`)
- Native simulated strategy: `codex_strategy_ai_base87_2024_oos_baseline_v1`
- Native strategy id: `1944189`
- URL: `https://www.portfolio123.com/port_summary.jsp?portid=1944189`

## Setup

- Universe: `No OTC Exchange + min 10 mil No Finance2`
- Benchmark: `S&P 500 (SPY:USA)`
- Period: `01/01/2024 - 06/21/2025`
- Rebalance: `Every Week`
- Position sizing: static weight, 20 ideal positions, 5% target position size
- Buy rules:
  - `Rank > 90`
  - `Close(0) > 1`
  - `AvgDailyTot(20) > 100000`
  - `1 = 1`
- Sell rules:
  - `Rank < 80`
  - three no-op placeholders: `0`, `0`, `0`

## Native Tier 2 Results

- Total return: `21.26%`
- Benchmark return: `27.39%`
- Active return: `-6.13%`
- Annualized return: `14.03%`
- Sharpe ratio: `0.23`
- Max drawdown: `-25.26%`
- Benchmark max drawdown: `-18.76%`
- Annual turnover: `96.97%`
- Overall winners: `27 / 58`, `46.55%`
- Correlation with SPY: `0.49`
- Final positions: `19`

## Interpretation

This baseline confirms the 2024-start validation strategy runs natively, but it is not a strong result. It made money, but it lagged SPY over the same period and had a low Sharpe ratio. The max drawdown was also slightly worse than the earlier `-25%` risk line we had been watching.

The useful takeaway is not that this baseline is ready. The useful takeaway is that the cloned model now has enough saved validation coverage to support native strategy tests back to the start of 2024, and the first clean 20-stock baseline did not beat the benchmark.

## Source Artifacts

- API ranking update response: `p123-output/ranking_update_api_system_2024_oos_20260525.json`
- Native strategy API details: `p123-output/native_strategy_1944189_details_20260525.json`

---

## Tags

#algo-trading/portfolio123 #algo-trading/ranking-systems #work/generated-artifacts #work/api-bridge
