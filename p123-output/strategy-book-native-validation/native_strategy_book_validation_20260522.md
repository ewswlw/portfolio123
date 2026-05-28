---
title: "Native Strategy Book Validation: Trial 386 Replication"
created_at: 2026-05-22 15:27 America/New_York
tags:
  - algo-trading/portfolio123
  - algo-trading/strategy-books
  - work/native-validation
  - work/generated-artifacts
created: 2026-05-22
updated: 2026-05-28
description: "Generated native Portfolio123 Strategy Book validation artifact for Native Strategy Book Validation: Trial 386 Replication."
---

# Native Strategy Book Validation: Trial 386 Replication

## Status

Outcome: `native_tier1_rejected`

Initial capability work was limited to authenticated platform inspection and unsaved wizard-state probing. After user approval to continue beyond the 5-run budget, all five native timed components were created, renamed with the required `codex_dynamic_*` prefix, and added to a native simulated Strategy Book with a raw `SHY` ETF sleeve.

The native platform supports the exact component-level route, but the reliable run path bypassed the naming dialog and initially saved the pilot component under P123's default clone name instead of the required `codex_dynamic_*` name. The pilot was then renamed through P123's Svelte component-properties endpoint after matching the platform's request headers.

Final native Tier 1 result: the Strategy Book did not meet the strict goal. Native annualized return was `15.88%`, Sharpe was `1.22`, and max drawdown was `-20.11%`. Drawdown passed the less-than-25% drawdown gate, but CAGR and Sharpe failed.

## Candidate Being Replicated

- Trial: `386`
- Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: `20.68%`
- API-estimated Sharpe: `2.00`
- API-estimated max drawdown: `-12.81%`
- Corrected local timing window start: `2007-06-26`
- Native target: CAGR > 20%, Sharpe > 2, max drawdown better than -25%

Primary allocation intended for native Strategy Book:

| Component | Weight | Intended behavior |
|---|---:|---|
| `codex_dynamic_1873038_timed_200d` | 16% | Source strategy when risk-on, `SHY` when risk-off |
| `codex_dynamic_1934014_timed_200d` | 16% | Source strategy when risk-on, `SHY` when risk-off |
| `codex_dynamic_1934023_timed_200d` | 16% | Source strategy when risk-on, `SHY` when risk-off |
| `codex_dynamic_1934030_timed_200d` | 16% | Source strategy when risk-on, `SHY` when risk-off |
| `codex_dynamic_1934037_timed_200d` | 16% | Source strategy when risk-on, `SHY` when risk-off |
| `SHY` ETF sleeve | 20% | Always-on defensive proxy |

## Capability Gate

| Area inspected | Native observation | Classification |
|---|---|---|
| New Simulated Book wizard | General, Assets, Rebalance, and Period tabs expose static assets, fixed-weight allocation, rebalance cadence, tolerances, exposure, and period controls. No visible book-level timing, formula, conditional allocation, or hedge tab was found. | `blocked` for book-level exact timing |
| Source simulated strategy trading system | Trading System view exposes Buy, Sell, Stop Loss, Hedge, Period, and Review tabs. Existing source inspected had `Hedge / Market Timing DISABLED`. | `available` for component-level timing |
| Hedge tab on unsaved cloned simulation | Enabling Hedge reveals `Go To Cash` and `Choose Position`. The hedge vehicle chooser includes `Treasury 1-3 Year (SHY:USA)`. | `available` for SHY vehicle selection |
| Exact substitution pattern | Exact behavior appears implementable by adding a risk-on Buy rule, risk-off Sell rule, and a long `SHY` hedge during risk-off. | `available_unrun` |
| Simulated strategy save/run path | New simulated strategy clone exposes visible `Run Simulation`, but that link did not fire through the Browser wrapper. Direct navigation to `port_sim_go.jsp?<timestamp>` successfully ran the currently configured simulated-strategy wizard session. | `available_with_naming_caveat` |
| Simulated book save/run path | Direct navigation to `port_sim_go.jsp?<timestamp>` failed for the simulated-book wizard with `Session trading system changed`. The working path was the page's own `BookSimulButton`, which opened the native properties modal; after naming and saving, P123 ran the book and redirected to the summary page. | `available_via_native_button_and_modal` |
| Naming path | The direct run endpoint skipped the Svelte component-properties naming dialog, so the first pilot object was saved with P123's default clone name. Browser clicks did not surface editable modal fields, but the authenticated `POST /spr/user/compProps` endpoint successfully renamed the object when sent with `ANGULAR_REQ: 1`, `SVELTE_REQ: 1`, JSON content, and the full component properties payload. | `available_via_authenticated_endpoint` |

## Exact Component Pattern Identified

For each copied source strategy:

- Add Buy rule:
  `Close(0,#bench) > SMA(200,0,#bench)`
- Add Sell rule:
  `Close(0,#bench) <= SMA(200,0,#bench)`
- Enable Hedge.
- Select `Choose Position`.
- Choose hedge vehicle:
  `Treasury 1-3 Year (SHY:USA)`
- Set hedge ratio:
  `100%`
- Use long hedge transaction type.
- Add Hedge Entry rule:
  `Close(0,#bench) <= SMA(200,0,#bench)`
- Add Hedge Exit rule:
  `Close(0,#bench) > SMA(200,0,#bench)`

Reason this is the exact route: the added Buy/Sell rules force the stock component out of equities during risk-off, while the Hedge tab holds long `SHY` during the same risk-off state. This is closer to the promoted local component behavior than a simple `Go To Cash` timing rule.

Native acceptance result: P123 accepted the formulas and settings for all five component simulations. The exact hedge setting used by this pass was `100% of Current Holdings`, not `100% of Total Equity`.

## Source Strategy Mapping

| Source ID | Name | Period | Benchmark | Universe | Ranking system | Native annualized return | Native Sharpe | Native max drawdown |
|---:|---|---|---|---|---|---:|---:|---:|
| `1873038` | `Canada Core Combo - Eddy/Kurtis` | `01/01/06 - 01/06/26` | `S&P/TSX Capped Composite (XIC:CAN)` | `Toronto Stock Exchange` | `Core Combo Canada - Copy` | `21.70%` | `1.17` | `-42.44%` |
| `1934014` | `SAMCF + Quality Filter Group - Copy` | `01/01/06 - 04/20/26` | `S&P 500 (SPY:USA)` | `No OTC Exchange` | `Small and Micro Cap Focus` | `31.30%` | `1.29` | `-50.90%` |
| `1934023` | `Small Cap Focus - Small Cap Universe - Small AUM - Copy` | `01/01/06 - 04/20/26` | `Russell 2000 (IWM:USA)` | `No OTC Exchange + min 10 mil min vol` | `Small and Micro Cap Focus` | `30.46%` | `1.11` | `-65.68%` |
| `1934030` | `Small Caps + Altman in Ranking + Altman > 1 - Copy` | `01/01/06 - 04/20/26` | `S&P 500 (SPY:USA)` | `No OTC Exchange` | `Small and Micro Cap Focus + Altman - Copy(2)` | `34.19%` | `1.37` | `-52.96%` |
| `1934037` | `Advisor TSX Mighty Mouse Momentum - Copy` | `01/01/06 - 04/20/26` | `S&P/TSX Capped Composite (XIC:CAN)` | `Toronto Stock Exchange` | `Canada Momentum V-G-LV - Copy` | `18.31%` | `1.01` | `-40.59%` |

## Run Ledger

Initial approved native run budget: `5`

Expanded native run budget: approved by user after the first report. Exact route requires at least `6` runs if each component must be simulated before final Strategy Book construction.

| Item | Required for exact route? | Run status | Count |
|---|---:|---|---:|
| Create/run `codex_dynamic_1873038_timed_200d` | Yes | `run_completed_and_renamed` | 1 |
| Create/run timed source `1934014` pilot | Yes | `run_completed_and_renamed` | 1 |
| Create/run `codex_dynamic_1934023_timed_200d` | Yes | `run_completed_and_renamed` | 1 |
| Create/run `codex_dynamic_1934030_timed_200d` | Yes | `run_completed_and_renamed` | 1 |
| Create/run `codex_dynamic_1934037_timed_200d` | Yes | `run_completed_and_renamed` | 1 |
| Create/run final `codex_dynamic_strategy_book_candidate` | Yes | `run_completed` | 1 |

Runs spent in this native replication execution: `6`

The user approved continuing beyond the original 5-run cap before the component batch was completed.

## Pilot Native Component Result

| Field | Value |
|---|---|
| Source ID | `1934014` |
| Intended object name | `codex_dynamic_1934014_timed_200d` |
| Initial platform name | `SAMCF + Quality Filter Group - Copy(2)` |
| Current platform name | `codex_dynamic_1934014_timed_200d` |
| New object ID | `1943514` |
| URL | `https://www.portfolio123.com/port_summary.jsp?portid=1943514` |
| Period | `01/01/06 - 04/20/26` |
| Annualized return | `22.41%` |
| Sharpe ratio | `1.18` |
| Max drawdown | `-27.50%` |
| Correlation with benchmark | `0.48` |
| Run status | `native_component_run_completed` |

Pilot settings used:

- Added Buy rule:
  `Close(0,#bench) > SMA(200,0,#bench)`
- Added Sell rule:
  `Close(0,#bench) <= SMA(200,0,#bench)`
- Enabled Hedge / Market Timing.
- Hedge vehicle:
  `Treasury 1-3 Year (SHY:USA)`
- Hedge ratio:
  `100% of Current Holdings`
- Hedge entry rule:
  `Close(0,#bench) <= SMA(200,0,#bench)`
- Hedge exit rule:
  `Close(0,#bench) > SMA(200,0,#bench)`

## Native Component Results

All component results below are native P123 Simulated Strategy results, Tier 2. They are not final Strategy Book results, but they explain why the final book underperformed the API-estimated candidate.

| Source ID | Native object | Port ID | Period | Annualized return | Sharpe | Max drawdown | Status |
|---:|---|---:|---|---:|---:|---:|---|
| `1873038` | `codex_dynamic_1873038_timed_200d` | `1943550` | `01/01/06 - 01/06/26` | `17.52%` | `1.19` | `-19.37%` | `run_completed_and_renamed` |
| `1934014` | `codex_dynamic_1934014_timed_200d` | `1943514` | `01/01/06 - 04/20/26` | `22.41%` | `1.18` | `-27.50%` | `run_completed_and_renamed` |
| `1934023` | `codex_dynamic_1934023_timed_200d` | `1943547` | `01/01/06 - 04/20/26` | `12.27%` | `0.58` | `-38.33%` | `run_completed_and_renamed` |
| `1934030` | `codex_dynamic_1934030_timed_200d` | `1943548` | `01/01/06 - 04/20/26` | `26.88%` | `1.28` | `-31.32%` | `run_completed_and_renamed` |
| `1934037` | `codex_dynamic_1934037_timed_200d` | `1943549` | `01/01/06 - 04/20/26` | `14.35%` | `0.98` | `-20.42%` | `run_completed_and_renamed` |

## Native Strategy Book Result

| Field | Value |
|---|---|
| Native object name | `codex_dynamic_strategy_book_candidate` |
| Port ID | `1943551` |
| URL | `https://www.portfolio123.com/port_summary.jsp?portid=1943551` |
| Period | `12/30/05 - 01/06/26` |
| Assets | `6` |
| Rebalance | `Every 4 Weeks` |
| Sizing method | `Static Weight` |
| Benchmark | `S&P 500 (SPY:USA)` |
| Total return | `1,814.56%` |
| Annualized return | `15.88%` |
| Sharpe ratio | `1.22` |
| Max drawdown | `-20.11%` |
| Correlation with S&P 500 | `0.58` |
| Native Tier 1 gate result | `failed_cagr_and_sharpe` |

Book allocation configured on the native review page before run:

| Asset | Type | Target allocation |
|---|---|---:|
| `codex_dynamic_1934014_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1873038_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934023_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934030_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934037_timed_200d` | `SIM` | `16.0%` |
| `iShares 1-3 Year Treasury Bond ETF (SHY)` | `ETF` | `20.0%` |

Gate comparison:

| Gate | Target | Native result | Pass? |
|---|---:|---:|---|
| CAGR / annualized return | `>20%` | `15.88%` | No |
| Sharpe ratio | `>2.0` | `1.22` | No |
| Max drawdown | better than `-25%` | `-20.11%` | Yes |

## Replication Status Matrix

| Object or step | Status | Reason |
|---|---|---|
| Book-level timing | `blocked` | No visible book-level timing/formula/conditional allocation surface in new Simulated Book wizard. |
| Component-level timing | `available_and_run` | Hedge tab accepted timing rules and `SHY` vehicle selection on cloned simulations. |
| `codex_dynamic_1873038_timed_200d` | `created_run_and_renamed` | Native object `1943550` was created, run, and renamed. |
| `codex_dynamic_1934014_timed_200d` | `created_run_and_renamed` | Native object `1943514` was created and run with timing settings, initially saved as `SAMCF + Quality Filter Group - Copy(2)`, then renamed through the authenticated Svelte component-properties endpoint. |
| `codex_dynamic_1934023_timed_200d` | `created_run_and_renamed` | Native object `1943547` was created, run, and renamed. |
| `codex_dynamic_1934030_timed_200d` | `created_run_and_renamed` | Native object `1943548` was created, run, and renamed. |
| `codex_dynamic_1934037_timed_200d` | `created_run_and_renamed` | Native object `1943549` was created, run, and renamed. |
| Final Strategy Book | `created_and_run` | Native object `1943551` was created as `codex_dynamic_strategy_book_candidate` and run. |
| Native Tier 1 result | `failed` | Annualized return `15.88%` and Sharpe `1.22` failed the strict gates, while max drawdown `-20.11%` passed. |

## Rename Endpoint Finding

The Browser wrapper could click the `Edit Details` / component-properties controls, but editable modal fields did not surface reliably. The Svelte bundle revealed the save endpoint:

`POST https://www.portfolio123.com/spr/user/compProps`

The successful rename used the project-local encrypted secrets to establish an authenticated web session, then posted the component properties payload with these non-secret headers:

- `Content-Type: application/json`
- `ANGULAR_REQ: 1`
- `SVELTE_REQ: 1`
- `X-Requested-With: XMLHttpRequest`
- `Referer: https://www.portfolio123.com/port_summary.jsp?portid=1943514`

No secret values, cookies, or session tokens were written to this file. The current platform name was verified on the summary page after the rename.

## Interpretation

The API-estimated trial `386` candidate did not survive native Strategy Book validation. The main discrepancy came from the native component implementations: several timed component simulations had much lower Sharpe and/or CAGR than the API-estimated timed return streams, and the final book's raw `SHY` sleeve reduced drawdown but did not create enough return or Sharpe lift.

The most actionable next native iteration is to test a corrected hedge-sizing variant: use `100% of Total Equity / Includes cash` instead of `100% of Current Holdings` for the component hedge, because the intended behavior is full defensive substitution into `SHY` when risk-off. That would be a new native variant, not this exact run.

---

## Tags

#algo-trading/portfolio123 #algo-trading/strategy-books #work/native-validation #work/generated-artifacts
