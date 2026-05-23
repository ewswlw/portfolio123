Created: 2026-05-22 14:56 America/New_York

# Native P123 Strategy Book Validation Manual Handoff

## Summary

This handoff defines the manual, platform-only validation workflow for the promoted dynamic Strategy Book candidate. The workflow is intentionally non-automated: no agent creates, edits, deletes, or runs Portfolio123 objects unless the user later gives explicit permission.

---

## Problem Frame

The API-estimated dynamic candidate passed the stricter research gates locally, but Portfolio123 performance claims must be validated on the native platform before being treated as final. The candidate also uses a timing overlay with a corrected effective start date of 2007-06-26, so the native validation must explicitly check whether the platform result satisfies the user's intended "going back that far" requirement.

Existing native simulated books already come close to the target. The closest inspected example, `BookSim - Copy`, shows 22.90% annualized return, 1.90 Sharpe, and -25.52% max drawdown on the native summary page. That is useful context, but it does not meet the stricter Sharpe > 2 and max drawdown better than -25% goal.

---

## Requirements

**Validation boundaries**

- R1. The agent must not create, modify, delete, copy, or run any Portfolio123 object during this manual-handoff flow.
- R2. All performance conclusions must be labeled by validation tier: native Strategy Book results are Tier 1; API/local estimates remain non-final.
- R3. The manual workflow must preserve the promoted candidate's allocation weights exactly unless the user chooses a deliberate variant.
- R4. The workflow must record both native metrics and any discrepancy between native P123 output and the API-estimated candidate.

**Candidate definition**

- R5. The primary candidate to validate is trial `386`, optimizer family `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`.
- R6. The candidate allocation is 16% to each of five 200-day timed strategy components and 20% to the defensive proxy.
- R7. Conditional inverse and tactical ETF sleeves are not part of the promoted native candidate because their promoted allocation weights were 0%.
- R8. The defensive proxy should be represented first by `SHY` if available, then `IEF`, then `AGG`, matching the research pipeline's fallback order.

**Native platform checks**

- R9. The native validation must first verify whether Portfolio123 can express the 200-day timing overlay inside a Strategy Book asset or whether timed components must be represented as separate simulated strategies.
- R10. If timed components must be separate simulated strategies, each component should use a `codex_` name and preserve the source strategy identity in the name or notes.
- R11. The book-level allocation should use static weights and the same rebalance cadence used for the comparable native books unless the user deliberately chooses a variant.
- R12. The native validation must capture annualized return, Sharpe ratio, max drawdown, inception/start date, rebalance cadence, asset count, and component weights.

---

## Manual Platform Steps

1. Open the simulated books list:
   `https://www.portfolio123.com/app/opener/BOOKSIM?cat=-2`

2. Review the closest existing native books before building anything:
   - `BookSim - Copy`: 22.90% annualized return, 1.90 Sharpe, -25.52% max drawdown, 4 assets.
   - `BookSim - Copy(2)`: 26.5% annualized return, 1.84 Sharpe, -31.9% drawdown.
   - `BookSim - Copy(3)`: 22.0% annualized return, 1.86 Sharpe, -25.2% drawdown.
   - `BookSim(6)`: 23.6% annualized return, 1.85 Sharpe, -27.1% drawdown.

3. Open each existing close book and record:
   - Asset names.
   - Asset weights.
   - Rebalance cadence.
   - Inception/start date.
   - Annualized return.
   - Sharpe ratio.
   - Max drawdown.

4. Compare the existing close book components to the promoted candidate's source strategies:
   - `1873038` / `Canada Core Combo - Eddy/Kurtis`
   - `1934014` / `SAMCF + Quality Filter Group - Copy`
   - `1934023` / `Small Cap Focus - Small...erse - Small AUM - Copy`
   - `1934030` / `Small Caps + Altman in Ranking + Altman > 1 - Copy`
   - `1934037` / `Advisor TSX Mighty Mouse Momentum - Copy`

5. If the existing book already contains materially similar components, use it as a reference point only. Do not overwrite it.

6. To create a clean native validation candidate manually, create or clone separate `codex_` timed strategy components only if Portfolio123 cannot apply the timing rule directly at the book-asset level.

7. For each timed strategy component, express the 200-day timing concept as:
   - Risk-on when `Close(0,#Bench) > SMA(200,0,#Bench)`.
   - Risk-off allocation goes to the defensive proxy.
   - Confirm the formula is evaluated using information available before the rebalance return period.

8. Create the simulated book candidate with this allocation:
   - 16% `strategy_1873038_timed_200d`
   - 16% `strategy_1934014_timed_200d`
   - 16% `strategy_1934023_timed_200d`
   - 16% `strategy_1934030_timed_200d`
   - 16% `strategy_1934037_timed_200d`
   - 20% defensive proxy component, preferably `SHY`

9. Name the book with a `codex_` prefix, for example:
   `codex_dynamic_strategy_book_candidate`

10. Run the native simulated book only after confirming the settings:
    - Static weights.
    - Intended rebalance cadence.
    - Start date or MAX period.
    - Component count and weights.
    - No unintended inverse or tactical ETF sleeves.

11. Record the native Tier 1 result and compare it against the API-estimated candidate:
    - API-estimated CAGR: 20.68%.
    - API-estimated Sharpe: 2.00.
    - API-estimated max drawdown: -12.81%.
    - Effective local timing-panel start: 2007-06-26.

---

## Acceptance Examples

- AE1. Covers R1, R2. Given the user selected manual handoff only, when the agent opens P123 pages, the agent may inspect and summarize but does not click save, copy, create, delete, or run.
- AE2. Covers R5-R8. Given the promoted candidate is being validated, when the user builds the native book manually, the promoted inverse and tactical sleeves are excluded because their promoted weights are 0%.
- AE3. Covers R9-R12. Given native results are recorded, when the final summary is written, the native Strategy Book result is treated as authoritative and any API/local estimate is shown only as a comparison.

---

## Success Criteria

- The user can reproduce the exact native-validation workflow without relying on the agent to perform account-changing actions.
- The validation record clearly answers whether the native book meets CAGR > 20%, Sharpe > 2, and max drawdown better than -25%.
- The record preserves the timing warmup caveat and does not overstate the API-estimated result.

---

## Scope Boundaries

- No live trading or live rebalancing.
- No creation, copying, editing, deleting, or running of Portfolio123 objects by the agent in this handoff mode.
- No final performance claim until native P123 Strategy Book output is available.
- No inverse ETF sleeve in the promoted candidate unless the user starts a separate variant.
- No tactical ETF sleeve in the promoted candidate unless the user starts a separate variant.

---

## Key Decisions

- Manual handoff only: the user chose not to have the agent create or run native platform objects.
- Start with existing close books: they provide useful native reference points and may reveal reusable platform structure.
- Preserve the promoted allocation: changing weights would turn the validation into a new experiment rather than a replication.
- Treat timing warmup as a first-class caveat: the local candidate begins after timing signal warmup, so native start-date interpretation matters.

---

## Dependencies / Assumptions

- The user has an authenticated Portfolio123 browser session.
- Portfolio123 may or may not support the desired timing overlay at the Strategy Book level; the manual workflow must verify this before deciding whether separate timed simulated strategies are required.
- The defensive proxy in the research pipeline resolves to `SHY` when available.

---

## Outstanding Questions

### Resolve Before Running Native Validation

- Should the native candidate use the same every-4-weeks book rebalance cadence as the closest existing native books, or should it use annual book-level rebalance per the general Strategy Book template guidance?
- Should `SHY` alone represent the defensive proxy, or should the user test `IEF` and `AGG` as separate native variants after the primary replication?

### Deferred to Planning

- Determine the exact Portfolio123 UI surface for expressing a 200-day timing overlay without introducing lookahead or same-period signal use.
