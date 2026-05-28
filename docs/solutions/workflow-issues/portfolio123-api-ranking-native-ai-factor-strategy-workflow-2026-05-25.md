---
title: Portfolio123 API Ranking Native AI Factor Strategy Workflow
date: 2026-05-25
created_at: 2026-05-25 14:36 America/New_York
category: workflow-issues
module: Portfolio123 AI Factor strategy development
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Creating a native Portfolio123 simulated strategy from an AI Factor validation model"
  - "P123 native ranking-system Save As is unavailable or blocked by membership level"
  - "The exact native ranking-system opener has been checked and a browser-only route is insufficient"
  - "A strategy must use saved AIFactorValidation predictions from a cloned AI Factor"
  - "A native Tier 2 simulation is needed after an API ranking-system update"
tags:
  - portfolio123
  - ai-factor
  - api-ranking
  - ranking-system
  - native-simulation
  - aifactorvalidation
  - strategy-wizard
  - apirankingsystem
  - tier-2-validation
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-25
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 API Ranking Native AI Factor Strategy Workflow."
---

# Portfolio123 API Ranking Native AI Factor Strategy Workflow

## Context

When a Portfolio123 AI Factor validation model has saved predictions, the next research step is usually a native simulated strategy. The preferred path is a named `codex_` ranking-system copy, but the native ranking-system `Save As` route can be blocked even when the account can still use the strategy wizard.

This learning was captured after validating the cloned AI Factor:

```text
AI Factor: codex_ai_base87_etm4_2024_oos_v1
AI Factor ID: 28612
Validation model: extra trees medium 4 #2
Saved prediction window: 12/23/2023 - 06/21/2025
```

The native ranking copy route failed because `/app/ranking-system/545001/save-as` displayed:

```text
This page is not available at your current membership level.
```

The workable route for that specific run was to update Portfolio123's API-owned ranking system, `ApiRankingSystem` (`541785`), via `rank_update`, then select that ranking system in the native simulated-strategy wizard and run the simulation there.

## Guidance

Use `ApiRankingSystem` only as a deliberate bridge when a separate named ranking copy is unavailable and the user has not constrained the work to browser-only. Before invoking this fallback, check the exact native opener:

```text
https://www.portfolio123.com/app/opener/RNK
```

Do not infer a membership block from guessed ranking URLs. The exact ranking-system opener can be available even when a specific `Save As` or edit route is blocked. If the user says browser-only or no API, keep the workflow on native web pages and report any limitation instead of using `rank_update`.

`ApiRankingSystem` is mutable account state: a later `rank_update` call will overwrite what future strategies using `ApiRankingSystem` see. For durable audit trails, save the exact XML, API response, native strategy ID, and summary metrics under `p123-output/`.

The working ranking XML pattern was:

```xml
<RankingSystem RankType="Higher">
  <StockFormula Weight="0" RankType="Higher" Name="codex_ai_base87_2024_oos" Description="codex 2024 OOS validation - extra trees medium 4 #2" Scope="Universe">
    <Formula>AIFactorValidation(&quot;codex_ai_base87_etm4_2024_oos_v1&quot;, &quot;extra trees medium 4&quot;, &quot;2&quot;)</Formula>
  </StockFormula>
</RankingSystem>
```

The successful API payload omitted `name`. Including `name` failed with:

```text
Unrecognized parameter <name>
```

Use:

```python
client.rank_update({
    "nodes": xml,
    "type": "stock",
    "rankingMethod": 2,
})
```

The successful response was:

```json
{
  "cost": 1,
  "quotaRemaining": 7351
}
```

After updating the API ranking system, create the native simulated strategy through the wizard, not through a local or screen-only backtest. In the verified run, the selected native setup was:

| Setting | Value |
|---|---|
| Ranking system | `ApiRankingSystem` (`541785`) |
| Universe | `No OTC Exchange + min 10 mil No Finance2` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Period | `01/01/2024 - 06/21/2025` |
| Rebalance | `Every Week` |
| Position sizing | Static weight, 20 ideal positions, 5% target |
| Buy rules | `Rank > 90`; `Close(0) > 1`; `AvgDailyTot(20) > 100000`; `1 = 1` |
| Sell rules | `Rank < 80`; no-op placeholders `0`, `0`, `0` |

Always inspect the Review tab before running. In this run, the wizard initially showed `Every 4 Weeks` even though the intended strategy family used weekly rebalancing. The Review page caught that mismatch; switching both `recon_period` and `rebal_period` to `Every Week` fixed the setup before the native run.

## Why This Matters

The API ranking update and native wizard solve different parts of the problem. The API can update the formula surface cheaply, but it does not replace native Portfolio123 simulated-strategy validation. The native wizard remains the authority for Tier 2 strategy performance, date-window acceptance, universe selection, rebalance cadence, and strategy object creation.

This route also avoids two misleading failure modes:

- treating a blocked ranking `Save As` as if native validation is impossible;
- reporting API or local estimates when a real native strategy can still be run.

The tradeoff is mutability. `ApiRankingSystem` is a shared API object, so the strategy result must be documented immediately with the exact formula and native strategy ID. Otherwise a future agent may see the same ranking-system name but a different formula underneath.

## When to Apply

- When P123's native ranking-system copy or raw-editor `Save As` route is blocked.
- When the user has confirmed that a P123 API credit may be spent.
- When the user has not requested browser-only work.
- When exact saved validation predictions are available for `AIFactorValidation(...)`.
- When the next claim needs native P123 simulated-strategy results rather than Tier 3 screen estimates.
- When a temporary API ranking bridge is acceptable and the exact formula will be logged.

## Examples

Verified native strategy:

```text
Name: codex_strategy_ai_base87_2024_oos_baseline_v1
Strategy ID: 1944189
URL: https://www.portfolio123.com/port_summary.jsp?portid=1944189
```

Native Tier 2 result:

| Metric | Strategy | Benchmark |
|---|---:|---:|
| Total return | `21.26%` | `27.39%` |
| Annualized return | `14.03%` | `17.92%` |
| Max drawdown | `-25.26%` | `-18.76%` |
| Sharpe ratio | `0.23` | |
| Annual turnover | `96.97%` | |
| Overall winners | `27 / 58` (`46.55%`) | |
| Correlation with SPY | `0.49` | |

Interpretation from the verified run:

```text
The strategy runs natively from the start of 2024, but the 20-position baseline is weak. It made money, lagged SPY, had low Sharpe, and slightly breached the earlier -25% drawdown line.
```

Useful artifact pattern:

```text
p123-output/ranking_update_api_system_YYYYMMDD.json
p123-output/native_strategy_<strategy-id>_details_YYYYMMDD.json
p123-output/native_strategy_ai_base87_2024_oos_baseline_YYYYMMDD.md
```

## Related

- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-ai-factor-clone-validation-setup-2026-05-25.md`
- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- `p123-output/ai_factor_28612_validation_status_20260525.md`
- `p123-output/ranking_update_api_system_2024_oos_20260525.json`
- `p123-output/native_strategy_1944189_details_20260525.json`
- `p123-output/native_strategy_ai_base87_2024_oos_baseline_20260525.md`

---

## Tags

#portfolio123 #ai-factor #api-ranking #ranking-system #native-simulation #aifactorvalidation #strategy-wizard #apirankingsystem #tier-2-validation #algo-trading/portfolio123 #work/solutions #work/workflow-issues
