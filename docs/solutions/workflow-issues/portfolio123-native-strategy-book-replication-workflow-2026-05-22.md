---
title: Portfolio123 Native Strategy Book Replication Workflow
created_at: 2026-05-22 16:55 America/New_York
date: 2026-05-22
category: workflow-issues
module: portfolio123-native-strategy-book-validation
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "Replicating an API-estimated Portfolio123 Strategy Book candidate directly on the native platform"
  - "Creating P123 simulated strategy components with market-timing hedge rules"
  - "Adding timed simulated strategy components and raw ETF sleeves to a native simulated book"
  - "Renaming P123 objects when the reliable run path bypasses the naming modal"
  - "Interpreting API-estimated candidates after native Tier 1 Strategy Book validation"
related_components:
  - assistant
  - tooling
  - documentation
tags:
  - portfolio123
  - strategy-book
  - native-validation
  - browser-automation
  - comp-props
  - hedge
  - shy
  - tier1
---

# Portfolio123 Native Strategy Book Replication Workflow

## Context

This learning was captured after replicating API-estimated dynamic Strategy Book trial `386` inside Portfolio123's native platform.

The promoted API-estimated candidate looked strong enough to justify native validation:

```text
Trial: 386
Optimizer family: dynamic_grid_timed_200d_s0.80_inv0.00_taa0.00_def0.20
API-estimated CAGR: 20.68%
API-estimated Sharpe: 2.00
API-estimated max drawdown: -12.81%
Corrected local timing window: 2007-06-26 to 2026-01-05
```

Native validation told a different story. After creating five timed native components plus a raw `SHY` sleeve, the native simulated Strategy Book returned:

```text
Object: codex_dynamic_strategy_book_candidate
Port ID: 1943551
Period: 12/30/05 - 01/06/26
Annualized return: 15.88%
Sharpe Ratio: 1.22
Max drawdown: -20.11%
```

The drawdown gate passed, but the CAGR and Sharpe gates failed. This is a clean example of why API-estimated Strategy Book candidates must remain nominations until Portfolio123's native Strategy Book engine validates them.

## Guidance

When a dynamic Portfolio123 Strategy Book candidate needs native validation, first determine whether the Strategy Book wizard itself exposes book-level timing. In this run, the native simulated-book wizard exposed static assets, fixed weights, rebalance cadence, tolerances, exposure, and period controls, but no visible book-level timing, hedge, formula, or conditional allocation surface.

Use component-level timing when book-level timing is absent. For each source simulated strategy, clone the strategy and add these rules:

```text
Buy rule:
Close(0,#bench) > SMA(200,0,#bench)

Sell rule:
Close(0,#bench) <= SMA(200,0,#bench)

Hedge entry:
Close(0,#bench) <= SMA(200,0,#bench)

Hedge exit:
Close(0,#bench) > SMA(200,0,#bench)
```

Enable `Hedge / Market Timing`, select `Choose Position`, and select:

```text
Treasury 1-3 Year (SHY:USA)
```

The exact component setting used in this run was:

```text
Hedge ratio: 100% of Current Holdings
Transaction type: Long
```

Treat that hedge ratio as an important implementation detail. The intended local behavior was full risk-off substitution into `SHY`; the next native variant should test `100% of Total Equity / Includes cash` because `Current Holdings` may leave the component behavior different from the API-estimated model.

For simulated-strategy components, the normal visible `Run Simulation` link may not fire through the in-app Browser wrapper. Direct navigation to the native runner worked:

```text
https://www.portfolio123.com/port_sim_go.jsp?<timestamp>
```

That path saved and ran the configured simulated-strategy wizard session, but it bypassed the naming modal. If the object is saved with P123's default clone name, rename it through the Svelte component-properties endpoint instead of creating more default-named objects:

```http
POST https://www.portfolio123.com/spr/user/compProps
```

Use an authenticated session and send JSON with the non-secret request characteristics used by the Svelte app:

```text
Content-Type: application/json
ANGULAR_REQ: 1
SVELTE_REQ: 1
X-Requested-With: XMLHttpRequest
Referer: https://www.portfolio123.com/port_summary.jsp?portid=<PORT_ID>
```

Payload shape:

```json
{
  "catType": "SIM",
  "itemUid": 1943514,
  "mkttypeUid": 0,
  "name": "codex_dynamic_1934014_timed_200d",
  "description": "",
  "categoryUid": 45166,
  "groupUid": 0,
  "resolveGroupUid": 0
}
```

Do not write passwords, API keys, cookies, tokens, or session values into docs, logs, or chat. Load Portfolio123 credentials through the project-local encrypted secrets script and pass values through environment variables only.

For simulated Strategy Books, do not use the direct `port_sim_go.jsp?<timestamp>` runner. That produced:

```text
Session trading system changed.
Please do not simultaneously edit trading systems in different browser windows.
```

The working path for a new simulated book was:

1. Build the book in one in-app Browser session.
2. Add the five timed `codex_dynamic_*` simulated strategies from `Add Existing Model`.
3. Add raw `SHY` through the `Add Stock / ETF` field.
4. Set fixed weights: 16% for each timed component and 20% for `SHY`.
5. Use the page's own `BookSimulButton`.
6. In the `New Simulated Book Properties` modal, set the name.
7. Click `Save`; P123 runs the book and redirects to the summary page.

The final book allocation in the verified run was:

| Asset | Type | Target allocation |
|---|---|---:|
| `codex_dynamic_1934014_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1873038_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934023_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934030_timed_200d` | `SIM` | `16.0%` |
| `codex_dynamic_1934037_timed_200d` | `SIM` | `16.0%` |
| `iShares 1-3 Year Treasury Bond ETF (SHY)` | `ETF` | `20.0%` |

## Why This Matters

This workflow prevents three expensive mistakes.

First, it prevents declaring API-estimated success too early. Trial `386` appeared to meet the strict target in local/API research, but the native Tier 1 Strategy Book failed CAGR and Sharpe:

| Gate | Target | Native result | Pass? |
|---|---:|---:|---|
| Annualized return | `>20%` | `15.88%` | No |
| Sharpe ratio | `>2.0` | `1.22` | No |
| Max drawdown | better than `-25%` | `-20.11%` | Yes |

Second, it preserves account hygiene. The simulated-strategy runner can create valid native objects with default clone names. Stop and rename those objects through `compProps` before continuing, or the final book becomes hard to audit.

Third, it avoids losing wizard state. Simulated strategies and simulated books do not share the same reliable run path. Strategy components accepted direct `port_sim_go.jsp` navigation; the simulated book rejected that path and had to be run through the native book button and naming modal.

## When to Apply

Apply this workflow when:

- an API-estimated Strategy Book candidate graduates to native P123 validation;
- a candidate needs timing behavior that the Strategy Book wizard cannot express directly;
- cloned simulated strategy components must hold `SHY` or another defensive asset in risk-off states;
- the Browser wrapper clicks P123 run or rename controls but the UI does not fire as expected;
- or a final performance claim depends on native P123 Strategy Book output.

Do not apply this as a live trading or live rebalancing workflow. It is for simulated strategies, simulated books, and research validation only.

## Examples

Native component results from the verified run:

| Source ID | Native object | Port ID | Annualized return | Sharpe | Max drawdown |
|---:|---|---:|---:|---:|---:|
| `1873038` | `codex_dynamic_1873038_timed_200d` | `1943550` | `17.52%` | `1.19` | `-19.37%` |
| `1934014` | `codex_dynamic_1934014_timed_200d` | `1943514` | `22.41%` | `1.18` | `-27.50%` |
| `1934023` | `codex_dynamic_1934023_timed_200d` | `1943547` | `12.27%` | `0.58` | `-38.33%` |
| `1934030` | `codex_dynamic_1934030_timed_200d` | `1943548` | `26.88%` | `1.28` | `-31.32%` |
| `1934037` | `codex_dynamic_1934037_timed_200d` | `1943549` | `14.35%` | `0.98` | `-20.42%` |

Outcome language to use after a native rejection:

```text
The API-estimated candidate did not survive native Portfolio123 Tier 1 validation.
Native drawdown passed, but CAGR and Sharpe failed. The next native iteration should be treated as a new variant, not a continuation of the same exact validation run.
```

Potential next variant:

```text
Clone the five timed components again and set the hedge ratio to
100% of Total Equity / Includes cash.

Reason: the validated run used 100% of Current Holdings, which may not
match the intended full risk-off substitution into SHY.
```

## Related

- `p123-output/native_strategy_book_validation_20260522.md`
- `iteration.md`
- `docs/solutions/workflow-issues/portfolio123-dynamic-strategy-book-timing-warmup-workflow-2026-05-22.md`
- `docs/solutions/workflow-issues/portfolio123-api-strategy-book-research-workflow-2026-05-22.md`
- `docs/plans/2026-05-22-005-native-p123-replication-execution-plan.md`
- `docs/ideation/2026-05-22-native-p123-replication-ideation.md`
