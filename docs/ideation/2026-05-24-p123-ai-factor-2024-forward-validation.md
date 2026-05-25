Created: 2026-05-24 15:47 -04:00

# P123 AI Factor 2024-Forward Validation Ideation

## Focus

Find the best way to keep the underlying `AI Factor Base 87 Features Andreas 2` idea while creating a defensible strategy test that can begin around January 2024.

## Context

- Current AI Factor dataset: `2010-01-01` to `2025-06-21`.
- Current best validation branch: `extra trees medium 4 #2`.
- Current Basic Holdout validation window is only around `2024-06-22` to `2025-06-21`.
- Current live predictor branch is `extra trees medium 4`, not `extra trees medium 4 #2`.
- Native live predictor strategy was accepted only from `2026-01-19` forward in the prior verified run.
- Portfolio123 guidance in this workspace: use `AIFactorValidation(...)` for saved out-of-sample validation predictions; use `AIFactor(...)` only for live predictor testing.

## Ranked Ideas

### 1. Rolling Time Series CV Clone For 2024-Forward Validation

Create a new `codex_` AI Factor clone using the same universe, target, feature set, preprocessing, and `extra trees medium 4` model family, but switch validation to Rolling Time Series CV and explicitly save validation predictions.

Why it survives:

- Preserves the same strategy recipe while producing honest out-of-sample prediction windows.
- Gives a native P123 path to `AIFactorValidation(...)` strategy tests.
- Avoids pretending the 2026 live predictor existed in 2024.
- Lets the strategy begin on the first available saved prediction date, ideally near `2024-01-02`.

Tradeoffs:

- It will not be the exact same trained model as `extra trees medium 4 #2`.
- More compute cost and setup complexity than Basic Holdout.
- Exact start date depends on P123's fold/gap mechanics.

### 2. Time Series CV Clone With 2024-Focused Holdout Coverage

Create a clone using Time Series CV instead of Rolling Time Series CV, tuned so saved validation predictions cover 2024 onward.

Why it is plausible:

- Stronger than Basic Holdout for forward generalization.
- Simpler conceptual story than rolling windows.
- Good if the priority is past-to-future purity over maximum date coverage.

Why it ranks below option 1:

- May provide less continuous coverage than Rolling Time Series CV.
- Less aligned with the goal of strategy-style multi-year monitoring.

### 3. Historical Cutoff Clone Trained Only Through 2022

Try to create a clone whose training data ends before 2024, then create a predictor or validation test from there.

Why it is tempting:

- It sounds closest to "make the model live as of 2024."
- Easy to explain: train before 2024, test after 2024.

Why it is risky:

- P123 may still bind live predictor availability to the actual predictor creation date.
- It may not create a usable historical live `AIFactor(...)` path.
- Validation folds are more reliable than trying to force a live predictor into historical service.

### 4. Use Current Basic Holdout And Start Mid-2024

Keep the existing validation result and accept the saved prediction window as the test period.

Why it is useful:

- Already exists.
- Exact `extra trees medium 4 #2` branch can be tested via `AIFactorValidation(...)`.

Why it is not enough:

- It cannot honestly start on `2024-01-02`.
- The window is too short for a robust strategy conclusion.

## Recommendation

Use option 1: create a `codex_` clone with Rolling Time Series CV and saved validation predictions. Configure folds, training length, and gap so the first saved validation predictions start as close as P123 permits to `2024-01-02`, then build a native simulated strategy using `AIFactorValidation(...)`.

This is the best balance of preserving the underlying AI strategy idea and avoiding in-sample leakage.

## Open Checks Before Execution

- Confirm whether the existing AI Factor can be cloned cleanly or must be rebuilt from copied settings.
- Confirm the exact validation method fields P123 exposes for this account.
- Confirm estimated resource units before running validation.
- Confirm the exact first saved prediction date after training succeeds.
