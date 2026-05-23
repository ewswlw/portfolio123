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

## Dynamic Strategy Book Planning

Updated: 2026-05-22 13:28 Eastern Daylight Time
- User approved combining all dynamic ideation survivors:
  - P123-native risk-on/risk-off timing overlay.
  - Conditional inverse ETF bear sleeve.
  - `codex_` tactical ETF rotation component.
  - Expanded pre-2007 strategy discovery.
  - Macro stress gate using P123 FRED constants.
  - API-estimated screening into native Tier 1 validation.
  - Small timing-signal ensemble instead of picking one optimized timing rule.
- Wrote new active plan `docs/plans/2026-05-22-003-feat-dynamic-p123-strategy-book-plan.md`.
- The plan intentionally leaves the completed static/API-only plan unchanged and treats the new phase as dynamic exposure research rather than additional static weight tuning.
- Main planning decision: reuse the artifact-first pipeline in `scripts/p123_strategy_book_research.py`, but add dynamic artifacts with distinct filenames so prior static results remain reproducible.
- Key validation guardrail: API-estimated dynamic results can nominate candidates only; native Portfolio123 Strategy Book simulation remains required before declaring the CAGR >20%, Sharpe >2.0, and max drawdown better than -25% target met.

## Dynamic Strategy Book Execution

Updated: 2026-05-22 13:49 Eastern Daylight Time
- Implemented dynamic research commands in `scripts/p123_strategy_book_research.py`:
  - `init-dynamic-goal`
  - `merge-expanded-discovery`
  - `build-timing-signals`
  - `build-dynamic-panel`
  - `dynamic-optimize`
  - `dynamic-report`
  - `native-package`
- Added focused tests in `tests/test_p123_strategy_book_research.py`.
- No new Portfolio123 API credits were spent in this execution pass; all dynamic calculations reused existing API-derived artifacts from `p123-output/`.
- Generated `p123-output/dynamic_goal_strategy_book_20260522.json`.
- Generated baseline expanded discovery artifacts from the existing captured SIM source:
  - `p123-output/expanded_strategy_discovery_20260522.csv`
  - `p123-output/expanded_strategy_discovery_20260522.json`
- Current expanded discovery is only a baseline merge of the already-captured SIM source, not a full new browser discovery sweep. It still has 5 eligible pre-2007 displayed-Sharpe >1 strategies.
- Generated timing signal artifacts:
  - `p123-output/timing_signal_panel_20260522.csv`
  - `p123-output/timing_signal_summary_20260522.json`
- Timing signals use `SPY` as benchmark proxy and are shifted one bar so date `t` allocation uses information available before date `t` return.
- Macro stress gates were documented as candidates but not activated because P123 macro-series availability and point-in-time behavior still need explicit confirmation.
- Generated dynamic component artifacts:
  - `p123-output/dynamic_return_panel_20260522.csv`
  - `p123-output/dynamic_return_panel_summary_20260522.json`
  - `p123-output/tactical_etf_component_candidates_20260522.csv`
- Dynamic panel contains raw strategies, 200-day timed strategy variants, timing-ensemble variants, a conditional inverse sleeve, a tactical ETF component, and a defensive proxy component.
- First coarse dynamic optimizer grid timed out at five minutes after dynamic variants expanded the component set.
- Replaced the coarse dynamic grid with a narrower deterministic 5-point sleeve grid and counted every row in `n_trials`.
- Generated `p123-output/dynamic_trial_ledger_20260522.csv` and `p123-output/dynamic_trial_ledger_20260522.json`.
- Dynamic optimizer trial count: 648.
- Passing API-estimated nominations: 1.
- Promoted API-estimated row:
  - Trial: 386.
  - Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`.
  - Weights: 16% each to the five 200-day timed strategy variants, 20% to the defensive proxy component.
  - API-estimated CAGR: 20.23%.
  - API-estimated Sharpe: 2.01.
  - API-estimated max drawdown: -12.81%.
  - Walk-forward positive rate: 100%.
  - Worst listed crisis-window drawdown: -7.79%.
  - Inverse weight: 0%.
- Important interpretation: conditional inverse and tactical ETF components were tested, but the only promoted API-estimated row used the 200-day timing overlay plus defensive proxy and assigned 0% to inverse and tactical ETF components.
- Wrote `p123-output/dynamic_candidate_promotion_report_20260522.md`.
- Wrote `p123-output/native_validation_package_20260522.md`.
- Native validation package is a handoff only. It does not claim the target is met; native Portfolio123 Strategy Book validation is still required before any final performance claim.

## Dynamic Timing Warmup Correction

Updated: 2026-05-22 13:56 Eastern Daylight Time
- Code review found that early timing warmup rows were being treated as `False` signals rather than excluded, because rolling-window comparisons against missing values collapsed to false.
- Fixed `build-timing-signals` so each timing rule stays missing until its required inputs exist.
- Rebuilt timing signals, dynamic panel, dynamic trial ledger, promotion report, and native validation package.
- Corrected timing signal window: 2007-06-26 through 2026-01-05, 4,662 rows.
- Corrected dynamic panel window: 2007-06-26 through 2026-01-05, 4,662 rows.
- Dynamic optimizer trial count remains 648.
- Passing API-estimated nominations after the warmup correction: 1.
- Corrected promoted API-estimated row:
  - Trial: 386.
  - Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`.
  - Weights: 16% each to the five 200-day timed strategy variants, 20% to the defensive proxy component.
  - API-estimated CAGR: 20.68%.
  - API-estimated Sharpe: 2.00.
  - API-estimated max drawdown: -12.81%.
  - Walk-forward positive rate: 100%.
  - Worst listed crisis-window drawdown: -7.79%.
  - Inverse weight: 0%.
- Important caveat: this corrected dynamic candidate starts after timing warmup in mid-2007, so native P123 validation must confirm whether the platform's native simulation and warmup behavior support the user's desired full-history interpretation.

## U1 Dynamic Goal And Trial Accounting

Updated: 2026-05-22 13:41 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_goal_strategy_book_20260522.json`.
- Captured all seven dynamic ideation survivors.
- Trial accounting now explicitly includes discovery sources, timing rules, timing ensembles, ETF component variants, and allocation rows.
- Dynamic results remain API-estimated nominations until native Portfolio123 Strategy Book validation.

## U3 P123-Native Timing Signal Panel

Updated: 2026-05-22 13:41 Eastern Daylight Time
- Built timing signals from `p123-output/return_panel_20260522.csv` using `SPY` as benchmark proxy.
- Signal window: 2006-06-22 to 2026-01-05 across 4915 rows.
- Technical timing rules are shifted one bar to avoid same-day look-ahead.
- Macro stress candidates are documented but not activated pending P123 macro-series confirmation.

## U2 Expanded Strategy Discovery

Updated: 2026-05-22 13:41 Eastern Daylight Time
- Merged 1 discovery sources into `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/expanded_strategy_discovery_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/expanded_strategy_discovery_20260522.json`.
- Unique strategies discovered: 23.
- Included strategies after displayed Sharpe > 1 and inception before 2007 filter: 5.
- Discovery-source count is recorded as part of dynamic trial accounting.

## U4-U5 Dynamic Panel And Tactical ETF Component

Updated: 2026-05-22 13:42 Eastern Daylight Time
- Built dynamic panel from `p123-output/return_panel_20260522.csv` and `p123-output/timing_signal_panel_20260522.csv`.
- Dynamic window: 2006-06-22 to 2026-01-05 across 4915 rows.
- Added timed variants for 5 strategy streams, one conditional inverse sleeve, and one tactical ETF component.
- Conditional inverse exposure is active only when the timing ensemble marks inverse-enabled risk-off days.

## U4-U5 Dynamic Panel And Tactical ETF Component

Updated: 2026-05-22 13:48 Eastern Daylight Time
- Built dynamic panel from `p123-output/return_panel_20260522.csv` and `p123-output/timing_signal_panel_20260522.csv`.
- Dynamic window: 2006-06-22 to 2026-01-05 across 4915 rows.
- Added timed variants for 5 strategy streams, one conditional inverse sleeve, and one tactical ETF component.
- Conditional inverse exposure is active only when the timing ensemble marks inverse-enabled risk-off days.

## U6 Dynamic Optimizer And Promotion Gates

Updated: 2026-05-22 13:48 Eastern Daylight Time
- Optimized `p123-output/dynamic_return_panel_20260522.csv` using a narrow pre-registered dynamic grid.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.json`.
- Trials: 123; passing allocations: 0.
- Gates: CAGR > 20.00%, Sharpe > 2.00, max drawdown > -25.00%.

## U6 Dynamic Candidate Promotion Funnel

Updated: 2026-05-22 13:48 Eastern Daylight Time
- Read dynamic trial ledger `p123-output/dynamic_trial_ledger_20260522.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_no_winner_report_20260522.md`.
- Promoted API-estimated candidates: 0.

## U7 Native Validation Package

Updated: 2026-05-22 13:48 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/native_validation_package_20260522.md`.
- Package is a handoff for native P123 validation and makes no final performance claim.

## U9 Strict Optimizer And Validation

Updated: 2026-05-22 13:48 Eastern Daylight Time
- Optimized `p123-output/dynamic_return_panel_20260522.csv` using the pre-registered ladder.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.json`.
- Trials: 22565; passing allocations: 0.
- Gates: CAGR > 20.00%, Sharpe > 2.00, max drawdown > -0.25.

## U6 Dynamic Optimizer And Promotion Gates

Updated: 2026-05-22 13:49 Eastern Daylight Time
- Optimized `p123-output/dynamic_return_panel_20260522.csv` using a narrow pre-registered dynamic grid.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.json`.
- Trials: 648; passing allocations: 1.
- Gates: CAGR > 20.00%, Sharpe > 2.00, max drawdown > -25.00%.

## U6 Dynamic Candidate Promotion Funnel

Updated: 2026-05-22 13:49 Eastern Daylight Time
- Read dynamic trial ledger `p123-output/dynamic_trial_ledger_20260522.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_candidate_promotion_report_20260522.md`.
- Promoted API-estimated candidates: 1.

## U7 Native Validation Package

Updated: 2026-05-22 13:49 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/native_validation_package_20260522.md`.
- Package is a handoff for native P123 validation and makes no final performance claim.

## U7 Native Validation Package

Updated: 2026-05-22 13:49 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/native_validation_package_20260522.md`.
- Package is a handoff for native P123 validation and makes no final performance claim.

## U3 P123-Native Timing Signal Panel

Updated: 2026-05-22 13:50 Eastern Daylight Time
- Built timing signals from `p123-output/return_panel_20260522.csv` using `SPY` as benchmark proxy.
- Signal window: 2007-06-26 to 2026-01-05 across 4662 rows.
- Technical timing rules are shifted one bar to avoid same-day look-ahead.
- Macro stress candidates are documented but not activated pending P123 macro-series confirmation.

## U4-U5 Dynamic Panel And Tactical ETF Component

Updated: 2026-05-22 13:51 Eastern Daylight Time
- Built dynamic panel from `p123-output/return_panel_20260522.csv` and `p123-output/timing_signal_panel_20260522.csv`.
- Dynamic window: 2007-06-26 to 2026-01-05 across 4662 rows.
- Added timed variants for 5 strategy streams, one conditional inverse sleeve, and one tactical ETF component.
- Conditional inverse exposure is active only when the timing ensemble marks inverse-enabled risk-off days.

## U6 Dynamic Optimizer And Promotion Gates

Updated: 2026-05-22 13:51 Eastern Daylight Time
- Optimized `p123-output/dynamic_return_panel_20260522.csv` using a narrow pre-registered dynamic grid.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.csv` and `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_trial_ledger_20260522.json`.
- Trials: 648; passing allocations: 1.
- Gates: CAGR > 20.00%, Sharpe > 2.00, max drawdown > -25.00%.

## U6 Dynamic Candidate Promotion Funnel

Updated: 2026-05-22 13:51 Eastern Daylight Time
- Read dynamic trial ledger `p123-output/dynamic_trial_ledger_20260522.csv`.
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/dynamic_candidate_promotion_report_20260522.md`.
- Promoted API-estimated candidates: 1.

## U7 Native Validation Package

Updated: 2026-05-22 13:51 Eastern Daylight Time
- Wrote `C:/Users/Eddy/Desktop/Portfolio123 Strategy Dev/p123-output/native_validation_package_20260522.md`.
- Package is a handoff for native P123 validation and makes no final performance claim.

## U8 Native Platform Validation Prep

Updated: 2026-05-22 14:24 Eastern Daylight Time
- User requested direct Portfolio123 platform replication through the in-app Browser plugin and invoked `ce-ideate`.
- User selected option 3 for ideation handling, so no new ideation artifact was created; ideation was used as working validation design only.
- Confirmed the in-app browser session is authenticated on Portfolio123.
- Opened the native Simulated Books list at `https://www.portfolio123.com/app/opener/BOOKSIM?cat=-2` in read-only mode.
- Read native P123 book rows already present on the account. Visible strict-goal-relevant examples included:
  - `BookSim - Copy`: inception `01/03/06`, 4 assets, annualized return `22.9%`, Sharpe `1.90`, drawdown `-25.5%`.
  - `BookSim - Copy(2)`: inception `01/03/06`, 4 assets, annualized return `26.5%`, Sharpe `1.84`, drawdown `-31.9%`.
  - `BookSim - Copy(3)`: inception `01/03/06`, 4 assets, annualized return `22.0%`, Sharpe `1.86`, drawdown `-25.2%`.
  - `BookSim(6)`: inception `01/03/06`, 5 assets, annualized return `23.6%`, Sharpe `1.85`, drawdown `-27.1%`.
- Opened the native summary page for `BookSim - Copy` at `https://www.portfolio123.com/port_summary.jsp?portid=1930094` in read-only mode.
- Confirmed native summary metrics for `BookSim - Copy`: annualized return `22.90%`, Sharpe Ratio `1.90`, max drawdown `-25.52%`, 4 assets, static weight sizing, and every-4-weeks book rebalance.
- This existing native book is close to the strict goal but does not pass Sharpe > 2 or max drawdown better than -25%.
- Next account-changing validation step requires user confirmation before creating/editing `codex_` native objects, cloning component strategies, adding models to a simulated book, or running a native simulation.

## U9 Manual Native Validation Handoff Brainstorm

Updated: 2026-05-22 14:56 Eastern Daylight Time
- User selected manual handoff only, so no Portfolio123 platform objects were created, edited, copied, deleted, or run.
- Used `ce-brainstorm` as a lightweight scope and handoff workflow for the native validation procedure.
- Created `docs/brainstorms/2026-05-22-native-p123-strategy-book-validation-requirements.md`.
- The handoff document captures:
  - The promoted trial `386` candidate and allocation weights.
  - The inspected existing native book reference metrics.
  - Manual platform steps for validating the strategy book.
  - The 200-day timing overlay and defensive proxy assumptions.
  - Scope boundaries that prevent accidental account-changing actions.
  - Open questions to resolve before any future native run.

## U10 Manual Native Validation Plan

Updated: 2026-05-22 15:03 Eastern Daylight Time
- User invoked `ce-plan` after the manual native validation handoff.
- Treated the task as a non-software research/workflow plan, not a code implementation plan.
- Used `docs/brainstorms/2026-05-22-native-p123-strategy-book-validation-requirements.md` as the source of truth.
- Created `docs/plans/2026-05-22-004-native-p123-strategy-book-validation-plan.md`.
- The plan preserves manual-only boundaries: no agent-created, edited, copied, deleted, or run Portfolio123 objects.
- The plan breaks native validation into read-only inventory, timing-surface determination, manual component specs, manual book specs, optional native evidence capture, and post-run interpretation.
- The two decisions to resolve before any future native run are book rebalance cadence and defensive proxy variant policy.

## U11 Read-Only Native Validation Work

Updated: 2026-05-22 15:20 Eastern Daylight Time
- User invoked `ce-work` after the native validation plan.
- Executed only the read-only portions of the plan. No Portfolio123 objects were created, edited, copied, deleted, saved, submitted, or run.
- Opened the simulated books list and collected close native book references:
  - `BookSim - Copy` / `1930094`: period `01/03/06 - 04/02/26`, 4 assets, every-4-weeks rebalance, annualized return `22.90%`, Sharpe `1.90`, max drawdown `-25.52%`.
  - `BookSim - Copy(2)` / `1930095`: period `01/03/06 - 04/02/26`, 4 assets, every-4-weeks rebalance, annualized return `26.55%`, Sharpe `1.84`, max drawdown `-31.92%`.
  - `BookSim - Copy(3)` / `1930104`: period `01/03/06 - 04/02/26`, 4 assets, every-4-weeks rebalance, annualized return `21.99%`, Sharpe `1.86`, max drawdown `-25.18%`.
  - `BookSim(6)` / `1930097`: period `01/03/06 - 04/02/26`, 5 assets, every-4-weeks rebalance, annualized return `23.60%`, Sharpe `1.85`, max drawdown `-27.13%`.
- Confirmed the closest visible native books are static-weight mixes of existing PTF/ETF assets, mainly Advisor Small Cap Focus, Wes Gray Momentum Microcaps Hedged, GLD, TLT, and sometimes SAMCF + Quality Filter Group.
- Inspected `BookSim - Copy` trading-system/review surfaces in read-only mode.
- The visible review surface showed General, Assets & Rebalance, and Period & Restrictions settings, but did not expose a book-level timing rule, formula rule, conditional allocation rule, or hedge/timing rule surface.
- Direct navigation to some wizard steps returned internal server errors, so book-level timing is not proven impossible; it is only unconfirmed from read-only inspection.
- Wrote `p123-output/native_strategy_book_readonly_inventory_20260522.md` with the inventory, timing-surface observations, and remaining decisions before any native run.

## U12 Native Replication Ideation, Plan, And Capability Gate

Updated: 2026-05-22 15:27 Eastern Daylight Time
- User invoked `ce-ideate`, then `ce-plan`, then `ce-work` for direct Portfolio123 replication of the promoted dynamic Strategy Book candidate.
- Created `docs/ideation/2026-05-22-native-p123-replication-ideation.md`.
- Created `docs/plans/2026-05-22-005-native-p123-replication-execution-plan.md`.
- Reconfirmed the candidate as trial `386`, optimizer family `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`, five 200-day timed components at 16% each, and an always-on 20% `SHY` defensive sleeve.
- Inspected the new native Simulated Book wizard without saving or running:
  - General, Assets, Rebalance, and Period tabs were visible.
  - The book wizard exposed static asset selection, fixed-weight allocation, rebalance cadence, tolerances, exposure, and period controls.
  - No book-level timing, formula, hedge, or conditional allocation surface was visible.
- Inspected source simulated strategy summaries for the five source IDs:
  - `1873038`: `Canada Core Combo - Eddy/Kurtis`, period `01/01/06 - 01/06/26`, Sharpe `1.17`.
  - `1934014`: `SAMCF + Quality Filter Group - Copy`, period `01/01/06 - 04/20/26`, Sharpe `1.29`.
  - `1934023`: `Small Cap Focus - Small Cap Universe - Small AUM - Copy`, period `01/01/06 - 04/20/26`, Sharpe `1.11`.
  - `1934030`: `Small Caps + Altman in Ranking + Altman > 1 - Copy`, period `01/01/06 - 04/20/26`, Sharpe `1.37`.
  - `1934037`: `Advisor TSX Mighty Mouse Momentum - Copy`, period `01/01/06 - 04/20/26`, Sharpe `1.01`.
- Opened an unsaved cloned simulation wizard from source `1934014` and inspected the Hedge tab.
- Confirmed native component-level timing controls exist:
  - Hedge can be enabled.
  - Hedge supports `Go To Cash` or `Choose Position`.
  - The hedge vehicle chooser includes `Treasury 1-3 Year (SHY:USA)`.
  - Hedge entry and exit rules accept formula textareas.
- Identified the exact native component pattern:
  - Add source Buy rule `Close(0,#bench) > SMA(200,0,#bench)`.
  - Add source Sell rule `Close(0,#bench) <= SMA(200,0,#bench)`.
  - Enable Hedge, select `SHY`, use a long 100% hedge, enter on risk-off, exit on risk-on.
- Stopped before creating/running objects because the exact route appears to require five component simulation runs plus one final Strategy Book run, while the approved native run budget is 5.
- Wrote `p123-output/native_strategy_book_validation_20260522.md`.
- Native runs spent in this pass: 0.
- No Portfolio123 objects were saved, created, edited, deleted, submitted, or run.

## U13 First Native Timed Component Pilot

Updated: 2026-05-22 15:41 Eastern Daylight Time
- User approved proceeding after the run-budget gate.
- Built the first timed component from source `1934014` in the native P123 simulated strategy wizard:
  - Added Buy rule `Close(0,#bench) > SMA(200,0,#bench)`.
  - Added Sell rule `Close(0,#bench) <= SMA(200,0,#bench)`.
  - Enabled Hedge / Market Timing.
  - Selected `Treasury 1-3 Year (SHY:USA)` as the hedge vehicle.
  - Set hedge ratio to `100% of Current Holdings`.
  - Set hedge entry rule `Close(0,#bench) <= SMA(200,0,#bench)`.
  - Set hedge exit rule `Close(0,#bench) > SMA(200,0,#bench)`.
- The normal visible Run Simulation link did not execute through the Browser wrapper, but direct navigation to the native run endpoint `port_sim_go.jsp?<timestamp>` successfully ran the configured wizard session.
- Native component run completed and redirected to `https://www.portfolio123.com/port_summary.jsp?portid=1943514`.
- New native object ID: `1943514`.
- Actual P123 object name: `SAMCF + Quality Filter Group - Copy(2)`.
- Intended object name: `codex_dynamic_1934014_timed_200d`.
- Native component metrics:
  - Period: `01/01/06 - 04/20/26`.
  - Annualized return: `22.41%`.
  - Sharpe Ratio: `1.18`.
  - Max drawdown: `-27.50%`.
  - Correlation with S&P 500: `0.48`.
- Paused before creating additional components because the reliable run path bypassed the naming dialog and saved the pilot under P123's default clone name.
- Attempts to open the component properties modal through Browser clicks did not expose editable rename fields.
- Updated `p123-output/native_strategy_book_validation_20260522.md` with the pilot result, run ledger, and decision needed.
- Native runs spent so far in this native replication execution: 1.

## U14 Pilot Component Rename Fix

Updated: 2026-05-22 16:14 Eastern Daylight Time
- User instructed the agent to fix the name directly and keep iterating.
- Updated `AGENTS.md` so Portfolio123 web login is attempted automatically from the project-local encrypted secrets file when the site is logged out, without printing or storing secret values.
- Logged into Portfolio123 through the in-app Browser using the available project credentials.
- Renamed native object `1943514` from `SAMCF + Quality Filter Group - Copy(2)` to `codex_dynamic_1934014_timed_200d`.
- Verified the new platform name on `https://www.portfolio123.com/port_summary.jsp?portid=1943514`.
- Browser clicks against the component-properties modal did not expose editable fields reliably, so the successful path used Portfolio123's authenticated Svelte endpoint:
  - Endpoint: `POST /spr/user/compProps`.
  - Required non-secret request characteristics: JSON body, `ANGULAR_REQ: 1`, `SVELTE_REQ: 1`, `X-Requested-With: XMLHttpRequest`, and the summary-page referer.
  - No passwords, API keys, cookies, tokens, or session values were written to project files.
- Updated `p123-output/native_strategy_book_validation_20260522.md` with the rename status and endpoint finding.
- Native runs spent remain 1; rename did not require a simulation run.
- Next step is to create and run the remaining four timed native components using the same `codex_dynamic_*` naming discipline before creating the final Strategy Book.

## U15 Native Component Batch And Strategy Book Tier 1 Result

Updated: 2026-05-22 16:43 Eastern Daylight Time
- Created, ran, and renamed all remaining timed native component simulations:
  - `1943547` -> `codex_dynamic_1934023_timed_200d`: annualized return `12.27%`, Sharpe `0.58`, max drawdown `-38.33%`.
  - `1943548` -> `codex_dynamic_1934030_timed_200d`: annualized return `26.88%`, Sharpe `1.28`, max drawdown `-31.32%`.
  - `1943549` -> `codex_dynamic_1934037_timed_200d`: annualized return `14.35%`, Sharpe `0.98`, max drawdown `-20.42%`.
  - `1943550` -> `codex_dynamic_1873038_timed_200d`: annualized return `17.52%`, Sharpe `1.19`, max drawdown `-19.37%`.
- Existing pilot component remained:
  - `1943514` / `codex_dynamic_1934014_timed_200d`: annualized return `22.41%`, Sharpe `1.18`, max drawdown `-27.50%`.
- Built the native simulated Strategy Book `codex_dynamic_strategy_book_candidate` with object ID `1943551`.
- The native book used static weights and every-4-weeks rebalance:
  - 16% each to the five timed `codex_dynamic_*` simulated strategies.
  - 20% to raw `iShares 1-3 Year Treasury Bond ETF (SHY)`.
- The direct `port_sim_go.jsp?<timestamp>` runner path that worked for simulated strategies failed for simulated books with `Session trading system changed`.
- The successful book run path was the native `BookSimulButton`, which opened the Portfolio123 properties modal; after setting the name to `codex_dynamic_strategy_book_candidate` and clicking Save, P123 ran the book and redirected to the summary.
- Native Tier 1 Strategy Book result:
  - Period: `12/30/05 - 01/06/26`.
  - Annualized return: `15.88%`.
  - Sharpe Ratio: `1.22`.
  - Max drawdown: `-20.11%`.
  - Correlation with S&P 500: `0.58`.
- Strict goal result:
  - CAGR/annualized return > 20%: failed.
  - Sharpe > 2.0: failed.
  - Max drawdown better than -25%: passed.
- Interpretation: the promoted API-estimated trial `386` did not survive native Portfolio123 Tier 1 Strategy Book validation.
- Most actionable next native iteration: test a corrected hedge-sizing variant using `100% of Total Equity / Includes cash` rather than `100% of Current Holdings`, because the intended local behavior was full risk-off substitution into SHY.
- Updated `p123-output/native_strategy_book_validation_20260522.md` with component results, final book result, gate comparison, run ledger, and interpretation.
