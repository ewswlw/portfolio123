---
created_at: 2026-05-22 13:27 America/New_York
date: 2026-05-22
topic: dynamic-p123-strategy-book
focus: "Combine market timing overlay, timed inverse ETFs, tactical ETF component, and expanded pre-2007 strategy discovery for a Portfolio123 Strategy Book targeting CAGR >20%, Sharpe >2.0, max drawdown better than -25%."
mode: repo-grounded
---

# Ideation: Dynamic Portfolio123 Strategy Book Push

## Grounding Context

The prior API-only Strategy Book research pipeline found that static allocation alone is probably not enough for the stricter goal. The synchronized Portfolio123 API-derived panel covered 45 components from 2006-06-22 to 2026-01-05: five qualifying simulated strategy streams and 40 pre-2007 ETFs, including inverse ETFs `SH`, `DOG`, and `PSQ`. A looser API-estimated candidate cleared CAGR >20% and Sharpe >1.6, but with max drawdown around -35%, so it was not adequate for the new risk target.

The strict static pass tested 22,565 allocation rows and found no allocation passing CAGR >20%, Sharpe >2.0, and max drawdown better than -25%. The nearest Sharpe/drawdown passes clustered around 12-14% CAGR with 15-20% inverse ETF exposure and 30-38% bond exposure. The best CAGR among drawdown-passing candidates reached about 16% CAGR with Sharpe around 1.8. This makes additional static weight nudging low value.

Portfolio123 supports the relevant native building blocks for a dynamic next iteration. The local P123 skill references technical rules such as `SMA`, `Close`, `Ret%Chg`, `ATRN`, `Volatility`, `HiValue`, and benchmark/ticker series such as `#Bench`, `$SPY`, `$QQQ`, and `$IWM`. It also lists macro constants such as `##FEDFUNDS`, `##UST10YR`, `##UST2YR`, `##CPI`, `##CORPBBBOAS`, and `##CORPBBOAS`. The official P123 moving-average documentation gives a native market timing example: `SMA(50,0,#Bench) > SMA(200,0,#Bench)`. The P123 strategy template also includes an ETF momentum rotation pattern with `Ret1Y%Chg > 0` as an absolute momentum filter.

All performance numbers from API/local work remain candidate research only. Final success must come from native Portfolio123 Strategy Book simulation, with component strategies validated as native simulations first. New P123 objects should use the project-required `codex_` prefix.

## Topic Axes

- Timing rules: binary or regime-based rules that change exposure using P123-native market, technical, or macro data.
- Timed inverse sleeve: inverse ETF exposure used conditionally rather than as a static drag.
- Tactical ETF component: a standalone ETF rotation/safety strategy that can enter the Strategy Book as a component.
- Expanded strategy discovery: finding more pre-2007 strategy streams with usable API/native return history.
- Validation discipline: preventing timing and discovery from becoming an overfit search.

## Ranked Ideas

### 1. Build A Binary Risk-On/Risk-Off Overlay For Every Risky Component

**Description:** Create a small family of pre-registered market timing overlays and apply them to the existing five strategy streams before testing any new allocation weights. The first-pass rules should be deliberately simple: benchmark above 200-day SMA, 50-day SMA above 200-day SMA, 12-month return positive, or benchmark drawdown from 1-year high below a threshold. The output is not one optimized timing rule; it is a comparison of a few named timing archetypes.

**Axis:** Timing rules

**Basis:** direct: the strict static pass found no winner after 22,565 trials, while P123 supports benchmark series timing through examples like `SMA(50,0,#Bench) > SMA(200,0,#Bench)`.

**Rationale:** The previous frontier shows a return/drawdown tradeoff: enough defense gets drawdown under control but cuts CAGR too far. A binary overlay attacks the actual failure mode by reducing crash exposure only when risk is elevated instead of permanently holding low-return hedges.

**Downsides:** Timing rules can overfit badly. We should pre-register no more than 4-6 variants and count each variant in `n_trials`.

**Confidence:** 86%

**Complexity:** Medium

**Status:** Unexplored

### 2. Convert Static Inverse Exposure Into A Conditional Bear Sleeve

**Description:** Replace the static inverse sleeve grid with a conditional bear sleeve that activates `SH`, `DOG`, and/or `PSQ` only when risk-off rules fire. The simplest version would allocate to inverse ETFs when SPY or `#Bench` is below trend and otherwise allocate that sleeve to the highest-ranked defensive ETF or cash-like ETF.

**Axis:** Timed inverse sleeve

**Basis:** direct: static inverse allocations helped strict drawdown and Sharpe but capped CAGR around 13-16%; the user explicitly wants inverse ETFs explored.

**Rationale:** The inverse ETFs are probably useful in the left tail but expensive during long bull markets. Timing them preserves the hedge's crisis role while reducing the long-run return drag that blocked the strict CAGR target.

**Downsides:** Inverse ETF timing can whipsaw in choppy markets. Native validation must inspect 2008, 2011, 2018 Q4, 2020, and 2022 separately.

**Confidence:** 82%

**Complexity:** Medium

**Status:** Unexplored

### 3. Create A `codex_` Tactical ETF Rotation Strategy As A Book Component

**Description:** Build a standalone ETF strategy that rotates among pre-2007 ETFs across risk-on, defensive, and inverse buckets. A conservative seed universe could include `SPY`, `QQQ`, `IWM`, `EFA`, `EEM`, `TLT`, `IEF`, `SHY`, `LQD`, `GLD`, `DBC`, `IYR`, `SH`, `DOG`, and `PSQ`, subject to P123 API history validation. Ranking can begin with 12-month momentum, 6-month momentum, and volatility penalty; buy rules can require positive absolute momentum except in explicitly defensive/inverse regimes.

**Axis:** Tactical ETF component

**Basis:** direct: the P123 strategy template lists an ETF momentum rotation template using `Ret1Y%Chg > 0`; external: P123 community material discusses ETF rotation and market timing as native use cases.

**Rationale:** Instead of treating ETFs as passive ballast, this creates a component whose job is to add positive return in risk-on periods and reduce book drawdown in risk-off periods. It can later be validated as a native simulated strategy, then added to the Strategy Book.

**Downsides:** ETF rotation can look great in-sample and fail after costs or whipsaw. Keep the first version sparse and interpretable.

**Confidence:** 84%

**Complexity:** High

**Status:** Unexplored

### 4. Expand Strategy Discovery Beyond The Current SIM Page Slice

**Description:** Search more categories, pages, and sortable views for simulated strategies with Sharpe >1 and inception before 2007, then push each discovered ID through the existing API feasibility classifier. Only strategies with clean `dailyPerf.ret` streams or native-simulation-compatible histories should enter the next panel.

**Axis:** Expanded strategy discovery

**Basis:** direct: the current strict search used only five qualifying strategy streams, and the no-winner report says the cheapest defensible next iteration is to expand the relevant strategy return-stream source.

**Rationale:** The strict target probably needs more alpha, not just better hedging. Additional low-correlation high-return streams are the most direct way to lift CAGR without pushing drawdown back above -25%.

**Downsides:** Browser discovery is unavoidable if P123 lacks a broad listing API. This must remain discovery-only until IDs are known, then switch back to API/native data.

**Confidence:** 88%

**Complexity:** Medium

**Status:** Unexplored

### 5. Add A Macro Stress Gate Using P123 FRED Constants

**Description:** Test a small set of macro gates that disable or reduce risky components during hostile macro regimes. Candidate families include inverted yield curve, widening credit spreads, rising inflation, and rising policy-rate pressure, using P123 constants such as `##UST10YR`, `##UST2YR`, `##CORPBBBOAS`, `##CORPBBOAS`, `##CPI`, and `##FEDFUNDS`.

**Axis:** Timing rules

**Basis:** direct: the P123 local reference lists those FRED-backed macro constants, and the ML trading skill emphasizes regime-dependent return processes.

**Rationale:** Technical timing catches price damage after it appears. Macro stress gates may help de-risk before or during slow-moving hostile regimes, especially 2008 and 2022-style periods.

**Downsides:** Monthly macro series can have publication lags and revision issues. We must confirm P123 point-in-time behavior and avoid using macro values that would not have been known at the rebalance date.

**Confidence:** 70%

**Complexity:** High

**Status:** Unexplored

### 6. Use A Two-Stage Candidate Funnel: Cheap API Estimates, Then Native Tier 1 Book Validation

**Description:** Keep the current API panel/ledger workflow for cheap screening, but add a formal promotion rule. A candidate only graduates to native P123 Strategy Book work if it passes API-estimated CAGR, Sharpe, max drawdown, PSR/DSR, crisis-window, and walk-forward gates. Once promoted, create native `codex_` component strategies and validate the final Strategy Book in P123.

**Axis:** Validation discipline

**Basis:** direct: the P123 skill requires native Strategy Book simulation for final claims and the prior workflow already established trial ledgers as the source of truth.

**Rationale:** Dynamic rules multiply the research search space. A promotion funnel keeps P123 credits and browser work focused on candidates that have already survived disciplined screening.

**Downsides:** API-estimated dynamic strategy behavior may not perfectly match native P123 simulations. Promotion should be treated as nomination, not validation.

**Confidence:** 90%

**Complexity:** Medium

**Status:** Unexplored

### 7. Pre-Register A Small Timing Ensemble Instead Of Picking One Winner

**Description:** Rather than selecting the single best timing rule, create a small ensemble where multiple simple risk-off signals vote. Example signal families: benchmark trend, benchmark momentum, realized volatility, drawdown-from-high, and macro stress. Exposure steps could be 100%, 60%, 30%, and defensive/inverse depending on the number of bearish votes.

**Axis:** Validation discipline

**Basis:** reasoned: timing rules are noisy and regime-dependent; an ensemble of simple independent signals is less brittle than choosing the best single full-sample rule after looking at results.

**Rationale:** This may preserve the key benefit of timing while reducing parameter fragility. It also gives a cleaner story to validate natively: the book responds to broad market stress, not one optimized threshold.

**Downsides:** More moving parts than a single binary rule. Needs strict limit on signal count and threshold choices.

**Confidence:** 78%

**Complexity:** High

**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Run a much larger static allocation search | The strict no-winner result already showed static weight nudging is low value and increases data-snooping pressure. |
| 2 | Add leveraged or leveraged inverse ETFs immediately | Out of current approved scope and likely to inflate tail risk; could be a later explicit expansion. |
| 3 | Use external non-P123 macro data directly in final rules | User asked for Portfolio123 data; external data can inform hypotheses but final rules should use P123-native data. |
| 4 | Optimize dozens of timing thresholds | Too overfit-prone; violates the ML trading skill's `n_trials` and data-snooping discipline. |
| 5 | Declare success from API-estimated dynamic backtests | Violates P123 validation hierarchy; API/local results can nominate, not prove. |
| 6 | Relax the 2007 inception requirement | Scope mismatch; the goal is explicitly to go back that far. |
| 7 | Treat inverse ETFs as always-on crash insurance | Already effectively tested through static sleeves and appears to cap CAGR too much. |

## Recommended Handoff

The strongest next `ce-brainstorm` seed is:

> Design a P123-native dynamic Strategy Book research campaign that combines more pre-2007 strategy discovery, a binary market timing overlay, conditional inverse ETF exposure, and a tactical ETF rotation component, with API-estimated screening first and native Strategy Book validation only for promoted candidates.

