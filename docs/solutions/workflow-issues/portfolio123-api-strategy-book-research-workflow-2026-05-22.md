---
title: Portfolio123 API-Only Strategy Book Research Workflow
created_at: 2026-05-22 13:15 America/New_York
date: 2026-05-22
category: workflow-issues
module: portfolio123-strategy-book-research
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Running Portfolio123 Strategy Book research where SIM-page access is allowed only for candidate ID discovery"
  - "Building API-derived strategy and ETF return panels for estimated candidate validation"
  - "Evaluating allocation searches that require honest n_trials accounting for PSR and DSR"
  - "Reporting strict no-winner outcomes without loosening CAGR, Sharpe, drawdown, PSR, or DSR gates"
related_components:
  - tooling
  - documentation
tags:
  - portfolio123
  - strategy-book
  - api-only
  - trial-ledger
  - inverse-etfs
  - no-winner-report
  - dsr
  - return-panel
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-22
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 API-Only Strategy Book Research Workflow."
---

# Portfolio123 API-Only Strategy Book Research Workflow

## Context

This workflow was captured after building an API-only Portfolio123 Strategy Book research pipeline for existing simulated strategies plus a broad ETF set, including inverse ETFs. The SIM page was used only as a discovery exception for strategy IDs and displayed filter fields. After candidate IDs were known, all return streams, ETF price histories, portfolio metrics, optimizer trials, and reports came from API-derived artifacts.

The run produced two useful outcomes:

- An API-estimated candidate that cleared CAGR >20% and Sharpe >1.6, but still required native Portfolio123 Strategy Book validation before any final claim.
- A stricter no-winner pass for CAGR >20%, Sharpe >2.0, and max drawdown better than -25%, showing that static weight tuning alone did not meet the stronger target under the approved constraints.

Session-history search was requested during compounding, but the `ce-sessions` discovery pipeline could not run because this Windows machine has no WSL distribution installed. This document is therefore grounded in the committed plan, script, iteration log, and existing P123 solution docs rather than prior-session extraction.

## Guidance

Use the SIM page only for candidate discovery:

- strategy ID
- strategy name
- displayed Sharpe used for the initial filter
- inception date used for the initial filter
- inclusion or exclusion reason codes

Do not use browser-table performance as final research data. Once IDs are known, switch to the API.

For simulated strategy return streams, prefer the strategy API response's `dailyPerf.ret` series when available. Classify strategies conservatively before optimization:

```text
tradable_stream  -> clean API-derived return stream exists
metadata_only    -> metadata exists but no clean return stream
api_failed       -> endpoint, auth, or data failure
```

Only `tradable_stream` strategies enter the optimizer. Do not synthesize strategy returns from summary CAGR, drawdown, annual return, holdings, or transaction counts.

For ETF validation, use Portfolio123 API `data_prices`. Include inverse ETFs only when they are in scope, pre-2007, and have usable API history. Treat inverse ETFs as long positions in inverse products, not as short positions. Keep leveraged and leveraged-inverse ETFs out of scope unless a separate plan approves them.

Build the return panel by joining all eligible strategy and ETF return streams by date, then dropping rows with any missing component return. Do not backfill missing pre-inception returns, fill them with zero, or allow an asset to behave like cash before it existed. Always report the synchronized start date, end date, row count, and component count.

Pre-register deterministic allocation families before running optimization. The approved ladder for this run was:

```text
equal_weight
inverse_volatility
HRP
constrained ensemble / sleeve grids
strict risk-control grid for stronger gates
```

Every tested allocation increments `n_trials`, including deterministic grid rows. The trial ledger is the primary artifact. Reports are summaries of the ledger, not independent sources of truth.

When targets are not met, write a first-class no-winner report. The report should name:

- the exact gates
- total trials
- nearest misses
- which gates failed
- why thresholds were not loosened
- the cheapest defensible next iteration

Label all results as API-estimated candidate research. Native Portfolio123 Strategy Book simulation remains Tier 1 and is required before final performance claims.

## Why This Matters

This workflow avoids two common Strategy Book research failures:

1. Mixing browser-discovered summary values into performance claims.
2. Optimizing allocation weights until an attractive metric appears without recording the search breadth.

The clean return-stream rule prevents false precision. If a strategy lacks API-derived daily returns, it cannot be safely synchronized with ETF returns.

The missing-row rule prevents survivorship-like panel errors. Without it, a pre-inception ETF can accidentally contribute zero returns and reduce volatility as if it were a cash sleeve.

The trial ledger protects DSR accounting. A deterministic grid is still a search over many hypotheses, so future readers need the exact `n_trials` count and every allocation row.

The strict no-winner result is actionable. In this run, 22,565 strict trials produced no allocation that cleared CAGR >20%, Sharpe >2.0, and max drawdown better than -25% under static long-only weights, non-leveraged ETFs, max 25% component weight, and max 35% inverse sleeve. That says the next iteration needs different ingredients or a separately approved dynamic risk-control model, not more static weight nudging.

## When To Apply

Apply this workflow when researching Portfolio123 Strategy Book candidates using:

- existing simulated strategies from the user's account
- SIM-page discovery followed by API-only performance work
- ETF sleeves, including inverse ETFs
- static allocation grids
- PSR, DSR, or other multiple-testing-aware validation
- API-estimated research artifacts that may later need native P123 Tier 1 validation

Also apply it when deciding whether a candidate is ready for native Strategy Book validation. API-estimated results can nominate candidates, but they do not replace native P123 Strategy Book output.

## Examples

Discovery-only SIM page use:

```text
Allowed:
- strategy_id
- strategy name
- displayed Sharpe used for initial filter
- inception date used for initial filter

Not allowed for final metrics:
- browser-table CAGR
- browser-table drawdown
- browser-table Sharpe as final validation
```

Return-stream feasibility lanes:

```text
1934030 -> tradable_stream -> dailyPerf.ret available
1934014 -> tradable_stream -> dailyPerf.ret available
metadata-only candidate -> exclude from optimizer
api_failed candidate -> exclude from optimizer and preserve reason
```

ETF validation pattern:

```text
Use data_prices for SPY, QQQ, SHY, IEF, TLT, GLD, and related ETF families.
Include inverse ETFs such as SH, DOG, and PSQ if pre-2007 and API history is usable.
Exclude leveraged and leveraged-inverse ETFs unless the user approves a new scope.
```

Return panel rule:

```text
Good:
- join all return streams by date
- drop rows with any missing component return
- report synchronized start/end dates and component count

Bad:
- fill missing ETF history with 0
- treat missing pre-inception periods as cash
- synthesize strategy returns from summary CAGR/drawdown
```

Artifact naming examples:

```text
p123-output/candidate_strategy_discovery_YYYYMMDD.csv
p123-output/strategy_return_feasibility_YYYYMMDD.json
p123-output/etf_universe_candidates_YYYYMMDD.csv
p123-output/return_panel_YYYYMMDD.csv
p123-output/trial_ledger_YYYYMMDD.csv
p123-output/strict_trial_ledger_YYYYMMDD_strict_sh2_dd25.csv
p123-output/api_estimated_strategy_book_report_YYYYMMDD.md
p123-output/strict_no_winner_report_YYYYMMDD_strict_sh2_dd25.md
```

## Related

- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-browser-login-encrypted-credentials-2026-05-22.md`
- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`
- `docs/plans/2026-05-22-002-feat-api-only-p123-strategy-book-plan.md`
- `iteration.md`
- `scripts/p123_strategy_book_research.py`

---

## Tags

#portfolio123 #strategy-book #api-only #trial-ledger #inverse-etfs #no-winner-report #dsr #return-panel #algo-trading/portfolio123 #work/solutions #work/workflow-issues
