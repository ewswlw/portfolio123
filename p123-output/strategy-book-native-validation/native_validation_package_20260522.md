---
title: "Native Portfolio123 Validation Package"
created_at: 2026-05-22 13:51 Eastern Daylight Time
tags:
  - algo-trading/portfolio123
  - algo-trading/strategy-books
  - work/native-validation
  - work/generated-artifacts
created: 2026-05-22
updated: 2026-05-28
description: "Generated native Portfolio123 Strategy Book validation artifact for Native Portfolio123 Validation Package."
---

# Native Portfolio123 Validation Package

This package prepares native validation only. It does not claim the Strategy Book target was met.

Source ledger: `p123-output/dynamic_trial_ledger_20260522.csv`

## Candidate To Validate

- Trial: `386`
- Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: 20.68%
- API-estimated Sharpe: 2.00
- API-estimated max drawdown: -12.81%

## Proposed Native Objects

- `codex_dynamic_strategy_book_candidate`
- `codex_dynamic_200d_timing_overlay_components`

## Allocation Weights

- `defensive_proxy_component`: 20.00%
- `strategy_1873038_timed_200d`: 16.00%
- `strategy_1934014_timed_200d`: 16.00%
- `strategy_1934023_timed_200d`: 16.00%
- `strategy_1934030_timed_200d`: 16.00%
- `strategy_1934037_timed_200d`: 16.00%

## Dynamic Component Note

The promoted API-estimated candidate uses the 200-day timing overlay and defensive proxy. Conditional inverse and tactical ETF components were tested but did not appear in the promoted row.

## Confirmation Gate

Ask the user before creating or modifying any native Portfolio123 object or running credit-heavy native validation.

---

## Tags

#algo-trading/portfolio123 #algo-trading/strategy-books #work/native-validation #work/generated-artifacts
