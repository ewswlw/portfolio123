---
title: "AI Factor 28612 Validation Status"
created_at: 2026-05-25 13:10 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-25
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for AI Factor 28612 Validation Status."
---

# AI Factor 28612 Validation Status

AI Factor: `codex_ai_base87_etm4_2024_oos_v1`
AI Factor ID: `28612`
Checked: `2026-05-25`

## Dataset

- Dataset status: `SUCCESS`
- Dataset period: `2010-01-01` to `2025-06-21`
- Universe: `No OTC Exchange + min 10 mil No Finance2`
- Benchmark: `S&P 500 (SPY:USA)`
- Features: `87`
- Dataset load Resource Units: `21`
- Dataset load time: `1 min, 58 sec`

## Validation Model

- Model ID: `1117490`
- Model display: `extra trees medium 4 #2`
- Template: `extra trees medium 4`
- Name / duplicate ID: `2`
- Algorithm: `extratrees`
- Status: `SUCCESS`
- Worker: `Basic`
- Save validation predictions: `true`
- Model validation Resource Units: `3`
- Task log:
  - `2026-05-24 15:29:01` STARTED
  - `2026-05-24 15:29:07` Fitting model
  - `2026-05-24 15:41:57` Making predictions
  - `2026-05-24 15:42:02` COMPLETED

## Saved Prediction Window

- `12/23/2023` to `06/21/2025`

## Model Stats

- RMSE: `1.6245718566564669`
- R2: `0.02914989619017394`
- Pearson: `0.17775947909638617`
- Spearman: `0.1864269005796416`
- High-low mean: `57.90198265817457`
- High-low Sharpe: `1.5798585653653556`
- High bucket mean: `24.344687142229816`
- High bucket Sharpe: `1.0089386868194559`
- High bucket turnover: `596`

## Formula To Use Next

```text
AIFactorValidation("codex_ai_base87_etm4_2024_oos_v1", "extra trees medium 4", "2")
```

For a ranking node, wrap or blend it as needed, for example:

```text
FRank(AIFactorValidation("codex_ai_base87_etm4_2024_oos_v1", "extra trees medium 4", "2"))
```

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
