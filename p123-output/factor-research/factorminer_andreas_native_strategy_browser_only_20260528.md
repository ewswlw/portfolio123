---
title: "FactorMiner Andreas Browser-Only Native Strategy Test"
created_at: 2026-05-28 16:14 America/New_York
tags:
  - algo-trading/portfolio123
  - research/factors
  - native-validation
  - work/generated-artifacts
created: 2026-05-28
updated: 2026-05-28
description: "Browser-only Portfolio123 native simulated-strategy test using FactorMiner Andreas broad-run factors."
---

# FactorMiner Andreas Browser-Only Native Strategy Test

## Summary

Created and tested a native Portfolio123 simulated strategy from the FactorMiner broad-run factors using only the in-app Browser plugin. No Portfolio123 API calls were used.

Final saved P123 object:

| Field | Value |
|---|---|
| Strategy name | `codex_strategy_factorminer_andreas_v1_30w` |
| Strategy ID | `1945400` |
| URL | `https://www.portfolio123.com/port_summary.jsp?portid=1945400` |
| Universe | `No OTC Exchange + min 10 mil No Finance` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Ranking system | `Core Combination` |
| Period | `01/01/2006 - 05/28/2026` |
| Rebalance | Every Week |
| PIT method | Exclude prelims |

## Native Results

| Variant | Positions | Composite gate | Total return | Benchmark return | Annualized return | Max drawdown | Sharpe | Turnover | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Strict first pass | 7 current | `> 765` | 59.04% | 775.53% | 2.30% | -17.74% | 0.11 | 25.37% | Too restrictive; held too much cash. |
| Main 20-position pass | 20 | `> 700` | 2,027.91% | 775.53% | 16.15% | -47.22% | 0.79 | 89.37% | Fully invested but weak risk-adjusted result. |
| Concentrated pass | 10 | `> 700` | 1,166.27% | 775.53% | 13.24% | -54.02% | 0.62 | 73.63% | Concentration worsened return and drawdown. |
| Final diversified pass | 31 current | `> 700` | 2,096.27% | 775.53% | 16.33% | -48.24% | 0.81 | 96.27% | Best quick native variant, but still not strong. |

## Final Formula

This browser-only implementation used the FactorMiner winners as a composite buy rule with `Core Combination` as the native ranking/tie-break system. After these runs, I confirmed that the exact ranking-system opener is available at `/app/opener/RNK`; the next cleaner pass should create a dedicated `codex_` ranking system instead of encoding the signal only as buy-rule filters.

```text
(FRank("NetFCFPSTTM/Price")
+FRank("Price/PriceH")
+FRank("ROI%5YAvg")
+FRank("Close(60)/Close(120)")
+FRank("Pr26W%ChgInd")
+FRank("GrossProfitTTM/EV")
+FRank("OpIncGr%PYQ")
+FRank("Close(120)/Close(180)")
+(100-FRank("MedianVol(65)/SharesCur(0)"))) > 700
```

Additional buy rules:

```text
Close(0) > 2
AvgDailyTot(20) > 100000
```

Sell rules:

```text
Rank < 80
Close(0) < 1
0
```

## Findings

The broad FactorMiner run is useful for diagnosing alpha themes, but it did not translate into a strong standalone native simulated strategy through browser-only formula filters.

The first implementation issue was syntax: P123 requires `FRank()` formulas to be quoted strings. The unquoted first pass failed and was corrected.

The second issue was portfolio construction. A high composite gate left the model underinvested. Lowering the gate produced full investment and acceptable absolute return, but the strategy still had low Sharpe and very large drawdown.

The 30-position version was the best quick native variant. It beat SPY on total and annualized return over the full native period, but the Sharpe ratio of `0.81` and drawdown of `-48.24%` are not good enough to call this a best-possible production strategy.

## Tags

#algo-trading/portfolio123 #research/factors #native-validation #work/generated-artifacts
