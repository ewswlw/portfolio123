---
title: "AI Factor 20015 Baseline"
created_at: 2026-05-24 15:47 -04:00
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-24
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for AI Factor 20015 Baseline."
---

# AI Factor 20015 Baseline

## Source

Portfolio123 browser capture on 2026-05-24.

## AI Factor

- ID: 20015
- Name: AI Factor Base 87 Features Andreas 2
- Universe: No OTC Exchange + min 10 mil No Finance2
- Benchmark: S&P 500 (SPY:USA)
- Target: 3MTotReturn
- Target normalization: Date
- Formula: Future%Chg_D(65)
- Dataset period: 2010-01-01 to 2025-06-21 (15.5 years)
- Frequency: Every Week
- Features: 87
- Scaling: Z-Score
- Trim: 7.5%
- Outlier handling: clip, limit 5
- Validation method: Basic Holdout
- Gap: 52 weeks
- Training period: 13.5 years
- Holdout period: 12 months

## Exact Validation Formula

Copied from Portfolio123's Validation Prediction Formula dialog:

```text
AIFactorValidation("AI Factor Base 87 Features Andreas 2", "extra trees medium 4", "2")
```

Binding context from the dialog:

- Universe: No OTC Exchange + min 10 mil No Finance2
- Period: 06/22/2024 - 06/21/2025
- Frequency: Every Week

## Key Validation Rows

```text
 |  | Model | details | Rank | Validation | Resource Units | Update Date
 |  | extra trees I 𝑓𝑥 #random #multithreaded Predefined | show | 23 | SUCCESS Basic: 3 min, 49 sec (1.7 GB) | 1 | 10/21/2025
 |  | extra trees I - gotlessp 𝑓𝑥 #random #multithreaded Custom | show | 11 | SUCCESS Basic: 57 sec (1.7 GB) | 1 | 10/21/2025
 |  | extra trees II 𝑓𝑥 #random #multithreaded Predefined | show | 82 | SUCCESS Basic: 13 min, 10 sec (1.7 GB) | 1 | 10/21/2025
 |  | extra trees III 𝑓𝑥 #random #multithreaded Predefined | show | 82 | SUCCESS Basic: 54 min, 22 sec (2.7 GB) | 1 | 10/21/2025
 |  | extra trees III - Deepseek 𝑓𝑥 #random #multithreaded Custom | show | 5 | SUCCESS Basic: 5 min, 51 sec (1.8 GB) | 1 | 10/21/2025
 |  | extra trees III - GPT 𝑓𝑥 #random #multithreaded Custom | show | 88 | SUCCESS Basic: 44 min, 48 sec (1.8 GB) | 1 | 10/21/2025
 |  | extra trees III - TOF 𝑓𝑥 #random #multithreaded Custom | show | 82 | SUCCESS Basic: 12 min, 57 sec (2.0 GB) | 1 | 10/21/2025
 |  | extra trees medium 4 #2 𝒇𝒙 #random #multithreaded Predefined | show | 100 | SUCCESS Basic: 28 min, 14 sec (1.8 GB) | 3 | 4/16/2026
 |  | extra trees medium 4 𝑓𝑥 #random #multithreaded Predefined | show | 94 | SUCCESS Basic: 28 min, 9 sec (1.8 GB) | 1 | 10/21/2025
 |  | lightgbm I 𝑓𝑥 #random #multithreaded Predefined | show | 47 | SUCCESS Basic: 42 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II 𝑓𝑥 #random #multithreaded Predefined | show | 17 | SUCCESS Basic: 1 min, 17 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II - deepseek 𝑓𝑥 #random #multithreaded Custom | show | 35 | SUCCESS Basic: 1 min, 37 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II - deepseek 3 𝑓𝑥 #random #multithreaded Custom | show | 58 | SUCCESS Basic: 4 min, 41 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II - GPT 6/6 𝑓𝑥 #random #multithreaded Custom | show | 41 | SUCCESS Basic: 3 min, 21 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II - GPT1 𝑓𝑥 Custom | show | 64 | SUCCESS Basic: 1 min, 56 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm II - TOF 𝑓𝑥 #random #multithreaded Custom | show | 52 | SUCCESS Basic: 2 min, 13 sec (2.4 GB) | 1 | 10/21/2025
 |  | lightgbm III 𝑓𝑥 #random #multithreaded Predefined | show | 29 | SUCCESS Basic: 2 min, 23 sec (2.4 GB) | 1 | 10/21/2025
```

## Predictors

```text
 |  | Name | details | Training Period | Train | Resource Units | Update Date
 |  | extra trees III - TOF 𝒇𝒙 #random #multithreaded Custom | show | 2005-01-01 to 2020-05-01 | SUCCESS Basic: 11 min, 31 sec (1.7 GB) | 7 | 10/21/2025
 |  | extra trees medium 4 𝒇𝒙 #random #multithreaded Predefined | show | 2010-01-01 to 2025-06-21 | SUCCESS Basic: 18 min, 43 sec (1.9 GB) | 4 | 1/18/2026
 |  | lightgbm II - GPT 6/6 𝒇𝒙 #random #multithreaded Custom | show | 2005-01-01 to 2020-01-01 | SUCCESS Basic: 2 min, 22 sec (2.0 GB) | 1 | 10/21/2025
 |  | lightgbm medium 3 𝒇𝒙 #random #multithreaded Predefined | show | 2005-01-01 to 2020-01-01 | SUCCESS Basic: 1 min, 47 sec (2.0 GB) | 1 | 10/21/2025
```

## Compare Rows

```text
 | Accuracy | H−L | High | Low
 |  | Model | Rank | RMSE | Spearman | Avg% | SR | SD | Avg% | SR | SD | Turn% | Avg% | SR | SD | Turn%
 |  | extra trees medium 4 #2 | 100 | 1.6371 | 0.1671 | 58.86 | 1.50 | 31.06 | 31.03 | 1.11 | 24.52 | 567 | -17.66 | -0.42 | 45.92 | 667
 |  | extra trees medium 4 | 94 | 1.6373 | 0.1671 | 66.83 | 1.73 | 29.79 | 33.78 | 1.18 | 24.76 | 550 | -19.98 | -0.49 | 45.47 | 669
 |  | extra trees III - GPT | 88 | 1.6371 | 0.1681 | 56.27 | 1.38 | 32.59 | 29.69 | 1.06 | 24.62 | 511 | -17.14 | -0.40 | 46.62 | 577
 |  | extra trees III | 82 | 1.6379 | 0.1621 | 57.14 | 1.65 | 27.52 | 30.99 | 1.08 | 25.05 | 665 | -16.77 | -0.41 | 44.26 | 754
 |  | extra trees II | 82 | 1.6374 | 0.1676 | 55.98 | 1.38 | 32.44 | 27.39 | 1.00 | 24.32 | 528 | -18.47 | -0.43 | 46.95 | 576
 |  | extra trees III - TOF | 82 | 1.6373 | 0.1680 | 55.80 | 1.37 | 32.46 | 27.83 | 1.00 | 24.56 | 565 | -18.09 | -0.43 | 46.69 | 606
 |  | lightgbm II - GPT1 | 64 | 1.6372 | 0.1564 | 49.30 | 1.38 | 29.09 | 24.93 | 0.86 | 25.94 | 945 | -16.44 | -0.40 | 45.18 | 703
 |  | lightgbm II - deepseek 3 | 58 | 1.6393 | 0.1503 | 62.91 | 1.93 | 25.40 | 30.34 | 0.92 | 28.82 | 1,179 | -20.16 | -0.52 | 43.59 | 812
 |  | lightgbm II - TOF | 52 | 1.6389 | 0.1519 | 58.57 | 1.78 | 25.94 | 26.65 | 0.86 | 27.46 | 1,147 | -20.29 | -0.52 | 43.64 | 810
 |  | lightgbm I | 47 | 1.6377 | 0.1534 | 51.71 | 1.47 | 28.55 | 25.10 | 0.84 | 26.66 | 979 | -17.67 | -0.43 | 45.14 | 744
 |  | lightgbm II - GPT 6/6 | 41 | 1.6380 | 0.1544 | 53.70 | 1.52 | 28.38 | 30.74 | 0.99 | 27.01 | 999 | -15.05 | -0.36 | 45.10 | 736
 |  | lightgbm II - deepseek | 35 | 1.6406 | 0.1484 | 58.34 | 1.82 | 25.31 | 30.83 | 0.97 | 27.78 | 1,193 | -17.51 | -0.43 | 44.38 | 833
 |  | lightgbm III | 29 | 1.6380 | 0.1546 | 46.01 | 1.32 | 28.82 | 31.85 | 1.05 | 26.41 | 907 | -9.77 | -0.23 | 45.32 | 720
 |  | extra trees I | 23 | 1.6389 | 0.1669 | 36.54 | 0.90 | 34.61 | 24.85 | 0.94 | 23.62 | 574 | -8.61 | -0.19 | 47.77 | 551
 |  | lightgbm II | 17 | 1.6399 | 0.1488 | 43.84 | 1.37 | 26.66 | 24.89 | 0.80 | 27.72 | 1,145 | -13.26 | -0.31 | 45.16 | 807
 |  | extra trees I - gotlessp | 11 | 1.6439 | 0.1692 | 35.80 | 0.83 | 36.98 | 22.69 | 0.91 | 22.63 | 781 | -9.71 | -0.21 | 48.82 | 597
 |  | extra trees III - Deepseek | 5 | 1.6476 | 0.1673 | 31.03 | 0.69 | 39.04 | 20.95 | 0.96 | 19.91 | 609 | -7.73 | -0.17 | 48.68 | 544
```

## Return Rows

```text
Return Statistics | Entire Period 6/22/2024 to 6/28/2025 | First Half 6/22/2024 to 12/27/2024 | Second Half 12/28/2024 to 6/28/2025
Bucket 10 Compounded | 27.19% | 55.90% | 2.96%
Average | 31.03% | 59.76% | 6.57%
Estimate | 20.59% | 37.82% | 5.08%
Avg Stocks | 198 | 202 | 194
Annualized Turnover | 567% | 546% | 590%
Bucket 1 Compounded | -25.88% | -4.85% | -42.82%
Average | -17.66% | 5.65% | -36.52%
Estimate | -2.18% | 7.08% | -9.85%
Avg Stocks | 199 | 203 | 195
Annualized Turnover | 667% | 654% | 681%
rs - Spearman's Rank Correlation Coefficient | 0.38 | 0.55 | -0.15
r - Pearson Correlation Coefficient | 0.53 | 0.56 | 0.32
Slope (change per quantile) | 2.530% | 3.415% | 1.659%
X Intercept | 1.86 | -1.07 | 6.94
```

## Execution Notes

- This baseline is read-only; no P123 account objects were created, edited, trained, or deleted.
- Existing live predictor branch is `extra trees medium 4`, while the exact top validation branch is `extra trees medium 4 #2` encoded as the third `AIFactorValidation` argument.
- The exact validation window is not valid through today; it is limited to saved predictions from 06/22/2024 to 06/21/2025.

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
