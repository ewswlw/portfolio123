---
title: Portfolio123 Dynamic Strategy Book Timing Warmup Workflow
created_at: 2026-05-22 14:05 America/New_York
date: 2026-05-22
category: workflow-issues
module: portfolio123-dynamic-strategy-book-research
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Adding dynamic market-timing overlays to Portfolio123 Strategy Book research"
  - "Building API-estimated timed strategy variants before native P123 validation"
  - "Using rolling-window timing signals such as 200-day SMA, 12-month momentum, drawdown, or volatility"
  - "Interpreting a candidate that passes API-estimated gates but starts after timing warmup"
  - "Preparing a native P123 Strategy Book validation package from dynamic API-estimated research"
related_components:
  - tooling
  - documentation
tags:
  - portfolio123
  - strategy-book
  - timing
  - warmup
  - api-estimated
  - native-validation
  - trial-ledger
  - no-lookahead
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-22
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 Dynamic Strategy Book Timing Warmup Workflow."
---

# Portfolio123 Dynamic Strategy Book Timing Warmup Workflow

## Context

This learning was captured after extending the API-only Portfolio123 Strategy Book research pipeline with dynamic timing overlays, conditional inverse ETF exposure, tactical ETF components, and native-validation handoff artifacts.

The prior static research had already shown that weight tuning alone was not enough. A strict static grid tested 22,565 allocations and found no candidate that cleared CAGR >20%, Sharpe >2.0, and max drawdown better than -25%. That made dynamic risk control the next logical research path.

The dynamic pass added a 200-day trend overlay and a timing-signal ensemble to the existing strategy streams. A candidate passed the API-estimated gates after the timing implementation was corrected:

```text
optimizer_family: dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20
weights:
  16% each to five 200-day timed strategy variants
  20% to the defensive proxy component
  0% to conditional inverse sleeve
  0% to tactical ETF component
API-estimated window: 2007-06-26 to 2026-01-05
API-estimated CAGR: 20.68%
API-estimated Sharpe: 2.003
API-estimated max drawdown: -12.81%
```

This is a nomination only. It is not a final Portfolio123 Strategy Book result until native P123 validation confirms the same behavior.

## Guidance

When adding timing overlays to P123 Strategy Book research, treat timing signal construction as a separate validation surface from allocation optimization.

Pre-register the timing rules before running the optimizer. In the verified run, the technical timing candidates were:

```text
bench_above_200d
bench_50d_above_200d
bench_12m_momentum_positive
bench_drawdown_under_20pct
bench_volatility_below_median
```

The 200-day timing rule was the only active timing family in the promoted candidate. Conceptually, the rule was:

```text
Risk-on when the benchmark proxy is above its 200-day moving average.
Risk-off when the benchmark proxy is below its 200-day moving average.
```

For native P123 translation, the intended formula shape is:

```text
Close(0,#Bench) > SMA(200,0,#Bench)
```

For API-estimated local research, shift timing signals by one bar so date `t` allocation uses information available before date `t` returns. Do not allow same-day return information to affect the signal used for that same date.

Keep missing warmup values as missing until every required rolling input exists. Do not let missing rolling-window comparisons collapse to `False`, because that silently turns the warmup period into a risk-off regime.

For example, a local pandas expression like this is unsafe for timing warmup:

```python
signals["bench_above_200d"] = prior_close > sma_200
```

It treats periods where `sma_200` is missing as false. Use an explicit validity mask instead:

```python
signals["bench_above_200d"] = (prior_close > sma_200).where(
    prior_close.notna() & sma_200.notna()
)
```

Then drop rows until all pre-registered timing signals have valid values, or explicitly document why a narrower signal set allows an earlier start.

When the corrected timing signal panel starts later than the original return panel, report both dates. In the verified run:

```text
Original synchronized API return panel: 2006-06-22 to 2026-01-05
Corrected timing signal panel: 2007-06-26 to 2026-01-05
Corrected dynamic return panel: 2007-06-26 to 2026-01-05
```

That later start is not a cosmetic detail. It changes whether the candidate satisfies a "going back that far" requirement.

## Why This Matters

Timing overlays can improve a Strategy Book frontier dramatically, but they also create two new failure modes:

1. The timing signal can leak future information if the rule is not shifted.
2. The warmup period can be misclassified if missing rolling inputs are treated as bearish signals.

The second failure mode is subtle. The first dynamic run appeared to start on the full synchronized panel date because missing timing inputs were collapsed into `False`. That made the early warmup period behave like risk-off exposure rather than an unavailable signal. The code review caught this, the signal construction was fixed, and the corrected dynamic window moved to 2007-06-26.

This also affects interpretation of API-estimated success. The corrected dynamic run produced one promoted candidate with CAGR above 20%, Sharpe just above 2.0, and max drawdown far better than -25%, but the candidate starts after the timing warmup. Future agents must preserve that caveat instead of presenting the result as a full 2006-start Strategy Book.

The final authority remains native Portfolio123 Strategy Book validation. API-estimated dynamic research can nominate:

- which strategy variants to create,
- which timing rule to translate,
- what weights to test,
- and what native object names to use.

It cannot prove that P123 native simulation will use the same warmup, execution, rebalance, cash, and rule semantics.

## When to Apply

Apply this workflow when:

- static Strategy Book weights fail strict CAGR, Sharpe, or drawdown gates;
- the next research step adds market timing, conditional inverse exposure, or tactical ETF components;
- timing rules use rolling history such as SMA, momentum, drawdown, realized volatility, or macro series;
- a local/API candidate appears to pass gates after timing is added;
- or a native validation package is being prepared from API-estimated dynamic results.

Also apply it when reviewing any `dynamic_*` artifacts under `p123-output/`, especially:

```text
p123-output/timing_signal_panel_YYYYMMDD.csv
p123-output/timing_signal_summary_YYYYMMDD.json
p123-output/dynamic_return_panel_YYYYMMDD.csv
p123-output/dynamic_trial_ledger_YYYYMMDD.csv
p123-output/dynamic_candidate_promotion_report_YYYYMMDD.md
p123-output/native_validation_package_YYYYMMDD.md
```

## Examples

Unsafe warmup handling:

```python
signals["bench_50d_above_200d"] = sma_50 > sma_200
signals = signals.astype("boolean")
```

Why it is unsafe:

- `sma_50 > sma_200` returns false when either side is missing.
- The warmup period then becomes a real bearish signal instead of "signal unavailable."
- The dynamic backtest may appear to cover a longer window than it truly can support.

Safer warmup handling:

```python
signals["bench_50d_above_200d"] = (sma_50 > sma_200).where(
    sma_50.notna() & sma_200.notna()
)
valid = signals.notna().all(axis=1)
signals = signals.loc[valid].astype(int)
```

Native validation handoff language:

```text
This package prepares native validation only. It does not claim the Strategy Book target was met.

The promoted API-estimated candidate uses the 200-day timing overlay and defensive proxy.
Conditional inverse and tactical ETF components were tested but did not appear in the promoted row.
```

Candidate interpretation pattern:

```text
Good:
- API-estimated nomination from 2007-06-26 through 2026-01-05.
- Requires native P123 Strategy Book validation before final claim.
- Warmup behavior must be checked natively.

Bad:
- Strategy Book achieved 20.68% CAGR and Sharpe 2.0 back to 2006.
- Timing rule is final because the local run passed.
- Inverse ETFs are part of the final candidate even though their promoted weight is 0%.
```

## Related

- `docs/solutions/workflow-issues/portfolio123-api-strategy-book-research-workflow-2026-05-22.md`
- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- `docs/plans/2026-05-22-003-feat-dynamic-p123-strategy-book-plan.md`
- `docs/ideation/2026-05-22-dynamic-p123-strategy-book-ideation.md`
- `scripts/p123_strategy_book_research.py`
- `iteration.md`

---

## Tags

#portfolio123 #strategy-book #timing #warmup #api-estimated #native-validation #trial-ledger #no-lookahead #algo-trading/portfolio123 #work/solutions #work/workflow-issues
