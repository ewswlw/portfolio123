---
title: Portfolio123 Browser-Only Factor List FactorMiner Strategy Workflow
date: 2026-05-28
category: workflow-issues
module: Portfolio123 Factor List and FactorMiner strategy development
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Using the in-app Browser plugin for Portfolio123 Factor List or FactorMiner work"
  - "The user explicitly says browser-only or no API"
  - "Promoting FactorMiner diagnostics into native simulated strategies"
  - "Checking whether ranking-system access is available through the web platform"
  - "Reporting native P123 results from browser-created strategy candidates"
tags:
  - portfolio123
  - factor-list
  - factorminer
  - browser-only
  - ranking-system
  - native-validation
  - simulated-strategies
  - workflow-issues
---

# Portfolio123 Browser-Only Factor List FactorMiner Strategy Workflow

## Context

This learning was captured after a browser-only Portfolio123 strategy-development run using the Factor List `Andreas and portfolio123` (`3027`) and its FactorMiner broad analysis. The user explicitly required the in-app Browser plugin and no API use, even though API access was available through membership.

The verified source pages were:

| Task | Route |
|---|---|
| Factor List opener | `https://www.portfolio123.com/sv/opener/FACTORLIST/-2` |
| Factor List factors | `https://www.portfolio123.com/sv/factorList/3027/factors` |
| Factor List Generate tab | `https://www.portfolio123.com/sv/factorList/3027/generate` |
| FactorMiner analysis | `https://www.portfolio123.com/spr/factorList/factorMiner/3027` |
| Ranking systems opener | `https://www.portfolio123.com/app/opener/RNK` |
| Native strategy wizard | `https://www.portfolio123.com/port_wiz.jsp?new=1&type=3&mt=1` |

The FactorMiner run was useful for triage but not sufficient as final strategy evidence. The final browser-created native strategy was:

```text
Strategy: codex_strategy_factorminer_andreas_v1_30w
Strategy ID: 1945400
URL: https://www.portfolio123.com/port_summary.jsp?portid=1945400
Universe: No OTC Exchange + min 10 mil No Finance
Benchmark: S&P 500 (SPY:USA)
Ranking system: Core Combination
Period: 01/01/2006 - 05/28/2026
```

## Guidance

Honor browser-only as a hard constraint. Do not use Portfolio123 API calls, API-owned ranking systems, or DataMiner as a fallback unless the user explicitly lifts the constraint. If a page shows Resource Unit or credit cost, stop and confirm before clicking actions such as Generate, dataset loading, or model validation.

Use this workflow for Factor List to native strategy promotion:

1. Open `/sv/opener/FACTORLIST/-2` and select the target Factor List.
2. Confirm the Factor List name, ID, factor count, dataset status, universe, benchmark, and FactorMiner analysis window.
3. Open the Generate tab only to inspect status and cost. Do not generate if the dataset is already ready.
4. Open FactorMiner results and treat best-factor tables as diagnostic evidence, not native strategy validation.
5. Check `/app/opener/RNK` before concluding that ranking-system creation or editing is blocked. Do not infer a membership block from guessed ranking URLs.
6. Prefer a dedicated `codex_` ranking system when the browser route supports it. If a quick first pass stays inside the strategy wizard, state that the signal was encoded as buy-rule filters rather than a standalone ranking system.
7. Create `codex_` native simulated strategy candidates and use the Review page as the authority for universe, ranking system, period, rebalance cadence, buy rules, sell rules, and position sizing.
8. Report only native P123 simulation results as final performance. Label FactorMiner and formula experiments as triage or construction evidence.

When translating FactorMiner formulas into P123 `FRank()` expressions, quote the formula string:

```text
FRank("NetFCFPSTTM/Price")
```

The unquoted form failed in the native strategy wizard:

```text
FRank() requires the 1st parameter to be a quoted string
```

For a quick browser-only wizard pass, a composite gate can be implemented as a buy rule:

```text
(FRank("NetFCFPSTTM/Price")
+FRank("Price/PriceH")
+FRank("ROI%5YAvg")
+FRank("Close(60)/Close(120)")
+FRank("Pr26W%ChgInd")
+FRank("GrossProfitTTM/EV")
+FRank("OpIncGr%PYQ")
+FRank("Close(120)/Close(180)")
+(100-FRank("MedianVol(65)/SharesCur(0)"))) > 700
```

This is a construction shortcut, not the cleanest final design. A dedicated ranking system is the better next pass when `/app/opener/RNK` is available.

## Why This Matters

FactorMiner can identify promising factor themes, but it is not the same as a native P123 portfolio simulation. A broad FactorMiner run may show alpha while a long-only simulated strategy still has weak risk-adjusted results, large drawdowns, too much cash, or construction problems.

In the verified run, the strict composite gate held only seven current positions and badly lagged SPY. Lowering the gate improved investment and absolute return, but the best quick native variant still had only `0.81` Sharpe and `-48.24%` max drawdown. That is useful research output, not a finished best-possible production strategy.

The ranking opener lesson also matters. During browser navigation, guessed ranking routes can fail or look restricted even when the exact opener works. Always verify `/app/opener/RNK` before switching to workarounds or telling the user that ranking-system access is unavailable.

## When to Apply

- When the user points to a Portfolio123 Factor List or FactorMiner result.
- When the user explicitly says to use `@Browser`, browser-only, or no API.
- When a FactorMiner broad run needs promotion into native simulated strategies.
- When deciding between a quick wizard buy-rule composite and a dedicated ranking-system pass.
- When reporting whether a FactorMiner-derived strategy is genuinely production-quality.

## Examples

Native results from the verified browser-only run:

| Variant | Positions | Composite gate | Total return | Benchmark return | Annualized return | Max drawdown | Sharpe | Turnover | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Strict first pass | 7 current | `> 765` | 59.04% | 775.53% | 2.30% | -17.74% | 0.11 | 25.37% | Rejected; too restrictive and cash-heavy. |
| Main pass | 20 | `> 700` | 2,027.91% | 775.53% | 16.15% | -47.22% | 0.79 | 89.37% | Better but weak risk-adjusted result. |
| Concentrated pass | 10 | `> 700` | 1,166.27% | 775.53% | 13.24% | -54.02% | 0.62 | 73.63% | Rejected; concentration worsened results. |
| Diversified pass | 31 current | `> 700` | 2,096.27% | 775.53% | 16.33% | -48.24% | 0.81 | 96.27% | Best quick variant; not production-ready. |

Useful reporting language:

```text
The FactorMiner factors translated into native alpha versus SPY, but the best quick browser-only simulated strategy had 16.33% annualized return, 0.81 Sharpe, and -48.24% max drawdown over 01/01/2006 - 05/28/2026. That is a useful candidate, not a final best-possible strategy. The next cleaner pass is a dedicated codex_ ranking system from /app/opener/RNK, then native strategy retesting.
```

Useful artifact pattern:

```text
p123-output/factor-research/factorminer_<list-or-owner>_native_strategy_browser_only_YYYYMMDD.md
```

## Related

- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-api-ranking-native-ai-factor-strategy-workflow-2026-05-25.md`
- `docs/solutions/workflow-issues/portfolio123-platform-only-ai-factor-campaign-completion-2026-05-26.md`
- `p123-output/factor-research/factorminer_andreas_native_strategy_browser_only_20260528.md`

---

## Tags

#portfolio123 #factor-list #factorminer #browser-only #ranking-system #native-validation #simulated-strategies #workflow-issues
