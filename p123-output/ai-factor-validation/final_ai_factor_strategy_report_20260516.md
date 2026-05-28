---
title: "Portfolio123 AI Factor Strategy Search Report - 2026-05-16"
created_at: 2026-05-16 08:26 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-16
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for Portfolio123 AI Factor Strategy Search Report - 2026-05-16."
---

# Portfolio123 AI Factor Strategy Search Report - 2026-05-16

## Objective

Create native Portfolio123 simulated strategies using the previously identified best AI Factor model and test whether any defensible configuration can exceed both:

- CAGR > 20%
- Sharpe Ratio > 1.5

## Exact AI Factor Used

- AI Factor: `AI Factor Base 87 Features Andreas 2`
- Validation model display row: `extra trees medium 4 #2`
- Exact P123 formula from native dialog:

```text
AIFactorValidation("AI Factor Base 87 Features Andreas 2", "extra trees medium 4", "2")
```

## Required Validation Context

P123's native formula dialog required this validation context:

- Universe: `No OTC Exchange + min 10 mil No Finance2`
- Period: `06/22/2024 - 06/21/2025`
- Frequency: `Every Week`

Because this AI Factor uses Basic Holdout, the exact top model is only cleanly defensible over that one-year saved-validation window. Running this exact `#2` model through today is not valid because saved validation predictions stop on `06/21/2025`.

## Created P123 Objects

- Ranking system: `codex_ranking_ai_base87_et2_v1`, P123 id `545001`
- Simulated strategies:
  - `codex_strategy_ai_base87_et2_clean_v1`, P123 id `1941640`
  - `codex_strategy_ai_base87_et2_v2_conc10`, P123 id `1941642`
  - `codex_strategy_ai_base87_et2_v3_mid15`, P123 id `1941643`
  - `codex_strategy_ai_base87_et2_v4_smooth30`, P123 id `1941644`

All created objects use the required `codex_` prefix.

## Native Results

| Candidate | Positions | Buy/Sell | CAGR | Sharpe | Max DD | Turnover | Result |
|---|---:|---|---:|---:|---:|---:|---|
| `v2_conc10_rank95_sell85` | 10 target | `Rank > 95`, sell `Rank < 85` | 23.19% | 0.74 | -27.12% | 70.41% | CAGR pass, Sharpe fail |
| `v4_smooth30_rank90_sell80` | 30 | `Rank > 90`, sell `Rank < 80` | 21.62% | 0.77 | -24.83% | 72.19% | CAGR pass, Sharpe fail |
| `baseline_v1` | 20 | `Rank > 90`, sell `Rank < 80` | 19.16% | 0.80 | -24.65% | 73.97% | Near CAGR, Sharpe fail |
| `v3_mid15_rank95_sell85` | 15 target | `Rank > 95`, sell `Rank < 85` | 13.44% | 0.25 | -24.78% | 68.20% | Fail |

## Conclusion

No native simulated strategy met both requested thresholds for the exact top AI Factor validation model. Two variants exceeded 20% CAGR, but all variants had Sharpe ratios between 0.25 and 0.80, far below the 1.5 target.

The best CAGR candidate was `codex_strategy_ai_base87_et2_v2_conc10` at 23.19% CAGR, but its 0.74 Sharpe and -27.12% max drawdown make it a rejected candidate under the requested criteria.

The best Sharpe among tested candidates was the baseline at 0.80, but it did not clear 20% CAGR.

## Recommended Next Experiments

1. Test the through-today live Predictor branch using `AIFactor(...)` for `extra trees medium 4`, clearly labeled as a different model branch from the `#2` validation winner.
2. Re-train or configure a Rolling Time Series CV version of the same AI Factor with saved validation predictions to get a longer native validation window.
3. Test a Strategy Book or hedge/risk overlay only after deciding whether the one-year Basic Holdout window is too short for the original goal.
4. Compare the second-ranked AI Factor (`SCs Small and Micro Cap Focus + 10 Mil min Replic2`) because it may produce better portfolio-level Sharpe despite tying on model rank.

## Local Evidence

- DNA log: `p123-output/strategy_dna_log_20260516.csv`
- AI Factor verification: `p123-output/ai_factor_20015_verification_20260516.json`
- Formula validation: `p123-output/ai_factor_formula_validation_20260516.md`

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
