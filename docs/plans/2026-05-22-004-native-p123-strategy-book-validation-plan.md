Created: 2026-05-22 15:03 America/New_York

# Native P123 Strategy Book Validation Plan

## Summary

Plan a manual, platform-only validation of the promoted dynamic Portfolio123 Strategy Book candidate. The plan preserves the user's boundary: the agent may inspect and document, but does not create, edit, copy, delete, or run P123 objects unless a later request explicitly authorizes that action.

## Origin

- Requirements source: `docs/brainstorms/2026-05-22-native-p123-strategy-book-validation-requirements.md`
- Research source: `p123-output/native_validation_package_20260522.md`
- Dynamic candidate report: `p123-output/dynamic_candidate_promotion_report_20260522.md`
- Timing learning: `docs/solutions/workflow-issues/portfolio123-dynamic-strategy-book-timing-warmup-workflow-2026-05-22.md`
- Existing dynamic plan: `docs/plans/2026-05-22-003-feat-dynamic-p123-strategy-book-plan.md`

## Problem Frame

The promoted API-estimated candidate passed strict local gates after the timing warmup correction, but it is not a final Portfolio123 result. Native Strategy Book simulation is the Tier 1 authority. The plan must help the user reproduce the candidate on-platform while preserving the distinction between:

- API-estimated nomination: useful for deciding what to validate.
- Native P123 Strategy Book result: required before claiming the target was met.

The practical uncertainty is how Portfolio123 should represent the 200-day timing overlay. If the book can apply timing at the asset level, fewer objects are needed. If not, separate timed simulated strategy components are required.

## Candidate To Validate

- Trial: `386`
- Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: `20.68%`
- API-estimated Sharpe: `2.00`
- API-estimated max drawdown: `-12.81%`
- Corrected local timing panel starts: `2007-06-26`

Allocation:

| Component | Weight |
|---|---:|
| `strategy_1873038_timed_200d` | 16% |
| `strategy_1934014_timed_200d` | 16% |
| `strategy_1934023_timed_200d` | 16% |
| `strategy_1934030_timed_200d` | 16% |
| `strategy_1934037_timed_200d` | 16% |
| Defensive proxy component | 20% |

Excluded from the promoted candidate:

- Conditional inverse sleeve, because promoted weight was `0%`.
- Tactical ETF sleeve, because promoted weight was `0%`.

## Planning Decisions

- Use manual handoff mode first. No account-changing action belongs in this plan unless the user later changes the mode.
- Treat existing native books as reference points, not editable targets.
- Preserve the promoted allocation exactly for the primary validation. Weight changes become separate experiments.
- Prefer `SHY` as the defensive proxy when available, following the research pipeline's fallback order of `SHY`, then `IEF`, then `AGG`.
- Keep the timing warmup caveat visible in every validation note. The native result must clarify whether it starts in 2006, after the 200-day warmup, or under another P123-specific convention.

## Phase 1: Read-Only Native Inventory

Goal: understand the closest native P123 books and whether they already reveal the required object structure.

Steps:

1. Open the simulated books list:
   `https://www.portfolio123.com/app/opener/BOOKSIM?cat=-2`
2. Record the closest visible candidates:
   - `BookSim - Copy`: 22.90% annualized return, 1.90 Sharpe, -25.52% max drawdown, 4 assets.
   - `BookSim - Copy(2)`: 26.5% annualized return, 1.84 Sharpe, -31.9% drawdown.
   - `BookSim - Copy(3)`: 22.0% annualized return, 1.86 Sharpe, -25.2% drawdown.
   - `BookSim(6)`: 23.6% annualized return, 1.85 Sharpe, -27.1% drawdown.
3. Open each close book summary page in read-only mode.
4. Capture for each book:
   - Native annualized return.
   - Native Sharpe ratio.
   - Native max drawdown.
   - Inception/start date.
   - Asset count.
   - Asset names and weights.
   - Rebalance cadence.
   - Whether any timing or defensive component is visible.
5. Save the inventory in `p123-output/` or `iteration.md` only after removing any sensitive/account-private fields that are not needed for validation.

Completion check:

- The user has a table of close native reference books and knows which one, if any, is structurally closest to the promoted candidate.

## Phase 2: Determine Native Timing Surface

Goal: decide whether the 200-day timing overlay can be represented directly in a Strategy Book or needs separate timed simulated strategies.

Steps:

1. Inspect Strategy Book edit/re-run pages without saving.
2. Look for native controls that can apply a conditional rule or exposure rule to a book asset.
3. If book-level asset timing exists, document the exact surface and whether it can express:
   - Risk-on when benchmark close is above its 200-day moving average.
   - Risk-off behavior that allocates to the defensive proxy.
   - No same-period lookahead.
4. If book-level timing does not exist, use separate timed simulated strategy components as the primary validation path.
5. Do not click save, copy, run, or submit while performing this inspection.

Decision gate:

- If book-level timing is confirmed: use the direct book-level route.
- If book-level timing is absent or ambiguous: use separate `codex_` timed simulated strategy components.

Completion check:

- The user has a documented native route for representing the timing overlay, including any limitations or assumptions.

## Phase 3: Manual Component Specification

Goal: prepare exact human-entered component specs without executing them.

For each source strategy:

| Source ID | Source Name | Planned Timed Component |
|---:|---|---|
| `1873038` | `Canada Core Combo - Eddy/Kurtis` | `codex_1873038_timed_200d` |
| `1934014` | `SAMCF + Quality Filter Group - Copy` | `codex_1934014_timed_200d` |
| `1934023` | `Small Cap Focus - Small...erse - Small AUM - Copy` | `codex_1934023_timed_200d` |
| `1934030` | `Small Caps + Altman in Ranking + Altman > 1 - Copy` | `codex_1934030_timed_200d` |
| `1934037` | `Advisor TSX Mighty Mouse Momentum - Copy` | `codex_1934037_timed_200d` |

Timing concept:

- Risk-on: benchmark close is above the 200-day moving average.
- Risk-off: defensive proxy exposure.
- Benchmark proxy from local research: `SPY`.
- Defensive proxy default: `SHY`.

Manual validation notes:

- Confirm whether `#Bench` in the native object resolves to the intended benchmark.
- Confirm whether the native formula evaluates at rebalance using only already-known data.
- If formula semantics are unclear, record that ambiguity and do not treat native output as a clean replication.

Completion check:

- The user has a component list and timing rule translation ready to enter manually if they choose to proceed.

## Phase 4: Manual Book Specification

Goal: define the native Strategy Book candidate precisely enough for human entry.

Primary book name:

- `codex_dynamic_strategy_book_candidate`

Primary allocation:

| Asset | Weight |
|---|---:|
| `codex_1873038_timed_200d` | 16% |
| `codex_1934014_timed_200d` | 16% |
| `codex_1934023_timed_200d` | 16% |
| `codex_1934030_timed_200d` | 16% |
| `codex_1934037_timed_200d` | 16% |
| Defensive proxy component | 20% |

Settings to confirm before any run:

- Static weights.
- Start period: MAX or explicit date, with the timing warmup interpretation recorded.
- Rebalance cadence: choose one before running.
- Asset count and weights total 100%.
- No inverse or tactical ETF sleeves are included in the primary candidate.

Decision gate:

- Rebalance cadence must be selected before any native run:
  - Every 4 weeks matches the closest inspected native books.
  - Annual book-level rebalance matches the general Strategy Book template guidance.

Completion check:

- The user can enter the book without needing the agent to invent missing settings.

## Phase 5: Native Run And Evidence Capture

Goal: capture Tier 1 evidence only if and when the user manually runs the native simulation.

Evidence to record:

- Book name and P123 object ID.
- Run date.
- Start date and end date.
- Rebalance cadence.
- Asset names and weights.
- Annualized return.
- Sharpe ratio.
- Max drawdown.
- Any warnings, rejected formulas, or period resets.
- Screenshot/export references if available.

Comparison table:

| Metric | API-Estimated Candidate | Native P123 Result | Difference |
|---|---:|---:|---:|
| CAGR / annualized return | 20.68% | TBD | TBD |
| Sharpe | 2.00 | TBD | TBD |
| Max drawdown | -12.81% | TBD | TBD |
| Start date | 2007-06-26 local timing panel | TBD | TBD |

Completion check:

- The final note clearly states whether the native result met all three gates:
  - CAGR > 20%.
  - Sharpe > 2.
  - Max drawdown better than -25%.

## Phase 6: Post-Run Interpretation

Goal: avoid overclaiming and decide what to do next.

If native result passes all gates:

- Mark it as Tier 1 native validation.
- Record the exact start-date convention.
- Preserve screenshots/exports or written evidence.
- Summarize remaining live-trading caveats separately from backtest validation.

If native result fails:

- Do not tune weights immediately on the same evidence without labeling it a new experiment.
- Compare the failure mode:
  - Timing semantics mismatch.
  - Defensive proxy mismatch.
  - Rebalance cadence mismatch.
  - Native component behavior differs from API-derived return panel.
  - Warmup/start-date mismatch.
- Decide whether to run a new, pre-registered variant plan.

If native setup cannot represent the timing overlay:

- Mark the candidate as not natively replicable in the current P123 surface.
- Consider a separate plan for an approximate native proxy.

## Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Accidentally modifying account objects | Stay in read-only/manual handoff mode unless the user explicitly changes mode. |
| Treating API-estimated results as final | Label API/local numbers as estimates and native Strategy Book output as Tier 1. |
| Timing lookahead | Confirm formula timing and rebalance semantics before trusting a run. |
| Warmup ambiguity | Record native start date and compare it to the corrected local timing start of 2007-06-26. |
| Rebalance mismatch | Choose and record cadence before running; do not mix variants in one result. |
| Defensive proxy mismatch | Validate primary `SHY` result first; treat `IEF`/`AGG` as separate variants. |

## Outputs

- `iteration.md`: append each manual validation observation and decision.
- `p123-output/native_validation_package_20260522.md`: existing candidate handoff package.
- Optional new artifact after manual run: `p123-output/native_strategy_book_validation_YYYYMMDD.md`.

## Open Decisions Before Native Run

1. Choose book-level rebalance cadence:
   - every 4 weeks to match closest inspected native books, or
   - annual to match general Strategy Book template guidance.
2. Choose defensive proxy handling:
   - primary run uses `SHY` only, or
   - primary run plus separate `IEF` and `AGG` variants.

## Definition Of Done

- The user has a native P123 validation result or a documented reason native replication was not possible.
- The result is labeled with the correct validation tier.
- The timing warmup/start-date interpretation is explicit.
- No native performance target is claimed unless the native Strategy Book result passes all three gates.
