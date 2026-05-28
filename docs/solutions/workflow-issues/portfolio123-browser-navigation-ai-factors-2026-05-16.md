---
title: Portfolio123 Browser Navigation for Simulations and AI Factors
date: 2026-05-16
category: workflow-issues
module: Portfolio123 browser automation
problem_type: workflow_issue
component: assistant
severity: medium
applies_when:
  - "Using a logged-in Chrome session to inspect Portfolio123 account objects"
  - "Listing simulated strategies, AI Factors, validation models, results, or predictors"
  - "Ranking AI Factor models from native Portfolio123 validation output"
tags:
  - portfolio123
  - p123
  - chrome
  - ai-factor
  - simulated-strategies
  - browser-automation
  - native-validation
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-16
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 Browser Navigation for Simulations and AI Factors."
---

# Portfolio123 Browser Navigation for Simulations and AI Factors

## Context

Portfolio123 has a mix of legacy JSP routes and newer Svelte routes. During account inspection, normal menu navigation can waste time or land on legacy pages that do not expose the needed table cleanly. Future agents should use known working routes and read native P123 tables rather than reconstructing performance locally.

This learning was verified while answering:

- Top simulated strategies by native P123 `Annual`, `Excess`, `Sharpe Ratio`, and `DDown` columns.
- Top AI Factor models by native P123 model-table `Rank`, with tie-breaks based on populated `Results` and `Predictors` counts.

## Guidance

Use the Portfolio123 skill first, then use the Chrome plugin when account login state matters. Do not inspect cookies, local storage, or browser profile internals. Work from visible P123 pages and table text.

Useful routes:

| Task | Working Route | Notes |
|---|---|---|
| Simulated strategies list | `https://www.portfolio123.com/app/opener/SIM` | Exposes all simulated strategies and native columns: `Annual`, `Excess`, `Sharpe Ratio`, `DDown`. |
| AI Factor list | `https://www.portfolio123.com/sv/opener/AIFACTOR/-2` | New Svelte route. Shows AI Factor rows with counts for `Dataset`, `Validations`, `Results`, `Predictors`, `Resource Units`, created, updated. |
| AI Factor validation models | `https://www.portfolio123.com/sv/aiFactor/{id}/validation/models` | Shows model rows with `Model`, `Rank`, `Validation`, `Resource Units`, and `Update Date`. |
| AI Factor results | `https://www.portfolio123.com/sv/aiFactor/{id}/results` | Use when deeper lift/quantile diagnostics are needed. |
| AI Factor predictors | `https://www.portfolio123.com/sv/aiFactor/{id}/prediction/predictors` | Use to confirm live predictor availability. |

Avoid relying on `/app/opener/AIFACTOR/-2` for AI Factors. The verified route is `/sv/opener/AIFACTOR/-2`. Legacy URLs can redirect or fail depending on the page.

For simulated strategies:

1. Open `/app/opener/SIM`.
2. Read the rendered table.
3. Treat P123 table columns as native platform output.
4. If asked for "top" without another metric, rank by `Annual` and state that assumption. Mention that ranking by `Sharpe Ratio` can produce a different top list.
5. Capture strategy IDs from links like `/port_summary.jsp?portid=1934030`.

For AI Factor models:

1. Open `/sv/opener/AIFACTOR/-2`.
2. Identify factors with nonzero `Validations`; factors with zero validations have no trained model rows to compare.
3. Prefer factors where `Results` and `Predictors` are populated when breaking ties, because those indicate the factor is usable beyond a trained-model shell.
4. For each candidate factor, open `/sv/aiFactor/{id}/validation/models`.
5. Rank model rows by the native P123 `Rank` column.
6. If multiple models have `Rank = 100`, break ties by:
   - higher factor `Results` count,
   - higher factor `Predictors` count,
   - fit to the user's target universe,
   - recency only after the above.

Do not treat training duration, worker type, memory usage, or resource units as performance metrics. They are operational metadata.

## Why This Matters

P123's API does not provide broad account-level listing endpoints for strategies or AI Factors. Browser inspection is therefore the practical discovery path, but navigation must stay anchored to known native pages. Reading the rendered P123 tables preserves the platform's own validation hierarchy and avoids misleading local substitutes.

The AI Factor list also contains copies, unloaded datasets, and factors with validation counts but no result rows. Those can look important by name or recency, but they are not necessarily the best usable models. Tie-breaking on `Results` and `Predictors` helps separate trained experiments from models that are ready to use in ranking systems or predictions.

## When to Apply

- When a user asks for their top P123 simulated strategies.
- When a user asks for their best AI Factor models.
- When the task needs authenticated account state and the user is already logged in through Chrome.
- When deciding whether to use P123 API or browser navigation for discovery.
- When an agent needs exact AI Factor names and model display names for `AIFactorValidation()`.

## Examples

Simulated strategy extraction pattern:

```text
Open:
https://www.portfolio123.com/app/opener/SIM

Read columns:
Name, Universe, Type, Rank System, Inception, Update, Holdings, Annual, Excess, Sharpe Ratio, DDown

Default ranking:
Sort by Annual descending unless the user asks for Sharpe, drawdown, or another metric.
```

AI Factor model extraction pattern:

```text
Open:
https://www.portfolio123.com/sv/opener/AIFACTOR/-2

For each factor with Validations > 0:
https://www.portfolio123.com/sv/aiFactor/{id}/validation/models

Use:
Model + Rank + Validation status + Results count + Predictors count
```

Example tie-break reasoning:

```text
Model A: Rank 100, factor has 17 Results and 4 Predictors
Model B: Rank 100, factor has 5 Results and 0 Predictors

Prefer Model A when the user asks for "best" overall, because both tie on native Rank but Model A has stronger evidence of usable downstream output.
```

## Related

- Portfolio123 skill: `C:/Users/Eddy/.codex/skills/portfolio123/SKILL.md`
- Portfolio123 browser workflow reference: `C:/Users/Eddy/.codex/skills/portfolio123/browser-workflows.md`
- Portfolio123 AI Factor guide: `C:/Users/Eddy/.codex/skills/portfolio123/ai-factor-guide.md`
- Chrome skill route: use the bundled Chrome skill when the user says `ChromeChrome`, `@chrome`, or needs logged-in account state.

---

## Tags

#portfolio123 #p123 #chrome #ai-factor #simulated-strategies #browser-automation #native-validation #algo-trading/portfolio123 #work/solutions #work/workflow-issues
