---
title: "Portfolio123 Platform-Only AI Factor OOS Campaign"
created_at: 2026-05-25 10:20 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-25
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for Portfolio123 Platform-Only AI Factor OOS Campaign."
---

# Portfolio123 Platform-Only AI Factor OOS Campaign

Goal: discover and natively validate a long-only Portfolio123 AI Factor strategy with out-of-sample Sharpe above `1.9` and OOS active annualized return above `5` percentage points versus benchmark.

Constraint: all Portfolio123 work in this campaign is through the Portfolio123 web platform UI. No P123 API was used to create, update, run, or validate account objects in this campaign log.

## Baseline Evidence

Previous documented native AI Factor strategy baselines:

| Candidate | Period | Annualized Return | Sharpe | Active vs SPY | Status |
|---|---:|---:|---:|---:|---|
| `codex_strategy_ai_base87_et2_clean_v1` | 2024 holdout branch | `19.16%` | `0.80` | not recorded here | prior best Sharpe |
| `codex_strategy_ai_base87_2024_oos_baseline_v1` | `01/01/2024 - 06/21/2025` | `14.03%` | `0.23` | `-6.13%` total active | weak |
| `codex_strategy_ai_base87_live_v1_5y_conc10` | `01/19/2026 - 05/16/2026` | `1.67%` | `0.43` | `-6.63%` total active | weak |

The first cost-controlled step was therefore platform inspection of existing loaded AI Factors before spending new Resource Units.

## Existing AI Factor Triage

Promising existing platform object:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
AI Factor ID: 27417
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Dataset period: 2006-01-01 to 2026-01-17
Validation method: Basic Holdout
Gap: 20 weeks
Holdout period: 65 months
Validation prediction period shown by formula dialog: 08/22/2020 - 01/17/2026
```

Best platform compare-table signals from this AI Factor:

| Model | P123 Rank | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| `lightgbm slow 3` | `100` | `195.44` | `2.02` | `48.74` | `2.14` | `1,867` | strongest rank and H-L profile |
| `lightgbm II - SCGotlesp` | `92` | `188.01` | `2.02` | `48.46` | `2.13` | `1,792` | similar to top model |
| `lightgbm medium 2` | `92` | `182.39` | `1.88` | `52.30` | `2.17` | `1,918` | strong high bucket |
| `lightgbm II` | `50` | `163.11` | `1.74` | `56.88` | `2.40` | `1,971` | best high-bucket SR; promoted |

Formula confirmed from platform dialog for `lightgbm slow 3`:

```text
AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm slow 3")
```

In simulated-strategy rules, `FRank()` required the AI Factor expression as a quoted/backtick formula:

```text
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm slow 3")`, #All, #Desc)
```

## Native Candidate Runs

All candidates below were created and run directly in the Portfolio123 web platform.

Common setup unless noted:

```text
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Rebalance: Every Week
Position sizing: Static Weight
Commission: 0.005 USD per share
Slippage: Variable
PIT Method - Prelim: Exclude
Ranking system: Core Combination
```

| Native Strategy | Port ID | AI Model | Rules | Positions | Ann Ret | Sharpe | Max DD | Total Active vs SPY | Turnover | Outcome |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| `codex_strategy_sc_lgbm_slow3_oos_v1` | `1944196` | `lightgbm slow 3` | buy AI rank `>99`, sell `<95` | `20` | `25.71%` | `1.24` | `-17.03%` | `124.56%` | `311.64%` | beats old AI baseline, fails Sharpe gate |
| `codex_strategy_sc_lgbm_slow3_oos_v2_smooth` | `1944197` | `lightgbm slow 3` | buy `>98`, sell `<90` | `20` | `22.70%` | `1.11` | `-22.41%` | `82.29%` | `191.39%` | widening diluted signal |
| `codex_strategy_sc_lgbm_slow3_oos_v3_top1_smooth_exit` | `1944198` | `lightgbm slow 3` | buy `>99`, sell `<90` | `20` | `24.70%` | `1.19` | `-18.39%` | `109.94%` | `166.90%` | lower churn, lower Sharpe |
| `codex_strategy_sc_lgbm_slow3_oos_v4_mktgate` | `1944199` | `lightgbm slow 3` | buy `>99` plus `Close(0,#Bench) > SMA(200,0,#Bench)`, sell `<95` or risk-off | `20` | `21.71%` | `1.09` | `-17.49%` | `69.33%` | `329.32%` | market gate hurt |
| `codex_strategy_sc_lgbm2_oos_v1_top1` | `1944200` | `lightgbm II` | buy `>99`, sell `<95` | `20` | `35.94%` | `1.60` | `-15.65%` | `306.26%` | `398.55%` | current leader |
| `codex_strategy_sc_lgbm2_oos_v2_smooth_exit` | `1944201` | `lightgbm II` | buy `>99`, sell `<90` | `20` | `28.97%` | `1.29` | `-15.08%` | `175.87%` | `215.22%` | smoother exit lowered Sharpe |
| `codex_strategy_sc_lgbm2_oos_v3_conc10` | `1944203` | `lightgbm II` | buy `>99`, sell `<95` | `10` | `33.29%` | `1.35` | `-18.04%` | `252.96%` | `397.83%` | concentration lowered Sharpe |
| `codex_strategy_sc_lgbm_medium2_oos_v1_top1` | `1944204` | `lightgbm medium 2` | buy `>99`, sell `<95` | `20` | `30.05%` | `1.36` | `-20.77%` | `194.02%` | `392.97%` | lower than `lightgbm II` leader |
| `codex_strategy_sc_lgbm2_scgotlesp_oos_v1_top1` | `1944206` | `lightgbm II - SCGotlesp` | buy `>99`, sell `<95` | `20` | `30.08%` | `1.34` | `-15.15%` | `194.62%` | `309.42%` | adjacent model reduced turnover but missed Sharpe leader |
| `codex_strategy_sc_lgbm_medium3_oos_v1_top1` | `1944208` | `lightgbm medium 3` | buy `>99`, sell `<95` | `20` | `31.91%` | `1.37` | `-20.00%` | `227.19%` | `406.02%` | higher model-table high-bucket SR did not translate to portfolio Sharpe |
| `codex_strategy_sc_lgbm2_oos_v4_liq50k` | `1944209` | `lightgbm II` | buy `>99`, sell `<95`, `AvgDailyTot(20) > 50000` | `20` | `35.40%` | `1.59` | `-15.65%` | `294.86%` | `399.83%` | higher liquidity was nearly tied but slightly worse than leader |
| `codex_strategy_sc_lgbm2_oos_v5_monthly` | `1944210` | `lightgbm II` | buy `>99`, sell `<95`, rebalance every 4 weeks | `20` | `32.60%` | `1.42` | `-14.98%` | `239.98%` | `288.42%` | lower turnover and drawdown, but weaker Sharpe/return than weekly leader |

## Time Series CV Clone Experiment

After the no-Resource-Unit native strategy branch topped out at Sharpe `1.60`, a cost-capped clone was created directly through the Portfolio123 platform UI:

```text
AI Factor: codex_ai_sc_lgbm_tscv_smooth_v1
AI Factor ID: 28636
Source: Save As clone of SCs Small and Micro Cap Focus + 10 Mil min Replic2
Copied studies: No
Copied predictors: No
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Dataset period: 2006-01-01 to 2026-01-17
Features: 32
Scaling: Rank
Validation method: Time Series CV
Gap: 20 weeks
Folds: 8
Holdout per fold: 12 months
Saved validation prediction period shown by formula dialog: 01/13/2018 - 01/17/2026
```

Platform costs for the clone:

```text
Dataset load: 12 Resource Units, 315MB / 79.5M data points, 1 min 28 sec
lightgbm II validation: 3 Resource Units, SUCCESS, Basic worker, 4 min 2 sec, 1.7GB
lightgbm slow 3 validation: 3 Resource Units, SUCCESS, Basic worker, 8 min 39 sec, 1.9GB
Total new Resource Units in this branch: 18
```

Time Series CV compare-table results:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `lightgbm II` | `100` | `0.5682` | `0.1698` | `38.74` | `1.03` | `20.93` | `0.86` | `1,109` | `-12.91` | `-0.33` | `800` | reject for native promotion |
| `lightgbm slow 3` | `100` | `0.5678` | `0.1743` | `37.46` | `0.97` | `20.83` | `0.89` | `964` | `-12.17` | `-0.31` | `665` | reject for native promotion |

Formula confirmed by the platform dialog for the first model:

```text
AIFactorValidation("codex_ai_sc_lgbm_tscv_smooth_v1", "lightgbm II")
```

This clone achieved the intended longer saved-prediction window, but the time-series validation quality is far weaker than the original Basic Holdout model table. The high buckets are not strong enough to justify a native simulated strategy run: both high-bucket Sharpe values are below `0.90`, versus the current native strategy leader's already-insufficient portfolio Sharpe of `1.60`.

## Current Best

Current best native platform-only candidate:

```text
Name: codex_strategy_sc_lgbm2_oos_v1_top1
Port ID: 1944200
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944200
Model: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Period: 08/22/2020 - 01/17/2026
Annualized Return: 35.94%
Sharpe Ratio: 1.60
Max Drawdown: -15.65%
Benchmark Return: 120.07% total
Active Return: 306.26% total
Annual Turnover: 398.55%
```

This clears the active-return spirit of the goal versus SPY and materially beats prior native AI Factor strategy results, but it does not clear the hard Sharpe `>1.9` gate.

Closest universe-matched check available from the AI Factor platform Return page showed the validation universe around `8.77%` annualized over the same AI Factor result window, while the current best native strategy produced `35.94%` annualized. No obvious universe-relative failure was observed.

## Cost Notes

Initial native-strategy work reused existing loaded AI Factor `27417` and created native simulated strategies through the platform UI, with no new AI Factor Resource Units.

The later Time Series CV clone branch spent `18` new Resource Units: `12` for dataset load and `3` each for two single-model validations. No native strategy was created from that clone because the compare-table validation was too weak to promote.

Visible prior Resource Unit context for the reused AI Factor:

```text
SCs Small and Micro Cap Focus + 10 Mil min Replic2: 57 Resource Units already shown on AI Factor list.
Each existing validation model row showed 3 Resource Units already spent on 04/21/2026.
```

## Interpretation

The most valuable discovery is that the existing small/micro-cap AI Factor branch is much stronger than the prior base-87 AI Factor branch in native strategy form. The binding constraint is now portfolio-level Sharpe, not active return.

What did not work:

- widening the buy pool from top `1%` to top `2%`;
- loosening the sell threshold from `<95` to `<90`;
- adding a simple SPY 200-day market gate;
- concentrating to 10 positions.
- switching from `lightgbm II` to `lightgbm medium 2`.
- switching to adjacent saved models `lightgbm II - SCGotlesp` or `lightgbm medium 3`;
- raising the liquidity floor to `AvgDailyTot(20) > 50000`;
- reducing rebalance frequency from weekly to every 4 weeks.

The no-Resource-Unit branch is now mostly exhausted. `lightgbm II` remains the best existing saved-validation model in native strategy form. The next meaningful platform-only step is a small, deliberate new AI Factor experiment, preferably a Rolling or Time Series CV setup aimed at smoother top-decile performance rather than higher raw high-bucket return alone.

## Next Candidate Ideas

1. If staying inside the existing saved predictions, the only remaining cheap construction idea is `lightgbm II` with 15 positions by setting target position size around `6.67%`. A first UI attempt was not saved because the platform position-size field kept reverting to the default `5.0`; do not count it as a native result.
2. For a better shot at Sharpe `>1.9`, create a new cost-capped platform AI Factor run with Rolling or Time Series CV and saved validation predictions.
3. In the new AI Factor design, optimize for smoother OOS portfolio behavior: avoid relying only on model-table high-bucket return, inspect high-bucket Sharpe, high-low Sharpe, turnover, and native strategy results before expanding Resource Unit spend.
4. Keep SPY and the universe-matched return page as benchmark checks; current leader still has no obvious universe-relative failure, but portfolio-level volatility remains the binding constraint.

## Existing Enhanced ExtraTrees Branch Native Test

Tested existing no-new-RU AI Factor branch after inspecting platform compare/model pages:

```text
AI Factor: AI Factor Enhanced 150+ Features ExtraTrees v1
AI Factor ID: 20101
Model: extra trees medium 4
Formula: AIFactorValidation("AI Factor Enhanced 150+ Features ExtraTrees v1", "extra trees medium 4")
Saved prediction period: 07/30/2016 - 07/19/2025
Frequency: Every 4 Weeks
Universe: No OTC Exchange + min 10 mil No Finance2
Benchmark: S&P 500 (SPY:USA)
```

Platform compare-table diagnostics before promotion:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `extra trees medium 4` | `100` | `1.6005` | `0.1794` | `61.14` | `1.76` | `23.13` | `1.06` | `424` | `-24.35` | `-0.69` | `376` |

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_ai_enh150_etm4_oos_v1
Port ID: 1944212
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944212
Position sizing: 20 positions, 5.0% static weight
Rebalance: Every 4 Weeks
Buy rules:
  FRank(`AIFactorValidation("AI Factor Enhanced 150+ Features ExtraTrees v1", "extra trees medium 4")`, #All, #Desc) > 90
  Close(0) > 1
  AvgDailyTot(20) > 100000
Sell rules:
  FRank(`AIFactorValidation("AI Factor Enhanced 150+ Features ExtraTrees v1", "extra trees medium 4")`, #All, #Desc) < 80
  0
  0
```

Native Tier 2 simulated-strategy result:

```text
Period: 07/30/16 - 07/19/25
Total Return: 445.24%
Benchmark Return: 235.61%
Active Return: 209.63%
Annualized Return: 20.80%
Sharpe Ratio: 0.87
Max Drawdown: -48.59%
Benchmark Max Drawdown: -33.72%
Annual Turnover: 122.23%
Correlation with S&P 500: 0.75
```

Decision: reject. The branch has real return edge and likely clears the active annualized alpha spirit versus SPY, but it fails the hard Sharpe `>1.9` goal by a wide margin and has unacceptable drawdown. The high-low validation separation did not translate into a smooth enough long-only native portfolio.

## Existing `agent_ml_v2_150f` ExtraTrees Branch Native Test

Inspected another no-new-RU saved-validation candidate from `p123-output/ai_factor_models_top_20260516.csv`:

```text
AI Factor: agent_ml_v2_150f
AI Factor ID: 26878
Model: extra trees medium 4
Formula: AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")
Saved prediction period: 12/28/2024 - 12/27/2025
Frequency: Every Week
Universe: No OTC Exchange + min 10 mil No Finance2
Benchmark: S&P 500 (SPY:USA)
```

Platform compare-table diagnostics before promotion:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `extra trees medium 4` | `100` | `1.2798` | `0.2029` | `98.02` | `1.91` | `18.94` | `0.97` | `607` | `-40.34` | `-1.16` | `628` |

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_agentmlv2_etm4_oos_v1
Port ID: 1944214
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944214
Position sizing: 20 positions, 5.0% static weight
Rebalance: Every Week
Buy rules:
  FRank(`AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")`, #All, #Desc) > 90
  Close(0) > 1
  AvgDailyTot(20) > 100000
Sell rules:
  FRank(`AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")`, #All, #Desc) < 80
  0
  0
```

Native Tier 2 simulated-strategy result:

```text
Period: 12/28/24 - 12/27/25
Total Return: 33.25%
Benchmark Return: 17.38%
Active Return: 15.87%
Annualized Return: 33.35%
Sharpe Ratio: 1.32
Risk Samples: 11
Max Drawdown: -17.60%
Benchmark Max Drawdown: -18.76%
Annual Turnover: 119.08%
Correlation with S&P 500: 0.68
```

Decision: reject. This branch beats SPY over the accepted one-year OOS window and has tolerable drawdown, but it fails the hard Sharpe `>1.9` gate and does not beat the current native AI Factor baseline Sharpe of `1.60`. The one-year validation window also makes it weaker evidence than the current 2020-2026 small/micro-cap leader.

## Additional Small/Micro-Cap Adjacent Model Tests

After the no-finance existing candidates failed, the platform compare table for `SCs Small and Micro Cap Focus + 10 Mil min Replic2` was re-read for untested adjacent models with high-bucket Sharpe above `2.1`. Two remaining zero-RU candidates had enough decision value to test natively using the current leader's construction.

Shared setup:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Saved prediction period: 08/22/2020 - 01/17/2026
Frequency: Every Week
Position sizing: 20 positions, 5.0% static weight
Buy rules: AI rank > 99; Close(0) > 0.5; AvgDailyTot(20) > 10000
Sell rules: AI rank < 95; 0; 0
```

### `lightgbm II - TOF`

Formula confirmed by platform dialog:

```text
AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II - TOF")
```

Platform compare-table row:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `lightgbm II - TOF` | `35` | `0.5664` | `0.1856` | `138.54` | `1.52` | `55.64` | `2.35` | `1,964` | `-35.22` | `-0.68` | `1,315` |

Native Tier 2 simulated-strategy result:

```text
Name: codex_strategy_sc_lgbm2_tof_oos_v1_top1
Port ID: 1944215
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944215
Period: 08/22/20 - 01/17/26
Total Return: 408.00%
Benchmark Return: 120.07%
Active Return: 287.93%
Annualized Return: 35.06%
Sharpe Ratio: 1.58
Max Drawdown: -19.47%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 447.27%
Correlation with S&P 500: 0.63
```

Decision: reject. Nearly tied the current `lightgbm II` leader on annualized return and Sharpe, but still missed both the hard Sharpe `>1.9` gate and the current leader's Sharpe `1.60`.

### `lightgbm medium 4`

Formula used:

```text
AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm medium 4")
```

Platform compare-table row:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `lightgbm medium 4` | `42` | `0.5662` | `0.1912` | `147.23` | `1.53` | `50.42` | `2.23` | `1,929` | `-39.69` | `-0.78` | `1,222` |

Native Tier 2 simulated-strategy result:

```text
Name: codex_strategy_sc_lgbm_medium4_oos_v1_top1
Port ID: 1944216
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944216
Period: 08/22/20 - 01/17/26
Total Return: 309.07%
Benchmark Return: 120.07%
Active Return: 189.00%
Annualized Return: 29.75%
Sharpe Ratio: 1.38
Max Drawdown: -16.22%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 388.89%
Correlation with S&P 500: 0.63
```

Decision: reject. Drawdown was acceptable, but return and Sharpe were clearly below the `lightgbm II` leader.

Updated conclusion: the existing small/micro-cap saved-prediction branch is now effectively exhausted under the tested long-only construction. `lightgbm II` remains the current best native AI Factor candidate, with `35.94%` annualized return, `1.60` Sharpe, and `-15.65%` max drawdown over `08/22/2020 - 01/17/2026`.

## Current-Leader Risk/Quality Filter Variants

Because `codex_strategy_sc_lgbm2_oos_v1_top1` already clears the active-return hurdle but fails the Sharpe gate, the next no-new-RU step tested whether simple native buy-rule gates could improve portfolio smoothness without changing the AI Factor model.

Shared setup:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Rebalance: Every Week
Position sizing: 20 positions, 5.0% static weight
Core buy rules: AI rank > 99; Close(0) > 0.5
Core sell rule: AI rank < 95
```

### Low-volatility gate

Attempted buy filter:

```text
AvgDailyTot(20) > 10000 AND FRank("Volatility(63)", #All, #Asc) > 50
```

Platform result:

```text
Error in Buy Rule 'Buy3': Error near 'Volatility': Invalid command 'Volatility'
```

Decision: invalid in this stock strategy rule context. Do not count as a native result. Note: the strategy object name appeared in the opener after the run attempt, but no valid native summary result was produced.

### Low-beta gate

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_sc_lgbm2_lowbeta_oos_v1
Port ID: 1944220
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944220
Additional buy filter:
  AvgDailyTot(20) > 10000 AND FRank(`BetaFunc(52,104)`, #All, #Asc) > 50
```

Native Tier 2 simulated-strategy result:

```text
Period: 08/22/20 - 01/17/26
Total Return: 426.33%
Benchmark Return: 120.07%
Active Return: 306.26%
Annualized Return: 35.94%
Sharpe Ratio: 1.60
Max Drawdown: -15.65%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 398.55%
Correlation with S&P 500: 0.67
```

Decision: reject as non-improving. The result matched the current leader's headline metrics, so the beta gate was effectively non-binding for the selected names or not enough to change the portfolio path.

### Quality/size gate

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_sc_lgbm2_quality_size_oos_v1
Port ID: 1944221
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944221
Additional buy filter:
  AvgDailyTot(20) > 10000 AND MktCap > 100 AND ROE%TTM > 0
```

Native Tier 2 simulated-strategy result:

```text
Period: 08/22/20 - 01/17/26
Total Return: 343.91%
Benchmark Return: 120.07%
Active Return: 223.84%
Annualized Return: 31.73%
Sharpe Ratio: 1.37
Max Drawdown: -16.80%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 405.66%
Correlation with S&P 500: 0.68
```

Decision: reject. The simple quality/size filter diluted the AI Factor edge and worsened Sharpe, so the current leader's weakness does not appear to be fixable with a blunt positive-ROE / minimum-market-cap gate.

Updated construction conclusion: simple buy-rule risk filters have not improved the `lightgbm II` leader. The binding constraint remains portfolio-level volatility relative to the model's return edge. Further progress likely requires either a better saved-prediction model or a new validation design that explicitly favors smoother top-bucket behavior.

## Position-Level Loss-Control Variants

The next no-new-RU construction test checked whether position-level loss control could improve Sharpe without changing the AI Factor.

### Sell-rule hard loss attempt

Attempted sell rule:

```text
PosReturn% < -15
```

Platform result:

```text
Error in Sell Rule 'Sell2': Error near 'PosReturn%': Invalid command 'PosReturn%'
```

Decision: invalid in the strategy sell-rule parser. Do not count as a native result.

### Native entry stop loss

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_sc_lgbm2_stop15_oos_v1
Port ID: 1944223
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944223
Stop Loss Strategy: Entry Based Stop
Percent: 15.0%
Resulting Funds: Keep in Cash
```

Native Tier 2 simulated-strategy result:

```text
Period: 08/22/20 - 01/17/26
Total Return: 354.34%
Benchmark Return: 120.07%
Active Return: 234.27%
Annualized Return: 32.30%
Sharpe Ratio: 1.50
Max Drawdown: -15.76%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 449.63%
Correlation with S&P 500: 0.63
```

Decision: reject. The native stop loss preserved a reasonable drawdown profile but reduced return and Sharpe versus the current leader. Position-level hard loss control did not solve the Sharpe constraint.

## Diversification Variant

Because 10-position concentration worsened Sharpe and 20 positions remained the leader, a final no-new-RU construction check tested whether increasing the target position count to 30 would smooth the return stream enough to improve Sharpe.

Created native simulated strategy through the platform UI:

```text
Name: codex_strategy_sc_lgbm2_oos_v6_pos30
Port ID: 1944224
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944224
Model: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Position sizing: 30 positions, 3.33% static weight
Rebalance: Every Week
Buy rules:
  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
  Close(0) > 0.5
  AvgDailyTot(20) > 10000
Sell rules:
  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
  0
  0
```

Native Tier 2 simulated-strategy result:

```text
Period: 08/22/20 - 01/17/26
Total Return: 348.64%
Benchmark Return: 120.07%
Active Return: 228.57%
Annualized Return: 31.99%
Sharpe Ratio: 1.46
Max Drawdown: -17.14%
Benchmark Max Drawdown: -24.50%
Annual Turnover: 438.37%
Correlation with S&P 500: 0.67
```

Decision: reject. More diversification diluted the AI Factor edge, increased drawdown slightly, and reduced Sharpe. The best tested construction remains the 20-position `lightgbm II` leader.

Updated no-new-RU conclusion: existing saved-prediction and native-construction variants have repeatedly topped out around Sharpe `1.60`. The next meaningful step is a new cost-capped AI Factor experiment, not more simple rule tweaking around the current leader.

## Time Series CV Clone ExtraTrees Stability Check

Timestamp: 2026-05-25 17:26 -04:00

Purpose: test whether an ExtraTrees model on the already-loaded Time Series CV clone can produce smoother top-bucket behavior than the two weak LightGBM validation rows, without paying for a new dataset load.

Platform object:

```text
AI Factor: codex_ai_sc_lgbm_tscv_smooth_v1
AI Factor ID: 28636
URL: https://www.portfolio123.com/sv/aiFactor/28636/validation/models
Validation method: Time Series CV
Saved prediction period already configured: 01/13/2018 - 01/17/2026
Existing completed models before this step: lightgbm II, lightgbm slow 3
```

Action taken through the Portfolio123 web UI:

```text
Added predefined model: extra trees medium 4
Worker dialog: Basic worker, 4 CPU, 16GB RAM, $0.10/h, load 10/30
Save Validation Predictions: Yes
Started: 2026-05-25 17:25 -04:00
Visible status after first poll: IN PROGRESS... Basic: 1 min, 20 sec
Visible Resource Units while in progress: 0
```

Decision pending. Promote to native simulated strategy only if the completed compare/results diagnostics materially improve on the rejected Time Series CV LightGBM rows and plausibly clear the native Sharpe hurdle.

Checkpoint at 2026-05-25 18:04 -04:00:

```text
Visible status: IN PROGRESS... Basic: 38 min, 43 sec
Visible Resource Units while in progress: 0
No error shown.
No additional model, dataset load, or native simulation started while this job is pending.
```

Checkpoint at 2026-05-25 18:22 -04:00:

```text
Visible status: IN PROGRESS... Basic: 56 min, 55 sec
Visible Resource Units while in progress: 0
No error shown.
Still serialized: no additional model, dataset load, ranking edit, or native simulation was started while this job is pending.
```

Next required action: return to `https://www.portfolio123.com/sv/aiFactor/28636/validation/models`, wait for the `extra trees medium 4` row to reach `SUCCESS` or `FAIL`, then inspect the Results/Compare diagnostics before any native simulation decision.

Checkpoint at 2026-05-25 18:28 -04:00:

```text
Visible status: IN PROGRESS... Basic: 1 hr, 3 min
Visible Resource Units while in progress: 0
No error shown.
Still serialized: no additional model, dataset load, ranking edit, or native simulation was started while this job is pending.
```

Interpretation: the `extra trees medium 4` validation is an unusually long Basic-worker cloud run, but the UI continues to show an active in-progress state rather than a failure. Keep waiting; do not start another validation model until this row resolves.

Checkpoint at 2026-05-25 18:33 -04:00:

```text
Visible status: IN PROGRESS... Basic: 1 hr, 7 min
Visible Resource Units while in progress: 0
No error shown.
Still serialized: no additional model, dataset load, ranking edit, or native simulation was started while this job is pending.
```

Interpretation: still no decision-ready validation result. This branch remains pending until Portfolio123 resolves the `extra trees medium 4` row to `SUCCESS` or `FAIL`.

Final status at 2026-05-25 18:36 -04:00:

```text
Visible status: SUCCESS
Validation runtime: Basic: 1 hr, 8 min (1.4 GB)
Resource Units: 3
Update time: 6:34 PM
Rank: 33
Formula: AIFactorValidation("codex_ai_sc_lgbm_tscv_smooth_v1", "extra trees medium 4")
```

Time Series CV compare-table results after completion:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm slow 3` | `100` | `0.5678` | `0.1743` | `37.46` | `0.97` | `20.83` | `0.89` | `964` | `-12.17` | `-0.31` | `665` | prior reject |
| `lightgbm II` | `66` | `0.5682` | `0.1698` | `38.74` | `1.03` | `20.93` | `0.86` | `1,109` | `-12.91` | `-0.33` | `800` | prior reject |
| `extra trees medium 4` | `33` | `0.5679` | `0.1772` | `31.52` | `0.83` | `17.36` | `0.79` | `670` | `-10.82` | `-0.27` | `586` | reject |

Decision: reject; do not promote to native simulated strategy. The ExtraTrees model improved turnover and slightly improved Spearman versus the two LightGBM rows, but it materially weakened the H-L spread, H-L Sharpe, High bucket average return, and High bucket Sharpe. Because the stronger Time Series CV LightGBM rows were already too weak to promote, this lower-ranked ExtraTrees result has no clear decision value for another native simulation spend.

Updated branch conclusion: the already-loaded Time Series CV clone does not currently contain a model worth promoting. The campaign's current native leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` with `35.94%` annualized return, `1.60` Sharpe, and `-15.65%` max drawdown over `08/22/2020 - 01/17/2026`; it still fails the hard Sharpe `>1.9` objective.

## Existing SP500 / No-Finance AI Factor Triage

Timestamp: 2026-05-25 18:38 -04:00

Purpose: check remaining existing saved-prediction candidates before spending more Resource Units. All observations below came from Portfolio123 UI Results/Compare pages; no API and no new platform run was used.

| AI Factor ID | AI Factor | Best visible model(s) | Compare diagnostics | Decision |
| ---: | --- | --- | --- | --- |
| `20725` | `SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials` | `deeptables conf2 (linear+dnn+fm)` | Rank `100`, H-L Avg `5.69`, H-L SR `0.56`, High Avg `7.79`, High SR `0.66`; other rows have negative H-L or negative High returns | reject: too weak for promotion |
| `27238` | `agent_highsr_lgbm_sp500_v1` | `lgbm_andreas_1k_lr001_mcs100_v1`, `et_iter3_800_mf035_msl20_v1` | Best H-L Avg around `7.40`, H-L SR `0.50`; High Avg around `15.78-16.46`, High SR around `0.70-0.73` | reject: validation Sharpe too low |
| `20721` | `SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm` | `deeptables wide_regularized` | Rank `100`, H-L Avg `2.09`, H-L SR `0.06`, High Avg `24.06`, High SR `1.10`; other rows include negative High return or negative H-L | reject: no spread quality |
| `26875` | `agent_ml_2003_87f_v1` | `extra trees slow 4` | H-L Avg `28.46`, H-L SR `1.21`, High Avg `26.17`, High SR `0.57`, High Turn `1,282` | reject: High bucket too volatile |
| `26889` | `agent_ml_v3_lgbm` | `lightgbm slow 2` | H-L Avg `39.52`, H-L SR `1.30`, High Avg `16.17`, High SR `0.63`, High Turn `1,380` | reject: unlikely to beat native Sharpe leader |

Decision: do not promote any of these existing candidates to native simulated strategy. The current native leader's source model had far stronger validation diagnostics and still reached only `1.60` native Sharpe, so these weaker High-bucket Sharpe profiles are unlikely to clear the hard `>1.9` native Sharpe objective. The next useful experiment should spend Resource Units only on a more targeted new validation design, not on native simulations from weak compare rows.

## Aborted Native Variant: Sell Threshold 99

Timestamp: 2026-05-25 18:46 -04:00

Purpose: test a no-RU native strategy-construction variant of the current leader by changing the sell rule from rank < 95 to < 99.

Source strategy: codex_strategy_sc_lgbm2_oos_v1_top1 (portid=1944200)

Intended sell rule:

`  ext
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 99
`

Outcome: aborted before running. The in-app browser could read the P123 wizard fields, but clipboard-backed fill/type paths failed, and keyboard-only micro-edits did not place the digit safely. The wizard was reloaded and the original sell rule was verified restored:

`  ext
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
`

No native simulation was started, no Resource Units were spent, and no existing P123 object was saved or overwritten.

## Existing Small-Cap AI Factor Re-Triage

Timestamp: 2026-05-25 18:48 -04:00

Source: Portfolio123 UI SCs Small and Micro Cap Focus + 10 Mil min Replic2 (iFactor=27417) Results / Compare page.

Reason: before spending more Resource Units, re-check whether any existing saved-result model has enough decision value for another native simulated strategy.

Visible compare rows, sorted by native AI Factor Rank:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| lightgbm slow 3 | 100 | 0.5658 | 0.1980 | 195.44 | 2.02 | 48.74 | 2.14 | 1,867 | already promoted; native Sharpe 1.24 |
| lightgbm II - SCGotlesp | 92 | 0.5659 | 0.1979 | 188.01 | 2.02 | 48.46 | 2.13 | 1,792 | already promoted; native Sharpe 1.34 |
| lightgbm medium 2 | 92 | 0.5658 | 0.1938 | 182.39 | 1.88 | 52.30 | 2.17 | 1,918 | already promoted; native Sharpe 1.36 |
| lightgbm I | 78 | 0.5658 | 0.2003 | 160.29 | 1.62 | 44.84 | 1.95 | 2,046 | reject: weaker than promoted models and too much turnover |
| lightgbm III | 71 | 0.5661 | 0.1953 | 167.33 | 1.75 | 48.89 | 2.19 | 1,794 | watchlist only: unpromoted, but weaker than current leader's lightgbm II High SR 2.40 |
| lightgbm II - TOF ANH | 64 | 0.5663 | 0.1867 | 198.58 | 2.00 | 50.26 | 2.18 | 1,887 | already promoted via TOF family; native Sharpe 1.58 |
| lightgbm medium 3 | 57 | 0.5661 | 0.1923 | 160.98 | 1.64 | 53.20 | 2.26 | 1,974 | already promoted; native Sharpe 1.37 |
| lightgbm II | 50 | 0.5663 | 0.1876 | 163.11 | 1.74 | 56.88 | 2.40 | 1,971 | current native leader; native Sharpe 1.60 |
| lightgbm medium 4 | 42 | 0.5662 | 0.1912 | 147.23 | 1.53 | 50.42 | 2.23 | 1,929 | already promoted; native Sharpe 1.38 |
| lightgbm II - TOF | 35 | 0.5664 | 0.1856 | 138.54 | 1.52 | 55.64 | 2.35 | 1,964 | already promoted; native Sharpe 1.58 |
| extra trees II | 35 | 0.5663 | 0.2097 | 96.13 | 1.11 | 31.63 | 1.58 | 940 | reject: lower turnover but much weaker High return/SR |
| lightgbm slow 2 | 21 | 0.5665 | 0.1863 | 137.47 | 1.43 | 47.40 | 2.04 | 1,918 | reject: weaker than promoted rows |
| lightgbm fast 3 | 14 | 0.5679 | 0.2032 | 110.54 | 1.31 | 30.63 | 1.43 | 1,758 | reject |
| lightgbm fast 2 | 7 | 0.5666 | 0.2048 | 92.97 | 1.09 | 26.94 | 1.31 | 1,817 | reject |

Conclusion: no obvious unpromoted existing saved-result row has a stronger model-table case than the current lightgbm II leader. The next highest-value work is not another blind native promotion from this table; it is either safer platform editing of portfolio-construction variants or a narrow new validation design with decision value.

## Native Variant Result: Sell Threshold 99 Rejected

Timestamp: 2026-05-25 18:55 -04:00

Surface: Portfolio123 web platform UI in Chrome after authenticated platform login through the project-approved encrypted local login workflow. No P123 API was used.

Variant tested on existing leader object portid=1944200:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 99
`

Important workflow discovery: the port_wiz.jsp?rerun=1&editUid=1944200 / Re-Run Simulation path updated the existing simulated strategy object instead of creating a new saved copy. This is not safe for future variants unless the workflow first creates or selects an explicit copied simulation object.

Temporary sell99 native result on portid=1944200 before restoration:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 191.79% |
| Benchmark Return | 120.07% |
| Active Return | 71.72% |
| Annualized Return | 21.90% |
| Annual Turnover | 1,546.06% |
| Max Drawdown | -22.33% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | .98 |

Decision: reject. The stricter sell threshold caused materially worse return, Sharpe, drawdown, and turnover. It does not advance the hard objective.

Restoration performed immediately afterward on the same platform UI path:

`  ext
Sell restored to: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
`

Restored leader verification on portid=1944200:

| Metric | Restored Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 426.33% |
| Benchmark Return | 120.07% |
| Active Return | 306.26% |
| Annualized Return | 35.94% |
| Annual Turnover | 398.55% |
| Max Drawdown | -15.65% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.60 |

Current campaign leader remains codex_strategy_sc_lgbm2_oos_v1_top1; the hard Sharpe >1.9 objective remains unmet.

## Native Candidate: LightGBM III Top-1

Timestamp: 2026-05-25 19:00 -04:00

Surface: Portfolio123 web platform UI in Chrome. No P123 API was used.

Purpose: test the only unpromoted small-cap saved-result row with model-table diagnostics close enough to justify a low-cost native simulation, while using the safe Save As a new Simulated Strategy path instead of the overwrite-prone rerun path.

Strategy created:

`  ext
Name: codex_strategy_sc_lgbm3_oos_v1_top1
Port ID: 1944232
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944232
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm III
`

Rules:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm III")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm III")`, #All, #Desc) < 95
`

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 311.76% |
| Benchmark Return | 120.07% |
| Active Return | 191.69% |
| Annualized Return | 29.91% |
| Annual Turnover | 318.18% |
| Max Drawdown | -14.36% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.40 |

Decision: reject. This branch improves drawdown and turnover versus some variants, but it is below the current leader (35.94% annualized return, 1.60 Sharpe) and far below the hard Sharpe >1.9 target. The model-table advantage was not enough to overcome native long-only construction friction.

Workflow note: the safe Save As a new Simulated Strategy path created a new object with   ab_portUid=0 before running and produced new portid=1944232, confirming this is the preferred platform-only path for future native variants.

## Native Candidate: LightGBM II Top-1 Sell90 Slow Exit

Timestamp: 2026-05-25 19:03 -04:00

Surface: Portfolio123 web platform UI in Chrome. No P123 API was used.

Purpose: test whether a slower exit threshold improves Sharpe by lowering turnover and allowing winners more room. This is a no-RU construction variant of the current leader.

Strategy created:

`  ext
Name: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy
Port ID: 1944233
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944233
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
`

Rules:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 90
`

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 295.94% |
| Benchmark Return | 120.07% |
| Active Return | 175.87% |
| Annualized Return | 28.97% |
| Annual Turnover | 215.22% |
| Max Drawdown | -15.08% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.29 |

Decision: reject. The slower sell threshold reduced turnover but gave up too much return and lowered Sharpe versus the current leader (35.94%, 1.60 Sharpe). This confirms the native leader is not simply overtrading because of the <95 exit; loosening the exit damages the OOS profile.

## Aborted Diagnostic: Fixed Zero Slippage Copy

Timestamp: 2026-05-25 19:10 -04:00

Surface: Portfolio123 web platform UI. No P123 API was used.

Purpose: isolate whether transaction-cost/slippage friction is the main reason the current leader stalls near 1.60 Sharpe instead of the hard >1.9 objective.

Intended diagnostic setup on a safe copied strategy from portid=1944200:

`  ext
Name shown by P123: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(2)
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
Slippage: 0% fixed
`

Outcome: aborted before running. The platform form accepted the fixed-slippage radio button, but keyboard-only edits did not reliably change the slippage textbox from .5 to exact ; one verification caught 0.5, and the repair attempt reverted to .5. Because the review page still showed .5% of Total Amt (Fixed), no native simulation was launched.

Decision: do not count this as a tested result. A zero-slippage diagnostic may still be useful later, but only if the exact Review page shows % before the run. No Resource Units were spent and no native result was created from this aborted copy.

## Native Candidate: LightGBM II Top-1 With Benchmark 200D SMA Cash Hedge

Timestamp: 2026-05-25 19:17 -04:00

Surface: Portfolio123 web platform UI. No P123 API was used.

Purpose: test whether a simple market-risk overlay can lift Sharpe by moving to cash when the configured benchmark is below its 200-day moving average. This is a no-RU construction/risk-control variant of the current AI Factor leader.

Strategy created:

`  ext
Name: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(2)
Port ID: 1944235
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944235
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
`

Rules:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
Hedge: enabled, GO TO CASH
Hedge entry: Close(0,#bench) <= SMA(200,0,#bench)
Hedge exit:  Close(0,#bench) > SMA(200,0,#bench)
`

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 245.92% |
| Benchmark Return | 120.07% |
| Active Return | 125.85% |
| Annualized Return | 25.79% |
| Annual Turnover | 399.43% |
| Max Drawdown | -14.18% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.30 |

Decision: reject. The hedge reduced max drawdown slightly versus the current leader (-14.18% vs -15.65%), but it cut too much return and lowered Sharpe from 1.60 to 1.30. A simple benchmark 200-day cash hedge is not the path to the hard >1.9 Sharpe target for this AI Factor leader.

## Native Candidate: LightGBM II TOF ANH Top-1

Timestamp: 2026-05-25 19:21 -04:00

Surface: Portfolio123 web platform UI. No P123 API was used.

Purpose: test an existing saved-result model from the same small-cap AI Factor that had strong H-L spread diagnostics (lightgbm II - TOF ANH) but had not been logged as its own exact native simulation. This was a no-RU promotion from existing saved validation results.

Strategy created:

`  ext
Name: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(3)
Port ID: 1944236
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944236
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II - TOF ANH
`

Rules:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II - TOF ANH")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II - TOF ANH")`, #All, #Desc) < 95
`

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 384.92% |
| Benchmark Return | 120.07% |
| Active Return | 264.85% |
| Annualized Return | 33.90% |
| Annual Turnover | 404.36% |
| Max Drawdown | -19.40% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.52 |

Decision: reject. This model has strong return and clears the active-return hurdle, but it does not beat the current leader (35.94% annualized return, 1.60 Sharpe, -15.65% max drawdown) and remains below the hard Sharpe >1.9 target.

## Native Candidate: LightGBM II Top-1 With Stock 200D SMA Buy Filter

Timestamp: 2026-05-25 19:27 -04:00

Surface: Portfolio123 web platform UI. No P123 API was used.

Purpose: test whether filtering individual stock entries to only stocks above their own 200-day SMA improves Sharpe by avoiding weak-trend names while keeping the AI Factor leader model.

Strategy created:

`  ext
Name: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(4)
Port ID: 1944239
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944239
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
`

Rules:

`  ext
Buy:  FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99 and Close(0) > SMA(200,0)
Sell: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95
`

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 8/22/2020 - 01/17/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 406.93% |
| Benchmark Return | 120.07% |
| Active Return | 286.86% |
| Annualized Return | 35.00% |
| Annual Turnover | 415.61% |
| Max Drawdown | -19.31% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.49 |

Decision: reject. The stock-level trend filter preserved much of the return, but worsened drawdown and lowered Sharpe versus the current leader (35.94%, 1.60 Sharpe, -15.65% max drawdown). Avoiding stocks below their 200-day SMA is not enough to lift this AI Factor strategy toward >1.9 Sharpe.

## Read-Only Native Sim Leader Scan

Timestamp: 2026-05-25 19:27 -04:00

Surface: Portfolio123 web platform UI simulated-strategy opener. No P123 API was used.

Purpose: confirm whether any newly created or previously visible native AI Factor simulation now beats the documented campaign leader.

Visible AI Factor strategy rows confirm the leader remains:

`  ext
codex_strategy_sc_lgbm2_oos_v1_top1 | 08/22/20 - 05/25/26 | 20 positions | 35.9% annualized | 20.2% excess/active display | 1.60 Sharpe | -15.7% max drawdown
`

Closest challengers in the visible list:

| Strategy | Annualized | Visible excess/active display | Sharpe | Max DD | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| codex_strategy_sc_lgbm2_oos_v4_liq50k | 35.4% | 19.7% | 1.59 | -15.7% | below leader |
| codex_strategy_sc_lgbm2_tof_oos_v1_top1 | 35.1% | 19.4% | 1.58 | -19.5% | below leader |
| codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(4) | 35.0% | 19.3% | 1.49 | -19.3% | rejected stock-trend filter |
| codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(3) | 33.9% | 18.2% | 1.52 | -19.4% | rejected TOF ANH |

Conclusion: no existing native AI Factor simulation visible in the current platform list satisfies the hard >1.9 Sharpe target or beats the current native leader. The binding constraint now appears to be model/portfolio interaction quality, not a missing simple construction tweak around the existing small-cap LightGBM II leader. The next meaningful escalation likely requires a narrow new AI Factor validation design with clear decision value, rather than more blind native variants from this saved-results table.

## Native Strategy Book Candidate: Small-Cap AI Factor Model Diversification

Timestamp: 2026-05-25 19:38 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test whether a no-RU native Strategy Book made from already-created long-only AI Factor simulated strategies can lift Sharpe above the standalone leader through model diversification. This branch used existing native simulations only and did not train new AI Factor models.

Strategy Book created:

```text
Name: codex_book_ai_sc_lgbm_diversified_oos_v1
Port ID: 1944241
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944241
Type: Native P123 simulated book
```

Book setup:

```text
Benchmark: S&P 500 (SPY:USA)
Period accepted by P123: 08/21/2020 - 01/16/2026
Sizing method: Static Weight
Book rebalance: Every 4 Weeks
Asset rebalance slippage: 0.0%
Gross exposure: 1.0
Net exposure: 1
```

Assets:

| Asset | Source port ID | Target weight |
| --- | ---: | ---: |
| codex_strategy_sc_lgbm2_oos_v1_top1 | 1944200 | 20.0% |
| codex_strategy_sc_lgbm2_oos_v4_liq50k | 1944209 | 20.0% |
| codex_strategy_sc_lgbm2_tof_oos_v1_top1 | 1944215 | 20.0% |
| codex_strategy_sc_lgbm_medium3_oos_v1_top1 | 1944208 | 20.0% |
| codex_strategy_sc_lgbm3_oos_v1_top1 | 1944232 | 20.0% |

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/21/2020 - 01/16/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 380.75% |
| Benchmark Return | 120.07% |
| Active Return | 260.68% |
| Annualized Return | 33.69% |
| Max Drawdown | -14.93% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.55 |
| Correlation with SPY | 0.66 |

Decision: reject. The book clears the active-return hurdle and improves max drawdown slightly versus the standalone leader, but it does not beat the current best native AI Factor strategy's Sharpe ratio of 1.60 and remains well below the hard Sharpe >1.9 goal. This shows that simple diversification among nearby small-cap LightGBM validation strategies is not enough; the components are either too correlated, too similar in drawdown timing, or too individually noisy. Further equal-weight books from the same model cluster are unlikely to be the high-value path unless a component adds materially different signal or risk behavior.

## Aborted Validation Spend: Old Small-Cap Copy Dataset Boundary

Timestamp: 2026-05-25 19:43 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: check whether the older `SCs Small and Micro Cap Focus + 10 Mil min - Copy` AI Factor could be used as a low-cost, already-loaded duplicate validation surface for one narrow `lightgbm II` run.

Observed setup before attempting to start:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min - Copy
AI Factor ID: 27424
Validation method page displayed:
Dataset period: 20.1 years (2006-01-01 to 2026-01-17)
Gap: 20 weeks
Method: Basic Holdout
Training Period: 14.3 years
Holdout Period: 65.0 months
```

Attempted action:

```text
Open Validation -> Models
Target row: lightgbm II
Click Start
```

Outcome: aborted before spending. P123 opened a confirmation dialog:

```text
Dataset has not been loaded. Do you want to load it now?
```

The agent clicked `Cancel`. No dataset load was started, no model validation was started, and no Resource Units were spent.

Decision: do not use this old copy as a cheap duplicate-validation path. Although the Method page displays a dataset period and validation geometry, the Start workflow treats the dataset as not loaded. Re-loading this copy would be a fresh dataset-load spend for substantially the same small-cap AI Factor source already tested through the completed `codex_ai_sc_lgbm_tscv_smooth_v1` clone. That is not enough decision value unless the next experiment changes the dataset/preprocessing/target design materially.

## Native Strategy Book Candidate: Stock-Only Mix With AI Factor Sleeve

Timestamp: 2026-05-25 20:05 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test whether a stock-only native Strategy Book using two long-only stock strategies plus an explicit AI Factor sleeve can lift Sharpe above the current AI leader without relying on ETF ballast. This was motivated by the high-Sharpe `BookSim - Copy`, but that reference book included TLT and GLD, so it was not a clean fit for the long-only stock objective.

Strategy Book created:

```text
Name: codex_book_stock_ai_mix_oos_v1
Port ID: 1944242
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944242
Type: Native P123 simulated book
```

Book setup:

```text
Benchmark: S&P 500 (SPY:USA)
Period accepted by P123: 08/21/2020 - 01/16/2026
Sizing method: Static Weight
Book rebalance: Every 4 Weeks
Asset rebalance slippage: 0.0%
Gross exposure: 1.0
Net exposure: 1
```

Assets and final native weights:

| Asset | Source port ID | Native ending weight |
| --- | ---: | ---: |
| Advisor Small Cap Focus (P123) With Risk Reduction | 1724626 | 9.15% |
| Wes Gray Momentum Microcaps Hedged | 1848302 | 52.64% |
| codex_strategy_sc_lgbm2_oos_v1_top1 | 1944200 | 38.21% |

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/21/2020 - 01/16/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 214.89% |
| Benchmark Return | 120.07% |
| Active Return | 94.82% |
| Annualized Return | 23.63% |
| Max Drawdown | -9.70% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.73 |
| Correlation with SPY | 0.53 |

Decision: reject. The stock-only mix materially improved drawdown and correlation versus the standalone AI Factor leader and still cleared the active-return hurdle, but it did not clear Sharpe >1.9 and did not beat the current best native AI Factor Sharpe of 1.60 by enough to satisfy the full objective. This result suggests that adding a low-correlation stock strategy helps risk quality, but the AI sleeve plus microcap stock component still does not reach the required risk-adjusted return without non-stock ballast.

## Native Strategy Book Candidate: Wes Gray / AI Factor 80-20 Stock-Only Mix

Timestamp: 2026-05-25 20:24 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test a cleaner two-asset stock-only blend using the low-correlation Wes Gray stock strategy as the stabilizer and the current native AI Factor leader as a 20% sleeve. This avoids ETF ballast and avoids another AI Factor dataset/model RU spend.

Strategy Book created:

```text
Name: codex_book_wes_ai_oos_v1
Port ID: 1944243
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944243
Type: Native P123 simulated book
```

Book setup:

```text
Benchmark: S&P 500 (SPY:USA)
Period accepted by P123: 08/21/2020 - 01/16/2026
Sizing method: Static Weight
Book rebalance: Every 4 Weeks
Gross exposure: 1.0
Net exposure: 1
Intended relative weights: 4 / 1
```

Assets and final native weights:

| Asset | Source port ID | Native ending weight |
| --- | ---: | ---: |
| Wes Gray Momentum Microcaps Hedged | 1848302 | 77.58% |
| codex_strategy_sc_lgbm2_oos_v1_top1 | 1944200 | 22.42% |

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/21/2020 - 01/16/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 137.57% |
| Benchmark Return | 120.07% |
| Active Return | 17.50% |
| Annualized Return | 17.35% |
| Max Drawdown | -9.73% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.61 |
| Correlation with SPY | 0.31 |

Decision: reject. The 80/20 stock-only mix kept drawdown low and reduced SPY correlation sharply, but it gave up too much return. It does not clear Sharpe >1.9, only barely improves on the standalone AI Factor leader's Sharpe of 1.60, and has much lower active return than the AI leader. This is useful evidence that a low-correlation stock sleeve helps volatility but is not enough to solve the target by allocation alone.

## Native Strategy Book Candidate: Wes Gray / AI Factor Equal-Weight Stock-Only Mix

Timestamp: 2026-05-25 20:32 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test whether the diversification sweet spot between the Wes Gray stock strategy and the current native AI Factor leader is closer to equal weight than the conservative 80/20 mix.

Strategy Book created:

```text
Name: codex_book_wes_ai_equal_oos_v1
Port ID: 1944244
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944244
Type: Native P123 simulated book
```

Book setup:

```text
Benchmark: S&P 500 (SPY:USA)
Period accepted by P123: 08/21/2020 - 01/16/2026
Sizing method: Static Weight
Book rebalance: Every 4 Weeks
Gross exposure: 1.0
Net exposure: 1
Intended relative weights: 1 / 1
```

Assets and final native weights:

| Asset | Source port ID | Native ending weight |
| --- | ---: | ---: |
| Wes Gray Momentum Microcaps Hedged | 1848302 | 49.16% |
| codex_strategy_sc_lgbm2_oos_v1_top1 | 1944200 | 50.84% |

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/21/2020 - 01/16/2026 |
| Benchmark | S&P 500 (SPY:USA) |
| Total Return | 225.11% |
| Benchmark Return | 120.07% |
| Active Return | 105.04% |
| Annualized Return | 24.36% |
| Max Drawdown | -10.55% |
| Benchmark Max Drawdown | -24.50% |
| Sharpe Ratio | 1.74 |
| Correlation with SPY | 0.56 |

Decision: reject, but keep as the best stock-only book candidate so far. Equal-weighting restored enough AI exposure to beat the 80/20 book and slightly beat the earlier three-asset stock-only book on Sharpe, but it still fails the hard Sharpe >1.9 target. Allocation tuning with existing stock-only components appears capped around the mid-1.7 Sharpe range; reaching >1.9 likely requires a materially stronger AI Factor signal/model design rather than another static-weight blend.

## Existing AI Factor Candidate: agent_ml_v2_150f / extra trees medium 4

Timestamp: 2026-05-25 21:50 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: evaluate an existing high model-table candidate without spending new Resource Units.

AI Factor setup verified on platform:

```text
AI Factor: agent_ml_v2_150f
AI Factor ID: 26878
Model: extra trees medium 4
Formula: AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")
Saved validation prediction window: 12/28/2024 - 12/27/2025
Universe: No OTC Exchange + min 10 mil No Finance2
Validation method: Basic Holdout
Training period shown by P123: 13 years
Holdout period shown by P123: 12 months
Gap shown by P123: 52 weeks
```

Model-table signal quality:

| Metric | Result |
| --- | ---: |
| Native model Rank | 100 |
| Spearman | 0.2029 |
| High-Low Avg | 98.02 |
| High-Low Sharpe | 1.91 |
| High Avg | 18.94 |
| High Sharpe | 0.97 |
| High Turnover | 607 |
| Low Avg | -40.34 |
| Low Sharpe | -1.16 |

Ranking object repaired through platform UI:

```text
Name: codex_ranking_agent_ml_v2_etm4_v1
Ranking ID: 545804
Raw XML after repair:
<RankingSystem RankType="Higher">
  <StockFormula Weight="100" RankType="Higher" Name="codex_agent_ml_v2_etm4" Description="" Scope="Universe">
    <Formula>AIFactorValidation(&quot;agent_ml_v2_150f&quot;, &quot;extra trees medium 4&quot;)</Formula>
  </StockFormula>
</RankingSystem>
```

Existing native simulated strategy found:

```text
Name: codex_strategy_agentmlv2_etm4_oos_v1
Type: Native P123 simulated strategy
Period: 12/28/2024 - 12/27/2025
Universe: No OTC Exchange + min 10 mil No Finance2
Benchmark: S&P 500 (SPY:USA)
Ranking system shown in strategy: Core Combination
Buy signal: FRank(`AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")`, #All, #Desc) > 90
Sell signal: FRank(`AIFactorValidation("agent_ml_v2_150f", "extra trees medium 4")`, #All, #Desc) < 80
Positions: 20
Rebalance: Every Week
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Total Return | 33.25% |
| Benchmark Return | 17.38% |
| Active Return | 15.87% |
| Annualized Return | 33.35% |
| Annual Turnover | 119.08% |
| Max Drawdown | -17.60% |
| Benchmark Max Drawdown | -18.76% |
| Sharpe Ratio | 1.32 |
| Correlation with SPY | 0.68 |

Decision: reject. The model-table High-Low Sharpe looked excellent, and the native strategy cleared the active-return hurdle over its short one-year validation window, but realized portfolio Sharpe was only 1.32. The signal is directionally useful but too volatile in a concentrated long-only portfolio. It does not beat the current longer-window native AI Factor leader and is not a path to the >1.9 OOS Sharpe target without a much stronger risk-control or model redesign.

## Free Sweep: Existing Native AI Strategy Variants

Timestamp: 2026-05-25 22:05 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: harvest already-created native simulated strategy results before spending Resource Units on new AI Factor training.

Native P123 results read from existing strategy Summary pages:

| Strategy | Period | Annualized | Active | Sharpe | Max DD | Corr SPY |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| codex_strategy_sc_lgbm2_lowbeta_oos_v1 | 08/22/20 - 01/17/26 | 35.94% | 306.26% | 1.60 | -15.65% | 0.67 |
| codex_strategy_sc_lgbm2_oos_v1_top1 | 08/22/20 - 01/17/26 | 35.94% | 306.26% | 1.60 | -15.65% | 0.67 |
| codex_strategy_sc_lgbm2_oos_v2_smooth_exit | 08/22/20 - 01/17/26 | 28.97% | 175.87% | 1.29 | -15.08% | 0.66 |
| codex_strategy_sc_lgbm2_oos_v3_conc10 | 08/22/20 - 01/17/26 | 33.29% | 252.96% | 1.35 | -18.04% | 0.62 |
| codex_strategy_sc_lgbm2_oos_v4_liq50k | 08/22/20 - 01/17/26 | 35.40% | 294.86% | 1.59 | -15.65% | 0.66 |
| codex_strategy_sc_lgbm2_oos_v5_monthly | 08/22/20 - 01/17/26 | 32.60% | 239.98% | 1.42 | -14.98% | 0.64 |
| codex_strategy_sc_lgbm2_oos_v6_pos30 | 08/22/20 - 01/17/26 | 31.99% | 228.57% | 1.46 | -17.14% | 0.67 |
| codex_strategy_sc_lgbm2_quality_size_oos_v1 | 08/22/20 - 01/17/26 | 31.73% | 223.84% | 1.37 | -16.80% | 0.68 |
| codex_strategy_sc_lgbm2_stop15_oos_v1 | 08/22/20 - 01/17/26 | 32.30% | 234.27% | 1.50 | -15.76% | 0.63 |
| codex_strategy_sc_lgbm2_tof_oos_v1_top1 | 08/22/20 - 01/17/26 | 35.06% | 287.93% | 1.58 | -19.47% | 0.63 |
| codex_strategy_sc_lgbm_slow3_oos_v1 | 08/22/20 - 01/17/26 | 25.71% | 124.56% | 1.24 | -17.03% | 0.63 |
| codex_strategy_sc_lgbm_slow3_oos_v2_smooth | 08/22/20 - 01/17/26 | 22.70% | 82.29% | 1.11 | -22.41% | 0.67 |
| codex_strategy_sc_lgbm_slow3_oos_v3_top1_smooth_exit | 08/22/20 - 01/17/26 | 24.70% | 109.94% | 1.19 | -18.39% | 0.64 |
| codex_strategy_sc_lgbm_slow3_oos_v4_mktgate | 08/22/20 - 01/17/26 | 21.71% | 69.33% | 1.09 | -17.49% | 0.41 |
| codex_strategy_sc_lgbm_medium2_oos_v1_top1 | 08/22/20 - 01/17/26 | 30.05% | 194.02% | 1.36 | -20.77% | 0.64 |
| codex_strategy_sc_lgbm_medium3_oos_v1_top1 | 08/22/20 - 01/17/26 | 31.91% | 227.19% | 1.37 | -20.00% | 0.64 |
| codex_strategy_sc_lgbm_medium4_oos_v1_top1 | 08/22/20 - 01/17/26 | 29.75% | 189.00% | 1.38 | -16.22% | 0.63 |
| codex_strategy_sc_lgbm3_oos_v1_top1 | 08/22/20 - 01/17/26 | 29.91% | 191.69% | 1.40 | -14.36% | 0.61 |

Also observed:

```text
codex_strategy_sc_lgbm2_loss15_oos_v1: native Summary showed N/A / no usable completed result.
codex_strategy_sc_lgbm2_lowvol_oos_v1: native Summary showed N/A / no usable completed result.
```

Decision: no existing native single-strategy variant clears Sharpe >1.9. The best long-window native AI Factor strategy remains `codex_strategy_sc_lgbm2_oos_v1_top1` / equivalent lowbeta copy at Sharpe 1.60 with very strong active return. Existing rule tweaks, monthly rebalance, position count, liquidity filter, stop loss, and market gate did not solve the volatility/Sharpe problem. The next high-value branch should be a new model or materially different validation design, not more wrappers around the same signal.

## Native TSCV Saved-Prediction Test: codex_ai_sc_lgbm_tscv_smooth_v1 / lightgbm slow 3

Timestamp: 2026-05-25 20:47 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test the strongest currently available Time Series CV saved-prediction branch before spending new Resource Units. This branch offered a much longer defensible validation window than the recent Basic Holdout models, so it had decision value despite only moderate model-table Sharpe.

AI Factor setup verified on platform:

```text
AI Factor: codex_ai_sc_lgbm_tscv_smooth_v1
AI Factor ID: 28636
Universe: No OTC Exchange + min 10 mil min vol - OWN
Dataset period: 2006-01-01 to 2026-01-17
Validation method: Time Series CV
Folds: 8
Training period: 11.7 - 18.7 years
Holdout period: 12 months
Gap: 20 weeks
Testing: No
Visible Resource Units: 22 total for AI Factor, 3 RU for each completed validation model
```

Model selected:

```text
Model: lightgbm slow 3
Native model Rank: 100
Formula: AIFactorValidation("codex_ai_sc_lgbm_tscv_smooth_v1", "lightgbm slow 3")
Formula dialog period: 01/13/2018 - 01/17/2026
Formula dialog frequency: Every Week
```

Compare-table signal quality:

| Metric | Result |
| --- | ---: |
| RMSE | 0.5678 |
| Spearman | 0.1743 |
| High-Low Avg | 37.46 |
| High-Low Sharpe | 0.97 |
| High Avg | 20.83 |
| High Sharpe | 0.89 |
| High SD | 21.42 |
| High Turnover | 964 |
| Low Avg | -12.17 |
| Low Sharpe | -0.31 |

Native simulated strategy created:

```text
Name: codex_strategy_sc_tscv_lgbmslow3_oos_v1
Port ID: 1944248
Type: Native P123 simulated strategy
Period: 01/13/2018 - 01/17/2026
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Transaction type: Long
Use margin: No
Positions: 20
Sizing: Static Weight, 5.0%
Rebalance: Every Week
Buy constraint: 30% +/-
Slippage: Variable
Ranking system shown in strategy: Core Combination
Buy signal: FRank(`AIFactorValidation("codex_ai_sc_lgbm_tscv_smooth_v1", "lightgbm slow 3")`, #All, #Desc) > 99
Additional buy rules: Close(0) > 0.5; AvgDailyTot(20) > 10000
Sell signal: FRank(`AIFactorValidation("codex_ai_sc_lgbm_tscv_smooth_v1", "lightgbm slow 3")`, #All, #Desc) < 99
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Total Return | 90.84% |
| Benchmark Return | 181.98% |
| Active Return | -91.14% |
| Annualized Return | 8.40% |
| Annual Turnover | 1,309.71% |
| Max Drawdown | -56.78% |
| Benchmark Max Drawdown | -33.72% |
| Overall Winners | 996 / 2188, 45.00% |
| Sharpe Ratio | 0.37 |
| Correlation with SPY | 0.71 |

Decision: reject. This fails every hard goal except being a native long-only AI Factor strategy. The long Time Series CV window did not translate into portfolio quality: Sharpe was 0.37, SPY-relative active return was deeply negative, turnover was extremely high, and max drawdown was much worse than the benchmark. The binding constraint on this branch is model/portfolio quality, not platform date availability. Do not spend more Resource Units extending this exact TSCV smooth branch without a materially different feature/target design.

## Free Inventory Check: Existing SP500 AI Factors

Timestamp: 2026-05-25 20:55 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: check lower-volatility SP500 AI Factor inventory before spending new Resource Units. The goal is Sharpe-led, so an SP500/no-financials branch could be more attractive than microcap models if model-table High bucket Sharpe is materially stronger.

Candidates reviewed:

| AI Factor | ID | Universe | Best visible model-table signal | Decision |
| --- | ---: | --- | --- | --- |
| agent_highsr_lgbm_sp500_v1 | 27238 | SP500_NoFinancials | Best High SR about 0.73; H-L SR about 0.50 | Reject before native sim |
| SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials | 20725 | SP500_NoFinancials | Best usable High SR about 0.66; one inverted model had Low SR 1.27 but negative H-L | Reject before native sim |
| SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm | 20721 | S&P500 LargeCap (IVV) | `deeptables wide_regularized` High Avg 24.06%, High SR 1.10, but H-L SR only 0.06 and turnover about 1,002% | Watchlist only, not promoted yet |

Decision: no free SP500 AI Factor candidate currently justifies a native strategy build ahead of better experiments. The one superficially interesting model (`20721` / `deeptables wide_regularized`) has a decent High bucket but essentially no High-minus-Low separation, suggesting broad regime or benchmark exposure rather than reliable ranking power. Under the cost policy, the next RU spend should target a new Sharpe-aware design rather than promoting these weak/inverted SP500 validations.

## Native Construction Variant: Faster AI Exit on Current Best Model

Timestamp: 2026-05-25 21:18 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test a no-Resource-Unit construction tweak before spending on new AI Factor training. The current best native strategy buys the top 1% by the `lightgbm II` validation signal and sells when the signal falls below the top 5%. This variant kept the proven model but sold when the signal fell below the top 1%, to see whether quicker replacement improved Sharpe.

Native simulated strategy created:

```text
Name: codex_strategy_sc_lgbm2_sell99_oos_v1
Port ID: 1944255
Type: Native P123 simulated strategy
Period: 08/22/2020 - 01/17/2026
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Transaction type: Long
Use margin: No
Positions: 20
Rebalance: Every Week
Buy signal: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99
Sell signal: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 99
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Total Return | 191.79% |
| Benchmark Return | 120.07% |
| Active Return | 71.72% |
| Annualized Return | 21.90% |
| Annual Turnover | 1,546.06% |
| Max Drawdown | -22.33% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 854 / 1786, 47.00% |
| Sharpe Ratio | 0.98 |
| Correlation with SPY | 0.66 |

Decision: reject. Faster AI exits made the strategy much worse than the current baseline. Turnover exploded, return fell, drawdown worsened, and Sharpe dropped from 1.60 to 0.98. The current model needs smoother construction or better features, not a more reactive sell threshold.

## Native Construction Variant: Top-Decile AI Admission Pool

Timestamp: 2026-05-25 21:23 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test whether the `lightgbm II` signal works better as a broad top-decile admission filter, with Core Combination choosing the 20-stock portfolio inside that pool. This was a no-Resource-Unit native construction test motivated by the model-table High bucket Sharpe.

Native simulated strategy created:

```text
Name: codex_strategy_sc_lgbm2_buy90_sell80_oos_v1
Port ID: 1944257
Type: Native P123 simulated strategy
Period: 08/22/2020 - 01/17/2026
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Transaction type: Long
Use margin: No
Target positions: 20; ending positions shown: 21
Rebalance: Every Week
Buy signal: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 90
Sell signal: FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 80
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Total Return | 270.24% |
| Benchmark Return | 120.07% |
| Active Return | 150.17% |
| Annualized Return | 27.38% |
| Annual Turnover | 160.31% |
| Max Drawdown | -16.48% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 112 / 195, 57.00% |
| Sharpe Ratio | 1.36 |
| Correlation with SPY | 0.72 |

Decision: reject. The broader AI admission pool reduced turnover dramatically and kept active return positive, but Sharpe fell from the 1.60 baseline to 1.36. This indicates the useful `lightgbm II` edge is concentrated near the extreme top percentile; broadening the pool dilutes the signal more than it stabilizes the portfolio.

## New AI Factor Experiment: Small-Cap 3M Relative Return Target

Timestamp: 2026-05-25 21:07 -04:00 to 21:08 -04:00

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

Purpose: test whether the current best 32-feature small-cap AI Factor improves Sharpe when trained on relative return instead of raw total return. The current leader uses `3MTotReturn`, which creates very high active return but only 1.60 native Sharpe. A `3MRel` target is a targeted attempt to train the model toward alpha/market-relative behavior before spending on broader model sweeps.

AI Factor clone created:

```text
Name: codex_ai_sc_3mrel_lgbm2_oos_v1
AI Factor ID: 28647
Source AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Source AI Factor ID: 27417
Target changed from: 3MTotReturn
Target changed to: 3MRel
Target normalization after target change: Dataset / Date shown by P123
Training universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Prediction universe: Same as training universe
Dataset period: 2006-01-01 to 2026-01-17
Frequency: Every Week
Features: 32
Feature normalization: Rank
Validation method: Basic Holdout
Gap: 20 weeks
Training period: 14.3 years
Holdout period: 65 months
Testing: No
```

Resource usage:

```text
Initial load page estimate: 359MB, about 102.5M data points, 14 Resource Units
Actual loaded dataset shown after completion: 315MB, 79.5M data points, 12 Resource Units
Load start: 5/25/2026, 8:03 PM
Load time: 1 min, 23 sec
Target Information Regression: left disabled
Validation model started: lightgbm II
Save Validation Predictions: Yes
Validation result: SUCCESS, Basic: 46 sec (1.2 GB), 3 Resource Units
```

Model-table result:

| Metric | Result |
| --- | ---: |
| Native model Rank | 100 |
| RMSE | 0.5662 |
| Spearman | 0.1885 |
| High-Low Avg | 44.90 |
| High-Low Sharpe | 1.13 |
| High Avg | 27.52 |
| High Sharpe | 1.38 |
| High SD | 17.71 |
| High Turnover | 1,135 |
| Low Avg | -12.07 |
| Low Sharpe | -0.31 |
| Low Turnover | 834 |

Decision: stop before native simulation. Although the model completed successfully and saved validation predictions, the model-table signal is much weaker than the original `3MTotReturn` version of `lightgbm II`, which had High bucket Sharpe around 2.40 and still only reached 1.60 Sharpe in native simulation. The `3MRel` target reduced expected beta/raw-return behavior, but did not create a strong enough ranking edge to justify promoting to a native strategy. Do not spend more Resource Units on this exact 3MRel branch unless a different model preset is explicitly chosen for a narrow follow-up.

Follow-up model on same loaded dataset:

```text
Model: extra trees II
Reason: Extra Trees can be more stable than LightGBM on noisy relative-return targets with only 32 features.
Save Validation Predictions: Yes
Validation result: SUCCESS, Basic: 7 min, 35 sec (1.0 GB), 3 Resource Units
```

Extra Trees model-table result:

| Metric | Result |
| --- | ---: |
| Native model Rank | 50 |
| RMSE | 0.5663 |
| Spearman | 0.2100 |
| High-Low Avg | 39.34 |
| High-Low Sharpe | 0.92 |
| High Avg | 22.27 |
| High Sharpe | 1.17 |
| High SD | 17.26 |
| High Turnover | 549 |
| Low Avg | -12.32 |
| Low Sharpe | -0.31 |
| Low Turnover | 533 |

Decision: reject before native simulation. Extra Trees improved Spearman and roughly halved model-table turnover versus `lightgbm II`, but the High bucket Sharpe fell to 1.17 and H-L Sharpe fell to 0.92. It is more stable but too weak. The 3MRel branch does not currently justify promotion into a native simulated strategy.

## 2026-05-25 21:28 EDT - 6MTotRet clone period boundary blocked before load

Candidate:

```text
Name: codex_ai_sc_6mtot_lgbm2_oos_v1
AI Factor ID: 28648
Source AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Source AI Factor ID: 27417
Target changed from: 3MTotReturn
Target changed to: 6MTotRet
Rationale: preserve the source model's raw-return alpha family, but lengthen the target horizon to reduce ranking noise and turnover before trying another LightGBM validation.
```

Observed platform behavior:

```text
Dataset / Period page displays:
Start: 2006-01-01
End: 2025-11-15
Target Lookahead: 27 weeks
Frequency: Every Week
Max Return: 999

Load modal still displays:
Period: 2006-01-01 to 2026-01-17
Features: 32
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Normalization: Rank
Estimated data: about 359MB / 102.5M data points / 14 Resource Units
```

Tried platform-only fixes:

```text
1. Touched the end-date field and blurred it.
2. Changed the end date to 2025-11-14, blurred, and revisited the Load page.
3. Used the Period page Choose -> MAX preset.
4. Used the Period page Choose -> 20 years preset.
5. Saved object properties through Edit Details without changing the name.
```

Result: P123 continued to pass the cloned source end date (`2026-01-17`) to the load job. Pressing Start rejected before dataset load with: `Period cannot end after 2025-11-15 due to target lookahead`.

Cost impact: no dataset load completed and no model validation was started for this branch, so no successful dataset/model Resource Units were consumed here.

Decision: stop this clone for now. The 6-month target idea remains conceptually reasonable, but this specific cloned AI Factor is stuck in a stale-period state through the visible platform controls. Continue the campaign with lower-cost native strategy construction variants or a fresh AI Factor branch that avoids this clone-state issue.

## 2026-05-25 21:34 EDT - zero-RU native strategy variant inventory

Reviewed existing native simulated strategies that reuse the strongest small-cap AI Factor family. This was a platform-only summary-page read; no API calls, no dataset loads, no model validations.

| Strategy | Port ID | Annualized | Active Return | Max DD | Sharpe | Corr SPY | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| baseline `codex_strategy_sc_lgbm2_oos_v1_top1` | 1944200 | 35.94% | 306.26% | -15.65% | 1.60 | 0.67 | Current native best |
| smooth exit | 1944201 | 28.97% | 175.87% | -15.08% | 1.29 | 0.66 | Reject |
| concentrated 10 positions | 1944203 | 33.29% | 252.96% | -18.04% | 1.35 | 0.62 | Reject |
| liquidity 50k | 1944209 | 35.40% | 294.86% | -15.65% | 1.59 | 0.66 | Near-tie, not better |
| monthly rebalance | 1944210 | 32.60% | 239.98% | -14.98% | 1.42 | 0.64 | Reject |
| top-of-factor variant | 1944215 | 35.06% | 287.93% | -19.47% | 1.58 | 0.63 | Reject |
| low beta copy | 1944220 | 35.94% | 306.26% | -15.65% | 1.60 | 0.67 | Same as baseline |
| quality/size filter | 1944221 | 31.73% | 223.84% | -16.80% | 1.37 | 0.68 | Reject |
| stop 15 | 1944223 | 32.30% | 234.27% | -15.76% | 1.50 | 0.63 | Reject |
| 30 positions | 1944224 | 31.99% | 228.57% | -17.14% | 1.46 | 0.67 | Reject |
| sell 99 | 1944255 | 21.90% | 71.72% | -22.33% | 0.98 | 0.66 | Reject |
| buy 90 / sell 80 | 1944257 | 27.38% | 150.17% | -16.48% | 1.36 | 0.72 | Reject |

Also checked the `lightgbm slow 3` construction family:

| Strategy | Port ID | Annualized | Active Return | Max DD | Sharpe | Corr SPY | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| slow3 v1 | 1944196 | 25.71% | 124.56% | -17.03% | 1.24 | 0.63 | Reject |
| slow3 smooth | 1944197 | 22.70% | 82.29% | -22.41% | 1.11 | 0.67 | Reject |
| slow3 smooth exit | 1944198 | 24.70% | 109.94% | -18.39% | 1.19 | 0.64 | Reject |
| slow3 market gate | 1944199 | 21.71% | 69.33% | -17.49% | 1.09 | 0.41 | Reject |

Interpretation: the existing zero-RU construction variants do not get close to the >1.9 OOS Sharpe target. The baseline remains hard to beat; broadening, smoothing, monthly rebalance, stop-loss rules, simple liquidity/quality filters, and the prior market gate mostly reduce return faster than they reduce volatility.

## 2026-05-25 21:40 EDT - existing source ExtraTrees check

Reviewed the already-trained `extra trees II` row on the strongest source AI Factor before spending any new Resource Units.

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
AI Factor ID: 27417
Model: extra trees II
Status: SUCCESS
Existing validation cost shown by platform: 3 Resource Units on 04/21/2026
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "extra trees II")
```

Compare-table diagnostics:

| Metric | Result |
| --- | ---: |
| Native model Rank | 35 |
| RMSE | 0.5663 |
| Spearman | 0.2097 |
| High-Low Avg | 96.13 |
| High-Low Sharpe | 1.11 |
| High Avg | 31.63 |
| High Sharpe | 1.58 |
| High Turnover | 940 |
| Low Avg | -33.23 |
| Low Sharpe | -0.62 |
| Low Turnover | 955 |

Decision: reject before native simulation. ExtraTrees is materially smoother than the LightGBM rows by turnover, but the High-bucket Sharpe is only `1.58`, far below the current native leader model's `2.40` high-bucket Sharpe and below the desired portfolio-level Sharpe target. Since multiple stronger LightGBM rows already failed native Sharpe `>1.9`, this existing ExtraTrees row does not have enough promotion value.

## 2026-05-25 21:41 EDT - custom 1+2+3M target branch

Purpose: test a target that favors faster-persistence winners instead of a single 3-month endpoint. This follows the AI Factor guide's combined multi-month target idea and keeps the target lookahead near 3 months, avoiding the stale 6-month lookahead issue from the prior branch.

Custom target created through the platform UI:

```text
Target name: codex_1m2m3m_totret_v1
Description: Sum of 1-month, 2-month, and 3-month forward total returns for a faster-persistence AI Factor target.
Formula: Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)
```

The previous unloaded 6-month clone was repurposed and renamed:

```text
AI Factor name: codex_ai_sc_123m_lgbm2_oos_v1
AI Factor ID: 28648
Source AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Training universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Feature normalization: Rank
Dataset period accepted by Load: 2006-01-01 to 2026-01-17
Features: 32
Target normalization shown: Dataset / Date
```

Resource usage:

```text
Initial load estimate: about 359MB / 102.5M data points / 14 Resource Units
Actual loaded dataset: 315MB / 79.5M data points / 12 Resource Units
Load start: 5/25/2026, 8:36 PM
Load time: 1 min, 28 sec
Validation model: lightgbm II
Worker shown: Premium
Save Validation Predictions: Yes
Validation result: SUCCESS, Premium: 34 sec (1.2 GB), 3 Resource Units
Total successful new Resource Units in this branch: 15
```

Compare-table diagnostics at `Quantiles 100`:

| Metric | Result |
| --- | ---: |
| Native model Rank | 100 |
| RMSE | 0.5685 |
| Spearman | 0.1678 |
| High-Low Avg | 240.55 |
| High-Low Sharpe | 2.18 |
| High Avg | 55.42 |
| High Sharpe | 2.16 |
| High Turnover | 1,963 |
| Low Avg | -55.21 |
| Low Sharpe | -1.28 |
| Low Turnover | 1,332 |

Decision before native run: promote exactly once. The model-table result did not beat the current source `lightgbm II` row on High-bucket Sharpe (`2.16` vs `2.40`), but it improved High-Low Sharpe (`2.18`) and spread quality enough to justify one native simulated strategy.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_strategy_sc_123m_lgbm2_oos_v1_top1
Port ID: 1944275
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944275
Formula: AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II")
Buy:  FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc) > 99
Sell: FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc) < 95
Other buy rules: Close(0) > 0.5; AvgDailyTot(20) > 10000
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 363.89% |
| Benchmark Return | 120.07% |
| Active Return | 243.82% |
| Annualized Return | 32.81% |
| Annual Turnover | 419.31% |
| Max Drawdown | -17.33% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 289 / 502, 57.00% |
| Sharpe Ratio | 1.40 |
| Correlation with SPY | 0.67 |

Decision: reject. The 1+2+3M target produced an attractive top-1% model-table spread, but the native long-only strategy gave up too much smoothness and did not beat the current native leader (`35.94%` annualized, `1.60` Sharpe, `-15.65%` max drawdown). This is another example of model-table high-low strength not translating into portfolio-level Sharpe under the strict top-1% weekly construction.

## 2026-05-25 21:54 EDT - blended 3M endpoint and 1+2+3M target signal

Purpose: test a no-new-RU native construction that requires agreement between the current native leader's original 3-month total-return signal and the new 1+2+3M faster-persistence signal. This uses percentile-rank averaging rather than raw prediction averaging so the two AI Factor outputs are on the same 0-100 scale.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_strategy_sc_blend3m123m_lgbm2_oos_v1
Port ID: 1944281
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944281
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
New Resource Units: 0
```

Rules:

```text
Source rank:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)

Persistence rank:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc)

Buy:
(source rank + persistence rank) / 2 > 99

Sell:
(source rank + persistence rank) / 2 < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 339.52% |
| Benchmark Return | 120.07% |
| Active Return | 219.45% |
| Annualized Return | 31.49% |
| Annual Turnover | 398.54% |
| Max Drawdown | -14.60% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 281 / 479, 58.00% |
| Sharpe Ratio | 1.43 |
| Correlation with SPY | 0.65 |

Decision: reject. The blended agreement filter improved drawdown versus the current leader (`-14.60%` vs `-15.65%`) and maintained strong active return versus SPY, but it gave up too much annualized return and reduced Sharpe from `1.60` to `1.43`. The two-signal agreement idea helps risk a little, but it does not solve the portfolio-level Sharpe constraint.

## 2026-05-25 22:03 EDT - LightGBM II top-2% admission pool

Purpose: test the narrow middle point between the current top-1% native leader and the rejected top-10% admission-pool variant. This is a no-new-RU construction test: the hypothesis was that admitting the top 2% by AI Factor rank might reduce selection fragility without diluting the signal as much as the top-10% test did.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_strategy_sc_lgbm2_top2_oos_v1
Port ID: 1944282
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944282
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
New Resource Units: 0
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 98

Sell:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 329.58% |
| Benchmark Return | 120.07% |
| Active Return | 209.51% |
| Annualized Return | 30.93% |
| Annual Turnover | 494.82% |
| Max Drawdown | -16.80% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 327 / 579, 56.00% |
| Sharpe Ratio | 1.46 |
| Correlation with SPY | 0.64 |

Decision: reject. The top-2% admission pool reduced SPY correlation slightly, but it diluted the return edge and increased turnover versus the current top-1% leader. Together with the rejected top-10% and top-1% sell-threshold variants, this closes the obvious AI-rank threshold tuning path: the useful signal is concentrated at the extreme top percentile, and widening the gate does not improve Sharpe.

## 2026-05-25 22:09 EDT - LightGBM II every-2-weeks rebalance

Purpose: test the middle cadence between the current weekly leader and the rejected monthly variant. This is a no-new-RU construction test: the hypothesis was that every-2-weeks rebalance might lower turnover without losing as much alpha freshness as monthly rebalance.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_strategy_sc_lgbm2_2wk_oos_v1
Port ID: 1944283
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944283
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight
Rebalance: Every 2 Weeks
New Resource Units: 0
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 360.28% |
| Benchmark Return | 120.07% |
| Active Return | 240.21% |
| Annualized Return | 32.62% |
| Annual Turnover | 361.01% |
| Max Drawdown | -15.14% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 253 / 426, 59.00% |
| Sharpe Ratio | 1.40 |
| Correlation with SPY | 0.67 |

Decision: reject. Every-2-weeks rebalance reduced turnover and slightly improved drawdown versus the weekly leader, but gave up too much return and reduced Sharpe from `1.60` to `1.40`. Cadence smoothing is now bracketed: weekly remains best, every 2 weeks is worse, and the prior monthly variant was also worse.

## 2026-05-25 22:14 EDT - LightGBM II quality/value overlay calibration

Purpose: test a no-new-Resource-Unit construction axis that is different from the prior blunt quality/size gates and raw AI-rank threshold sweeps. Instead of requiring only the raw AI Factor percentile, these variants used an 85% AI rank / 10% ROE rank / 5% price-to-sales value rank composite directly in the native strategy buy/sell rules.

Shared setup:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
New Resource Units: 0
```

Composite expression:

```text
(0.85*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.10*FRank(`ROE%TTM`, #All, #Desc)+0.05*FRank(`Pr2SalesTTM`, #All, #Asc))
```

### Overlay top-1% admission

```text
Name: codex_sc_lgbm2_aiqualval_v1
Port ID: 1944288
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944288
Buy: composite > 99
Sell: composite < 95
Other buy rules: Close(0) > 0.5; AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 6.83% |
| Benchmark Return | 120.07% |
| Active Return | -113.24% |
| Annualized Return | 1.23% |
| Annual Turnover | 19.69% |
| Max Drawdown | -3.15% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 11 / 24, 45.00% |
| Sharpe Ratio | -0.79 |
| Correlation with SPY | -0.04 |
| Ending Positions | 0 |

Decision: reject. The overlay was far too restrictive at the top-1% gate. It nearly eliminated exposure, ended with zero holdings, failed the active-return hurdle by a wide margin, and produced a negative Sharpe. This does not indicate investable risk control; it indicates sparse-selection failure.

### Overlay top-2% admission

```text
Name: codex_sc_lgbm2_aiqv98_v1
Port ID: 1944290
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944290
Buy: composite > 98
Sell: composite < 93
Other buy rules: Close(0) > 0.5; AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 47.98% |
| Benchmark Return | 120.07% |
| Active Return | -72.09% |
| Annualized Return | 7.52% |
| Annual Turnover | 105.19% |
| Max Drawdown | -13.38% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 76 / 133, 57.00% |
| Sharpe Ratio | 0.51 |
| Correlation with SPY | 0.54 |
| Ending Positions | 3 |

Decision: reject. Loosening the composite gate improved exposure but still left the strategy badly underinvested and benchmark-relative performance deeply negative. The small quality/value overlay does not solve the Sharpe problem; it suppresses the AI Factor's high-return tail faster than it improves volatility. This closes the simple in-rule quality/value overlay branch for the current LightGBM II leader unless a broader ranking-system redesign is created inside the platform.

## 2026-05-25 22:31 EDT - LightGBM II immediate-buyback setting

Purpose: test another no-new-Resource-Unit construction knob on the current leader before spending on more AI Factor training. The hypothesis was that the weekly rebalance might be losing some alpha if a sold name could not be immediately bought back when it still ranked well.

Workflow note: the previously identified 15-position midpoint test remains unsafe through the current in-app browser surface. The P123 `posWeight` masked input repeatedly concatenated typed values instead of replacing them, and the browser sandbox blocked normal form-post helpers. Do not count the 15-position branch as a native result until the Review page can explicitly show `Ideal Size of a New Position` near `6.67%` and `Ideal Number of Positions` `15`.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_sc_lgbm2_buyback_v1
Port ID: 1944299
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944299
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Allow Immediate Buyback: Yes
New Resource Units: 0
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 426.33% |
| Benchmark Return | 120.07% |
| Active Return | 306.26% |
| Annualized Return | 35.94% |
| Annual Turnover | 398.55% |
| Max Drawdown | -15.65% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 278 / 474, 58.00% |
| Sharpe Ratio | 1.60 |
| Correlation with SPY | 0.67 |

Decision: reject as non-improving. The result exactly matched the current leader's headline return, turnover, drawdown, Sharpe, and correlation. Immediate buyback is effectively non-binding here, or at least not enough to change the native path. The current leader remains `codex_strategy_sc_lgbm2_oos_v1_top1`.

## 2026-05-25 22:29 EDT - 1+2+3M target ExtraTrees stability check

Purpose: spend a small model-only RU amount on an already-loaded dataset instead of paying for another dataset load. The prior `1+2+3M` target LightGBM II model had strong model-table spread but produced only `1.40` native Sharpe. This test asked whether ExtraTrees could keep enough edge while reducing turnover/noise.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

AI Factor branch:

```text
AI Factor: codex_ai_sc_123m_lgbm2_oos_v1
AI Factor ID: 28648
Target: codex_1m2m3m_totret_v1
Target formula: Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)
Universe: No OTC Exchange + min 10 mil min vol - OWN
Dataset: already loaded
Model started: extra trees II
Worker shown after start: Premium
Save Validation Predictions: Yes
New Resource Units: 3
```

Validation model status:

```text
Model: extra trees II
Status: SUCCESS
Runtime: Premium: 3 min, 10 sec (1.0 GB)
Resource Units: 3
Update Date: 10:28 PM
Native model Rank: 50
```

Compare-table diagnostics at Quantiles 100 / Slippage 0.1%:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm II | 100 | 0.5685 | 0.1678 | 240.55 | 2.18 | 55.42 | 2.16 | 1,963 | -55.21 | -1.28 | 1,332 |
| extra trees II | 50 | 0.5685 | 0.1878 | 136.76 | 1.53 | 34.84 | 1.72 | 923 | -43.58 | -0.93 | 973 |

Decision: reject before native simulation. ExtraTrees cut high-bucket turnover by more than half and improved Spearman, but it gave up too much return edge: High bucket Sharpe fell from `2.16` to `1.72`, H-L Sharpe fell from `2.18` to `1.53`, and High Avg fell from `55.42%` to `34.84%`. Since the stronger LightGBM II row from the same target already failed native promotion with only `1.40` Sharpe, this weaker ExtraTrees row has no clear path to the hard `>1.9` native Sharpe target. Do not promote `extra trees II` to a simulated strategy.

## 2026-05-25 22:34 EDT - 1+2+3M target LightGBM medium 3 promotion test

Purpose: spend one small model-only run on the already-loaded `1+2+3M` target branch to see whether a nearby LightGBM variant could improve the long-only high bucket enough to justify a native simulation. The prior `lightgbm II` model from this branch produced strong model-table spread but only `1.40` native Sharpe, so this was a narrow promotion test rather than a broad sweep.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

AI Factor branch:

```text
AI Factor: codex_ai_sc_123m_lgbm2_oos_v1
AI Factor ID: 28648
Target: codex_1m2m3m_totret_v1
Target formula: Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)
Universe: No OTC Exchange + min 10 mil min vol - OWN
Dataset: already loaded
Model started: lightgbm medium 3
Worker shown after start: Premium
Save Validation Predictions: Yes
New Resource Units: 3
```

Validation model status:

```text
Model: lightgbm medium 3
Status: SUCCESS
Runtime: Premium: 51 sec (1.2 GB)
Resource Units: 3
Update Date: 10:33 PM
Native model Rank: 100
```

Compare-table diagnostics at Quantiles 100 / Slippage 0.1%:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm II | 100 | 0.5685 | 0.1678 | 240.55 | 2.18 | 55.42 | 2.16 | 1,963 | -55.21 | -1.28 | 1,332 |
| lightgbm medium 3 | 100 | 0.5683 | 0.1714 | 203.59 | 2.14 | 61.48 | 2.41 | 1,899 | -47.53 | -1.09 | 1,221 |
| extra trees II | 33 | 0.5685 | 0.1878 | 136.76 | 1.53 | 34.84 | 1.72 | 923 | -43.58 | -0.93 | 973 |

Promotion rationale: promote to one native simulated strategy because `lightgbm medium 3` improved High Avg from `55.42%` to `61.48%`, improved High SR from `2.16` to `2.41`, slightly reduced high-bucket turnover, and kept H-L SR near the original `lightgbm II` row.

Native simulated strategy created through the safe `Save As a new "Simulated Strategy"` workflow:

```text
Name: codex_sc_123m_lgbm_med3_v1
Port ID: 1944311
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944311
Formula: AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm medium 3")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
New Resource Units after model: 0
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm medium 3")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm medium 3")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 329.97% |
| Benchmark Return | 120.07% |
| Active Return | 209.90% |
| Annualized Return | 30.96% |
| Annual Turnover | 413.01% |
| Max Drawdown | -17.35% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 264 / 490, 53.00% |
| Sharpe Ratio | 1.32 |
| Correlation with SPY | 0.68 |

Decision: reject. The model table correctly identified a stronger high bucket, but the native portfolio did not translate that into better risk-adjusted returns. Native Sharpe fell to `1.32` versus the current leader's `1.60`, annualized return fell to `30.96%` versus `35.94%`, and drawdown worsened to `-17.35%` versus `-15.65%`. This weakens the case for more nearby `1+2+3M` model variants unless the next candidate changes the design axis materially.

## 2026-05-25 22:42 EDT - 1+2+3M target LightGBM II TOF model gate

Purpose: spend one more small model-only run on the already-loaded `1+2+3M` target branch, but only on a variant with a distinct rationale. `lightgbm II - TOF` was chosen because the TOF family was close to the current leader on the original small-cap AI Factor, and the unresolved constraint is portfolio translation, turnover, and risk-adjusted performance rather than raw model-table rank.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used.

AI Factor branch:

```text
AI Factor: codex_ai_sc_123m_lgbm2_oos_v1
AI Factor ID: 28648
Target: codex_1m2m3m_totret_v1
Target formula: Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)
Universe: No OTC Exchange + min 10 mil min vol - OWN
Dataset: already loaded
Model started: lightgbm II - TOF
Worker shown after start: Premium
Save Validation Predictions: Yes
New Resource Units: 3
```

Validation model status:

```text
Model: lightgbm II - TOF
Status: SUCCESS
Runtime: Premium: 1 min, 3 sec (1.2 GB)
Resource Units: 3
Update Date: 10:42 PM
Native model Rank: 50
```

Compare-table diagnostics at Quantiles 100 / Slippage 0.1%:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm II | 100 | 0.5685 | 0.1678 | 240.55 | 2.18 | 55.42 | 2.16 | 1,963 | -55.21 | -1.28 | 1,332 |
| lightgbm medium 3 | 75 | 0.5683 | 0.1714 | 203.59 | 2.14 | 61.48 | 2.41 | 1,899 | -47.53 | -1.09 | 1,221 |
| lightgbm II - TOF | 50 | 0.5686 | 0.1651 | 224.27 | 2.31 | 62.76 | 2.29 | 1,987 | -50.60 | -1.20 | 1,375 |
| extra trees II | 25 | 0.5685 | 0.1878 | 136.76 | 1.53 | 34.84 | 1.72 | 923 | -43.58 | -0.93 | 973 |

Native-promotion decision: TOF has enough model-table evidence for one native simulation because it has the best H-L SR (`2.31`) and highest High Avg (`62.76%`) in this branch. However, the native strategy was not run in this step because the in-app browser's long text-entry path failed with a virtual-clipboard error while editing the P123 wizard Text Editor, and the browser security policy blocked a page-context JavaScript edit attempt. A draft clone named `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(5)` was created from the leader, but the formula remained the original `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `lightgbm II`; no native result from that draft should be counted.

Required native formula when the browser editing path is available:

```text
AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")
```

Required native strategy rules:

```text
Buy:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Decision: pending native simulation, not a success. Do not report this candidate as meeting the goal unless a native P123 simulated strategy later confirms Sharpe `>1.9` and active annualized return `>5pp` versus SPY/S&P 500 over the accepted OOS dates.

### Native simulation completed

Follow-up: the in-app browser text-entry issue was worked around through normal visible UI input by focusing the P123 Text Editor field and sending character-level keypresses. The Review page was verified before running. The strategy name remained P123's clone name, but it is still `codex_` prefixed.

Verified Review-page setup:

```text
Name shown by P123: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(5)
Formula: AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Allow Immediate Buyback: No
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

```text
Port ID: 1944327
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944327
```

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 360.65% |
| Benchmark Return | 120.07% |
| Active Return | 240.58% |
| Annualized Return | 32.64% |
| Annual Turnover | 436.88% |
| Max Drawdown | -18.32% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 292 / 519, 56.00% |
| Sharpe Ratio | 1.36 |
| Correlation with SPY | 0.66 |

Decision: reject. The TOF branch cleared the active-return requirement versus SPY, but it failed the hard Sharpe target and failed to beat the current native leader. It produced `1.36` Sharpe versus the leader's `1.60`, annualized return `32.64%` versus `35.94%`, and max drawdown `-18.32%` versus `-15.65%`. This is another strong example of model-table high-bucket strength not translating into superior long-only portfolio Sharpe.

## 2026-05-25 22:59 EDT - 70/30 leader plus 1+2+3M TOF consensus test

Purpose: run one zero-new-Resource-Unit construction test after the `1+2+3M` TOF model failed as a standalone signal. The hypothesis was that a 70% weight to the proven native leader plus 30% weight to the distinct `1+2+3M TOF` target might preserve most of the leader's edge while filtering out some unstable names.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used. No new AI Factor Resource Units were spent after the previously logged TOF model run.

Verified Review-page setup:

```text
Name shown by P123: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(6)
Port ID: 1944331
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944331
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Allow Immediate Buyback: No
```

Composite expression:

```text
(0.70*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.30*FRank(`AIFactorValidation("codex_ai_sc_123m_lgbm2_oos_v1", "lightgbm II - TOF")`, #All, #Desc))
```

Rules:

```text
Buy:
composite > 99

Sell:
composite < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 325.38% |
| Benchmark Return | 120.07% |
| Active Return | 205.31% |
| Annualized Return | 30.70% |
| Annual Turnover | 407.02% |
| Max Drawdown | -18.93% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 277 / 486, 56.00% |
| Sharpe Ratio | 1.30 |
| Correlation with SPY | 0.68 |

Decision: reject. The 70/30 cross-target consensus still cleared active return versus SPY, but it materially underperformed the current leader and failed the hard Sharpe hurdle. It reduced turnover versus TOF alone (`407.02%` vs `436.88%`) but gave up too much return and worsened drawdown. This closes the simple leader-plus-`1+2+3M TOF` blend branch; the campaign needs a materially different AI Factor/validation design rather than another nearby wrapper.

## 2026-05-25 23:25 EDT - Small-cap 1+2+3M clipped target branch

Purpose: test a materially different target design after repeated wrappers around the original leader failed to raise portfolio-level Sharpe. The hypothesis was that clipping the combined 1-, 2-, and 3-month forward return target might keep the strong small-cap top-tail signal while reducing outlier-chasing.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used for create/update/run/validation.

AI Factor setup:

```text
Source clone: SCs Small and Micro Cap Focus + 10 Mil min Replic2
New AI Factor ID: 28651
Final AI Factor name: codex_ai_sc_123mclip_lgbm2_oos_v1
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 2006-01-01 to 2026-01-17
Features: 32
Frequency: Every Week
Normalization: Rank
```

Rejected target attempt before spend:

```text
Target name: codex_1m2m3m_rank_v1
Formula: FRank(`Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)`, #All, #Desc)
P123 error: Formula cannot be used as a target. Ensure that your formula does not yield values as of the latest historical date (05/23/2026).
Resource Units spent: 0
```

Accepted target:

```text
Target name: codex_1m2m3m_clip_v1
Formula: Bound(Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65),-50,150)
```

Dataset load:

| Item | Result |
| --- | ---: |
| Estimated Resource Units | 14 |
| Actual Resource Units | 12 |
| Data Points | 315MB, 79.5M data points |
| Load Start | 2026-05-25 22:11 EDT |
| Load Time | 2 min, 3 sec |
| Status | Completed |

Validation model runs:

| Model | Rank | Validation | Resource Units | Runtime | Decision |
| --- | ---: | --- | ---: | --- | --- |
| `lightgbm II` | 100 | SUCCESS | 3 | Premium: 35 sec, 1.2 GB | promoted to native simulation |
| `extra trees II` | 50 | SUCCESS | 3 | Premium: 3 min, 9 sec, 1.0 GB | rejected before native |

Compare diagnostics at 100 quantiles and 0.1% slippage:

| Model | RMSE | Spearman | H-L Avg | H-L SR | High Avg | High SR | High Turn | Low Avg | Low SR | Low Turn |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `lightgbm II` | 0.5651 | 0.1634 | 211.59 | 2.11 | 61.98 | 2.35 | 1,970 | -48.76 | -1.10 | 1,320 |
| `extra trees II` | 0.5652 | 0.1816 | 150.23 | 1.63 | 34.19 | 1.64 | 926 | -46.97 | -1.03 | 924 |

Promotion rationale: `lightgbm II` had a stronger high bucket than the current leader's reference diagnostics, so it earned one native simulated-strategy run. `extra trees II` had better Spearman but weak high-bucket return and SR, so it was not promoted.

Native simulation for promoted LightGBM II:

```text
Name: codex_strategy_sc_123mclip_lgbm2_oos_v1
Port ID: 1944354
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944354
Formula: AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Allow Immediate Buyback: No
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 429.82% |
| Benchmark Return | 120.07% |
| Active Return | 309.75% |
| Annualized Return | 36.11% |
| Annual Turnover | 413.84% |
| Max Drawdown | -17.91% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 283 / 498, 56.00% |
| Sharpe Ratio | 1.54 |
| Correlation with SPY | 0.60 |

Decision: reject as a final goal candidate. This branch slightly improved total return, active return, annualized return, and correlation versus the current leader, but it did not beat the leader on Sharpe (`1.54` vs `1.60`) and remained far below the hard `>1.9` Sharpe requirement. The important learning is that clipped targets can improve top-tail return and reduce market correlation, but this specific version still leaves too much standalone volatility/drawdown for the requested Sharpe hurdle.

## 2026-05-25 23:37 EDT - Small-cap 3M smooth-path target branch

Purpose: test whether a target that explicitly penalizes uneven forward return paths can improve the portfolio-level Sharpe constraint. The prior clipped 1+2+3M branch improved return and lowered SPY correlation but still produced only `1.54` native Sharpe. This branch intentionally traded raw upside for smoother expected forward behavior.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used for create/update/run/validation.

Setup note: reused the existing unloaded source clone `27424` because the campaign log had previously marked it as usable only if a materially different target design justified a fresh dataset load. It was renamed before load.

AI Factor setup:

```text
AI Factor ID: 27424
AI Factor name: codex_ai_sc_3msmooth_lgbm2_oos_v1
Source shell: SCs Small and Micro Cap Focus + 10 Mil min - Copy
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 2006-01-01 to 2026-01-17
Features: 32
Frequency: Every Week
Normalization: Rank
```

Accepted target:

```text
Target name: codex_3m_smoothpath_v1
Formula: Bound(Future%Chg_D(65),-40,120) - 0.6*Abs(Future%Chg_D(22)-Future%Chg_D(65)/3) - 0.4*Abs(Future%Chg_D(44)-2*Future%Chg_D(65)/3)
Description: Reward 3M upside but penalize uneven 1M/2M/3M forward path.
```

Dataset load:

| Item | Result |
| --- | ---: |
| Estimated Resource Units | 14 |
| Actual Resource Units | 12 |
| Data Points | 315MB, 79.5M data points |
| Load Start | 2026-05-25 22:32 EDT |
| Load Time | 1 min, 24 sec |
| Status | Completed |

Validation model run:

| Model | Rank | Validation | Resource Units | Runtime | Decision |
| --- | ---: | --- | ---: | --- | --- |
| `lightgbm II` | 100 | SUCCESS | 3 | Premium: 35 sec, 1.2 GB | rejected before native simulation |

Compare diagnostics:

| Quantiles | RMSE | Spearman | H-L Avg | H-L SR | High Avg | High SR | High Turn | Low Avg | Low SR | Low Turn |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 0.5519 | 0.2976 | 38.78 | 0.90 | 19.52 | 1.05 | 809 | -13.95 | -0.35 | 689 |
| 100 | 0.5519 | 0.2976 | 84.20 | 1.02 | 20.71 | 1.20 | 1,639 | -34.79 | -0.66 | 1,241 |

Decision: reject before native simulation. The smooth-path target did improve rank correlation substantially versus prior branches, but it destroyed the investable top-bucket economics. At 100 quantiles, the high bucket produced only `20.71%` average return and `1.20` SR, far below the current leader's top-bucket profile and far below the level that has been necessary even to reach `1.60` native Sharpe. This is useful negative evidence: training directly toward a smoother forward path made the model better at broad ordering but too weak in the extreme top percentile where the long-only strategy actually buys.

## 2026-05-25 23:50 EDT - 50/50 leader plus clipped-target consensus

Purpose: run one zero-new-RU native construction test combining the current native leader with the clipped-target LightGBM branch. The clipped branch had similar annualized return and lower SPY correlation, but lower standalone Sharpe. The hypothesis was that a 50/50 rank consensus might preserve return while smoothing the path.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used. No new AI Factor Resource Units were spent.

Verified Review-page setup:

```text
Name: codex_strategy_sc_blend_lgbm2_123mclip_v1
Port ID: 1944377
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944377
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
```

Composite expression:

```text
(0.50*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.50*FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc))
```

Rules:

```text
Buy:
composite > 99

Sell:
composite < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 425.08% |
| Benchmark Return | 120.07% |
| Active Return | 305.01% |
| Annualized Return | 35.89% |
| Annual Turnover | 410.37% |
| Max Drawdown | -15.45% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 286 / 489, 58.00% |
| Sharpe Ratio | 1.59 |
| Correlation with SPY | 0.64 |

Decision: reject as non-improving. The 50/50 consensus improved max drawdown slightly versus the current leader (`-15.45%` vs `-15.65%`) and kept active return very strong, but it did not beat the leader's Sharpe (`1.59` vs `1.60`) and remained far below the hard `>1.9` requirement. This suggests the clipped target's lower SPY correlation is not sufficiently diversifying at the stock-selection level; it mostly selects a nearby high-volatility small-cap return tail.

## 2026-05-26 00:00 EDT - 80/20 leader plus clipped-target consensus

Purpose: run one zero-new-RU native construction test using a lighter consensus weight. The 50/50 blend reduced max drawdown a little but diluted return too much, so this test kept the current leader dominant at 80% and used the clipped-target branch as a 20% stabilizer.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used. No new AI Factor Resource Units were spent.

Verified Review-page setup:

```text
Name shown by P123: codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(7)
Intended test label: codex_strategy_sc_blend80_lgbm2_123mclip_v1
Port ID: 1944378
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944378
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
```

Composite expression:

```text
(0.80*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.20*FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm II")`, #All, #Desc))
```

Rules:

```text
Buy:
composite > 99

Sell:
composite < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 369.15% |
| Benchmark Return | 120.07% |
| Active Return | 249.07% |
| Annualized Return | 33.08% |
| Annual Turnover | 411.49% |
| Max Drawdown | -16.39% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 280 / 491, 57.00% |
| Sharpe Ratio | 1.44 |
| Correlation with SPY | 0.67 |

Decision: reject. The 80/20 consensus was worse than both the 50/50 blend and the current native leader. It retained the leader's market correlation (`0.67`) while giving up too much return, so it did not create the volatility reduction needed to move Sharpe toward `>1.9`. This is strong evidence that simple blending between the leader and the clipped-target branch is not the path; the next smart iteration should seek either a genuinely different error profile or a construction rule that directly controls the drawdown/volatility regime without sacrificing the leader's top-bucket edge.
## 2026-05-26 00:20 EDT - Clipped 1+2+3M medium-3 model and 6M setup failure

Purpose: make one cost-controlled model-only spend on an already-loaded AI Factor branch, then promote only if the compare table improved enough to justify a native simulation. Also record the parked fresh 6M target setup that failed before any Resource Units were quoted or spent.

Surface: Portfolio123 web platform UI in the in-app browser. No P123 API was used for AI Factor setup, validation, strategy editing, or native simulation.

### Parked fresh 6M total-return branch

```text
AI Factor ID: 28652
AI Factor name: codex_ai_sc_6mtot_lgbm2_oos_v1
Target: 6MTotRet
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Features: 32 imported from SCs Small and Micro Cap Focus + 10 Mil min Replic2
Normalization/scaling: Rank
Visible default rules: Minimum Liquidity 10000, Minimum Price 0.5, Min Price Bars 260
```

Dataset-period attempts included the platform `MAX` range visible as `2006-01-01 - 2025-11-22`, plus trading-date attempts such as `2006-01-03 - 2025-11-14`. The Period page repeatedly displayed `Unexpected error encountered. Please contact support.` After reload, the Validation Method page still said the dataset period was not set, and the Load status route also showed the same unexpected error. No load estimate appeared and no Resource Units were spent.

Decision: park the branch. The shell has the intended name, universe, target, 32 features, and Rank scaling, but it is not currently loadable through the platform because the dataset period does not persist.

### Low-cost model run on clipped branch

AI Factor branch:

```text
AI Factor: codex_ai_sc_123mclip_lgbm2_oos_v1
AI Factor ID: 28651
Dataset: already loaded
Model started: lightgbm medium 3
Worker: Premium
Save Validation Predictions: Yes
Runtime: 52 sec (1.2 GB)
New Resource Units: 3
Status: SUCCESS
Native model Rank: 100
```

Compare-table diagnostics at Quantiles 100 / Slippage 0.1%:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm medium 3 | 100 | 0.5649 | 0.1672 | 225.95 | 2.18 | 62.43 | 2.36 | 1,967 | -50.96 | -1.17 | 1,242 |
| lightgbm II | 66 | 0.5651 | 0.1634 | 211.59 | 2.11 | 61.98 | 2.35 | 1,970 | -48.76 | -1.10 | 1,320 |
| extra trees II | 33 | 0.5652 | 0.1816 | 150.23 | 1.63 | 34.19 | 1.64 | 926 | -46.97 | -1.03 | 924 |

Promotion rationale: `lightgbm medium 3` only marginally improved the completed clipped `lightgbm II`, but it improved RMSE, Spearman, high-low average, high-low Sharpe, and high-bucket Sharpe while leaving high-bucket turnover roughly unchanged. That was enough for exactly one native simulation check, not a model sweep.

Native simulated strategy:

```text
Name shown by P123: codex_sc_123m_lgbm_med3_v1 - Copy
Port ID: 1944381
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944381
Formula: AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm medium 3")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Period: 08/22/2020 - 01/17/2026
Positioning: long-only, 20 positions, 5.0% static weight, weekly rebalance
Allow Immediate Buyback: No
```

Rules:

```text
Buy:
FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm medium 3")`, #All, #Desc) > 99

Sell:
FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm medium 3")`, #All, #Desc) < 95

Other buy rules:
Close(0) > 0.5
AvgDailyTot(20) > 10000
```

Native P123 result:

| Metric | Result |
| --- | ---: |
| Period | 08/22/2020 - 01/17/2026 |
| Total Return | 373.88% |
| Benchmark Return | 120.07% |
| Active Return | 253.81% |
| Annualized Return | 33.33% |
| Annual Turnover | 416.12% |
| Max Drawdown | -15.53% |
| Benchmark Max Drawdown | -24.50% |
| Overall Winners | 278 / 497, 55.00% |
| Sharpe Ratio | 1.52 |
| Correlation with SPY | 0.62 |

Decision: reject. The clipped `medium 3` branch improved drawdown slightly versus the clipped `lightgbm II` strategy (`-15.53%` vs `-17.91%`) but did not improve enough on return smoothness. It also failed to beat the current native campaign leader `codex_strategy_sc_lgbm2_oos_v1_top1`, which remains `35.94%` annualized return, `1.60` Sharpe, and `-15.65%` max drawdown over the same accepted OOS window.

Workflow note: P123 requires the first `FRank()` argument to be a quoted formula string. The accepted strategy formula was the backtick form:

```text
FRank(`AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm medium 3")`, #All, #Desc)
```

Two rejected syntax attempts were useful:

```text
FRank(AIFactorValidation('codex_ai_sc_123mclip_lgbm2_oos_v1', 'lightgbm medium 3'), #All, #Desc)
FRank(AIFactorValidation("codex_ai_sc_123mclip_lgbm2_oos_v1", "lightgbm medium 3"), #All, #Desc)
```

The first failed because P123 treated single-quoted strings as invalid commands. The second failed because `FRank()` requires the first parameter to be a quoted string.

Updated conclusion: nearby clipped-target LightGBM variants do not appear to solve the Sharpe constraint. The hard goal remains unmet; the current best native AI Factor strategy is still `codex_strategy_sc_lgbm2_oos_v1_top1` / port `1944200`.

## 2026-05-26 00:43 EDT - Native simulated-strategy inventory sweep after clipped medium-3

Purpose: perform a zero-RU platform inventory check before spending on another AI Factor branch. This looked for an already-created `codex_` native simulated strategy that might quietly beat the documented campaign leader.

Surface: Portfolio123 web platform UI simulated-strategy opener. No P123 API was used and no Resource Units were spent.

Top visible native rows:

| Strategy / port | Annualized | Excess | Sharpe | Max DD | Read-through |
| --- | ---: | ---: | ---: | ---: | --- |
| `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` | 35.9% | 20.2% | 1.60 | -15.7% | Current native leader. |
| `codex_sc_lgbm2_buyback_v1` / `1944299` | 35.9% | 20.2% | 1.60 | -15.7% | Exact-equivalent copy, not an improvement. |
| `codex_strategy_sc_lgbm2_lowbeta_oos_v1` / `1944220` | 35.9% | 20.2% | 1.60 | -15.7% | Exact-equivalent copy, not an improvement. |
| `codex_strategy_sc_blend_lgbm2_123mclip_v1` / `1944377` | 35.9% | 20.2% | 1.59 | -15.5% | Slight drawdown improvement but lower Sharpe. |
| `codex_strategy_sc_lgbm2_oos_v4_liq50k` / `1944209` | 35.4% | 19.7% | 1.59 | -15.7% | Liquidity filter does not raise Sharpe. |
| `codex_strategy_sc_lgbm2_tof_oos_v1_top1` / `1944215` | 35.1% | 19.4% | 1.58 | -19.5% | Lower return and worse drawdown. |
| `codex_sc_123m_lgbm_med3_v1 - Copy` / `1944381` | 33.3% | 17.6% | 1.52 | -15.5% | Clipped-target branch rejected. |

Decision: no hidden native winner exists in the visible `codex_` strategy inventory. The best native strategy remains port `1944200` with `35.94%` annualized return, `1.60` Sharpe, and `-15.65%` max drawdown over the accepted `08/22/2020 - 01/17/2026` OOS window. Existing wrappers, threshold variants, liquidity variants, buyback variants, and simple blend variants appear exhausted. The next useful iteration should be a genuinely different AI Factor target/model design or an untested existing AI Factor branch with materially different validation diagnostics.

## 2026-05-26 00:51 EDT - Existing AI Factor table sweep before next spend

Purpose: inspect the platform's visible existing AI Factor inventory and the original small-cap model compare table before choosing any additional Resource Unit spend.

Surface: Portfolio123 web platform UI. No P123 API was used and no new Resource Units were spent.

Inventory notes:

| AI Factor | ID | Dataset | Validations | Results | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `SCs Small and Micro Cap Focus + 10 Mil min Replic2` | `27417` | 32 | 14 | 14 | Original source table rechecked. No new native promotion candidate. |
| `codex_ai_sc_3mrel_lgbm2_oos_v1` | `28647` | 32 | 14 | 2 | Already rejected before native simulation; high-bucket economics too weak. |
| `codex_ai_sc_123m_lgbm2_oos_v1` | `28648` | 32 | 14 | 4 | Multiple native promotions rejected, including TOF and consensus blend. |
| `codex_ai_sc_123mclip_lgbm2_oos_v1` | `28651` | 32 | 14 | 3 | Native promotions rejected; best clipped branch reached only `1.52` Sharpe. |
| `codex_ai_sc_3msmooth_lgbm2_oos_v1` | `27424` | 32 | 14 | 1 | Rejected before native simulation; smooth-path target destroyed top-bucket economics. |
| `codex_ai_sc_lgbm_tscv_smooth_v1` | `28636` | 32 | 3 | 3 | Rejected; long TSCV branch translated poorly into native strategy results. |
| `codex_ai_sc_6mtot_lgbm2_oos_v1` | `28652` | 32 | 0 | 0 | Parked; period/load route repeatedly failed before any RU spend. |

Original `27417` compare-table recheck at Quantiles 100 / Slippage 0%:

| Model | Rank | Spearman | H-L SR | High Avg% | High SR | High Turn% | Campaign status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm slow 3` | 100 | 0.1980 | 2.02 | 48.74 | 2.14 | 1,867 | Native tested; Sharpe `1.24`. |
| `lightgbm II - SCGotlesp` | 92 | 0.1979 | 2.02 | 48.46 | 2.13 | 1,792 | Native tested; Sharpe `1.34`. |
| `lightgbm medium 2` | 92 | 0.1938 | 1.88 | 52.30 | 2.17 | 1,918 | Native tested; Sharpe `1.36`. |
| `lightgbm III` | 71 | 0.1953 | 1.75 | 48.89 | 2.19 | 1,794 | Native tested; Sharpe around `1.40`. |
| `lightgbm II - TOF ANH` | 64 | 0.1867 | 2.00 | 50.26 | 2.18 | 1,887 | Native tested; Sharpe `1.52`. |
| `lightgbm medium 3` | 57 | 0.1923 | 1.64 | 53.20 | 2.26 | 1,974 | Native tested; Sharpe `1.37`. |
| `lightgbm II` | 50 | 0.1876 | 1.74 | 56.88 | 2.40 | 1,971 | Current native leader; Sharpe `1.60`. |
| `lightgbm II - TOF` | 35 | 0.1856 | 1.52 | 55.64 | 2.35 | 1,964 | Native tested; Sharpe `1.58` in original TOF branch and `1.36` in 1+2+3M TOF branch. |
| `extra trees II` | 35 | 0.2097 | 1.11 | 31.63 | 1.58 | 940 | Rejected before native; smoother but too weak. |

Decision: do not spend on more native simulations from the original `27417` table. The remaining rows are either already tested or weaker versions of already-failed model profiles. The next cost-controlled experiment should change the target design rather than the wrapper. The leading hypothesis is a new small-cap target that keeps the leader's strong raw top-bucket edge but penalizes downside path and short-horizon crash exposure less aggressively than the failed `3msmooth` target.

## 2026-05-26 01:06 EDT - New 3M downside-penalty shell blocked before load

Purpose: create one genuinely different small-cap AI Factor target through the Portfolio123 web platform UI, reuse the successful 32-feature source stack, and stop before any Resource Unit spend unless the dataset load page showed a normal cost path.

Surface: Portfolio123 web platform UI only. No P123 API was used. No Resource Units were spent.

Created/updated platform objects:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_3mdownpen_lgbm2_oos_v1` / `28654` | New shell created through the AI Factor initializer. |
| Initial target | `codex_3m_downside_penalty_v1` | Saved successfully, but period evaluation later failed. |
| Corrected target | `codex_3m_downpen_eval_v1` | Replaced scalar `Max()` guards with `Eval(...)`; saved and selected, but period evaluation still failed. |
| Simple fallback target | `codex_3m_clip65_v1` | Single-lookahead fallback formula also saved and selected, but period evaluation still failed. |

Settings verified before the load attempt:

| Setting | Value |
| --- | --- |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Feature import source | `SCs Small and Micro Cap Focus + 10 Mil min Replic2` |
| Features imported | `32 of 32` |
| Feature/global scaling | `Rank` |
| Target normalization | `Date` |
| Frequency | `Every 4 Weeks` |
| Target lookahead shown by platform | `13 weeks` |

Target formulas attempted:

```text
Bound(Future%Chg_D(65),-40,120)-0.35*Max(0,-Future%Chg_D(22))-0.20*Max(0,-Future%Chg_D(44))
Bound(Future%Chg_D(65),-40,120)-0.35*Eval(Future%Chg_D(22)<0,-Future%Chg_D(22),0)-0.20*Eval(Future%Chg_D(44)<0,-Future%Chg_D(44),0)
Bound(Future%Chg_D(65),-40,120)
```

Period behavior:

| Preset / input | Visible period after selection | Platform result |
| --- | --- | --- |
| Manual source-like dates | `2006-01-01` to `2026-01-17` | `Unexpected error encountered. Please contact support.` |
| `20 years` preset | `2006-02-21` to `2026-02-21` | Same error; Load page still said dataset period not set. |
| `MAX` preset | `2006-01-01` to `2026-02-21` | Same error; Load page still said dataset period not set. |

Decision: stop this shell before dataset load. The failure happens before Portfolio123 shows a Resource Unit estimate, so spending is blocked by platform setup, not by a cost decision. The shell remains useful evidence but should not be promoted until the period route can persist. Next smart route is to avoid this initializer/period path and instead try a source `Save As`/clone workflow that preserves a known-good dataset period before changing only one controlled element.

## 2026-05-26 01:24 EDT - Source clone period route succeeded; clipped-target branch rejected before native promotion

Purpose: test whether the platform `Save As` path can preserve the known-good long source period, then change only the target to the simple clipped 3M return formula before spending Resource Units.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Created/updated platform objects:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor clone | `codex_ai_sc_sourceclone_period_v1` / `28656` | Created from source `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` through `Actions -> Save As`. |
| Target | `codex_3m_clip65_v1` | Selected on clone after creation; formula `Bound(Future%Chg_D(65),-40,120)`. |

Clone setup preserved:

| Setting | Value |
| --- | --- |
| Period | `2006-01-01` to `2026-01-17` (`20.1 years`) |
| Frequency | `Every Week` |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Features | `32` |
| Scaling | `Rank` |
| Validation | `Basic Holdout`, `20 weeks` gap, `65 months` holdout |

Cost and load result:

| Step | Visible cost/result |
| --- | --- |
| Initial load estimate | `14` Resource Units for `~359MB (~102.5M data points)` |
| Load option | Target Information Regression Sample set to `Disabled` |
| Actual loaded dataset | `315MB (79.5M data points)` |
| Actual dataset Resource Units shown | `12` |
| Load time | `1 min, 27 sec` |

Validated models:

| Model | Rank | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | RU | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm II` | `100` | `0.1898` | `49.90` | `1.23` | `28.01` | `1.38` | `1,102` | `-14.71` | `3` | Success, saved predictions requested. |
| `extra trees II` | `50` | `0.2089` | `39.70` | `0.93` | `21.70` | `1.14` | `557` | `-12.96` | `3` | Success, saved predictions requested. |

Return-page notes for `lightgbm II`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.41%` |
| Bucket 10 compounded | `25.98%` |
| Bucket 1 compounded | `-21.71%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `1,102%` |

Decision: do not promote this clipped-target branch to a native simulated strategy yet. Even the best model-table result, `lightgbm II`, has high-bucket SR `1.38`, below the goal hurdle and below the current native leader's Sharpe `1.60`. The clipped target made the signal cleaner enough to rank `100`, but it reduced the top-bucket economics versus the original source table (`lightgbm II` source high SR `2.40`, high Avg% `56.88`). This branch is evidence that the source-clone route fixes the period blocker, but the simple clipped 65-day target is not the right alpha-improvement direction.

## 2026-05-26 01:40 EDT - Source clone downside-penalty target branch rejected before native promotion

Purpose: reuse the successful source-clone period route to test the previously blocked downside-penalty target while preserving the known-good long source period.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Created/updated platform objects:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor clone | `codex_ai_sc_downpen_v1` / `28657` | Created from source `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` through the platform copy route. |
| Target | `codex_3m_downpen_eval_v1` | Formula `Bound(Future%Chg_D(65),-40,120)-0.35*Eval(Future%Chg_D(22)<0,-Future%Chg_D(22),0)-0.20*Eval(Future%Chg_D(44)<0,-Future%Chg_D(44),0)`. |

Setup verified before load:

| Setting | Value |
| --- | --- |
| Period | `2006-01-01` to `2026-01-17` (`20.1 years`) |
| Frequency | `Every Week` |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Features | `32` |
| Scaling | `Rank` |
| Validation | `Basic Holdout`, `20 weeks` gap, `65 months` holdout |

Cost and load result:

| Step | Visible cost/result |
| --- | --- |
| Initial load estimate | `14` Resource Units for `~359MB (~102.5M data points)` |
| Load option | Target Information Regression Sample set to `Disabled` |
| Actual loaded dataset | `315MB (79.5M data points)` |
| Actual dataset Resource Units shown | `12` |
| Load time | `1 min, 26 sec` |

Validated model:

| Model | Rank | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | RU | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm II` | `100` | `0.2026` | `44.96` | `1.11` | `25.18` | `1.27` | `1,093` | `-13.74` | `3` | Success, saved predictions requested. |

Return-page notes for `lightgbm II`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.52%` |
| Bucket 10 compounded | `23.24%` |
| Bucket 1 compounded | `-20.91%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `1,093%` |
| First-half bucket 10 compounded | `22.28%` |
| Second-half bucket 10 compounded | `24.22%` |
| Spearman rank correlation by quantile | `0.96` entire period, `0.98` first half, `0.53` second half |
| Slope per quantile | `3.459%` entire period, `4.220%` first half, `2.511%` second half |

Decision: reject this downside-penalty branch before native simulated-strategy promotion. It produced a Rank `100` model, but the economics are weaker than the clipped-target branch (`High SR 1.27` vs `1.38`, `Bucket 10 compounded 23.24%` vs `25.98%`) and far below the original source model-table top-bucket strength. The penalty improved rank correlation versus the simple clipped branch but did not improve the long-only top-bucket return stream. Do not spend more RU on nearby `extra trees II` or custom `lightgbm II` variants for this exact target unless a later hypothesis specifically explains why the native strategy translation would improve.

## 2026-05-26 01:55 EDT - 6M source-clone branch created but blocked before RU spend

Purpose: test whether a longer 6-month return target can reduce churn / improve smoothness versus the 3-month target family, using the same source-clone route that preserves the known-good 32-feature small-cap setup.

Surface: Portfolio123 web platform UI only. No P123 API was used. No Resource Units were spent on this branch.

Created/updated platform object:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor clone | `codex_ai_sc_6m_clone_v1` / `28658` | Created from source `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417`. |
| Target | `6MTotRet` | Built-in target selected after initially selecting `6M Vol` by mistake; corrected before any load attempt. Formula shown by P123: `Future%Chg_D(130)`. |

Setup verified:

| Setting | Value |
| --- | --- |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Features | `32` |
| Scaling | `Rank` |
| Frequency | `Every Week` |
| Target lookahead shown on Period page | `26 weeks` |
| Minimum Price Bars | Restored to `100` after target-selection drift |

Load blocker:

| Observation | Detail |
| --- | --- |
| Initial load page period | `2006-01-01 to 2026-01-17` |
| Load estimate before blocker | `14` Resource Units for `~359MB (~102.5M data points)` |
| Platform error on load start | `Period cannot end after 2025-11-22 due to target lookahead` |
| Period page display after error | Inputs showed `2006-01-01` to `2025-11-22`, `26 weeks` lookahead, `(19.9 years)` |
| Persistence issue | After navigating back to Load Status, P123 still displayed `2006-01-01 to 2026-01-17` and repeated the same target-lookahead error. |

Decision: park this 6M branch before Resource Unit spend. This is not a model failure; it is a UI/settings persistence issue around shortening the source-cloned dataset end date for a longer lookahead target. The next attempt should either find the exact period-control persistence action in the platform UI or create the clone with a period that already satisfies the 6M lookahead boundary before selecting/loading the target.

## 2026-05-26 02:05 EDT - 6M source-clone branch unblocked, validated, rejected before native promotion

Surface: Portfolio123 web platform UI only. No P123 API was used.

Resolution of blocker: P123 accepted the shortened 6M target period only when the corrected Period page end date was blurred and navigation continued through the platform's own SPA side menu. Direct URL navigation to Load Status reverted to the stale `2026-01-17` end date. The accepted dataset period was `2006-01-01` to `2025-11-22`.

Cost and load result:

| Step | Visible cost/result |
| --- | --- |
| Corrected load estimate | `14` Resource Units for `~359MB (~102.5M data points)` |
| Actual loaded dataset | `309MB (78M data points)` |
| Actual dataset Resource Units shown | `12` |
| Load start | `2026-05-26 00:53 EDT` |
| Load time | `1 min, 24 sec` |

Validation method:

| Setting | Value |
| --- | --- |
| Method | `Basic Holdout` |
| Dataset period | `19.9 years`, `2006-01-01` to `2025-11-22` |
| Gap | `20 weeks` |
| Holdout | `65.0 months` |
| Training period shown | `14.1 years` |

Validated model:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | RU | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm II` | `100` | `0.5607` | `0.2264` | `33.79` | `0.85` | `23.14` | `1.17` | `998` | `-8.01` | `-0.20` | `3` | Success, saved validation predictions requested. |

Worker/cost details: Premium worker, `34 sec`, `1.1 GB`, `3` validation Resource Units.

Return-page notes for `lightgbm II`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-06-23` to `2025-11-22` |
| Return statistics period | `6/27/2020` to `11/29/2025` |
| Benchmark annualized return shown | `17.57%` |
| Universe annualized return shown | `4.80%` |
| Bucket 10 compounded | `21.20%` |
| Bucket 10 average | `23.14%` |
| Bucket 10 estimate | `19.08%` |
| Bucket 10 average stocks | `195` |
| Bucket 10 annualized turnover | `998%` |
| First-half bucket 10 compounded | `20.50%` |
| Second-half bucket 10 compounded | `21.91%` |
| Bucket 1 compounded | `-15.85%` |
| Bucket 1 average | `-8.01%` |
| Spearman rank correlation by quantile | `0.99` entire period, `0.99` first half, `0.60` second half |
| Slope per quantile | `3.223%` entire period, `3.975%` first half, `2.350%` second half |

Decision: reject this 6M target branch before native simulated-strategy promotion. It is directionally valid and ranked cleanly, but the long-only top bucket is not strong enough for the campaign hurdle: `High SR 1.17`, `Bucket 10 compounded 21.20%`, and benchmark shown at `17.57%`. That is weaker than the current native leader (`35.94%` annualized return, `1.60` Sharpe) and weaker than the better 3M/clipped-target validation branches. Do not spend native simulation runs on this exact `6MTotRet` `lightgbm II` clone unless a later hypothesis changes the portfolio construction enough to justify retesting.

## 2026-05-26 02:18 EDT - Raw-plus-relative 3M alpha blend branch rejected before native promotion

Purpose: test a target that keeps part of the original source model's raw 3-month return edge while adding benchmark-relative reward, aiming for a smoother active-alpha signal without fully duplicating the already-rejected built-in `3MRel` branch.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Created/updated platform objects:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor clone | `codex_ai_sc_3malpha_v1` / `28659` | Created from source `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` through `Actions -> Save As`. |
| Target | `codex_3m_raw_rel_blend_v1` | New target created in platform target dialog. |

Target formula:

```text
0.5*Bound(Future%Chg_D(65),-40,120)+0.5*Bound(FutureRel%Chg_D(65,#Bench),-40,120)
```

Setup and cost:

| Step | Visible cost/result |
| --- | --- |
| Load estimate | `14` Resource Units for `~359MB (~102.5M data points)` |
| Load option | Target Information Regression Sample set to `Disabled` |
| Actual loaded dataset | `315MB (79.5M data points)` |
| Actual dataset Resource Units shown | `12` |
| Load start | `2026-05-26 01:10 EDT` |
| Load time | `1 min, 33 sec` |

Validated model:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | RU | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm II` | `100` | `0.5660` | `0.1896` | `50.63` | `1.24` | `27.44` | `1.35` | `1,101` | `-15.51` | `-0.41` | `3` | Success, saved validation predictions requested. |

Worker/cost details: Premium worker, `37 sec`, `1.1 GB`, `3` validation Resource Units.

Return-page notes for `lightgbm II`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.42%` |
| Bucket 10 compounded | `25.39%` |
| Bucket 10 average | `27.44%` |
| Bucket 10 estimate | `20.63%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `1,101%` |
| First-half bucket 10 compounded | `26.43%` |
| Second-half bucket 10 compounded | `24.35%` |
| Bucket 1 compounded | `-22.41%` |
| Bucket 1 average | `-15.51%` |
| Spearman rank correlation by quantile | `0.99` entire period, `0.99` first half, `0.48` second half |
| Slope per quantile | `3.598%` entire period, `4.301%` first half, `2.704%` second half |

Decision: reject before native simulated-strategy promotion. The branch is better than the 6M target and preserves more upside than the full relative-return idea, but it is still not strong enough to justify another native run: `High SR 1.35` and `Bucket 10 compounded 25.39%` are below the campaign's current native leader and still far below the source model-table `lightgbm II` profile (`High SR 2.40`, `High Avg% 56.88`). The raw-plus-relative blend improved active-return framing but did not solve the Sharpe constraint.

## 2026-05-26 02:33 EDT - Beta-penalized target branch rejected before native promotion

Purpose: test whether embedding a soft market-risk penalty directly in the AI Factor target can reduce the noisy high-beta small-cap tail earlier than native buy/sell filters. This followed repeated evidence that after-the-fact beta, trend, stop-loss, and allocation filters reduced return faster than volatility.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Created/updated platform objects:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor clone | `codex_ai_sc_riskadj_v1` / `28660` | Created from source `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` through `Actions -> Save As`. |
| Target | `codex_3m_ret_betapen_v1` | New target created and then edited in the platform target dialog. |

Parser/setup lessons:

| Attempt | Outcome |
| --- | --- |
| `Bound(Future%Chg_D(65),-40,120)-0.20*Volatility(65)` | Target editor rejected: `Invalid command 'Volatility'`. |
| `Bound(Future%Chg_D(65),-40,120)-10*StdDev(65)` | Target editor rejected: `StdDev - Missing operands`. |
| `Bound(Future%Chg_D(65),-40,120)-5*Beta` | Target saved, but dataset load failed because target N/A exceeded 20% on 91 dates. |
| `Bound(Future%Chg_D(65),-40,120)-5*Eval(IsNA(Beta),1,Beta)` | Target editor rejected: `- - Missing operands`. |
| `Bound(Future%Chg_D(65),-40,120)-5*Eval(Beta=NA,1,Beta)` | Target saved and dataset load succeeded. |

Final target formula:

```text
Bound(Future%Chg_D(65),-40,120)-5*Eval(Beta=NA,1,Beta)
```

Cost and load result:

| Step | Visible cost/result |
| --- | --- |
| First load estimate/result | `~255MB (~72.8M data points)`, `10` Resource Units shown, failed after `1 min, 19 sec` due target N/A coverage. |
| Successful retry estimate | `14` Resource Units for `~359MB (~102.5M data points)` |
| Actual successful dataset | `315MB (79.5M data points)` |
| Actual successful dataset Resource Units shown | `12` |
| Successful load start | `2026-05-26 01:27 EDT` |
| Successful load time | `1 min, 26 sec` |

Validated model:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | RU | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lightgbm II` | `100` | `0.5649` | `0.1985` | `48.00` | `1.12` | `26.39` | `1.46` | `822` | `-14.70` | `-0.37` | `3` | Success, saved validation predictions requested. |

Worker/cost details: Premium worker, `36 sec`, `1.2 GB`, `3` validation Resource Units.

Return-page notes for `lightgbm II`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.81%` |
| Bucket 10 compounded | `24.78%` |
| Bucket 10 average | `26.39%` |
| Bucket 10 estimate | `20.27%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `822%` |
| First-half bucket 10 compounded | `24.03%` |
| Second-half bucket 10 compounded | `25.55%` |
| Bucket 1 compounded | `-22.18%` |
| Bucket 1 average | `-14.70%` |
| Spearman rank correlation by quantile | `0.87` entire period, `0.99` first half, `0.48` second half |
| Slope per quantile | `3.446%` entire period, `4.053%` first half, `2.701%` second half |

Decision: reject before native simulated-strategy promotion. The target lowered high-bucket turnover materially versus the recent raw/relative branch (`822%` vs `1,101%`) and improved High SR slightly (`1.46` vs `1.35`), but it gave up too much top-bucket return and remains far below the original source `lightgbm II` row (`High SR 2.40`, `High Avg% 56.88`). Since several stronger model-table profiles already failed to clear native Sharpe `>1.9`, this beta-penalized target does not justify another native simulation run.

## 2026-05-26 02:38 EDT - AI-heavy Wes/AI book allocation rejected

Purpose: test whether the closest zero-RU stock-only book path could clear the Sharpe target by leaning more heavily into the native AI Factor strategy while keeping the low-correlation Wes Gray sleeve.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Constraint check on Wes component:

| Item | Platform observation |
| --- | --- |
| Component | `Wes Gray Momentum Microcaps Hedged` / `1848302` |
| Type | Live Strategy |
| Universe | `100K, $1 and NOOTC mktcap<300 ex-china` |
| Ranking system | `Wes Gray Quant Momentum + si fcf` |
| Benchmark | `Russell Micro (IWC:USA)` |
| Current summary period | `01/01/00 - 05/25/26` |
| Summary Sharpe | `1.63` |
| Summary max drawdown | `-17.16%` |
| Summary correlation with Russell Micro | `0.29` |
| Cash on summary | `29.6M` of `39.2M` total market value |
| Holdings/trades | Stock holdings and BUY/SELL stock trades visible; no explicit short/ETF hedge seen on summary. |

Interpretation: eligible only as a stock/cash risk-reduction sleeve, not as a pure AI Factor strategy. The large cash position likely explains much of its stabilizing effect. This is useful for risk control, but it also makes the branch less clean as an "underlying AI strategy" solution.

New native platform object:

| Object | Name / ID | Setup |
| --- | --- | --- |
| Simulated Book | `codex_book_wes_ai_60ai_oos_v1` / `1944392` | Cloned from `codex_book_wes_ai_equal_oos_v1` / `1944244` using platform `Save As new Simulated Book`. |

Allocation:

| Asset | ID | Relative weight | Ending weight |
| --- | ---: | ---: | ---: |
| `Wes Gray Momentum Microcaps Hedged` | `1848302` | `1.0` | `39.20%` |
| `codex_strategy_sc_lgbm2_oos_v1_top1` | `1944200` | `1.5` | `60.80%` |

Native result:

| Metric | Value |
| --- | ---: |
| Period | `08/21/20 - 01/16/26` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Total return | `259.27%` |
| Benchmark return | `120.07%` |
| Active return | `139.20%` |
| Annualized return | `26.68%` |
| Max drawdown | `-11.37%` |
| Benchmark max drawdown | `-24.50%` |
| Sharpe ratio | `1.72` |
| Correlation with SPY | `0.60` |

Decision: reject. The 60% AI / 40% Wes book improves annualized return versus the equal-weight book (`26.68%` vs `24.36%`) but lowers Sharpe (`1.72` vs `1.74`) and remains well below the hard `>1.9` OOS Sharpe gate. This confirms the current Wes/AI two-sleeve allocation is not the binding path to the goal; the equal-weight version remains the better risk-adjusted book in this local neighborhood, while `codex_strategy_sc_lgbm2_oos_v1_top1` remains the best pure AI Factor native strategy baseline.

## 2026-05-26 02:57 EDT - ATRN-penalized 3M target branch rejected

Purpose: test whether directly penalizing volatility in the AI Factor target could create a smoother long-only signal without spending on native simulations before model-table evidence justified promotion.

Surface: Portfolio123 web platform UI only. No P123 API was used.

New native platform object:

| Object | Name / ID | Setup |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_atrnpen_v1` / `28661` | Platform `Save As` clone of `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417`. |
| Target | `codex_3m_atrnpen_v1` | `bound(future%chg_d(65),-40,120)-0.8*atrn(63)` |

Inherited setup: universe `No OTC Exchange + min 10 mil min vol - OWN`, benchmark `S&P 500 (SPY:USA)`, period `2006-01-01` to `2026-01-17`, weekly frequency, 32 features, Rank normalization, Basic Holdout validation with 20-week gap, 14.3-year training period, and 65-month holdout period.

Dataset load:

| Item | Value |
| --- | ---: |
| Initial platform estimate | `~359MB`, `~102.5M data points`, `14` Resource Units |
| Actual completed load | `315MB`, `79.5M data points`, `12` Resource Units |
| Load start | `5/26/2026, 1:46 AM` platform time |
| Load time | `1 min, 28 sec` |

Validated models:

| Model | Rank | Validation | Worker | Resource Units | Notes |
| --- | ---: | --- | --- | ---: | --- |
| `lightgbm II` | `100` | `SUCCESS`, `34 sec`, `1.1 GB` | Premium | `3` | Saved validation predictions. |
| `extra trees II` | `50` | `SUCCESS`, `3 min, 11 sec`, `1.0 GB` | Premium | `3` | Saved validation predictions. |

Result-page metrics:

| Model | Period | Bucket 10 compounded | Bucket 10 average | Bucket 10 turnover | Bucket 1 compounded | Spearman | Slope |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `lightgbm II` | `8/22/2020` to `1/24/2026` | `20.76%` | `22.66%` | `1,033%` | `-20.57%` | `0.98` | `3.453%` |
| `extra trees II` | `8/22/2020` to `1/24/2026` | `17.15%` | `18.88%` | `520%` | `-16.74%` | `0.99` | `3.279%` |

Decision: reject before native simulated-strategy promotion. The target produced a clean monotonic quantile relationship, but top-bucket returns were far below the current native pure-AI leader (`codex_strategy_sc_lgbm2_oos_v1_top1`, `35.94%` annualized, Sharpe `1.60`) and far below the source model-table strength that previously justified native promotion. Extra Trees cut turnover roughly in half versus LightGBM, but it also lowered rank to `50` and reduced top-bucket return. Total branch spend was `18` Resource Units (`12` dataset + `6` validation). No native simulation spend was justified.

## 2026-05-26 03:10 EDT - Crash-penalty target branch started; dataset queued

Purpose: test a narrower target-design change after simple wrappers and broad volatility/beta penalties failed. This target keeps the original raw 3-month return edge but lightly penalizes stocks that suffer a sharp 1-month forward drop inside the horizon.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Existing saved-prediction inventory check before spend:

| Existing branch | Observation | Decision |
| --- | --- | --- |
| `SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials` / `20725` | Three saved `deeptables` rows had weak top-bucket returns over `4/27/2024 - 5/24/2025`; best top bucket was only `7.15%` compounded and second-half results were negative. | Reject before native promotion. |
| `agent_highsr_lgbm_sp500_v1` / `27238` | Existing saved rows covered `7/30/2016 - 8/16/2025`, but top-bucket compounded returns were only about `12.75% - 13.94%`, not enough to plausibly beat the current small-cap native leader or active-return hurdle. | Reject before native promotion. |

New native platform object:

| Object | Name / ID | Setup |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_crashpen_v1` / `28662` | Platform `Save As` clone of `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417`. |
| Target | `codex_3m_crashpen_v1` | `Bound(Future%Chg_D(65),-40,120)-10*Eval(Future%Chg_D(21)<-10,1,0)` |

Inherited setup: universe `No OTC Exchange + min 10 mil min vol - OWN`, benchmark `S&P 500 (SPY:USA)`, period `2006-01-01` to `2026-01-17`, weekly frequency, 32 features, Rank normalization, Basic Holdout validation with 20-week gap, 14.3-year training period, and 65-month holdout period.

Dataset load:

| Item | Value |
| --- | ---: |
| Initial platform estimate | `~359MB`, `~102.5M data points`, `14` Resource Units |
| Target Information Regression Sample | `Disabled` |
| Current platform status at `03:10 EDT` | `WAITING` |

Next step: when the dataset completes, record actual Resource Units, then validate exactly one high-decision-value model first (`lightgbm II`) with saved validation predictions. Promote to native simulation only if the result materially improves on the current leader's model-table-to-native hurdle.

### 2026-05-26 03:15 EDT update - branch rejected before native promotion

Dataset load completed:

| Item | Value |
| --- | ---: |
| Actual completed load | `315MB`, `79.5M data points` |
| Actual dataset Resource Units shown | `12` |
| Load start | `5/26/2026, 2:04 AM` platform time |
| Load time | `1 min, 29 sec` |

Validated model:

| Model | Rank | Validation | Worker | Resource Units | Notes |
| --- | ---: | --- | --- | ---: | --- |
| `lightgbm II` | `100` | `SUCCESS`, `34 sec`, `1.1 GB` | Premium | `3` | Saved validation predictions. |

Lift stats:

| Metric | Value |
| --- | ---: |
| RMSE | `0.5645` |
| Spearman | `0.2055` |
| R2 | `0.0444` |
| Pearson | `0.2165` |

Return-page metrics:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Bucket 10 compounded | `24.41%` |
| Bucket 10 average | `26.39%` |
| Bucket 10 estimate | `21.00%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `1,051%` |
| First-half bucket 10 compounded | `23.55%` |
| Second-half bucket 10 compounded | `25.29%` |
| Bucket 1 compounded | `-21.78%` |
| Bucket 1 average | `-14.62%` |
| Spearman rank correlation by quantile | `0.93` entire period, `0.99` first half, `0.53` second half |
| Slope per quantile | `3.653%` entire period, `4.374%` first half, `2.770%` second half |

Decision: reject before native simulated-strategy promotion. The model ranked `100` and has a clean monotonic quantile spread, but it does not improve the investable top-bucket economics. Bucket 10 compounded return of `24.41%` and turnover of `1,051%` are weaker than the current native leader's source branch and weaker than several already-rejected target designs. Since stronger model-table profiles have only translated to native Sharpe around `1.60`, this crash-penalty branch does not justify another native simulation. Total branch spend was `15` Resource Units (`12` dataset + `3` validation).

## 2026-05-26 03:25 EDT - Existing saved-prediction inventory exhausted; next branch must change setup layer

Purpose: re-check the Portfolio123 AI Factor opener before spending more Resource Units, because recent target-level tweaks all weakened the source model's investable top-bucket economics.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Inventory observation from the AI Factor opener:

| Branch family | Platform state | Campaign decision |
| --- | --- | --- |
| Original small-cap source `27417` | `14` results / `2` predictors; strongest native pure-AI strategy remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`. | Keep as current benchmark; do not re-promote remaining original rows. |
| 2026 source-clone target branches `28656`-`28662` | Loaded/validated branches include clipped 3M, downside penalty, 6M, raw+relative blend, beta penalty, ATRN penalty, and crash penalty. | All rejected before native promotion except earlier promoted variants; none beat the source model-table hurdle. |
| `28648` / `28651` 1+2+3M and clipped 1+2+3M branches | Multiple native promotions already rejected, including TOF and consensus/blend variants. | Exhausted for this campaign unless a new construction idea is materially different. |
| Older AI Factors page 2 (`20015`, `20101`, `26878`, `26875`, `26889`, `20725`, `20721`, `27238`) | Previously inspected or natively tested. | No untested saved-prediction row looks strong enough to promote. |

Binding evidence: the current native leader came from a source model-table row with very strong top-bucket diagnostics (`High Avg% 56.88`, `High SR 2.40`) but still translated to only `1.60` native Sharpe. Recent target designs with cleaner rank or lower turnover produced top-bucket compounded returns around `20.76% - 25.98%` and High SR around `1.17 - 1.46`, so native promotion would be a low-probability Resource Unit spend.

Next smart iteration:

| Item | Decision |
| --- | --- |
| Experiment type | Setup-layer change, not another target penalty. |
| Candidate | Clone the small-cap source again, preserve the raw 3M total-return target, and test a Recipe-B-style preprocessing variant. |
| Intended object name | `codex_ai_sc_zscore3m_v1` |
| Setup to test | Same universe/features/period as `27417`, but change preprocessing from Rank toward Z-score with tighter tail handling if the platform allows it. |
| Cost guard | Spend only the dataset load plus one `lightgbm II` validation first. Stop unless model-table diagnostics are plausibly above the current source-to-native hurdle. |
| Promotion gate | Native simulation only if High SR/top-bucket return is at least source-like, or if turnover/risk improves dramatically without sacrificing top-bucket return. |

Decision: the campaign should stop mining already-saved rows and move to one controlled preprocessing experiment. This is materially different from the failed target tweaks and keeps the next spend bounded.

## 2026-05-26 03:35 EDT - Z-score preprocessing branch rejected before native promotion

Purpose: test a setup-layer change after target-level tweaks failed. This branch preserved the source small-cap universe, 32 features, raw 3M total-return target, long dataset period, and Basic Holdout geometry, but changed feature scaling from `Rank` to `Z-Score`.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Platform object:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_zscore3m_v1` / `28663` | Clean `Save As` clone of `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417`; copied features only, not studies or predictors. |

Setup:

| Setting | Value |
| --- | --- |
| Target | `3MTotReturn` |
| Target formula | `Future%Chg_D(65)` |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Period | `2006-01-01` to `2026-01-17` |
| Frequency | `Every Week` |
| Features | `32` |
| Scaling | `Z-Score` |
| N/A handling | `Zero fill` |
| Validation | Basic Holdout, `20 weeks` gap, `14.3 years` training period, `65 months` holdout period |

Dataset load:

| Item | Value |
| --- | ---: |
| Initial platform estimate | `~359MB`, `~102.5M data points`, `14` Resource Units |
| Target Information Regression Sample | `Disabled` |
| Actual completed load | `315MB`, `79.5M data points` |
| Actual dataset Resource Units shown | `12` |
| Load start | `5/26/2026, 2:24 AM` platform time |
| Load time | `1 min, 20 sec` |

Validated model:

| Model | Rank | Validation | Worker | Resource Units | Notes |
| --- | ---: | --- | --- | ---: | --- |
| `lightgbm II` | `100` | `SUCCESS`, `34 sec`, `1.2 GB` | Premium | `3` | Saved validation predictions. |

Compare-table metrics at displayed settings `Quantiles 10`, `Slippage 0.1%`:

| RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1.2928` | `0.1774` | `52.71` | `1.39` | `30.08` | `1.37` | `1,118` | `-14.93` | `-0.39` | `801` |

Return-page metrics:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.32%` |
| Bucket 10 compounded | `27.69%` |
| Bucket 10 average | `30.08%` |
| Bucket 10 estimate | `22.14%` |
| Bucket 10 average stocks | `196` |
| Bucket 10 annualized turnover | `1,118%` |
| First-half bucket 10 compounded | `27.12%` |
| Second-half bucket 10 compounded | `28.27%` |
| Bucket 1 compounded | `-21.84%` |
| Bucket 1 average | `-14.93%` |
| Spearman rank correlation by quantile | `1.00` entire period, `0.98` first half, `0.50` second half |
| Slope per quantile | `3.922%` entire period, `4.609%` first half, `3.017%` second half |

Decision: reject before native simulated-strategy promotion. Z-score scaling improved top-bucket compounded return versus the recent target-penalty branches, but it remains far below the source row that produced the current native pure-AI leader. The High SR is only `1.37`, turnover is still high at `1,118%`, and the current native leader already needed much stronger source diagnostics to reach only `1.60` Sharpe. Total branch spend was `15` Resource Units (`12` dataset + `3` validation). The next iteration should not be another one-model preprocessing tweak unless it changes the feature set or validation geometry enough to explain a step-change in native Sharpe.

## 2026-05-26 03:55 EDT - 87-feature small-cap branch rejected before native promotion

Purpose: test whether the binding constraint was feature breadth rather than target definition or scaling. This branch preserved the source small-cap universe, raw 3M total-return target, long dataset period, weekly frequency, and Basic Holdout geometry, then imported the 87-feature `AI Factor Base 87 Features Andreas 2 - Copy` feature set.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Platform object:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_featureplus_v1` / `28664` | Clean `Save As` clone of `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417`; copied features only, not studies or predictors. |

Setup:

| Setting | Value |
| --- | --- |
| Target | `3MTotReturn` |
| Target formula | `Future%Chg_D(65)` |
| Training universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Period | `2006-01-01` to `2026-01-17` |
| Frequency | `Every Week` |
| Features | `87` |
| Scaling | `Rank` |
| Validation | Basic Holdout inherited from source setup |

Dataset load:

| Item | Value |
| --- | ---: |
| Initial platform estimate | `~893MB`, `~254.9M data points`, `35` Resource Units |
| Target Information Regression Sample | `Disabled` |
| Actual completed load | `986MB`, `254.7M data points` |
| Actual dataset Resource Units shown | `39` |
| Load start | `5/26/2026, 2:34 AM` platform time |
| Load time | `3 min, 24 sec` |

Validated model:

| Model | Rank | Validation | Worker | Resource Units | Notes |
| --- | ---: | --- | --- | ---: | --- |
| `lightgbm II` | `100` | `SUCCESS`, `1 min, 15 sec`, `3.5 GB` | Premium | `3` | Saved validation predictions. |

Compare-table metrics at displayed settings `Quantiles 10`, `Slippage 0.1%`:

| RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.5610` | `0.2305` | `65.81` | `1.42` | `28.01` | `1.46` | `1,306` | `-22.99` | `-0.61` | `879` |

Return-page metrics:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.46%` |
| Bucket 10 compounded | `26.19%` |
| Bucket 10 average | `28.01%` |
| Bucket 10 estimate | `25.91%` |
| Bucket 10 average stocks | `251` |
| Bucket 10 annualized turnover | `1,306%` |
| First-half bucket 10 compounded | `23.13%` |
| Second-half bucket 10 compounded | `29.36%` |
| Bucket 1 compounded | `-29.66%` |
| Bucket 1 average | `-22.99%` |
| Spearman rank correlation by quantile | `1.00` entire period, `0.99` first half, `0.90` second half |
| Pearson correlation by quantile | `0.93` entire period, `0.99` first half, `0.80` second half |
| Slope per quantile | `4.685%` entire period, `4.518%` first half, `4.762%` second half |

Decision: reject before native simulated-strategy promotion. The 87-feature import improved RMSE, Spearman, H-L spread, and cross-quantile monotonicity versus the Z-score branch, but it did not improve the metric that matters most for a long-only top-bucket strategy: top-bucket strength. High Avg was only `28.01%` and High SR only `1.46`, far below the source model-table row that produced the current native leader (`56.88%` High Avg, `2.40` High SR). Since that much stronger source row translated to only `1.60` native Sharpe, this branch is unlikely to clear the `>1.9` Sharpe goal after native costs. Total branch spend was `42` Resource Units (`39` dataset + `3` validation).

### 2026-05-26 04:10 EDT update - 87-feature ExtraTrees stability check started

Purpose: spend one small model-only validation on the already-loaded 87-feature branch to test whether ExtraTrees improves stability/turnover enough to change the promotion decision. This did not require another dataset load.

Platform action:

| Item | Value |
| --- | --- |
| AI Factor | `codex_ai_sc_featureplus_v1` / `28664` |
| Added model | `extra trees medium 4` |
| Validation worker | Premium |
| Saved validation predictions | Yes |
| Status at last check | `IN PROGRESS`, Premium elapsed `14 min, 25 sec` |
| Resource Units shown at last check | `0` while still running |
| Started | `5/26/2026, 3:55 AM` platform time |

Decision pending. Re-open `https://www.portfolio123.com/sv/aiFactor/28664/validation/models`, wait for the model to resolve to `SUCCESS` or `FAIL`, then inspect `results/compare` and `results/return`. Promote to native simulation only if ExtraTrees materially improves top-bucket Sharpe/turnover versus the weak `lightgbm II` 87-feature row and plausibly beats the current native leader's `1.60` Sharpe.

### 2026-05-26 04:25 EDT update - 87-feature ExtraTrees rejected before native promotion

Final validation state:

| Model | Rank | Validation | Worker | Resource Units | Notes |
| --- | ---: | --- | --- | ---: | --- |
| `extra trees medium 4` | `50` | `SUCCESS`, `16 min, 11 sec`, `2.8 GB` | Premium | `3` | Saved validation predictions. |

Compare-table metrics at displayed settings `Quantiles 10`, `Slippage 0.1%`:

| Model | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `lightgbm II` | `0.5610` | `0.2305` | `65.81` | `1.42` | `28.01` | `1.46` | `1,306` | `-22.99` | `-0.61` | `879` |
| `extra trees medium 4` | `0.5613` | `0.2445` | `58.44` | `1.22` | `24.64` | `1.43` | `696` | `-21.50` | `-0.55` | `611` |

Return-page metrics for `extra trees medium 4`:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `6.76%` |
| Bucket 10 compounded | `23.18%` |
| Bucket 10 average | `24.64%` |
| Bucket 10 estimate | `26.65%` |
| Bucket 10 average stocks | `251` |
| Bucket 10 annualized turnover | `696%` |
| First-half bucket 10 compounded | `18.24%` |
| Second-half bucket 10 compounded | `28.37%` |
| Bucket 1 compounded | `-28.65%` |
| Bucket 1 average | `-21.50%` |
| Spearman rank correlation by quantile | `0.99` entire period, `1.00` first half, `0.54` second half |
| Pearson correlation by quantile | `0.89` entire period, `0.97` first half, `0.70` second half |
| Slope per quantile | `4.389%` entire period, `4.437%` first half, `4.206%` second half |

Decision: reject before native simulated-strategy promotion. ExtraTrees did improve turnover materially versus the 87-feature LightGBM row (`696%` vs `1,306%`) and slightly improved Spearman, but it weakened H-L Sharpe, High Avg, and High SR. The long-only top bucket is too weak for the campaign hurdle: `24.64%` High Avg and `1.43` High SR are far below the source `lightgbm II` row that produced the current native leader (`56.88%` High Avg, `2.40` High SR), and even that source row only translated to native Sharpe `1.60`. Total 87-feature branch spend is now `45` Resource Units (`39` dataset + `3` LightGBM validation + `3` ExtraTrees validation). No native simulation spend is justified.

## 2026-05-26 04:31 EDT - 1+2+3M target plus Z-Score Time Series CV branch

Purpose: test one cost-controlled setup-layer variation after the 87-feature branch failed. This branch kept the source small-cap universe and 32-feature source clone, reused the proven `1+2+3M` target, changed feature scaling to `Z-Score`, and changed validation from Basic Holdout to Time Series CV.

Setup:

| Field | Value |
| --- | --- |
| AI Factor | `codex_ai_sc_123m_ztscv_v1` / `28668` |
| Source | `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` |
| Target | `codex_1m2m3m_totret_v1` |
| Target formula | `Future%Chg_D(22)+Future%Chg_D(44)+Future%Chg_D(65)` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Features | `32` |
| Normalization | `Z-Score` |
| Validation | Time Series CV, 20-week gap, 8 folds, 12-month holdout |
| Dataset period | `2006-01-01 to 2026-01-17` |

Cost and run state:

| Step | Result |
| --- | --- |
| Dataset estimate | `~359MB`, `~102.5M` data points, `14` Resource Units |
| Dataset actual | `315MB`, `79.5M` data points, `12` Resource Units |
| Load start | `5/26/2026, 3:24 AM` |
| Load time | `1 min, 18 sec` |
| Validation model | `lightgbm II` |
| Save validation predictions | `Yes` |
| Validation result | `SUCCESS`, Rank `100`, Premium `35 sec`, `1.2 GB`, `3` Resource Units |
| Total branch spend | `15` Resource Units |

Compare-table diagnostics at displayed settings `Quantiles 10`, `Slippage 0.1%`:

| Metric | Result |
| --- | ---: |
| RMSE | `1.2981` |
| Spearman | `0.1631` |
| High-Low Avg | `57.97` |
| High-Low SR | `1.51` |
| High Avg | `34.18` |
| High SR | `1.52` |
| High Turnover | `1,166` |
| Low Avg | `-15.18` |
| Low SR | `-0.40` |
| Low Turnover | `837` |

Return-page diagnostics:

| Metric | Entire Period | First Half | Second Half |
| --- | ---: | ---: | ---: |
| Period | `8/22/2020 to 1/24/2026` | `8/22/2020 to 5/12/2023` | `5/13/2023 to 1/24/2026` |
| Benchmark annualized | `15.47%` |  |  |
| Universe annualized | `4.09%` |  |  |
| Bucket 10 compounded | `31.68%` | `32.95%` | `30.42%` |
| Bucket 10 average | `34.18%` | `35.57%` | `32.79%` |
| Bucket 10 estimate | `22.73%` | `20.56%` | `24.92%` |
| Bucket 10 avg stocks | `196` | `201` | `192` |
| Bucket 10 turnover | `1,166%` | `1,141%` | `1,191%` |
| Bucket 1 compounded | `-22.10%` | `-21.26%` | `-22.93%` |
| Spearman by quantile | `0.99` | `0.99` | `0.61` |
| Slope | `4.088%` | `4.899%` | `3.128%` |

Decision: reject before native simulated strategy. The branch is active versus SPY on the model table, but it does not improve on the current native leader's `35.94%` annualized return and `1.60` Sharpe. High SR is only `1.52`, turnover is still high at `1,166%`, and the top-decile compounded return is weaker than the current leader's native annualized return. This does not justify another native simulation spend.

Updated campaign state: current native leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` with `35.94%` annualized return, `1.60` Sharpe, `-15.65%` max drawdown, and `306.26%` total active return versus SPY over `08/22/2020 - 01/17/2026`. The hard goal remains open because no native-tested branch has reached Sharpe `>1.9`.

## 2026-05-26 05:08 EDT - Sector concentration construction test attempt

Purpose: test the cheapest remaining pure-AI construction knob before spending Resource Units on more AI Factor training. The hypothesis was that the current native leader's return signal is strong enough, but a sector concentration cap might reduce volatility/drawdown enough to lift Sharpe.

Planned clone:

| Field | Value |
| --- | --- |
| Source simulated strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` |
| Intended clone name | `codex_strategy_sc_lgbm2_sectorcap_oos_v1` |
| AI formula | `AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")` |
| Existing buy rank rule | `FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc) > 99` |
| Intended added buy rule | `SectorCount() <= 4` or equivalent `SectorCount() < 5` |
| Expected AI/RU cost | `0` Resource Units unless a native simulated-strategy run completes |

Follow-up: retried the same branch through the P123 Buy-tab `Text Editor`, which avoided the rule editor's auto-parentheses issue and successfully applied a fourth buy rule:

```text
[Buy4] SectorCount() <= 4
```

The new strategy was named `codex_sc_lgbm2_sectorcap` in the native properties modal and submitted through P123's own simulation runner:

```text
https://www.portfolio123.com/port_sim_go.jsp?1779785714578
```

P123 rejected the native run before producing performance:

```text
Error in Buy Rule 'Buy4': Error near 'SectorCount': Invalid command 'SectorCount'
```

Decision: reject the sector-count construction branch as a native simulated-strategy platform limitation. `SectorCount()` is documented for screen-style concentration control, but P123 does not accept it in this simulated strategy Buy Rule context. No performance claim should be made from this branch, and no Resource Units were spent on AI training. The broader Sharpe problem remains: the best pure AI native strategy is still `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` at `1.60` Sharpe, below the hard `>1.9` objective.

## 2026-05-26 05:42 EDT - Zero-RU inventory recheck after sector-cap rejection

Purpose: before spending more Resource Units, re-open the Portfolio123 platform inventory for hidden loaded AI Factors, native simulated strategies, or native simulated books that might already improve the campaign baseline.

Surface: Portfolio123 web platform UI only. No P123 API was used and no Resource Units were spent.

AI Factor opener observation:

| AI Factor | Platform state | Finding |
| --- | --- | --- |
| `codex_ai_sc_3msmooth_lgbm2_oos_v1` / `27424` | Dataset loaded, `14` validations, `1` result, `2` predictors | Zero-RU inspection found only one saved result worth reading. |
| `AI Factor Base 87 Features Andreas 2 - Copy` / `27425` | Dataset not loaded | Results page said `No validated models found`. |
| `AI Factor Enhanced 150+ Features ExtraTrees - Copy` / `27426` | Dataset not loaded | Results page said `No validated models found`. |

`27424` saved result:

| Metric | Value |
| --- | ---: |
| Model | `lightgbm II` |
| Rank | `100` |
| RMSE | `0.5519` |
| Spearman | `0.2976` |
| H-L Avg | `84.20` |
| H-L SR | `1.02` |
| High Avg | `20.71` |
| High SR | `1.20` |
| High Turnover | `1,639%` |
| Low Avg | `-34.79` |
| Low SR | `-0.66` |
| Low Turnover | `1,241%` |
| Return stats period | `8/22/2020 - 1/24/2026` |
| Bucket 100 compounded | `19.24%` |
| Bucket 1 compounded | `-46.39%` |
| Spearman by quantile | `0.83` entire period, `0.86` first half, `0.27` second half |

Decision on `27424`: reject before native simulation and before additional model starts. The high-low spread is large, but the investable long-only top bucket is weak: `20.71%` average, `1.20` High SR, and `1,639%` turnover. Starting more models on this loaded dataset would be a low-value 3-RU spend because the only saved result is far weaker than the original source row that produced the current native leader.

Native simulated strategy opener recheck:

| Visible best/near-best row | Annual | Excess | Sharpe | Drawdown | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `codex_strategy_sc_lgbm2_oos_v1_top1` | `35.9%` | `20.2%` | `1.60` | `-15.7%` | Current pure AI leader. |
| `codex_sc_lgbm2_buyback_v1` | `35.9%` | `20.2%` | `1.60` | `-15.7%` | Equivalent to leader; no improvement. |
| `codex_strategy_sc_lgbm2_oos_v4_liq50k` | `35.4%` | `19.7%` | `1.59` | `-15.7%` | Near miss; does not improve Sharpe. |
| `codex_strategy_sc_blend_lgbm2_123mclip_v1` | `35.9%` | `20.2%` | `1.59` | `-15.5%` | Near miss; still below leader Sharpe. |
| `codex_strategy_sc_123mclip_lgbm2_oos_v1` | `36.1%` | `20.4%` | `1.54` | `-17.9%` | Higher return but weaker risk-adjusted result. |

Native simulated book opener recheck:

| Book | Inception | Assets | Annual | Sharpe | Drawdown | Clean fit? |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `BookSim - Copy` | `01/03/06` | `4` | `22.9%` | `1.90` | `-25.5%` | No. Older non-clean reference book with non-stock ballast; not an AI Factor stock strategy. |
| `BookSim - Copy(3)` | `01/03/06` | `4` | `22.0%` | `1.86` | `-25.2%` | No. Same issue. |
| `BookSim(6)` | `01/03/06` | `5` | `23.6%` | `1.85` | `-27.1%` | No. Same issue. |
| `BookSim(8)codex_book_wes_ai_equal_oos_v1` | `08/21/20` | `2` | `24.4%` | `1.74` | `-10.6%` | Clean stock/cash AI book, but below target. |
| `codex_book_stock_ai_mix_oos_v1` | `08/21/20` | `3` | `23.6%` | `1.73` | `-9.7%` | Clean stock/cash AI book, but below target. |
| `codex_book_wes_ai_60ai_oos_v1` | `08/21/20` | `2` | `26.7%` | `1.72` | `-11.4%` | Clean stock/cash AI book, but below target. |
| `codex_book_ai_sc_lgbm_diversified_oos_v1` | `08/21/20` | `5` | `33.7%` | `1.55` | `-14.9%` | AI strategy book but below target. |

Inventory conclusion: no hidden native platform object currently satisfies the hard goal. The clean AI Factor strategy/book family remains capped around Sharpe `1.60` for pure AI and `1.74` for stock/cash AI books. The only visible `1.90` Sharpe book is not a clean long-only stock AI Factor strategy and has worse drawdown; it is useful as a risk-control reference, not a goal-compliant winner.

## 2026-05-26 05:13 EDT - Reference stock sleeves plus AI replacement book

Purpose: test a zero-RU native simulated book inspired by the visible `BookSim - Copy` risk mix, but keep the candidate cleaner by replacing the non-stock ballast idea with the current AI Factor strategy sleeve.

Surface: Portfolio123 web platform UI only. No P123 API was used and no Resource Units were spent.

Source cloned book: `codex_book_stock_ai_mix_oos_v1` / `1944242`.

New native simulated book: `codex_book_refstock_ai_403030_oos_v1` / `1944441`.

Static weight setup:

| Asset | Type | Target weight |
| --- | --- | ---: |
| `Advisor Small Cap Focus (P123) With Risk Reduction` / `1724626` | PTF | `40%` |
| `Wes Gray Momentum Microcaps Hedged` / `1848302` | PTF | `30%` |
| `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` | SIM | `30%` |

Native result from Portfolio123 summary:

| Metric | Value |
| --- | ---: |
| Period | `08/21/2020 - 01/16/2026` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Total Return | `313.44%` |
| Benchmark Return | `120.07%` |
| Active Return | `193.37%` |
| Annualized Return | `30.01%` |
| Max Drawdown | `-16.16%` |
| Benchmark Max Drawdown | `-24.50%` |
| Sharpe Ratio | `1.61` |
| Correlation with SPY | `0.59` |

Decision: reject as a goal winner. It clears the active-return requirement, but Sharpe `1.61` is well below the hard `>1.9` objective and is worse than the existing clean stock/cash AI book leader `codex_book_wes_ai_equal_oos_v1` at Sharpe `1.74`. This test does add useful evidence: leaning toward the older reference book's stock sleeves does not recover the missing Sharpe once the TLT/GLD ballast is removed.

## 2026-05-26 05:28 EDT - Rolling-CV setup attempt consumed as Basic Holdout and rejected

Purpose: try the next justified cost-controlled AI Factor setup change after native construction and target tweaks topped out below Sharpe `>1.9`: clone the original small-cap source, keep the raw 3M target and 32 features, and attempt Rolling Time Series CV with saved validation predictions.

Surface: Portfolio123 web platform UI only. No P123 API was used.

Platform object:

| Object | Name / ID | Notes |
| --- | --- | --- |
| AI Factor | `codex_ai_sc_rollcv3m_v1` / `28671` | Created from `SCs Small and Micro Cap Focus + 10 Mil min Replic2` / `27417` through platform `Actions -> Save As`. Copied features only; studies and predictors were unchecked. |

Setup:

| Setting | Value |
| --- | --- |
| Target | `3MTotReturn` |
| Target formula | `Future%Chg_D(65)` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Period | `2006-01-01` to `2026-01-17` |
| Frequency | Every Week |
| Features | `32` |
| Scaling | Rank |
| Intended method | Rolling Time Series CV, `20` week gap, `4` folds, `5.0` year training period |
| Accepted/displayed method after reload | Basic Holdout, `20` week gap, `14.3` year training period, `65` month holdout |

Platform boundary: the Rolling Time Series CV radio button could be selected on the Method page, but after navigating through Load/Models and after reload, P123 displayed Basic Holdout again. The validation ran in `34 sec` on Premium, consistent with Basic Holdout rather than Rolling CV. Treat Basic Holdout as the accepted platform state for this object unless a future workflow finds a real save route for the Method page before dataset/model start.

Cost:

| Step | Value |
| --- | ---: |
| Dataset estimate | `~359MB`, `~102.5M` data points, `14` Resource Units |
| Dataset actual | `315MB`, `79.5M` data points, `12` Resource Units |
| Load start | `5/26/2026, 4:23 AM` platform time |
| Load time | `1 min, 25 sec` |
| Model | `lightgbm II` |
| Save validation predictions | Yes |
| Model validation | `SUCCESS`, Rank `100`, Premium `34 sec`, `1.2 GB`, `3` Resource Units |
| Total branch spend | `15` Resource Units |

Compare-table diagnostics at displayed settings `Quantiles 10`, `Slippage 0.1%`:

| RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Low Avg% | Low SR | Low Turn% |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.5662` | `0.1888` | `48.64` | `1.22` | `27.49` | `1.35` | `1,135` | `-14.33` | `-0.38` | `826` |

Return-page diagnostics:

| Metric | Value |
| --- | ---: |
| Validation display period | `2020-08-18` to `2026-01-17` |
| Return statistics period | `8/22/2020` to `1/24/2026` |
| Benchmark annualized return shown | `15.47%` |
| Universe annualized return shown | `4.40%` |
| Bucket 10 compounded | `25.45%` |
| Bucket 10 average | `27.49%` |
| Bucket 10 estimate | `21.08%` |
| Bucket 10 annualized turnover | `1,135%` |
| Bucket 1 compounded | `-21.23%` |
| Spearman by quantile | `0.99` entire period, `0.99` first half, `0.42` second half |
| Slope per quantile | `3.705%` entire period, `4.428%` first half, `2.766%` second half |

Decision: reject before native simulated-strategy promotion. The model is much weaker than the current source branch that produced native Sharpe `1.60`: High Avg `27.49%` and High SR `1.35` are far below the source `lightgbm II` row (`56.88%` High Avg, `2.40` High SR). Since stronger model-table candidates have repeatedly failed to clear native Sharpe `>1.9`, this branch has no decision value for another native simulation spend.

## 2026-05-26 05:45 EDT - Zero-RU live inventory continuation after final checkpoint

Purpose: continue the persistent goal by re-checking the live Portfolio123 platform inventory after the strict no-winner checkpoint, starting from existing saved objects before spending more Resource Units.

Native Strategy Book opener, `https://www.portfolio123.com/app/opener/BOOKSIM`, still shows no clean goal-compliant book:

| Book | Inception | Assets | Annual | Sharpe | Drawdown | Decision |
|---|---:|---:|---:|---:|---:|---|
| `BookSim - Copy` | `01/03/06` | `4` | `22.9%` | `1.90` | `-25.5%` | Not clean: relies on non-stock ballast rather than a long-only stock AI Factor result. |
| `BookSim(8)codex_book_wes_ai_equal_oos_v1` | `08/21/20` | `2` | `24.4%` | `1.74` | `-10.6%` | Best clean stock/cash AI book; below hard Sharpe gate. |
| `codex_book_stock_ai_mix_oos_v1` | `08/21/20` | `3` | `23.6%` | `1.73` | `-9.7%` | Below clean book leader. |
| `codex_book_wes_ai_60ai_oos_v1` | `08/21/20` | `2` | `26.7%` | `1.72` | `-11.4%` | Higher return, lower Sharpe than equal-weight book. |

Native simulated strategy opener, `https://www.portfolio123.com/app/opener/SIM`, still shows no long-only stock AI Factor strategy above the current pure-AI leader:

| Strategy | Inception | Annual | Excess | Sharpe | Drawdown | Decision |
|---|---:|---:|---:|---:|---:|---|
| `codex_strategy_sc_lgbm2_oos_v1_top1` | `08/22/20` | `35.9%` | `20.2%` | `1.60` | `-15.7%` | Current pure AI leader. |
| `codex_sc_lgbm2_buyback_v1` | `08/22/20` | `35.9%` | `20.2%` | `1.60` | `-15.7%` | Same headline result; no improvement. |
| `codex_strategy_sc_blend_lgbm2_123mclip_v1` | `08/22/20` | `35.9%` | `20.2%` | `1.59` | `-15.5%` | Near miss; lower Sharpe than leader. |
| `codex_strategy_sc_123mclip_lgbm2_oos_v1` | `08/22/20` | `36.1%` | `20.4%` | `1.54` | `-17.9%` | Slightly higher return, weaker risk-adjusted result. |

AI Factor opener, `https://www.portfolio123.com/sv/opener/AIFACTOR/-2`, still shows the loaded `codex_` small-cap experiment family plus older SP500/no-finance AI Factors. No new already-loaded object appeared with an obvious native promotion case.

One previously noted watchlist row was inspected directly without spending Resource Units:

| AI Factor | ID | Model | Validation window | Key diagnostics | Decision |
|---|---:|---|---|---|---|
| `SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm` | `20721` | `deeptables wide_regularized` | `04/27/2024 - 05/24/2025` | Rank `100`, Spearman `0.0066`, H-L Avg `2.09`, H-L SR `0.06`, High Avg `24.06`, High SR `1.10`, High Turn `1,002%`; Bucket 100 compounded `21.94%`, first half `52.98%`, second half `-2.81%`. | Reject before native simulation. The top bucket is unstable, the validation window is short, and the high-low spread is nearly absent. It does not have enough decision value to promote versus the current native leader. |

Updated state: the best native pure-AI strategy remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` at Sharpe `1.60`; the best clean stock/cash book remains `codex_book_wes_ai_equal_oos_v1` / `1944244` at Sharpe `1.74`. No Resource Units were spent in this continuation pass.

## 2026-05-26 06:05 EDT - Native ATRN entry-volatility gate rejected

Purpose: test one zero-new-Resource-Unit construction variant that was materially different from prior beta, trend, stop-loss, liquidity, and position-count wrappers. The hypothesis was that directly filtering high-normalized-ATR stocks at entry might reduce realized portfolio volatility while preserving the current `lightgbm II` AI Factor edge.

The current source AI Factor compare table was re-read before the test:

| Model | Rank | RMSE | Spearman | H-L Avg% | H-L SR | High Avg% | High SR | High Turn% | Native status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `lightgbm slow 3` | `100` | `0.5658` | `0.1980` | `195.44` | `2.02` | `48.74` | `2.14` | `1,867` | Already promoted; native Sharpe `1.24`. |
| `lightgbm II - SCGotlesp` | `92` | `0.5659` | `0.1979` | `188.01` | `2.02` | `48.46` | `2.13` | `1,792` | Already promoted; native Sharpe `1.34`. |
| `lightgbm medium 2` | `92` | `0.5658` | `0.1938` | `182.39` | `1.88` | `52.30` | `2.17` | `1,918` | Already promoted; native Sharpe `1.36`. |
| `lightgbm III` | `71` | `0.5661` | `0.1953` | `167.33` | `1.75` | `48.89` | `2.19` | `1,794` | Already promoted; native Sharpe below leader. |
| `lightgbm II` | `50` | `0.5663` | `0.1876` | `163.11` | `1.74` | `56.88` | `2.40` | `1,971` | Current native pure-AI leader; native Sharpe `1.60`. |
| `extra trees II` | `35` | `0.5663` | `0.2097` | `96.13` | `1.11` | `31.63` | `1.58` | `940` | Rejected before native promotion; weaker top-bucket economics. |

Conclusion from source table: no unpromoted saved-result row has a stronger promotion case than the already-tested `lightgbm II` leader. The remaining useful zero-RU test was construction-level, not another model promotion.

Native simulated strategy created through Portfolio123 UI `Save As a new "Simulated Strategy"` from `codex_strategy_sc_lgbm2_oos_v1_top1`:

| Field | Value |
|---|---|
| New strategy | `codex_strategy_sc_lgbm2_atrn50_oos_v1` |
| Port ID | `1944451` |
| Source strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Inception shown in opener | `08/22/20` |
| AI signal | `AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")` |
| Buy rule 1 | `FRank(\`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")\`, #All, #Desc) > 99` |
| Buy rule 2 | `Close(0) > 0.5` |
| Buy rule 3 | `AvgDailyTot(20) > 10000` |
| Buy rule 4 | `FRank(\`ATRN(20)\`, #All, #Asc) > 50` |
| Sell rule | `FRank(\`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")\`, #All, #Desc) < 95` |

Native result from Portfolio123 summary/opener:

| Metric | Value |
|---|---:|
| Total return | `318.79%` |
| Benchmark return | `120.07%` |
| Active return | `198.72%` |
| Annualized return | `30.32%` |
| Opener annual / excess | `30.3%` / `14.6%` |
| Sharpe ratio | `1.38` |
| Max drawdown | `-16.95%` |
| Benchmark max drawdown | `-24.50%` |
| Annual turnover | `398.01%` |
| Holdings | `20` |

Decision: reject. The ATRN entry-volatility gate cut too much return, did not reduce turnover, worsened drawdown versus the current leader, and lowered native Sharpe from `1.60` to `1.38`. This rules out a simple direct ATRN entry filter as the missing Sharpe fix. The current native pure-AI leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`; the hard `>1.9` Sharpe goal remains unmet.

## 2026-05-26 06:20 EDT - Soft ATR blend construction attempt aborted before simulation

Purpose: test a softer construction variant after the hard ATRN entry gate failed. Instead of excluding the higher-ATR half of the universe, the planned test would keep the AI Factor dominant and add a small low-ATR bonus inside the rank threshold.

Intended clone route:

| Field | Value |
|---|---|
| Source strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` |
| Intended name | `codex_strategy_sc_lgbm2_atrblend_oos_v1` |
| Platform action | `Save As a new "Simulated Strategy"` from the source strategy |
| Actual visible copied name before abort | `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(8)` |
| Resource Units | `0`; no AI Factor model, dataset load, or validation was started |

Intended buy rule:

```text
(0.85*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.15*FRank(`ATRN(20)`, #All, #Asc)) > 99
```

Intended sell rule:

```text
(0.85*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.15*FRank(`ATRN(20)`, #All, #Asc)) < 95
```

Abort reason: the Portfolio123 wizard opened correctly, but the current in-app browser session could not safely edit long text fields. `fill`, `type`, and DOM-CUA text entry failed with the browser clipboard bridge unavailable, and read-only page evaluation could not mutate the formula inputs. A single-key probe also did not reliably insert text. The branch was therefore stopped before running a native simulation to avoid saving a partially edited or corrupted strategy.

Decision: no performance claim. This is an aborted setup attempt, not a rejected native result. The idea remains a possible future zero-RU native construction test if editing is done manually in the browser or through a browser session whose text-entry bridge is working. Current validated leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` at native Sharpe `1.60`.

## 2026-05-26 06:35 EDT - Current leader native-statistics and requirement audit

Purpose: strengthen the evidence trail around the current best native candidate after the soft ATR blend could not be safely edited in the current browser session. No new Portfolio123 objects were created and no Resource Units were spent.

Authoritative pages inspected through the Portfolio123 web platform:

- Summary: `https://www.portfolio123.com/port_summary.jsp?portid=1944200`
- Statistics: `https://www.portfolio123.com/performance_stats.jsp?portid=1944200`

Native summary evidence for `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`:

| Field | Native P123 value |
|---|---:|
| Period | `08/22/20 - 01/17/26` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Positions | `20` |
| Total return | `426.33%` |
| Benchmark return | `120.07%` |
| Active return | `306.26%` |
| Annualized return | `35.94%` |
| Benchmark annualized return | `15.70%` |
| Annualized active spread | `20.24` percentage points |
| Annual turnover | `398.55%` |
| Max drawdown | `-15.65%` |
| Benchmark max drawdown | `-24.50%` |
| Winners | `278/474`, or `58.00%` |
| Sharpe ratio | `1.60` |
| Correlation with SPY | `0.67` |

Native statistics page period-return evidence:

| Return window | Model | SPY benchmark | Excess |
|---|---:|---:|---:|
| Total | `426.33%` | `120.07%` | positive |
| Annualized | `35.94%` | `15.70%` | `+20.24` percentage points |
| Year to date | `3.52%` | `1.43%` | positive |
| 4 week | `-0.29%` | `1.63%` | negative |
| 13 week | `13.15%` | `4.41%` | positive |
| 1 year | `26.33%` | `18.28%` | positive |
| 3 year | `129.55%` | `80.89%` | positive |

Native calendar-year evidence:

| Year | Model | SPY benchmark | Excess |
|---|---:|---:|---:|
| `2020*` | `26.63%` | `11.05%` | `+15.59%` |
| `2021` | `51.30%` | `28.73%` | `+22.57%` |
| `2022` | `8.94%` | `-18.18%` | `+27.11%` |
| `2023` | `52.98%` | `26.18%` | `+26.80%` |
| `2024` | `28.59%` | `24.89%` | `+3.70%` |
| `2025` | `23.83%` | `17.72%` | `+6.12%` |
| `2026**` | `3.52%` | `1.43%` | `+2.09%` |

Closest universe-matched check: P123's native simulated-strategy summary identifies the actual trading universe as `No OTC Exchange + min 10 mil min vol - OWN`. The direct native strategy page does not expose a separate investable universe-index benchmark beside SPY. The closest available universe-matched evidence remains the AI Factor Return page for the same source universe and validation model family, which showed universe annualized returns far below the current native strategy's `35.94%` annualized return in the accepted validation window. No obvious universe-relative failure is visible; the failure is strictly the hard Sharpe hurdle.

Requirement audit as of this checkpoint:

| Requirement | Evidence status |
|---|---|
| Long-only stock strategy using a P123 AI Factor signal | Satisfied for current leader: native SIM, Stock type, 20 holdings, AI formula based on `AIFactorValidation(...)`. |
| Platform-only work | Satisfied for campaign evidence in this log; no P123 API create/update/run/validate actions used for the current platform-only campaign. |
| Native P123 validation as source of truth | Satisfied for performance claims: current leader values come from P123 Summary/Statistics pages. |
| OOS Sharpe `>1.9` | Not satisfied. Current leader is `1.60`; closest clean stock/cash book is `1.74`. |
| OOS active annualized return `>5` percentage points vs SPY | Satisfied for current leader: `35.94%` vs `15.70%`, spread `+20.24` percentage points. |
| Closest universe-matched benchmark check | Partially satisfied from available platform evidence; no visible universe-relative failure, but native SIM exposes SPY as benchmark rather than a separate universe index. |
| Must beat documented prior AI Factor results | Satisfied on active return and Sharpe versus older base-87 AI Factor native strategies, but not enough for hard Sharpe `>1.9`. |
| Longest defensible OOS window | Satisfied for the current Basic Holdout saved-validation source: native accepted period is `08/22/20 - 01/17/26`. Longer Time Series CV branch was tested and rejected. |
| Track costs, object IDs, formulas, dates, and outcomes | Satisfied in this log for promoted/rejected branches; latest audit spent `0` Resource Units. |

Updated conclusion: the active-return goal is clearly met by the current leader, and the current leader does not show obvious SPY or universe-relative failure. The binding constraint remains native portfolio Sharpe. The campaign has not produced a goal-compliant winner because no native long-only stock AI Factor strategy has cleared Sharpe `>1.9`.

## 2026-05-26 06:48 EDT - Soft ATR blend retry blocked by platform text-entry boundary

Purpose: retry the previously aborted soft ATR blend idea using the P123 Buy-tab `Text Editor`, because an earlier campaign step had successfully worked around formula-field editing by using character-level visible input in that surface.

Intended formula remained:

```text
(0.85*FRank(`AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")`, #All, #Desc)+0.15*FRank(`ATRN(20)`, #All, #Asc)) > 99
```

Platform-only actions attempted:

- Re-opened the safe P123 `Save As a new "Simulated Strategy"` workflow from `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`.
- Opened the Buy tab and P123 `Text Editor`.
- Confirmed the current draft copy was still visible as `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(8)`.
- Tested text replacement through the P123 rule textarea and raw Text Editor textarea.
- Tried the user's Chrome profile through the Codex Chrome Extension as an alternate platform UI route.

Outcome:

- The in-app browser still could not safely replace long P123 wizard text. Clipboard-backed `fill`, `type`, and paste failed because the virtual clipboard bridge was unavailable.
- Character-level selection did not reliably select or replace the existing formula; a probe inserted a stray `X` into the draft formula text. This confirmed the copy was not safe to run.
- The raw Buy-tab `Text Editor` opened, but it exposed the same text-entry limitation.
- Chrome automation connected, but the visible P123 strategy-wizard tab in Chrome was `Access Restricted`, so it did not provide an authenticated editing path.
- No native simulation was run, no performance result was produced, and no AI Factor Resource Units were spent.

Decision: do not count the draft copy as a candidate. The soft ATR blend remains untested, but repeated platform/browser text-entry failure makes it a low-priority manual-only follow-up rather than an autonomous path. Current validated leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` at Sharpe `1.60`.

## 2026-05-26 07:05 EDT - 15-position sizing variant ran natively and was rejected

Purpose: finish checking the remaining cheap construction idea from the prior checkpoint: reduce the current leader from roughly 20 positions to about 15 positions by changing only static target position size from `5.0%` to `6.67%`.

Platform-only status: the strategy copy unexpectedly completed as a native Portfolio123 simulated-strategy run after the earlier wizard save/run uncertainty. No P123 API was used, no AI Factor dataset/model was loaded, and no new Resource Units were spent.

Native object and setup evidence:

| Field | Value |
|---|---|
| Strategy | `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(8)` |
| Port ID | `1944463` |
| Source strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Ranking system | `Core Combination` |
| Native period | `08/22/20 - 01/17/26` |
| Intended construction change | Static target position size `6.67%`, producing about `15` ideal positions |
| Actual holdings on summary | `14` |

Native Portfolio123 summary result:

| Metric | Value |
|---|---:|
| Total return | `406.36%` |
| Benchmark return | `120.07%` |
| Active return | `286.28%` |
| Annualized return | `34.98%` |
| Opener annual / excess | `35.0%` / `19.3%` |
| Sharpe ratio | `1.49` |
| Max drawdown | `-18.47%` |
| Benchmark max drawdown | `-24.50%` |
| Annual turnover | `396.26%` |
| Correlation with SPY | `0.67` |
| Winners | `201/329`, or `61.00%` |

Portfolio123 SIM opener inventory was also checked after the run. No visible `codex_` or `agent_` long-only stock AI Factor simulation exceeded the current pure-AI leader's Sharpe `1.60`; the highest clean rows remained `codex_strategy_sc_lgbm2_oos_v1_top1` and the duplicate `codex_sc_lgbm2_buyback_v1` at Sharpe `1.60`.

Decision: reject. The 15-position sizing variant preserves strong active return, but it worsens drawdown and lowers native Sharpe from `1.60` to `1.49`. This exhausts the remaining simple position-count tweak around the current leader. Current validated leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`.

## 2026-05-26 07:25 EDT - Remaining loaded AI Factor inventory rechecked, no promotion candidate

Purpose: continue the goal from existing platform state before spending any more Resource Units. The check focused on older loaded AI Factors on page 2 of the Portfolio123 AI Factor opener plus remaining source-clone evidence in the local log.

Surface: Portfolio123 web platform UI only. No P123 API was used, no native simulations were launched, and no new Resource Units were spent.

Inventory rows rechecked through the platform:

| AI Factor | ID | Platform state | Best visible diagnostics | Decision |
|---|---:|---|---|---|
| `agent_highsr_lgbm_sp500_v1` | `27238` | Dataset loaded, `3` results, `1` predictor | Best rows had Rank `100`, but H-L Avg only `6.00 - 7.40`, H-L SR `0.38 - 0.50`, High Avg `15.78 - 16.46`, High SR `0.70 - 0.73`, high turnover `304 - 564`. | Reject before native promotion. Not enough spread or high-bucket strength to beat the current leader. |
| `SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials` | `20725` | Dataset loaded, `3` results, `2` predictors | Best H-L row had H-L Avg `5.69`, H-L SR `0.56`, High Avg `7.79`, High SR `0.66`; other rows had negative H-L or negative High Avg. | Reject before native promotion. Weak high bucket and weak separation. |
| `SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm` | `20721` | Dataset loaded, `3` results, `1` predictor | `deeptables wide_regularized` had High Avg `24.06`, High SR `1.10`, but H-L Avg only `2.09` and H-L SR `0.06`; other rows had negative High Avg or negative H-L. | Reject before native promotion. Unstable ranking surface; no robust long-only signal. |
| `SP500_Alpha_MaxSharpe_3M_v1` | `20717` | Dataset loaded, `3` validations, `0` results, `0` predictors | Compare page exposed no saved result rows. | Not usable for `AIFactorValidation(...)` native promotion without new validation/result work. |
| `agent_ml_v3_lgbm` | `26889` | Dataset loaded, `1` result, `2` predictors | `lightgbm slow 2`: Rank `100`, H-L Avg `39.52`, H-L SR `1.30`, High Avg `16.17`, High SR `0.63`, high turnover `1,380`. | Reject before native promotion. High bucket is too weak and volatile. |
| `agent_ml_2003_87f_v1` | `26875` | Dataset loaded, `4` results | Best visible row `extra trees slow 4`: H-L Avg `28.46`, H-L SR `1.21`, High Avg `26.17`, but High SR only `0.57` and high turnover `1,282`; other rows had weaker high-bucket economics. | Reject before native promotion. |

Context for the threshold: the current winning source row from `SCs Small and Micro Cap Focus + 10 Mil min Replic2` had much stronger diagnostics (`lightgbm II` High Avg `56.88`, High SR `2.40`) and still produced only native Sharpe `1.60`. None of the rechecked inventory rows is close to that model-table-to-native hurdle.

Local log cross-check: the remaining first-page source clone `codex_ai_sc_sourceclone_period_v1` / `28656` was already rejected before native promotion. Its best model, `lightgbm II`, had High Avg `28.01`, High SR `1.38`, high turnover `1,102`, and weaker top-bucket economics than the current source leader.

Decision: no existing loaded saved-prediction AI Factor is worth promoting to another native simulated strategy at this checkpoint. The next meaningful progress would require either a materially different platform AI Factor design or a browser text-entry path that can safely create richer ranking blends. Current validated leader remains `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`; hard Sharpe `>1.9` remains unmet.

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
