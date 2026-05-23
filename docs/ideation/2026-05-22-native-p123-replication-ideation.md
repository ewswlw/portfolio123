Created: 2026-05-22 15:20 America/New_York

# Native P123 Dynamic Strategy Book Replication Ideation

## Topic

Generate implementation ideas for replicating promoted dynamic Strategy Book trial `386` directly inside the Portfolio123 platform, then carry all sensible survivors into planning and execution.

## Grounding

Relevant artifacts:

- `p123-output/native_validation_package_20260522.md`
- `p123-output/dynamic_candidate_promotion_report_20260522.md`
- `p123-output/native_strategy_book_readonly_inventory_20260522.md`
- `docs/solutions/workflow-issues/portfolio123-dynamic-strategy-book-timing-warmup-workflow-2026-05-22.md`
- `docs/plans/2026-05-22-004-native-p123-strategy-book-validation-plan.md`

Promoted candidate:

- Trial: `386`
- Optimizer family: `dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20`
- API-estimated CAGR: `20.68%`
- API-estimated Sharpe: `2.00`
- API-estimated max drawdown: `-12.81%`
- Corrected local timing start: `2007-06-26`
- Allocation: five 200-day timed strategy variants at 16% each, plus 20% defensive proxy.

Native constraints already observed:

- Existing close books use static-weight allocations with every-4-weeks rebalance.
- The read-only Strategy Book review surface did not expose a book-level timing/formula surface.
- Some direct wizard tab URLs returned internal server errors.
- Existing close books are useful references but are not clean trial `386` replications.

## Candidate Ideas Considered

### 1. Book-Level Conditional Timing

Try to find a native Strategy Book surface that applies conditional allocation or timing directly to each asset.

Assessment:

- Highest exactness if available.
- Lowest object count.
- Previous read-only inspection did not confirm this surface.

Status: survivor.

Reason:

- It must be checked first because it is the cleanest exact route and avoids unnecessary component cloning.

### 2. Separate Timed Component Strategies

Create/copy one `codex_dynamic_*` timed component per source strategy and then add those components to a Strategy Book.

Assessment:

- Most likely fallback if book-level timing is unavailable.
- Exactness depends on whether a P123 simulated strategy can move to `SHY` or another defensive asset during risk-off periods.
- A stock strategy may be able to move to cash but not to an ETF, which would be an approximation, not exact replication.

Status: survivor.

Reason:

- This is the principal implementation route if exact component-level defensive substitution is supported.

### 3. Cash-Timed Component Approximation

Create timed versions of source strategies that go to cash when the benchmark is below the 200-day moving average, while keeping the book's 20% defensive proxy.

Assessment:

- More likely to be expressible in standard P123 stock simulations.
- Not exact because the local promoted components used the defensive proxy return during risk-off, not cash.

Status: survivor as fallback only.

Reason:

- Useful if exact defensive substitution is impossible, but must be labeled `approximation` and requires user approval before running.

### 4. Existing Risk-Reduction Model Proxy

Use existing P123 models such as `Advisor Small Cap Focus (P123) With Risk Reduction` as proxies for the desired 200-day timed components.

Assessment:

- Easy platform path.
- Not trial `386` replication.
- Risks false success because existing close books already use these models and still miss the strict gates.

Status: rejected for primary replication.

Reason:

- This creates a new strategy-book concept, not a native replication of the promoted API-estimated candidate.

### 5. Clone Existing Close Book And Edit

Copy `BookSim - Copy` or another close book, then adjust assets/weights toward the promoted candidate.

Assessment:

- Practical UI shortcut.
- Existing book assets differ materially from trial `386`.
- Could preserve hidden settings, but also risks inheriting unrelated structure.

Status: survivor only as a UI scaffolding tactic.

Reason:

- It may help discover fields or avoid wizard bugs, but the resulting object must still be named and validated as a new `codex_dynamic_*` candidate.

### 6. Primary Run With Every-4-Weeks Rebalance

Use every-4-weeks book rebalance for the primary native run.

Assessment:

- Matches inspected native close books.
- Aligns with accepted project-spec defaults.
- Annual rebalance remains a separate variant, not primary.

Status: survivor.

Reason:

- It reduces one source of native/API mismatch in the initial replication attempt.

### 7. Defensive Proxy Variant Matrix

Run separate `SHY`, `IEF`, and `AGG` defensive proxy variants.

Assessment:

- Could reveal whether the local defensive-proxy fallback materially changes native results.
- Consumes run budget and can turn replication into an experiment.

Status: rejected for primary run; survivor as later variant only.

Reason:

- User accepted primary `SHY`; variants require a separate decision after primary evidence.

### 8. Replication Status Matrix

Track every object and run as `exact`, `approximation`, `variant`, `blocked`, or `not_run`.

Assessment:

- Low effort.
- Prevents ambiguity in final reporting.
- Already accepted in project-spec innovation step.

Status: survivor.

Reason:

- It makes partial platform success auditable and prevents approximations from being mistaken for exact replication.

### 9. Hard Five-Run Ledger

Count every native component validation, failed setup run, final book run, and variant run against the 5-run maximum.

Assessment:

- Keeps P123 compute/credit use bounded.
- Forces the workflow to stop instead of thrashing.

Status: survivor.

Reason:

- The user explicitly accepted up to 5 native runs including variants.

### 10. Stop-Before-Approximation Gate

If exact timing cannot be represented, stop and ask before running an approximation.

Assessment:

- Protects scientific validity.
- May interrupt execution before a final book result exists.

Status: survivor.

Reason:

- Exactness is more important than producing a misleading native number.

## Survivor Set To Carry Into Plan

1. Book-level conditional timing capability check.
2. Separate timed component strategy route.
3. Cash-timed component approximation as gated fallback only.
4. Existing close-book clone as UI scaffolding tactic only, not as replication.
5. Every-4-weeks primary book rebalance.
6. `SHY` primary defensive proxy.
7. Replication status matrix.
8. Hard 5-run ledger.
9. Stop-before-approximation gate.
10. Native evidence artifact and `iteration.md` updates.

## Rejected Primary Paths

- Treat existing close books as trial `386` validation.
- Use existing risk-reduction models as the primary replication.
- Run defensive proxy/cadence variant matrices before primary evidence.
- Tune weights after seeing native results.
- Declare success from API-estimated results.

## Recommended Plan Direction

Use a gated execution flow:

1. Inspect platform capability for exact book-level timing.
2. If absent, inspect whether component-level exact defensive substitution is possible.
3. If exact route exists, create `codex_dynamic_*` objects and run within the 5-run budget.
4. If exact route does not exist, stop with a blocked/approximation decision rather than improvise.
5. Always write final evidence with status matrix and tier labeling.
