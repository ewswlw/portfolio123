---
title: "FactorMiner: Andreas and portfolio123"
created_at: 2026-05-28 15:09 America/New_York
tags:
  - algo-trading/portfolio123
  - research/factors
  - work/generated-artifacts
created: 2026-05-28
updated: 2026-05-28
description: "Generated Portfolio123 factor research artifact for FactorMiner: Andreas and portfolio123."
---

# FactorMiner: Andreas and portfolio123

Source: Portfolio123 FactorMiner for factor list 3027, dataset "Andreas and portfolio123".

## Tool Surface Observed

FactorMiner supports:

- Your Results: completed analysis table with run date, universe, best-factor count, rows, average alpha, period, dataset creation time, parameters, status, and notes.
- New Analysis: selects Rank By Annual Alpha or IC; high/low quantile percentages; max return filter; auto-detect factor direction; min annual alpha or IC threshold; max factors; max NA; correlation threshold; use-last-settings; run analysis.
- Result detail: Settings, Best Factors, All Factors, Correlations, Logs, notes, copy-to-clipboard, CSV download.
- About: explains univariate factor analysis, benchmark alpha/beta, tail-weighted IC, t-statistics, high/low quantile returns, and correlation-based best-factor selection.

## Active Broad Run

- Result: analysis_2
- Run: 2026-05-28 19:01 UTC
- Dataset generated: 2026-05-28 18:59 UTC
- Universe: No OTC Exchange + min 10 mil No Finance
- Period: 2006-01-01 to 2026-05-26
- Frequency: 4 weeks
- Rows: 656,988
- Benchmark: S&P 500 (SPY:USA)
- Benchmark return: 748.89% cumulative, 11.09% annualized
- Settings: Annual Alpha, max 10 factors, min annual alpha 0.5%, max correlation 0.5, high/low 10%, max return 200%, max NA 40%, auto-detect direction
- Status: Success; found 10 of 10 requested best factors; 8 factors excluded by NAs

### Broad Run Best Factors

| Rank | Factor | Formula | Direction | H-L Alpha % | H-L Beta | H-L T-Stat | Tail-Weighted IC | IC t-stat | Ann. High Qtl % | Ann. Low Qtl % | NA % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Free Cash Flow to Price | NetFCFPSTTM / Price | High better | 58.33 | -0.106 | 9.14 | 0.0966 | 13.82 | 15.72 | -29.58 | 11.15 |
| 2 | Price to 52-week high | Price / PriceH | High better | 57.64 | -0.766 | 4.91 | 0.1085 | 10.49 | 10.86 | -29.42 | 0.06 |
| 13 | share turnover, 3 months | MedianVol(65)/SharesCur(0) | Low better | 42.05 | -0.896 | 4.29 | 0.0308 | 3.70 | 1.22 | -25.72 | 0.08 |
| 19 | ROI%5YAvg | ROI%5YAvg | High better | 33.65 | -0.304 | 5.17 | 0.0902 | 11.37 | 8.92 | -19.00 | 23.71 |
| 22 | 3MoRet3MoAgo | Close(60) / Close(120) | High better | 31.96 | -0.244 | 5.73 | 0.0515 | 9.07 | 2.91 | -22.65 | 2.87 |
| 23 | Pr26W%ChgInd | Pr26W%ChgInd | High better | 31.69 | -0.403 | 4.93 | 0.0416 | 6.84 | 13.84 | -11.76 | 0.00 |
| 28 | Gross Profit to EV | GrossProfitTTM / EV | High better | 30.56 | -0.079 | 7.69 | 0.0472 | 9.86 | 8.77 | -17.34 | 14.10 |
| 29 | subindustry momentum | Aggregate("TotalReturn",#subindustry) | High better | 30.44 | -0.380 | 4.64 | 0.0532 | 8.14 | 9.38 | -15.21 | 0.51 |
| 30 | OpIncGr%PYQ | OpIncGr%PYQ | High better | 29.21 | -0.084 | 9.61 | 0.0444 | 13.27 | 14.95 | -11.35 | 5.97 |
| 36 | 3MoRet6MoAgo | Close(120) / Close(180) | High better | 26.66 | -0.181 | 5.33 | 0.0490 | 8.91 | 2.12 | -19.99 | 4.43 |

## Prior S&P 500 Run

- Result: analysis_1
- Run: 2026-05-26 17:32 UTC
- Universe: S&P500 LargeCap (IVV)
- Period: 2006-01-01 to 2026-05-26
- Frequency: Weekly
- Rows: 528,591
- Benchmark return: 733.25% cumulative, 10.97% annualized
- Status: Success; found 10 of 10 requested best factors; 0 factors excluded by NAs

### S&P 500 Best Factors

| Rank | Factor | Direction | H-L Alpha % | H-L Beta | H-L T-Stat | Tail-Weighted IC | IC t-stat | Ann. High Qtl % | Ann. Low Qtl % | NA % |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Beta5Y | Low better | 9.30 | -1.199 | -0.81 | 0.0020 | 0.21 | 9.54 | 9.61 | 0.97 |
| 3 | EPS Estimate Revision CQ | High better | 7.78 | -0.264 | 1.30 | 0.0148 | 4.30 | 13.87 | 7.14 | 0.40 |
| 6 | 160, close(0)/close(160) | High better | 7.54 | -0.621 | -0.04 | 0.0094 | 1.29 | 11.88 | 7.62 | 0.27 |
| 7 | EPS Estimate Variability CQ | Low better | 7.38 | -0.478 | 0.32 | 0.0119 | 2.39 | 9.89 | 5.19 | 0.36 |
| 9 | unlevered free cash flow to EV | High better | 6.74 | 0.095 | 2.78 | 0.0110 | 2.61 | 14.31 | 6.52 | 1.34 |
| 11 | ROA%Q | High better | 6.60 | -0.418 | 0.31 | 0.0134 | 2.66 | 12.58 | 8.16 | 0.31 |
| 12 | EV2SalesTTM | Low better | 6.34 | -0.061 | 1.63 | 0.0045 | 0.93 | 12.66 | 6.60 | 0.91 |
| 14 | Institutional Ownership vs industry | Low better | 6.32 | -0.166 | 1.65 | 0.0028 | 0.79 | 12.66 | 7.12 | 1.91 |
| 15 | EPS current quarter growth | High better | 6.27 | -0.146 | 1.05 | 0.0168 | 3.57 | 13.48 | 7.00 | 1.10 |
| 20 | velocity | High better | 5.96 | -0.174 | 0.96 | 0.0180 | 2.85 | 9.67 | 4.55 | 0.78 |

## Interpretation

The broad no-financials universe produced much stronger factor spreads than the S&P 500 run. The broad run's strongest signals were value/cash-flow yield, relative price strength or distance from prior highs, quality/profitability, intermediate momentum, low turnover/low-risk behavior, and industry momentum. The S&P 500 run was weaker and more defensive: low beta/volatility, estimate revisions, valuation, quality, and momentum survived, but alpha spreads were much smaller and several t-stats were weak.

FactorMiner's "Best Factors" are not just the top 10 raw alpha ranks. The broad run skipped many high-ranked candidates because of correlation conflicts, including ROE%5YAvg vs ROI%5YAvg, unlevered FCF/EV vs FCF/Price, EMA and close-ratio momentum vs Price-to-52-week-high, and Short Interest vs share turnover. This left a more diversified factor set across value, quality, momentum, industry momentum, and trading-liquidity/risk.

These are FactorMiner diagnostics, not native simulated-strategy or Strategy Book results.

---

## Tags

#algo-trading/portfolio123 #research/factors #work/generated-artifacts
