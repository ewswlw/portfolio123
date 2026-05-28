---
title: "P123 AI Factor 2024-Forward Validation Plan"
tags:
  - algo-trading/portfolio123
  - work/plans
created: 2026-05-24
updated: 2026-05-28
description: "Portfolio123 implementation plan covering scope, workflow, validation, and deliverables for P123 AI Factor 2024-Forward Validation Plan."
---

# P123 AI Factor 2024-Forward Validation Plan

## Objective

Create a defensible Portfolio123 AI Factor validation workflow that keeps the underlying `AI Factor Base 87 Features Andreas 2` recipe but allows a native simulated strategy to begin as close as Portfolio123 permits to `2024-01-02`.

This is not a plan to make the existing 2026 live predictor appear live in 2024. The plan uses saved out-of-sample validation predictions through `AIFactorValidation(...)`.

Origin: `docs/ideation/2026-05-24-p123-ai-factor-2024-forward-validation.md`

## Core Decision

Use a two-run validation design:

1. **2024-focused saved-prediction run**: tune the validation setup so the saved prediction window starts near `2024-01-02`.
2. **Robustness run**: run a broader Rolling Time Series CV setup to test whether the same AI Factor recipe works across more than one historical regime.

Why two runs: the 2024 start-date goal and the broad robustness goal pull in different directions. A setup calibrated to start near 2024 may not produce many folds; a robust Rolling CV setup may start much earlier than 2024.

## Scope

In scope:

- Use Portfolio123 browser workflow.
- Keep the same conceptual recipe:
  - Universe: `No OTC Exchange + min 10 mil No Finance2`
  - Benchmark: `S&P 500 (SPY:USA)`
  - Target: `3MTotReturn`
  - Target normalization: `Date`
  - Feature set: current 87-feature Andreas setup
  - Model family: `extra trees medium 4`
- Create new `codex_` AI Factor, ranking, and simulated-strategy objects.
- Use native P123 validation and native simulated strategy results.
- Save outputs under `p123-output/`.

Out of scope:

- No live trading or live rebalance actions.
- No deletion of existing AI Factors, trained models, strategies, ranking systems, or universes.
- No claim that current `AIFactor(...)` live predictor results are valid from 2024.
- No local Python backtest as substitute for native P123 validation.

## Phase 1: Baseline Capture

Goal: preserve the current recipe before creating new objects.

Actions:

- Open `AI Factor Base 87 Features Andreas 2`.
- Capture:
  - AI Factor name and ID.
  - Dataset period.
  - target and target normalization.
  - training universe and benchmark.
  - preprocessing settings.
  - features or imported feature source.
  - current validation method.
  - current `extra trees medium 4 #2` result and formula-dialog syntax.
  - predictor list and live predictor date constraints.
- Save a baseline report:
  - `p123-output/ai_factor_20015_baseline_20260524.md`
  - `p123-output/ai_factor_20015_baseline_20260524.json`

Verification:

- Confirm the exact universe remains `No OTC Exchange + min 10 mil No Finance2`.
- Confirm the benchmark remains `S&P 500 (SPY:USA)`.
- Confirm the current exact validation formula for the `#2` branch is copied from the P123 formula dialog, not inferred from the row name.

## Phase 2: Create The 2024-Focused AI Factor Clone

Goal: produce saved validation predictions that can power a native simulated strategy starting near `2024-01-02`.

Proposed object name:

- `codex_ai_base87_etm4_2024_oos_v1`

Setup:

- Clone or recreate the current AI Factor settings.
- Keep the same universe, target, feature set, preprocessing, and `extra trees medium 4` model family.
- Configure the validation method to make the first saved prediction date land as close as possible to `2024-01-02`.
- Candidate settings to test in the P123 Method tab:
  - Training period: approximately 13 years if dataset starts `2010-01-01`.
  - Gap: enough to avoid target overlap, ideally 26 to 52 weeks.
  - Holdout/validation coverage: from early 2024 through the latest available 2025 validation date.

Important constraint:

- Before starting any validation that spends resource units, summarize the worker choice, estimated resource use, and settings, then ask for confirmation.

Verification:

- P123 must show saved validation predictions beginning near the target start date.
- The model row must show `SUCCESS`.
- The validation training dialog must have `Save Validation Predictions = Yes`.
- If P123 reports a different prediction window, record the exact start and end dates and use those as binding.

## Phase 3: Create The Robustness AI Factor Clone

Goal: test whether the same recipe works across multiple folds/regimes, even if the first prediction date is earlier than 2024.

Proposed object name:

- `codex_ai_base87_etm4_rolling_oos_v1`

Setup:

- Same recipe as Phase 2.
- Validation method: Rolling Time Series CV.
- Initial candidate configuration:
  - Training period: 5 to 7 years.
  - Gap: 52 weeks, or 26 weeks only if P123 constraints make 52 weeks too restrictive.
  - Holdout period: long enough to cover multiple folds.
  - Folds: enough to cover several market regimes without exploding resource use.
- Save validation predictions explicitly.

Verification:

- Confirm prediction window and fold coverage from P123.
- Compare Lift, Return, and Compare All diagnostics across first half and second half.
- Reject the model as fragile if performance is only strong in one fold or one half.

## Phase 4: Build Ranking Systems

Goal: turn saved AI Factor predictions into native P123 ranking systems without editing existing user objects.

Objects:

- `codex_ranking_ai_base87_2024_oos_v1`
- `codex_ranking_ai_base87_rolling_oos_v1`

Formula guidance:

- Use `AIFactorValidation(...)`, not `AIFactor(...)`.
- Copy exact formula strings from the P123 validation formula dialog.
- If P123 creates duplicate model syntax, preserve third-argument syntax like:

```text
AIFactorValidation("AI Factor Name", "model name", "2")
```

Ranking variants:

- Pure AI rank: 100% AI Factor.
- Operational blend: 95% AI Factor / 5% classic quality kicker.

Verification:

- Ranking system saves without formula errors.
- Ranking performance date range is entirely inside the saved prediction window.
- Any "No predictions are available" error is used to correct the date range, not ignored.

## Phase 5: Build Native Simulated Strategies

Goal: test the saved predictions in native P123 simulated strategies.

Objects:

- `codex_strategy_ai_base87_2024_oos_pure_v1`
- `codex_strategy_ai_base87_2024_oos_blend_v1`
- `codex_strategy_ai_base87_rolling_oos_pure_v1`
- `codex_strategy_ai_base87_rolling_oos_blend_v1`

Baseline strategy settings:

- Universe: `No OTC Exchange + min 10 mil No Finance2`.
- Benchmark: `S&P 500 (SPY:USA)`.
- Start date: first valid saved prediction date, ideally `2024-01-02` for the 2024-focused run.
- End date: final valid saved prediction date.
- Position counts: test at least 10, 20, and 30 holdings if resource/time permits.
- Rebalance: weekly or the frequency matching the saved prediction cadence.
- Slippage: realistic, not zero.
- Liquidity rules: consistent with the current universe and strategy constraints.

Verification:

- Review page confirms correct universe, ranking system, dates, position count, rebalance frequency, buy/sell rules, and slippage before running.
- Native P123 run completes without prediction-window errors.
- Each serious candidate is saved separately; do not overwrite one strategy repeatedly.

## Phase 6: Evaluate And Decide

Primary metrics:

- Annualized return.
- Excess return versus SPY.
- Excess return versus eligible universe where available.
- Sharpe ratio.
- Max drawdown.
- Turnover.
- Hit/decile behavior from Lift/Return/Compare diagnostics.

Interpretation rules:

- Treat the 2024-focused run as the answer to: "Could this strategy have started around 2024?"
- Treat the Rolling CV run as the answer to: "Is this recipe robust across multiple regimes?"
- Do not declare the strategy successful unless native P123 simulated strategy results support it.
- Label every result by source:
  - native simulated strategy,
  - ranking performance,
  - AI Factor validation diagnostics,
  - live predictor branch.

Output artifacts:

- `p123-output/ai_factor_2024_oos_validation_20260524.md`
- `p123-output/ai_factor_2024_oos_strategy_dna_20260524.csv`
- `p123-output/ai_factor_rolling_oos_validation_20260524.md`
- `p123-output/final_ai_factor_2024_forward_report_20260524.md`

## Stop Conditions

Stop and ask for direction if:

- P123 cannot clone or recreate the feature set without manual user action.
- P123 estimates unexpectedly high resource-unit usage.
- Validation method settings cannot produce predictions near `2024-01-02`.
- Saved prediction windows do not overlap the requested simulation window.
- Native simulated strategy results are materially worse than validation diagnostics imply.

## Success Criteria

Minimum successful plan outcome:

- A `codex_` AI Factor with saved validation predictions that can be used in `AIFactorValidation(...)`.
- A native simulated strategy that starts as close as possible to `2024-01-02`.
- A report stating exact prediction windows, strategy windows, metrics, and whether the 2024-forward thesis survived.

Strong successful outcome:

- The 2024-focused strategy is positive versus SPY and the eligible universe.
- The robustness run shows persistent top-bucket strength across folds or halves.
- Turnover and drawdown are practical enough to justify further strategy development.

---

## Tags

#algo-trading/portfolio123 #work/plans
