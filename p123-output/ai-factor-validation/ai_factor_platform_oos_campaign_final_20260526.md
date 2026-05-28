---
title: "Portfolio123 Platform-Only AI Factor Campaign Final Report"
created_at: 2026-05-26 05:35 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/ai-factors
  - work/generated-artifacts
  - work/validation
created: 2026-05-26
updated: 2026-05-28
description: "Generated Portfolio123 AI Factor validation artifact for Portfolio123 Platform-Only AI Factor Campaign Final Report."
---

# Portfolio123 Platform-Only AI Factor Campaign Final Report

## Goal

Find a Portfolio123 AI Factor strategy, created and evaluated through the web platform only, that satisfies both hard gates:

- Long-only stock strategy or clean stock/cash AI Factor book.
- Native Portfolio123 out-of-sample Sharpe ratio greater than `1.9`.
- Native Portfolio123 out-of-sample active annualized return greater than `5` percentage points versus SPY/S&P 500.

Native Portfolio123 output is the binding evidence. AI Factor compare/return tables were used only for triage; screen/API/local estimates were not treated as final.

## Final Result

No platform-tested candidate satisfied the hard Sharpe `>1.9` gate.

The campaign did find a much stronger AI Factor family than the older base-87 branch, and it clears the active-return requirement by a wide margin. The binding failure is portfolio-level Sharpe, not alpha.

## Best Native Pure AI Factor Strategy

| Field | Value |
|---|---|
| Strategy | `codex_strategy_sc_lgbm2_oos_v1_top1` |
| Port ID | `1944200` |
| AI model formula | `AIFactorValidation("SCs Small and Micro Cap Focus + 10 Mil min Replic2", "lightgbm II")` |
| Universe | `No OTC Exchange + min 10 mil min vol - OWN` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Native period | `08/22/2020 - 01/17/2026` |
| Annualized return | `35.94%` |
| Sharpe ratio | `1.60` |
| Max drawdown | `-15.65%` |
| Total active return vs SPY | `306.26%` |
| Opener excess annualized | `20.2%` |
| Turnover | `398.55%` |
| Decision | Best pure AI Factor candidate; rejected as final winner because Sharpe is below `1.9`. |

## Closest Clean AI Stock/Cash Book

| Field | Value |
|---|---|
| Book | `codex_book_wes_ai_equal_oos_v1` |
| Port ID | `1944244` |
| Components | `Wes Gray Momentum Microcaps Hedged` plus `codex_strategy_sc_lgbm2_oos_v1_top1` |
| Native period | `08/21/2020 - 01/16/2026` |
| Annualized return | `24.36%` |
| Sharpe ratio | `1.74` |
| Max drawdown | `-10.55%` |
| Active return vs SPY | `105.04%` |
| Correlation to SPY | `0.56` |
| Decision | Closest clean stock/cash AI book; still below Sharpe `>1.9`. |

The visible `BookSim - Copy` family reached about `1.90` Sharpe in the Strategy Book opener, but it is not a clean long-only stock AI Factor result because it relies on non-stock ballast such as TLT/GLD and has worse drawdown. It is a risk-control reference, not a goal-compliant winner.

## What Was Tried

The campaign tested the major low-cost platform-only avenues that could plausibly lift Sharpe:

- Existing top AI Factor models from the original base-87 and small/micro-cap model families.
- Native strategy construction changes: top-1% selection, smoother exits, 10/20/30 position variants, monthly rebalance, liquidity filter, stop loss, quality/value overlays, low-beta/low-vol attempts, and blend ranks.
- Strategy Book combinations using stock/cash strategy sleeves.
- New cost-capped AI Factor clones with altered target definitions, z-scoring/clipping, longer validation windows, time-series CV attempts, 87-feature expansion, LightGBM, ExtraTrees, and top-decile diagnostics.
- Fresh platform inventories of AI Factors, simulated strategies, and Strategy Books to check that no existing object already met the target, including older loaded SP500/no-finance AI Factors on page 2 of the AI Factor opener.

## Key Negative Evidence

- Strong AI Factor table diagnostics did not translate into Sharpe above `1.9` in native simulated strategies. The source `lightgbm II` row had strong high-bucket diagnostics, yet the native strategy capped at `1.60`.
- The 1+2+3M target family repeatedly produced native Sharpe around `1.32 - 1.40`, despite acceptable returns.
- The longer-window time-series branch produced a longer saved-prediction range but weak native performance: annualized return around `8.4%`, Sharpe `0.37`, and deep drawdown.
- New feature/algorithm branches had weaker top-bucket strength than the current leader and were rejected before native promotion to avoid wasting Resource Units.
- Stock/cash books improved smoothness but topped out at Sharpe `1.74` under clean constraints.
- The final 15-position sizing variant preserved active return but worsened risk-adjusted performance: native annualized return `34.98%`, Sharpe `1.49`, max drawdown `-18.47%`.
- The remaining loaded saved-prediction AI Factors had validation diagnostics far below the current leader's source hurdle. The best current source row had High Avg `56.88` and High SR `2.40`, yet only produced native Sharpe `1.60`; the remaining inventory rows were materially weaker.

## Most Recent Cost-Controlled Branch

The last native simulated-strategy run was a zero-Resource-Unit construction variant:

| Field | Value |
|---|---|
| Strategy | `codex_strategy_sc_lgbm2_oos_v1_top1 - Copy(8)` |
| Port ID | `1944463` |
| Source | `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200` |
| Intended change | Static target position size `6.67%`, about `15` ideal positions |
| Actual holdings | `14` |
| Native period | `08/22/20 - 01/17/26` |
| Annualized return | `34.98%` |
| Sharpe ratio | `1.49` |
| Max drawdown | `-18.47%` |
| Active return vs SPY | `286.28%` total |
| Decision | Rejected; lower Sharpe and worse drawdown than the current leader. |

The last AI Factor Resource Unit spend was `codex_ai_sc_rollcv3m_v1` / `28671`, created from the small/micro-cap source through `Actions -> Save As`, copying features only.

- Intended setup: Rolling Time Series CV, 20-week gap, 4 folds, 5-year training, saved validation predictions.
- Platform outcome: after load/validation, the Method page displayed Basic Holdout again, so this branch is treated as the platform-accepted Basic Holdout state, not a true rolling-CV result.
- Load cost: `12` Resource Units.
- Validation cost: `3` Resource Units.
- Model: `lightgbm II`, validation `SUCCESS`, rank `100`.
- Saved validation display: `2020-08-18 - 2026-01-17`.
- Top-bucket diagnostics: High Avg `27.49%`, High SR `1.35`, High turnover `1,135%`.
- Decision: rejected before native simulation because it is materially weaker than the current leader's source row and unlikely to clear native Sharpe `>1.9`.

The final zero-Resource-Unit inventory pass rechecked older loaded AI Factors:

| AI Factor | ID | Reason not promoted |
|---|---:|---|
| `agent_highsr_lgbm_sp500_v1` | `27238` | H-L Avg only `6.00 - 7.40`; High SR only `0.70 - 0.73`. |
| `SP500_Alpha_MediumTerm_MaxSharpe_NoFinancials` | `20725` | Weak high bucket; best High SR `0.66`. |
| `SP500_Alpha_MaxSharpe_6M_NoFinancials_MediumTerm` | `20721` | High SR `1.10` but H-L SR only `0.06`; unstable ranking surface. |
| `SP500_Alpha_MaxSharpe_3M_v1` | `20717` | No saved result rows visible for `AIFactorValidation(...)` promotion. |
| `agent_ml_v3_lgbm` | `26889` | High Avg `16.17`, High SR `0.63`, high turnover `1,380%`. |
| `agent_ml_2003_87f_v1` | `26875` | Best High Avg `26.17`, but High SR only `0.57`. |

## Binding Interpretation

The current best AI Factor has real edge: it strongly beats SPY on active return. The unresolved problem is that the edge arrives through volatile, high-turnover small/micro-cap exposure. Native portfolio Sharpe is dragged down by concentration, turnover, drawdowns, and regime noise. More tiny construction tweaks around the same signal family are unlikely to bridge the gap from `1.60` to `>1.9`.

## Next Viable Direction

The next serious attempt should be a materially different platform design, not another small tweak:

- Train a new AI Factor on a smoother target that explicitly rewards risk-adjusted forward returns, not only raw 3-month return.
- Consider a broader, more liquid universe if Sharpe is more important than max alpha.
- Use model-table high-bucket Sharpe, high-low Sharpe, turnover, and second-half validation stability as promotion gates before spending native simulation effort.
- Treat `codex_strategy_sc_lgbm2_oos_v1_top1` as the benchmark to beat: any new candidate must plausibly exceed `35.94%` annualized return or materially lift Sharpe above `1.60` before it deserves expensive expansion.

## Final Decision

Campaign status: strict no-winner.

Best native candidate found: `codex_strategy_sc_lgbm2_oos_v1_top1` / `1944200`.

Closest clean stock/cash book: `codex_book_wes_ai_equal_oos_v1` / `1944244`.

No secrets, cookies, credentials, or API keys are included in this report.

---

## Tags

#algo-trading/portfolio123 #algo-trading/ai-factors #work/generated-artifacts #work/validation
