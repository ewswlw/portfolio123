---
title: Portfolio123 Platform-Only AI Factor Campaign Completion
created_at: 2026-05-26 08:23 America/New_York
date: 2026-05-26
category: workflow-issues
module: Portfolio123 AI Factor research
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Running platform-only Portfolio123 AI Factor campaigns"
  - "Evaluating native Sharpe and active-return goals"
  - "Deciding whether an AI Factor model deserves native simulated-strategy promotion"
  - "Closing a no-winner AI Factor campaign with a best-candidate report"
tags:
  - portfolio123
  - ai-factor
  - native-validation
  - platform-only
  - resource-units
  - sharpe
  - oos
  - codex-naming
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-26
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 Platform-Only AI Factor Campaign Completion."
---

# Portfolio123 Platform-Only AI Factor Campaign Completion

## Context

This learning was captured after completing a cost-controlled Portfolio123 AI Factor campaign whose hard goal was a long-only stock strategy with native out-of-sample Sharpe above `1.9` and active annualized return above `5` percentage points versus `S&P 500 (SPY:USA)`.

The campaign was constrained to the Portfolio123 web platform. AI Factor setup, dataset loads, validation starts, saved validation predictions, ranking/strategy construction, and native simulations were handled through the UI. Native Portfolio123 output was the source of truth; AI Factor compare and return tables were used only as triage evidence before native promotion.

For platform-only work, keep the entire workflow on native web pages. Do not fall back to the Portfolio123 API or `ApiRankingSystem` unless the user explicitly lifts the browser-only constraint. If ranking-system access is uncertain, first check the exact native opener at `https://www.portfolio123.com/app/opener/RNK` and document what the web platform allows.

The final result was a strict no-winner. The best native pure AI Factor strategy found was:

```text
Strategy: codex_strategy_sc_lgbm2_oos_v1_top1
Port ID: 1944200
Formula: AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")
Universe: No OTC Exchange + min 10 mil min vol - OWN
Benchmark: S&P 500 (SPY:USA)
Native period: 08/22/2020 - 01/17/2026
Annualized return: 35.94%
SPY annualized return: 15.70%
Active annualized spread: +20.24 percentage points
Sharpe ratio: 1.60
Max drawdown: -15.65%
Annual turnover: 398.55%
```

This candidate clearly cleared the active-return hurdle and beat older documented native AI Factor branches, but it failed the hard Sharpe `>1.9` requirement.

## Guidance

Use the current native leader as the promotion benchmark, not just the user-requested target. For this campaign, any new branch had to plausibly beat `codex_strategy_sc_lgbm2_oos_v1_top1` at `35.94%` annualized return and `1.60` Sharpe before it deserved more native simulation work.

Promote AI Factor models into native simulated strategies only when model-table evidence clears the source-to-native hurdle. The source row that produced the leader had unusually strong diagnostics:

```text
AI Factor: SCs Small and Micro Cap Focus + 10 Mil min Replic2
Model: lightgbm II
High Avg%: 56.88
High SR: 2.40
High Turn%: 1,971
```

Even that row translated to only `1.60` native Sharpe. Later candidates with materially weaker high-bucket Sharpe, high-low Sharpe, top-bucket return, or stability were rejected before native promotion to avoid wasting effort and Resource Units.

Stop weak branches early. The campaign repeatedly found that smoother-looking target designs or longer validation windows reduced top-bucket economics enough that a native strategy run had low decision value. Examples included clipped 3M targets, downside/crash/ATRN/beta penalties, z-score preprocessing, 87-feature expansion, and attempted Time Series or Rolling CV setups.

Keep native strategy construction tests separate from AI Factor model tests. Construction variants such as 10/15/20/30 positions, smoother exits, liquidity filters, stop losses, monthly or two-week rebalance, market gates, low-volatility gates, and stock/cash books clarified the binding constraint, but they did not change the underlying AI Factor model quality.

Log every promoted branch with:

- object name and P123 ID,
- exact `AIFactorValidation(...)` formula,
- native accepted OOS period,
- universe and benchmark,
- native return, active return, Sharpe, drawdown, turnover,
- visible dataset/model Resource Units,
- decision and reason for rejection or promotion.

Use `codex_` names for new account objects and do not overwrite or delete existing P123 objects.

## Why This Matters

Strong AI Factor table diagnostics do not guarantee a goal-compliant native portfolio. In this campaign, the best source model had a strong high-bucket profile and produced excellent active return, but the native long-only strategy still capped at Sharpe `1.60`.

The binding constraint was not alpha. It was portfolio-level risk: volatile small/micro-cap exposure, high turnover, drawdowns, and regime noise. Many variants preserved or improved active return in spots, but none improved native risk-adjusted performance enough to clear `>1.9` Sharpe.

This distinction prevents two common mistakes:

- declaring success from AI Factor compare-table `High SR` or lift metrics without native simulation;
- spending more Resource Units or native runs on models whose validation profiles are weaker than the already-insufficient source row.

The no-winner result is still useful. It establishes a native benchmark and a promotion gate for future work: a new platform design must either materially improve top-bucket stability or broaden/smooth the investable universe before it deserves expansion.

## When to Apply

- When running a platform-only Portfolio123 AI Factor campaign with a high Sharpe and active-return target.
- When deciding whether saved validation predictions are strong enough for a native simulated strategy.
- When an existing native AI Factor leader already clears active return but fails Sharpe.
- When closing a campaign where no candidate met all hard requirements.
- When deciding whether to spend more Resource Units on another AI Factor clone or validation model.

## Examples

Current native leader:

| Field | Value |
|---|---|
| Strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` |
| Port ID | `1944200` |
| Formula | `AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")` |
| Native period | `08/22/2020 - 01/17/2026` |
| Annualized return | `35.94%` |
| Active annualized spread vs SPY | `+20.24` percentage points |
| Sharpe | `1.60` |
| Max drawdown | `-15.65%` |
| Decision | Best native pure AI Factor candidate; rejected as final winner because Sharpe is below `1.9`. |

Rejected 15-position sizing variant:

| Field | Value |
|---|---|
| Strategy | `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(8)` |
| Port ID | `1944463` |
| Intended change | Static target position size `6.67%`, about `15` ideal positions |
| Actual holdings | `14` |
| Native period | `08/22/2020 - 01/17/2026` |
| Annualized return | `34.98%` |
| Active return vs SPY | `286.28%` total |
| Sharpe | `1.49` |
| Max drawdown | `-18.47%` |
| Decision | Rejected; preserved alpha but worsened drawdown and Sharpe versus the leader. |

Rejected remaining inventory pass:

| AI Factor | ID | Reason not promoted |
|---|---:|---|
| `agent_highsr_lgbm_sp500_v1` | `27238` | Best rows had H-L Avg only `6.00 - 7.40` and High SR only `0.70 - 0.73`. |
| `SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials` | `20725` | Weak high bucket; best High SR `0.66`. |
| `SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm` | `20721` | High SR `1.10` but H-L SR only `0.06`, indicating unstable separation. |
| `SP500_Alpha_MaxSharpe_3M_v1` | `20717` | No saved result rows visible for `AIFactorValidation(...)` promotion. |
| `agent_ml_v3_lgbm` | `26889` | High Avg `16.17`, High SR `0.63`, high turnover `1,380%`. |
| `agent_ml_2003_87f_v1` | `26875` | Best High Avg `26.17`, but High SR only `0.57`. |

Useful reporting language:

```text
No native long-only stock AI Factor candidate met Sharpe >1.9. The best native candidate was codex_strategy_sc_lgbm2_oos_v1_top1 / 1944200 at 35.94% annualized return and 1.60 Sharpe over 08/22/2020 - 01/17/2026. It cleared the active-return requirement but failed the hard Sharpe gate. The binding constraint was portfolio-level risk and turnover in small/micro-cap long-only construction, not lack of alpha.
```

## Related

- Portfolio123 AI Factor validation strategy workflow: `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- Portfolio123 AI Factor clone validation setup workflow: `docs/solutions/workflow-issues/portfolio123-ai-factor-clone-validation-setup-2026-05-25.md`
- Portfolio123 API-ranking native AI Factor strategy workflow: `docs/solutions/workflow-issues/portfolio123-api-ranking-native-ai-factor-strategy-workflow-2026-05-25.md`
- Portfolio123 browser navigation for simulations and AI Factors: `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- Final campaign report: `p123-output/ai_factor_platform_oos_campaign_final_20260526.md`
- Running campaign log: `p123-output/ai_factor_platform_oos_campaign_20260525.md`
- Portfolio123 skill: `C:/Users/Eddy/.codex/skills/portfolio123/SKILL.md`

---

## Tags

#portfolio123 #ai-factor #native-validation #platform-only #resource-units #sharpe #oos #codex-naming #algo-trading/portfolio123 #work/solutions #work/workflow-issues
