---
title: Portfolio123 AI Factor Clone Validation Setup Workflow
date: 2026-05-25
created_at: 2026-05-25 12:57 America/New_York
last_updated: 2026-05-25
category: workflow-issues
module: Portfolio123 AI Factor validation setup
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Cloning an existing Portfolio123 AI Factor to create a new out-of-sample validation window"
  - "Loading an AI Factor dataset before starting selected validation models"
  - "Starting a single AI Factor validation model while preserving saved validation predictions"
  - "Estimating and confirming P123 Resource Units before resource-spending browser actions"
tags:
  - portfolio123
  - ai-factor
  - validation
  - clone-workflow
  - resource-units
  - saved-predictions
  - basic-holdout
  - browser-automation
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-25
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 AI Factor Clone Validation Setup Workflow."
---

# Portfolio123 AI Factor Clone Validation Setup Workflow

## Context

When a user wants to keep an existing Portfolio123 AI Factor design but move the validation/live-test window earlier, the safest path is to clone the AI Factor and run a new validation model, rather than changing the original factor or pretending an existing validation model can support a different date window.

This learning was captured while creating a clone of `AI Factor Base 87 Features Andreas 2` so the `extra trees medium 4 #2` branch could be re-run with a longer Basic Holdout window intended to produce earlier out-of-sample saved predictions.

Verified clone:

```text
Name: codex_ai_base87_etm4_2024_oos_v1
AI Factor ID: 28612
URL: https://www.portfolio123.com/sv/aiFactor/28612/overview
```

## Guidance

Use a clone when changing validation geometry. Keep the original AI Factor untouched, create a `codex_` clone, then perform dataset loading and model starts only after confirming Resource Units and the exact target model.

Important setup details from the verified run:

| Item | Observed value |
|---|---|
| Source dataset period | `2010-01-01 to 2025-06-21` |
| Universe | `No OTC Exchange + min 10 mil No Finance2` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Frequency | `Every Week` |
| Features | `87` |
| Dataset size | `~545MB (~155.5M data points)` |
| Load cost shown by P123 | `21 Resource Units` |
| P123 conversion | `1 Resource Unit = 25MB` |
| Load time | `1 min, 58 sec` |

Before loading the dataset, P123 opened a confirmation dialog with this operational warning:

```text
You will not be able to change any Settings once you start loading the Dataset.
```

That means the agent must treat dataset loading as a boundary. Confirm the cloned AI Factor's target, universe, feature set, dataset period, validation method, and expected Resource Units before starting the load.

For this workflow, leave Target Information Regression disabled unless the user explicitly needs that optional diagnostic. It can lengthen load time on large datasets and is not required for using saved AI Factor validation predictions in a later ranking/simulation workflow.

## Method Setup

The intended validation shape was:

```text
Method: Basic Holdout
Gap: 52 weeks
Holdout Period: 18.0 months
Displayed Training Period: 13 years
```

P123 did not show a visible Save or Apply control on the Method tab. Before the dataset was loaded, changing Holdout from `12.0` to `18.0` temporarily updated the displayed Training Period but reverted after navigation/reload.

After the dataset was loaded, the Method tab still allowed the Holdout field to be changed. The verified sequence was:

1. Open `/sv/aiFactor/28612/validation/method`.
2. Confirm `Gap = 52`.
3. Change `Holdout Period` from `12.0` to `18.0`.
4. Press Tab or otherwise blur the field.
5. Confirm the page displays `Training Period = 13 years`.
6. Navigate directly to `/sv/aiFactor/28612/validation/models` and start the intended model from that state.

Do not assume the Method edit has persisted across future reloads unless P123 later confirms it through the finished validation model's own metadata or result window.

## Model Start

On the Models page, start only the intended row. In the verified run, the target row was:

```text
extra trees medium 4 #2
```

Clicking the row's `Start` button opened:

```text
Validate Model - Choose Worker(s)
```

The dialog showed the target model as:

```text
CPU Model: extra trees medium 4 #2
Worker: least expensive
```

The dialog also included `Save Validation Predictions` with `Yes` and `No` radio buttons. In the verified run, neither option appeared checked initially through browser inspection, so the agent explicitly selected:

```text
Save Validation Predictions: Yes
```

This is the key gotcha. Without saved validation predictions, the run may still train/validate, but it will not provide the clean saved-prediction surface needed for a later native strategy test using `AIFactorValidation(...)`.

After starting, P123 showed the expected transition:

```text
WAITING...
IN PROGRESS... Basic
```

The final authenticated check later confirmed the model completed successfully:

```text
extra trees medium 4 #2
Status: SUCCESS
Save Validation Predictions: true
Validation date range: 12/23/2023 - 06/21/2025
Resource Unit Cost: 3
```

The exact validation formula produced by this completed clone/model branch is:

```text
AIFactorValidation("codex_ai_base87_etm4_2024_oos_v1", "extra trees medium 4", "2")
```

For ranking-system use, wrap that in `FRank(...)` when the strategy should buy the highest predicted names:

```text
FRank(AIFactorValidation("codex_ai_base87_etm4_2024_oos_v1", "extra trees medium 4", "2"))
```

The final model logs showed the successful sequence: fitting model, making predictions, generating report, storing result, and `COMPLETED`.

## Why This Matters

AI Factor model setup has two different kinds of cost and state:

- dataset loading cost, shown before the load (`21 Resource Units` in this run);
- model validation/training execution state, shown later on the Models table.

An agent should not blur these together or treat Resource Units as dollars. P123 displayed Resource Units, not an explicit cash charge. Whether that maps to out-of-pocket cost depends on the user's plan and quota.

The saved-prediction choice is also easy to miss because it appears inside the worker-selection dialog, not on the model table. For strategy research, saved validation predictions are the bridge between the ML validation run and later native P123 strategy testing.

Finally, the Method tab's no-visible-save behavior means agents should verify what P123 actually accepts. If the field value only changes the current UI state until the validation start workflow consumes it, the defensible record is the finished validation model's own metadata and resulting prediction window, not the transient form value.

## When to Apply

- When the user wants a live-test or validation window starting earlier than an existing AI Factor validation model supports.
- When preserving the original AI Factor matters.
- When an AI Factor clone shows `Dataset not loaded`.
- When the next action will spend P123 Resource Units.
- When a later simulated strategy needs exact saved validation predictions.
- When a later native simulated strategy needs a saved prediction window that starts before the original validation period.

## Examples

Safe progress pattern:

```text
1. Clone the AI Factor with a codex_ name.
2. Capture baseline setup under p123-output/.
3. Inspect Load -> Status and report Resource Units.
4. Ask confirmation before clicking Load Dataset.
5. In the load dialog, leave Target Information Regression disabled unless needed.
6. Start loading and wait for Dataset loaded.
7. Re-open Validation -> Method.
8. Set the desired Basic Holdout gap/holdout and confirm displayed training period.
9. Open Validation -> Models.
10. Start only the intended row.
11. In the worker dialog, explicitly set Save Validation Predictions = Yes.
12. Wait for native model status before using or reporting final results.
```

Useful URLs:

```text
https://www.portfolio123.com/sv/aiFactor/{id}/overview
https://www.portfolio123.com/sv/aiFactor/{id}/load/status
https://www.portfolio123.com/sv/aiFactor/{id}/validation/method
https://www.portfolio123.com/sv/aiFactor/{id}/validation/models
```

Useful reporting language:

```text
P123 shows this dataset load as 21 Resource Units. It is not displayed as a dollar charge on the page. The model-validation step may have separate compute usage, so check the worker/start dialog and final model row before reporting total resource usage.
```

## Related

- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-api-ranking-native-ai-factor-strategy-workflow-2026-05-25.md`
- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- Baseline and validation artifacts from this run:
  - `p123-output/ai_factor_20015_baseline_20260524.md`
  - `p123-output/ai_factor_20015_baseline_20260524.json`
  - `p123-output/ai_factor_28612_validation_status_20260525.md`
  - `p123-output/native_strategy_ai_base87_2024_oos_baseline_20260525.md`
- Portfolio123 skill: `C:/Users/Eddy/.codex/skills/portfolio123/SKILL.md`
- Portfolio123 AI Factor guide: `C:/Users/Eddy/.codex/skills/portfolio123/ai-factor-guide.md`

---

## Tags

#portfolio123 #ai-factor #validation #clone-workflow #resource-units #saved-predictions #basic-holdout #browser-automation #algo-trading/portfolio123 #work/solutions #work/workflow-issues
