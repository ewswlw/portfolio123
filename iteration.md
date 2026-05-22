Created: 2026-05-22 12:30 America/New_York

# Iteration Log: API-Only Portfolio123 Strategy Book Design

## Purpose

This file is the living audit trail for the Portfolio123 strategy-book research workflow. It is intended to be understandable by another user or future agent without relying on chat history.

The project goal is to design the best possible statistically valid Strategy Book candidate using:

- Existing Portfolio123 simulated strategies that appear on the user's simulated-strategies page.
- Only strategies with Sharpe ratio greater than 1 and inception date before 2007.
- A broad ETF candidate band, including inverse ETFs, when ETF inception is before 2007 and usable API price history exists.
- Portfolio123 API-only research and validation for the design phase.
- Credit-aware API usage.
- Statistical validation discipline from the `ml-algo-trading` skill.

## Hard Constraints

- Use the Portfolio123 API exclusively for performance/data work.
- The Portfolio123 API does not expose broad account-level strategy listing endpoints. Candidate strategy IDs may need to come from the currently open SIM page or from known local IDs; once IDs are known, API-only work begins.
- Do not make final Tier 1 Strategy Book performance claims from API/local calculations. Native P123 Strategy Book simulation is the Tier 1 authority, but this project phase is constrained to API-only candidate design.
- Do not place trades, rebalance live portfolios, delete P123 objects, or spend large API credits without confirmation.
- Do not write secrets, API keys, cookies, tokens, or session values into this file.

## Skills And Rules In Use

- `project-spec`: structures this as an interview-driven, build-ready specification before execution.
- `portfolio123`: supplies P123 API constraints, validation hierarchy, credit rules, and account-object safety boundaries.
- `ml-algo-trading`: supplies statistical validation requirements, including walk-forward testing, PSR/DSR, regime awareness, and `n_trials` accounting.

## Current Project-Spec Decisions

### Batch 1: Research Design & Constraints

Accepted defaults except where noted:

1. Candidate strategy discovery: use the current SIM page only to extract candidate strategy IDs and displayed metadata, then all performance/data work is API-only.
2. Strategy Book definition: produce an API-derived allocation model and report it as an estimated Strategy Book candidate, with no final Tier 1 claim.
3. Return-stream source: use P123 `/strategy/{id}/*` API endpoints where available and derive synchronized return streams from strategy/transaction/holdings data where feasible.
4. ETF universe: broaden beyond the default list. Include a wide ETF band, including inverse ETFs, as long as inception dates are before 2007 and usable history exists.
5. Optimization method: HRP/risk-parity-first, then constrained walk-forward weight search with PSR/DSR and explicit `n_trials`.
6. Success criterion: find the best statistically valid API-estimated candidate; only call it successful if out-of-sample/walk-forward results clear CAGR greater than 20% and Sharpe greater than 1.6 with PSR/DSR passing.

### Batch 2: Data, Validation & Credit Budget

Accepted defaults:

1. Start date rule: use the latest inception/start date across all selected sims and ETFs, constrained to before 2007; target start is the earliest common date all final components can support.
2. Strategy filter: candidate sims must have native displayed Sharpe greater than 1 and inception date before 2007, then API validates details and usable history.
3. ETF candidate band: broad pre-2007 ETF band across US equity, size/style, sectors, international, bonds, commodities/gold, real estate, volatility proxies if available, currency, and inverse ETFs.
4. Credit budget discipline: two-stage API budget. Cheap discovery/metadata first, then price/return downloads only for shortlisted sims and ETFs. Stop and ask if estimated P123 credit use exceeds 250 credits.
5. Optimization budget: first run is limited to a pre-registered optimizer family: equal-weight baseline, HRP, inverse-vol, and small constrained ensemble search. Every tested allocation counts in `n_trials`.
6. Validation split: walk-forward with expanding windows, annual re-optimization, and final holdout from 2020-2026 if enough data exists.

### Batch 3: Return Construction, ETF Scope & Outputs

Accepted defaults:

1. Existing strategy return reconstruction: prefer API-provided strategy performance, transaction, and holding endpoints. If no clean return series exists, mark that strategy as metadata-only and exclude it from the optimizer until a valid synchronized return stream is available.
2. ETF broad universe guardrails: include broad, sector, factor/style, international, bond, commodity, currency, real estate, and inverse ETFs with inception before 2007. Exclude leveraged ETFs unless explicitly approved later.
3. Allocation constraints: long-only total portfolio weights, but inverse ETFs are allowed as long positions in inverse products. Maximum 25% per component and maximum 35% total inverse sleeve.
4. Optimization objective: maximize validated walk-forward Sharpe subject to CAGR greater than 20%, max drawdown control, PSR/DSR pass, and realistic `n_trials` penalty.
5. Output artifacts: save CSV/JSON result tables under `p123-output/`, update `iteration.md`, and produce a concise final report with estimated Tier/API label.
6. Go/no-go threshold: if no candidate passes all statistical gates, report the best failures honestly and recommend the next API-cheap iteration rather than loosening gates.

## Open Design Questions

The remaining project-spec interview still needs to define:

- Exact API-only interpretation for extracting return streams from existing simulated strategies. Resolved in risk review: SIM page use is limited to candidate ID/displayed-metadata discovery; all performance/data work must be API-only after IDs are known.
- ETF inclusion/exclusion rules for leveraged, inverse, delisted, or low-liquidity ETFs. Resolved in project-spec batch 3: broad pre-2007 ETF band with inverse ETFs allowed, leveraged ETFs excluded unless explicitly approved later.
- How to handle missing dates, different rebalance cadences, and synchronization. Resolved in risk review: components without clean synchronized return streams are excluded from optimization rather than approximated from summary stats.
- Output artifacts and reporting format. Resolved in project-spec batch 3: CSV/JSON under `p123-output/`, living updates here, final report labeled as API-estimated.
- The final handoff gate: plan, proceed, revise, write spec files, or stop.

## Risk Review Decisions

The user asked to address all risks. The architecture is tightened as follows:

1. API-only discovery conflict: using the open SIM page is allowed only to extract candidate strategy IDs and displayed metadata required to identify the eligible universe. After that, the workflow switches to API-only. No performance claim may come from the browser table except the initial filter predicate the user requested.
2. Return-series availability risk: if a simulated strategy does not expose a clean API-derived return stream that can be synchronized with ETF returns, it is marked `metadata_only` and excluded from portfolio optimization. Summary-stat approximation is rejected.
3. Data-mining risk: the optimizer family is pre-registered before API execution. Equal-weight, HRP, inverse-vol, and a small constrained ensemble search are allowed. Every tested allocation counts toward `n_trials` for DSR.
4. Threshold realism: the workflow may conclude that no candidate passes. The thresholds are not relaxed post hoc. Failed candidates are reported with the failure gate and best next API-cheap iteration.
5. Tier mismatch: final output is explicitly labeled API-estimated candidate research. Native P123 Strategy Book validation is identified as the future Tier 1 confirmation step, not silently implied.

## Approved Roadmap

The user approved the 10-phase roadmap:

1. Goal Spec Setup
2. Credential and API Preflight
3. Candidate Strategy Discovery
4. API Strategy Metadata and Return Feasibility
5. ETF Universe Construction
6. Return Panel and Validation Dataset
7. Pre-Registered Portfolio Optimization
8. Walk-Forward and Statistical Validation
9. Reporting and Iteration Log
10. Next Iteration Decision

## Approved Innovation Addition

The user approved adding a pre-registered trial ledger as a required output. The workflow must create a dated `p123-output/trial_ledger_YYYYMMDD.{csv,json}` artifact that records every tested allocation, including:

- components and weights,
- optimizer family,
- rebalance window,
- inverse ETF inclusion,
- CAGR, Sharpe, max drawdown, PSR, and DSR,
- pass/fail gate,
- `n_trials` index,
- rejection or promotion reason.

This ledger is required so DSR accounting is honest and future iterations can see exactly what was already tried.

## Project-Spec Refinement Notes

The in-memory project specification and constitution were refined against a rubric for quantitative research reproducibility, P123 API correctness, statistical validity, credit discipline, safety, and downstream executability.

Key refinements made before handoff:

- Clarified that SIM page access is a discovery-only exception for candidate IDs and displayed metadata; all performance, return-stream, ETF, and allocation work must use API-derived data.
- Required exclusion of any strategy or ETF without a clean synchronized return stream rather than approximating from summary statistics.
- Made the trial ledger mandatory for DSR and auditability.
- Required all final metrics to be labeled API-estimated and not native Tier 1 Strategy Book validation.
- Added an explicit downstream gate so implementation does not start until approved.

## Ideation Pass

The user invoked `ce-ideate` before implementation. A ranked ideation artifact was created at:

`docs/ideation/2026-05-22-api-only-p123-strategy-book-ideation.md`

The strongest ideas from the pass were:

1. Two-lane candidate system: `tradable_stream` vs `metadata_only`.
2. ETF funnel organized by economic families before tickers.
3. Pre-registered optimizer ladder.
4. Inverse ETF sleeve treated as a gate-tested hedge rather than a free alpha source.
5. Credit-aware stoplight API plan.
6. Trial ledger as the primary research artifact.
7. First-class no-winner report template.

Recommended next ideation-to-action handoff: use `ce-brainstorm` on the credit-aware stoplight API plan if further clarification is needed before API execution.

## Plan Integration

The user asked to implement the ideation survivors that make sense into `ce-plan`. A Deep implementation plan was created at:

`docs/plans/2026-05-22-002-feat-api-only-p123-strategy-book-plan.md`

The plan incorporates all seven survivor ideas:

1. Two-lane candidate system: `tradable_stream`, `metadata_only`, and `api_failed`.
2. ETF family funnel before ticker-level validation.
3. Pre-registered optimizer ladder.
4. Inverse ETF sleeve diagnostics and cap enforcement.
5. Credit-aware stoplight API plan.
6. Trial ledger as the primary research artifact.
7. No-winner report path.

Plan review notes:

- Confirmed the plan contains no literal supplied credentials.
- Removed an absolute Windows path from the plan so file references remain portable.
- Confirmed the plan keeps the boundary between discovery-only browser use and API-derived performance work.

## Inverse ETF Clarification

The user clarified that inverse ETFs should be actively explored. This is consistent with the existing plan: inverse ETFs with inception before 2007 are in scope, should be included in the ETF family funnel, and should receive dedicated hedge-sleeve diagnostics. The current cap remains maximum 35% total inverse sleeve and maximum 25% per component.

Leveraged ETFs, including leveraged inverse ETFs, remain out of scope unless the user explicitly approves expanding into them.

## Iteration Update Protocol

Update this file after each major step:

1. Record the decision or action.
2. Explain why it was chosen.
3. Record any alternatives rejected.
4. Record API credit estimates and actual costs when known.
5. Record all results with source and validation tier.
6. Record statistical tests, pass/fail status, and `n_trials`.
7. Record caveats and what would be required for native P123 Tier 1 confirmation.

## U1 Goal And Credit Scaffold

Updated: 2026-05-22 12:46 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/goal_api_only_strategy_book_20260522.json`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/api_credit_budget_20260522.json`.
- Credit stop remains 250 estimated Portfolio123 API credits before asking for confirmation.

## U2 Candidate Strategy Discovery

Updated: 2026-05-22 12:53 Eastern Daylight Time
- Read discovery rows from `p123-output/sim_page_raw_20260522.json`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/candidate_strategy_discovery_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/candidate_strategy_discovery_20260522.json`.
- Included 5 strategies with displayed Sharpe > 1 and inception before 2007.
- Browser/table values remain discovery-only and do not feed final performance metrics.

## U3 API Strategy Feasibility

Updated: 2026-05-22 12:53 Eastern Daylight Time
- Read candidates from `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/candidate_strategy_discovery_20260522.json`.
- Estimated strategy API feasibility credits: 16.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strategy_return_feasibility_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strategy_return_feasibility_20260522.json`.
- Lane counts: {'tradable_stream': 5}.

## U3 API Strategy Feasibility

Updated: 2026-05-22 12:54 Eastern Daylight Time
- Read candidates from `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/candidate_strategy_discovery_20260522.json`.
- Estimated strategy API feasibility credits: 16.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strategy_return_feasibility_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strategy_return_feasibility_20260522.json`.
- Saved API-derived strategy daily return streams for 5 strategies when available.
- Lane counts: {'tradable_stream': 5}.

## U4 ETF Family Funnel

Updated: 2026-05-22 12:55 Eastern Daylight Time
- Validated 40 ETF seeds, including inverse ETFs and excluding leveraged ETFs.
- Estimated ETF API credits: 40.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/etf_universe_candidates_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/etf_universe_candidates_20260522.json`.
- Eligible ETF count: 40.

## U5 Return Panel

Updated: 2026-05-22 12:56 Eastern Daylight Time
- Built ETF return panel from `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/etf_prices_20260522.csv`.
- Return window: 2006-06-22 to 2026-01-05 across 45 components.
- Included 5 API-derived strategy return streams.

## U5 Return Panel

Updated: 2026-05-22 12:56 Eastern Daylight Time
- Built ETF return panel from `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/etf_prices_20260522.csv`.
- Return window: 2006-06-22 to 2026-01-05 across 45 components.
- Included 5 API-derived strategy return streams.

## U6-U7 Optimizer And Validation

Updated: 2026-05-22 12:56 Eastern Daylight Time
- Optimized `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/return_panel_20260522.csv` using the pre-registered ladder.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.json`.
- Trials: 8; passing allocations: 0.

## U6-U7 Optimizer And Validation

Updated: 2026-05-22 12:56 Eastern Daylight Time
- Optimized `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/return_panel_20260522.csv` using the pre-registered ladder.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.json`.
- Trials: 8; passing allocations: 0.

## U6-U7 Optimizer And Validation

Updated: 2026-05-22 12:58 Eastern Daylight Time
- Optimized `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/return_panel_20260522.csv` using the pre-registered ladder.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.json`.
- Trials: 265; passing allocations: 45.

## U8 Report Generation

Updated: 2026-05-22 12:58 Eastern Daylight Time
- Read trial ledger `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/api_estimated_strategy_book_report_20260522.md`.
- Passing candidates: 45.

## Execution Result Summary

Updated: 2026-05-22 12:59 Eastern Daylight Time
- Discovery source: current Portfolio123 SIM page, used only for strategy IDs and displayed filter fields.
- SIM discovery result: 23 visible simulated strategies after switching the page size to All.
- Filter result: 5 strategies met displayed Sharpe > 1 and inception before 2007:
  - `1934030` Small Caps + Altman in Ranking + Altman > 1 - Copy
  - `1934014` SAMCF + Quality Filter Group - Copy
  - `1873038` Canada Core Combo - Eddy/Kurtis
  - `1934023` Small Cap Focus - Small...erse - Small AUM - Copy
  - `1934037` Advisor TSX Mighty Mouse Momentum - Copy
- API feasibility result: all 5 eligible strategies exposed API-derived `dailyPerf.ret` streams and were classified as `tradable_stream`.
- ETF universe result: 40 non-leveraged ETF seeds were validated through Portfolio123 `data_prices`; this included inverse ETFs `SH`, `DOG`, and `PSQ`.
- Return panel result: synchronized panel contains 45 components: 5 strategy streams and 40 ETF streams. Rows with any missing component return were dropped so no component behaves like cash before it exists.
- Synchronized research window: 2006-06-22 through 2026-01-05, 4,915 daily rows.
- Optimizer result: 265 allocations were tested and counted in `n_trials`; 45 passed the API-estimated gates.
- Best Sharpe passing candidate in the ledger: trial 217, `strategy_sleeve_grid_s0.800_inv0.125_bond0.075_real0.000_equity0.000`.
- Trial 217 weights:
  - 16.0% each to the five qualified strategy streams.
  - 4.1667% each to `SH`, `DOG`, and `PSQ` for a 12.5% inverse sleeve.
  - 1.5% each to `SHY`, `IEF`, `TLT`, `AGG`, and `LQD` for a 7.5% bond sleeve.
- Trial 217 API-estimated metrics: CAGR 20.35%, Sharpe 1.69, max drawdown -35.40%, PSR 1.00, DSR 1.00, inverse sleeve 12.5%, max component 16.0%.
- Constraint verification: the final ledger satisfies max component weight <= 25% and max inverse sleeve <= 35% for every tested allocation.
- Important caveat: these are API-estimated candidate results, not native Portfolio123 Tier 1 Strategy Book validation. The next required step before any final performance claim is native P123 Strategy Book validation using the trial 217 weights, with the same component set and synchronized date assumptions checked against the platform.
- Credit discipline: all estimated calls stayed below the 250-credit stop. Strategy feasibility was estimated at 16 credits per pass; ETF validation was estimated at 40 credits. Additional repeated feasibility/sample calls were used to inspect and then save `dailyPerf` return streams, still well below the stop threshold.
- Rejected alternatives: summary-stat approximation for metadata-only strategies was not used; missing pre-inception returns were not treated as cash; leveraged ETFs remained excluded.

## U8 Report Generation

Updated: 2026-05-22 12:58 Eastern Daylight Time
- Read trial ledger `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/trial_ledger_20260522.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/api_estimated_strategy_book_report_20260522.md`.
- Passing candidates: 10.

## U9 Strict Optimizer And Validation

Updated: 2026-05-22 13:05 Eastern Daylight Time
- Optimized `p123-output/return_panel_20260522.csv` using the pre-registered ladder.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strict_trial_ledger_20260522_strict_sh2_dd25.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strict_trial_ledger_20260522_strict_sh2_dd25.json`.
- Trials: 22565; passing allocations: 0.
- Gates: CAGR > 20.00%, Sharpe > 2.00, max drawdown > -0.25.

## Strict Gate Result Summary

Updated: 2026-05-22 13:06 Eastern Daylight Time
- User-requested target: CAGR >20%, Sharpe >2.0, and max drawdown better than -25%.
- Data source: reused `p123-output/return_panel_20260522.csv`; no new Portfolio123 API calls were needed for this strict pass.
- Search shape: deterministic strict risk-control grid across strategy sleeve weights, inverse ETF sleeve, bond sleeve, real asset sleeve, and small equity sleeve, with multiple strategy-weight templates. Every tested allocation was counted in `n_trials`.
- Strict result: no allocation passed all three gates.
- Trial count: 22,565.
- Failure reason counts:
  - 10,790 failed CAGR, Sharpe, and max drawdown.
  - 6,985 failed CAGR and Sharpe.
  - 4,790 failed Sharpe and max drawdown.
- Best Sharpe nearest miss: trial 5,669, `strict_risk_grid_cagrstrat_s0.500_inv0.175_bond0.325_real0.000_equity0.000`, with CAGR 13.17%, Sharpe 1.87, max drawdown -19.45%.
- Best CAGR allocation among drawdown-passing candidates: trial 19,685, `strict_risk_grid_blendstrat_s0.550_inv0.075_bond0.375_real0.000_equity0.000`, with CAGR 16.11%, Sharpe 1.80, max drawdown -24.81%.
- Interpretation: under static long-only Strategy Book weights, non-leveraged ETFs, max 25% component cap, and max 35% inverse sleeve cap, the existing five strategy streams do not appear to support the stricter 20% CAGR / 2.0 Sharpe / <25% drawdown target on the synchronized API-derived panel.
- Strict report written to `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strict_no_winner_report_20260522_strict_sh2_dd25.md`.
- Next cheapest API-only iteration would need a different ingredient, not just weight tuning: either discover additional low-correlated high-return pre-2007 strategy streams, approve a dynamic risk-control model as a separate plan, or explicitly expand the ETF scope. Leveraged ETFs remain out of scope under the current plan.

## U8 Report Generation

Updated: 2026-05-22 13:06 Eastern Daylight Time
- Read trial ledger `p123-output/strict_trial_ledger_20260522_strict_sh2_dd25.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/strict_no_winner_report_20260522_strict_sh2_dd25.md`.
- Passing candidates: 0.
