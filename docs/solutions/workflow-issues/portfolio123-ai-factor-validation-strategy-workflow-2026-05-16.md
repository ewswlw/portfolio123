---
title: Portfolio123 AI Factor Validation Strategy Workflow
date: 2026-05-16
last_updated: 2026-05-25
category: workflow-issues
module: Portfolio123 AI Factor strategy development
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Creating native Portfolio123 simulated strategies from AI Factor validation models"
  - "Testing an exact validation model such as a duplicate run with a # suffix"
  - "Deciding whether an AI Factor strategy can be run through today"
  - "Running native Portfolio123 simulations for live AIFactor predictor strategies"
  - "Recording auditable P123 strategy candidates created by an agent"
tags:
  - portfolio123
  - ai-factor
  - simulated-strategies
  - aifactorvalidation
  - live-predictor
  - native-validation
  - strategy-dna
  - codex-naming
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-16
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 AI Factor Validation Strategy Workflow."
---

# Portfolio123 AI Factor Validation Strategy Workflow

## Context

When turning a Portfolio123 AI Factor validation model into a simulated strategy, the dangerous failure mode is treating a model-table winner as if it automatically supports any backtest window or live predictor formula. The native P123 formula dialog, validation method, and strategy Review page are the authority.

This learning was captured after testing `AI Factor Base 87 Features Andreas 2` / `extra trees medium 4 #2` in native simulated strategies. The model was a valid top validation model, but no candidate met both `>20% CAGR` and `>1.5 Sharpe` over the exact defensible validation window.

Session-history search found no usable additional prior Codex sessions for this workspace/topic beyond the current work, so this doc is grounded in current P123 artifacts and the related browser-navigation learning.

## Guidance

Start by loading the Portfolio123 skill and checking `docs/solutions/` for relevant P123 learnings. Use the logged-in Chrome session for account-state work, and use P123 native pages for formula and performance claims.

For exact validation models, copy the formula from P123's native Validation Prediction Formula dialog. Do not infer the formula from the display row alone. In the verified case, the table row was:

```text
extra trees medium 4 #2
```

but the exact formula was:

```text
AIFactorValidation("AI Factor Base 87 Features Andreas 2", "extra trees medium 4", "2")
```

P123 encoded the `#2` duplicate/run suffix as the third argument, not as part of the second model-name argument. That distinction matters; the Predictors tab listed `extra trees medium 4`, but not `extra trees medium 4 #2`, so a live `AIFactor(...)` run would be a different branch from the exact validation winner.

Treat the validation context from the formula dialog as binding:

```text
Universe: No OTC Exchange + min 10 mil No Finance2
Period:   06/22/2024 - 06/21/2025
Frequency: Every Week
```

For a Basic Holdout AI Factor, the exact validation model may only be cleanly defensible over the saved holdout prediction window. If the user asks to run through today, split that into a separate live Predictor experiment with `AIFactor(...)`, and label it as a different model branch.

Do not assume that a populated live Predictor can be backtested through the full AI Factor dataset history, through the latest five years, or even from the day after the predictor training cutoff. P123 can reject native simulations that request predictions on dates covered by the predictor's training or internal availability window. In the verified live-predictor branch:

```text
AIFactor("AI Factor Base 87 Features Andreas 2", "extra trees medium 4")
```

P123 rejected these native simulated-strategy windows:

```text
05/16/2021 - 05/16/2026
06/22/2025 - 05/16/2026
06/23/2025 - 05/16/2026
```

with this error:

```text
Predictions may only be made using data from dates with which the predictor was not trained.
Predictor was trained until 06/21/2025.
```

The first accepted native window found for that live predictor was:

```text
01/19/2026 - 05/16/2026
```

This creates three separate dates/windows agents must keep distinct:

| Window | Verified Example | Meaning |
|---|---|---|
| AI Factor dataset/training history | `2010-01-01 to 2025-06-21` | Data available to train or validate the model; not automatically a valid strategy backtest window. |
| `AIFactorValidation(...)` holdout prediction window | `06/22/2024 - 06/21/2025` | Exact saved validation predictions for the `extra trees medium 4 #2` branch. |
| live `AIFactor(...)` predictor simulation window | accepted only from `01/19/2026 - 05/16/2026` in the verified run | Native P123 accepted out-of-sample live predictor window; must be proven by the Review/run page. |

Create agent-owned P123 objects with the project-required `codex_` prefix. Prefer creating separate candidate strategies instead of repeatedly editing and rerunning one object, because separate objects preserve an audit trail and avoid wizard persistence issues. Record every serious candidate in a local DNA log under `p123-output/`.

## Workflow

1. Confirm the AI Factor and model row on:

```text
https://www.portfolio123.com/sv/aiFactor/{id}/validation/models
```

2. Open the validation/results/predictor pages and capture:

- exact AI Factor name,
- exact model row,
- native rank and validation status,
- validation method and holdout period,
- universe, frequency, and prediction period,
- whether a live predictor exists for the same exact model.

3. Use the formula dialog to get the exact formula. For duplicate validation runs, expect a third argument like `"2"`.

4. Create a `codex_` ranking system copy before editing formulas. In the verified workflow, an existing ranking was copied with Save As, then the copy was edited in the raw editor. This avoided touching the user's original ranking.

If the native ranking-system `Save As` route is blocked, use the API-owned `ApiRankingSystem` as a temporary bridge instead of abandoning native validation. Update it with `rank_update` using the exact `AIFactorValidation(...)` XML, then select `ApiRankingSystem` in the native strategy wizard. This object is mutable shared API state, so immediately log the exact XML/formula, API response, and native strategy ID under `p123-output/`. See the API-ranking workflow learning for the full fallback.

5. Create simulated strategies from the ranking system using:

```text
https://www.portfolio123.com/port_wiz.jsp?new=1&type=3&mt=1&initRankId={ranking_id}
```

6. Before running, verify the wizard Review page, not just form fields. Confirm universe, ranking system, rebalance frequency, period, buy rules, sell rules, and position sizing.

7. For live predictor branches using `AIFactor(...)`, start with the desired maximum period but treat P123 date-window rejections as binding. If P123 reports that predictions may only be made using data outside the predictor training dates, shorten the native simulation window until the run is accepted. Record every rejected period and the exact accepted period.

8. Save each tested variant as a separate `codex_strategy_...` object and log the native summary metrics. Do not claim success from local calculations or screen-backtest estimates.

## Why This Matters

P123 AI Factor names, validation model display names, and predictor names can look nearly identical while pointing to different prediction surfaces. A strategy can be technically runnable while no longer testing the exact model the user asked for.

The validation window also changes the truth of the request. For `extra trees medium 4 #2`, the source dataset covered `2010-01-01 to 2025-06-21`, but the Basic Holdout validation predictions were only clean for `06/22/2024 - 06/21/2025`. Running "as far back as possible" meant using the holdout window, not the full dataset history. Running through today requires a different live-predictor experiment, and even that branch may have a much shorter accepted native simulation window than the predictor table implies.

This matters because using live `AIFactor(...)` inside dates the predictor learned from would contaminate the live-style validation. P123 enforces that boundary at native simulation time. The resulting performance must be reported with the accepted dates; a strategy named or intended as a "5Y" test can still be a short-window test if P123 rejects earlier dates.

Separate `codex_` strategy objects and a DNA log also make failure useful. In the verified search, concentrated and smoother variants clarified that the AI Factor could clear 20% CAGR in native simulation, but the portfolio-level Sharpe stayed far below 1.5.

## When to Apply

- When a user asks to create a P123 simulated strategy from an AI Factor model.
- When the selected AI Factor model has a suffix such as `#2`.
- When the user asks for the longest sensible backtest window.
- When deciding between `AIFactorValidation(...)` and live `AIFactor(...)`.
- When P123 reports that AI Factor predictions may only be made on dates outside the predictor training window.
- When an agent creates P123 strategies, ranking systems, screens, universes, reports, or other saved account objects.

## Examples

Verified objects and results from the search:

| Object | P123 id | Notes |
|---|---:|---|
| `codex_ranking_ai_base87_et2_v1` | 545001 | Ranking copy containing exact validation formula |
| `codex_strategy_ai_base87_et2_clean_v1` | 1941640 | 19.16% CAGR, 0.80 Sharpe |
| `codex_strategy_ai_base87_et2_v2_conc10` | 1941642 | 23.19% CAGR, 0.74 Sharpe |
| `codex_strategy_ai_base87_et2_v3_mid15` | 1941643 | 13.44% CAGR, 0.25 Sharpe |
| `codex_strategy_ai_base87_et2_v4_smooth30` | 1941644 | 21.62% CAGR, 0.77 Sharpe |
| `codex_ranking_ai_base87_live_v1` | 545009 | Live predictor ranking copy using `AIFactor(...)` |
| `codex_strategy_ai_base87_live_v1_5y_conc10` | 1941664 | Live predictor branch; 5Y request rejected, accepted only from `01/19/2026 - 05/16/2026` |
| `ApiRankingSystem` | 541785 | API-owned fallback ranking system; mutable, so log exact XML/formula after every `rank_update` |
| `codex_strategy_ai_base87_2024_oos_baseline_v1` | 1944189 | Clone validation branch from `01/01/2024 - 06/21/2025`; native Tier 2 run made 14.03% annualized with 0.23 Sharpe and lagged SPY |

The correct conclusion was not "we found a winning strategy." It was:

```text
No native simulated strategy met both requested thresholds for the exact top AI Factor validation model. Two variants exceeded 20% CAGR, but all variants had Sharpe ratios between 0.25 and 0.80.
```

Useful artifact pattern:

```text
p123-output/ai_factor_20015_verification_YYYYMMDD.json
p123-output/ai_factor_formula_validation_YYYYMMDD.md
p123-output/strategy_dna_log_YYYYMMDD.csv
p123-output/candidate_search_summary_YYYYMMDD.md
p123-output/final_ai_factor_strategy_report_YYYYMMDD.md
p123-output/live_predictor_strategy_report_YYYYMMDD.md
p123-output/live_predictor_strategy_dna_YYYYMMDD.csv
```

Verified live predictor result:

| Period | Total Return | Benchmark Return | Active Return | Annualized Return | Sharpe | Max DD | Turnover | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `01/19/2026 - 05/16/2026` | 0.53% | 7.16% | -6.63% | 1.67% | 0.43 | -18.32% | 65.98% | Accepted native run, rejected as weak |

The practical reporting pattern is:

```text
Native P123 simulated strategy, 01/19/2026 - 05/16/2026:
Total Return 0.53%, Benchmark 7.16%, Active -6.63%, Annualized 1.67%,
Sharpe 0.43, Max DD -18.32%, turnover 65.98%.
```

Avoid calling this a five-year result. The requested five-year native run was rejected by P123.

## Related

- Portfolio123 skill: `C:/Users/Eddy/.codex/skills/portfolio123/SKILL.md`
- Portfolio123 AI Factor guide: `C:/Users/Eddy/.codex/skills/portfolio123/ai-factor-guide.md`
- Portfolio123 API-ranking native strategy fallback: `docs/solutions/workflow-issues/portfolio123-api-ranking-native-ai-factor-strategy-workflow-2026-05-25.md`
- Portfolio123 browser navigation learning: `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- Local final report: `p123-output/final_ai_factor_strategy_report_20260516.md`
- Local DNA log: `p123-output/strategy_dna_log_20260516.csv`
- Live predictor report: `p123-output/live_predictor_strategy_report_20260516.md`
- Live predictor DNA log: `p123-output/live_predictor_strategy_dna_20260516.csv`

---

## Tags

#portfolio123 #ai-factor #simulated-strategies #aifactorvalidation #live-predictor #native-validation #strategy-dna #codex-naming #algo-trading/portfolio123 #work/solutions #work/workflow-issues
