---
title: "Ideation: API-Only Portfolio123 Strategy Book Candidate Design"
created_at: 2026-05-22 12:45 America/New_York
date: 2026-05-22
topic: api-only-p123-strategy-book
focus: "Stronger ideas for API-only Portfolio123 Strategy Book candidate design"
mode: repo-grounded
tags:
  - algo-trading/portfolio123
  - work/ideation
created: 2026-05-22
updated: 2026-05-28
description: "Portfolio123 ideation note evaluating strategy research options for Ideation: API-Only Portfolio123 Strategy Book Candidate Design."
---

# Ideation: API-Only Portfolio123 Strategy Book Candidate Design

## Grounding Context

The active project-spec defines an API-only Portfolio123 research workflow. The goal is to design an API-estimated Strategy Book candidate from simulated strategies with displayed Sharpe ratio greater than 1 and inception before 2007, plus a broad pre-2007 ETF universe that can include inverse ETFs. The workflow must optimize Portfolio123 credits, use API-derived performance/data after SIM-page ID discovery, and avoid final Tier 1 claims until native P123 Strategy Book validation.

Relevant project rules:

- `AGENTS.md` says P123 has no broad account-level listing endpoint for some objects, and IDs may need to be discovered through the browser UI before API calls.
- `iteration.md` states SIM-page use is discovery-only; performance and allocation must be API-derived.
- `iteration.md` requires a pre-registered trial ledger for every tested allocation.
- The Portfolio123 skill warns that local/API estimates must not be reported as final native Strategy Book performance.
- The ML algo-trading skill requires walk-forward validation, PSR/DSR, regime awareness, and honest `n_trials`.

External grounding:

- HRP is attractive here because it avoids full covariance inversion and does not depend on fragile expected-return forecasts.
- DSR/PSR are relevant because searching across allocations, ETF sets, inverse sleeves, and constraints creates multiple-testing pressure.
- Recent Codex docs did not surface an official `/goal` command reference, so the project-spec treats `/goal` as a structured goal artifact unless a local command/tool appears during implementation.

## Topic Axes

- Candidate discovery and return-stream feasibility
- ETF universe breadth and safety
- Portfolio optimization and validation
- Credit efficiency and iteration control
- Auditability and handoff

## Ranked Ideas

### 1. Two-Lane Candidate System: `tradable_stream` vs `metadata_only`

**Description:** Split every discovered simulated strategy into one of two lanes before optimization. `tradable_stream` candidates have an API-derived, synchronized return stream and can enter the optimizer. `metadata_only` candidates pass the SIM-page filter but lack sufficient API return data and are preserved in the report without entering allocation math.

**Axis:** Candidate discovery and return-stream feasibility

**Basis:** direct: `iteration.md` says components without clean synchronized return streams are excluded from optimization rather than approximated from summary stats.

**Rationale:** This prevents the optimizer from quietly mixing real return streams with inferred or summary-stat proxies. It also makes the failure mode useful: the user can see whether a promising strategy was excluded because of data access rather than poor performance.

**Downsides:** The final candidate pool may become much smaller than the SIM-page filter suggests.

**Confidence:** 95%

**Complexity:** Low

**Status:** Unexplored

### 2. ETF Funnel with Families, Not Just Tickers

**Description:** Build the ETF universe as families first, then tickers: broad equity, size/style, sectors, international, rates duration, credit, gold/commodities, real estate, currency, and inverse hedges. Pick pre-2007 representatives from each family only after API price-history checks confirm common-window availability.

**Axis:** ETF universe breadth and safety

**Basis:** direct: the user explicitly widened the ETF band to include inverse ETFs with inception before 2007; `iteration.md` requires broad ETF categories and usable API history.

**Rationale:** A family-first funnel avoids overloading the first API pass with a random ticker zoo, while still preserving breadth. It also lets the report say which economic sleeves were missing because no pre-2007 ETF survived.

**Downsides:** Requires a maintained seed list and may miss obscure ETFs unless the list is expanded later.

**Confidence:** 90%

**Complexity:** Medium

**Status:** Unexplored

### 3. Pre-Registered Optimizer Ladder

**Description:** Run optimizers in a fixed ladder: equal-weight baseline, inverse-vol, HRP, then constrained ensemble search. Stop early if a simpler method passes all gates, and only run the next rung if the current rung fails a pre-specified gate.

**Axis:** Portfolio optimization and validation

**Basis:** external: HRP is useful when covariance estimates are noisy because it avoids full covariance inversion; direct: `iteration.md` already limits the optimizer family and requires `n_trials`.

**Rationale:** This keeps the search disciplined and credit/computation efficient. It also creates a clean story: if HRP beats the constrained search after DSR, the user gets robustness over backtest cosmetics.

**Downsides:** A fixed ladder may miss a high-CAGR allocation that a larger search could find, but that is the point of the anti-overfit design.

**Confidence:** 92%

**Complexity:** Medium

**Status:** Unexplored

### 4. Inverse ETF Sleeve as a Gate-Tested Hedge, Not a Free Alpha Source

**Description:** Treat inverse ETFs as a constrained hedge sleeve with its own diagnostics: maximum 35% total inverse weight, contribution to drawdown reduction, contribution to CAGR drag, and standalone crisis-window behavior in 2008, 2020, and 2022. Promote inverse exposure only if it improves walk-forward Sharpe or drawdown without failing DSR.

**Axis:** ETF universe breadth and safety

**Basis:** direct: the user allowed inverse ETFs; `iteration.md` sets a maximum inverse sleeve and requires crisis-stress awareness through the ML trading checklist.

**Rationale:** Inverse ETFs can manufacture attractive historical hedges if treated as unconstrained return assets. Framing them as a tested hedge sleeve keeps them useful while guarding against path-specific overfit.

**Downsides:** May reject inverse exposure that boosts in-sample CAGR but weakens statistical validity.

**Confidence:** 88%

**Complexity:** Medium

**Status:** Unexplored

### 5. Credit-Aware “Stoplight” API Plan

**Description:** Before execution, create a stoplight budget: green calls are metadata and one-off auth/quota checks; yellow calls are ETF price pulls and strategy detail pulls; red calls are repeated backtest-like or broad data calls. The implementation should estimate calls before each phase and append actual `quotaRemaining` changes to `iteration.md`.

**Axis:** Credit efficiency and iteration control

**Basis:** direct: `iteration.md` requires stopping for approval if estimated P123 credit use exceeds 250 credits and recording actual costs when known.

**Rationale:** Credit control should not be a note at the end; it should shape the execution order. A stoplight plan turns “optimize credits” into a concrete mechanism future agents can follow.

**Downsides:** Adds bookkeeping overhead before the first result appears.

**Confidence:** 93%

**Complexity:** Low

**Status:** Unexplored

### 6. Trial Ledger as the Primary Research Artifact

**Description:** Treat `trial_ledger_YYYYMMDD.csv/json` as the central output, not a sidecar. Every result table, final report, and next-iteration recommendation should be derivable from the ledger.

**Axis:** Auditability and handoff

**Basis:** direct: the user approved a required pre-registered trial ledger; external: DSR requires honest accounting for multiple tested configurations.

**Rationale:** If the ledger is primary, selection bias becomes harder to hide. Another user can reconstruct why the final candidate survived and which alternatives failed.

**Downsides:** The ledger schema needs to be stable enough that later scripts do not drift.

**Confidence:** 96%

**Complexity:** Low

**Status:** Unexplored

### 7. “No Winner” Report Template

**Description:** Prepare a first-class final-report path for the case where no allocation clears all gates. It should rank the nearest misses, identify the exact failed gate, and propose the cheapest next iteration without changing thresholds.

**Axis:** Auditability and handoff

**Basis:** direct: `iteration.md` states that if no candidate passes, failed candidates should be reported honestly and gates should not be loosened.

**Rationale:** The target thresholds are high enough that failure is plausible. A polished no-winner path keeps the workflow valuable even when the result is not the hoped-for backtest.

**Downsides:** Less emotionally satisfying than declaring a winner; requires discipline in final wording.

**Confidence:** 90%

**Complexity:** Low

**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Run a large random-weight search until CAGR and Sharpe clear the target | Fails data-snooping controls and inflates `n_trials` without strong expected value. |
| 2 | Treat SIM-page displayed Sharpe and inception as final inputs for allocation | Violates the API-derived performance constraint. |
| 3 | Include leveraged ETFs because they may help hit CAGR >20 | Explicitly out of scope unless later approved; likely raises path-dependence and overfit risk. |
| 4 | Use summary stats to synthesize strategy returns | Rejected by the approved risk response; summary-stat approximation is not a synchronized return stream. |
| 5 | Optimize directly for CAGR >20 then check Sharpe after | Weaker than the approved objective of maximizing walk-forward Sharpe subject to CAGR, drawdown, PSR, and DSR gates. |
| 6 | Skip the no-winner path and keep iterating until something passes | Violates the requirement not to loosen gates or keep searching post hoc. |

## Suggested Next Step

Use `ce-brainstorm` on Idea 5, `Credit-Aware Stoplight API Plan`, if the next action is to sharpen implementation sequencing before running API calls. It has high leverage because it determines how quickly the workflow learns whether the problem is feasible without wasting Portfolio123 credits.

---

## Tags

#algo-trading/portfolio123 #work/ideation
