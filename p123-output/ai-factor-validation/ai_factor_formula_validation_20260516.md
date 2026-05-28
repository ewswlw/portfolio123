---
title: "AI Factor Formula Validation - 2026-05-16"
created_at: 2026-05-16 07:55 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-16
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for AI Factor Formula Validation - 2026-05-16."
---

# AI Factor Formula Validation - 2026-05-16

## Source

- AI Factor: `AI Factor Base 87 Features Andreas 2`
- AI Factor id: `20015`
- Validation model row: `extra trees medium 4 #2`
- P123 model rank: `100`
- Source route: `https://www.portfolio123.com/sv/aiFactor/20015/validation/models`

## Exact P123 Formula

P123's Validation Prediction Formula dialog gives:

```text
AIFactorValidation("AI Factor Base 87 Features Andreas 2", "extra trees medium 4", "2")
```

This differs from the display row `extra trees medium 4 #2`; P123 encodes the duplicate/run suffix as a third argument, not as part of the second model-name argument.

## Required Native Context

P123 states the backtest must use the same:

- Universe: `No OTC Exchange + min 10 mil No Finance2`
- Period: `06/22/2024 - 06/21/2025`
- Frequency: `Every Week`

## Implications

- Use `AIFactorValidation(...)`, not live `AIFactor(...)`, for this model's validation-period strategy test.
- The longest defensible native strategy window for this exact top validation model is currently `06/22/2024 - 06/21/2025`, unless a different model, predictor, or retrained validation method is approved later.
- The Predictors tab lists `extra trees medium 4` but not `extra trees medium 4 #2`, so using live `AIFactor(...)` would not reference the exact top model found earlier.
- The formula has been verified from P123's native formula dialog, but full simulated-strategy integration still needs a native strategy/ranking object using this formula.

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
