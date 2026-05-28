# Portfolio123 Research Workspace

This workspace is for full-lifecycle Portfolio123 strategy development and research using both:

- the Portfolio123 web platform through the user's logged-in Chrome session, and
- the Portfolio123 API/DataMiner interface when API access is the right tool.

## Required Skills And Knowledge

When work involves Portfolio123, P123, simulated strategies, AI Factors, ranking systems, screens, universes, Strategy Books, backtests, DataMiner, formula syntax, or P123 API calls, load and follow:

`C:/Users/Eddy/.codex/skills/portfolio123/SKILL.md`

That skill is the source of truth for:

- P123 validation hierarchy and performance-reporting rules.
- Browser routes and platform quirks.
- API-first vs browser-first decisions.
- AI Factor setup, validation, `AIFactor()` vs `AIFactorValidation()`, and model evaluation.
- Ranking-system XML patterns and formula-language references.
- Strategy creation and native simulation workflows.

If the user invokes `/portfolio123` or otherwise asks for Portfolio123 work, use the skill before deciding the implementation path.

## Compounded Learnings

This workspace has a growing local knowledge store:

`docs/solutions/`

Before doing non-trivial P123 work, debugging navigation/API behavior, or making workflow decisions, search `docs/solutions/` for relevant compounded learnings. These docs are organized by category and use YAML frontmatter fields like `module`, `problem_type`, `component`, `severity`, and `tags`.

Current relevant learning:

- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`
- `docs/solutions/workflow-issues/portfolio123-ai-factor-validation-strategy-workflow-2026-05-16.md`

These docs capture verified P123 routes, model-ranking practices, and AI Factor validation strategy workflow rules, including:

- simulated strategies list: `https://www.portfolio123.com/app/opener/SIM`
- AI Factor list: `https://www.portfolio123.com/sv/opener/AIFACTOR/-2`
- AI Factor model table: `https://www.portfolio123.com/sv/aiFactor/{id}/validation/models`
- using native P123 `Rank`, `Results`, and `Predictors` when deciding the best AI Factor models.
- using the native formula dialog for exact `AIFactorValidation(...)` syntax.
- treating Basic Holdout validation windows as binding for exact validation-model strategy tests.
- creating separate `codex_` P123 strategy candidates and logging them in `p123-output/`.

## Authentication And Secrets

Do not write Portfolio123 passwords, API IDs, API keys, browser cookies, tokens, or session values into repo/workspace files, docs, logs, screenshots, or chat output.

For web access, prefer an already-authenticated browser session. If Portfolio123 is logged out, automatically try to log in using the project-local encrypted secrets file and `scripts/Import-Portfolio123Secrets.ps1` without printing or storing secret values. Ask the user to complete login only if the encrypted secrets are missing, fail to decrypt, or the site requires an interactive challenge that the agent cannot complete safely.

This workspace may contain a local encrypted secrets file:

`secrets/portfolio123.local.secrets.clixml`

It is encrypted with Windows DPAPI for the current Windows user on this machine. It is not portable to other users or machines. To load it into the current PowerShell process without printing secret values, run:

```powershell
.\scripts\Import-Portfolio123Secrets.ps1
```

That script sets:

- `PORTFOLIO123_USERNAME`
- `PORTFOLIO123_PASSWORD`
- `P123_API_ID`
- `P123_API_KEY`

Do not print these values. If a command needs them, pass them through environment variables.

For API access, read credentials from environment variables:

- `P123_API_ID`
- `P123_API_KEY`

If API credentials are missing, tell the user which environment variables are needed. Do not hard-code secrets into scripts or instructions.

## Chrome Browser Workflow

When the user mentions `ChromeChrome`, `@chrome`, a logged-in P123 browser session, or asks to inspect account objects through the website, use the bundled Chrome skill before any fallback:

Prefer the newest installed Chrome skill under:

`C:/Users/Eddy/.codex/plugins/cache/openai-bundled/chrome/*/skills/chrome/SKILL.md`

Use Chrome for account pages that require session state. Keep browser work read-only unless the user explicitly asks to create, edit, run, delete, or submit something.

After Chrome browser work, finalize tabs according to the Chrome skill. Keep a tab only when the user needs the live page as a handoff or deliverable.

## P123 Validation Rules

Use native Portfolio123 output for performance claims.

- Strategy Books are Tier 1.
- Native simulated strategies are Tier 2.
- API `screen_backtest` is Tier 3 and must be labeled `ESTIMATED (Tier 3)`.
- Local Python backtests are not substitutes for P123 native validation.

Do not report P123 performance numbers as final unless they come from the appropriate native P123 source. If using a lower tier for exploration, label it clearly.

For "top" rankings, state the ranking metric. If the user does not specify:

- simulated strategies: default to `Annual` return and mention that `Sharpe Ratio` can rank differently.
- AI Factor models: default to native model-table `Rank`, then break ties with populated `Results`, `Predictors`, target-universe fit, and recency.

## Portfolio123 API Workflow

Use the API when the task is data collection, known-ID strategy data, ranking performance, screen runs/backtests, universe updates, or other supported API operations.

Before expensive API work:

- confirm credentials are available from environment variables,
- estimate credit cost when possible,
- watch quota/credit usage,
- save outputs to `p123-output/` with descriptive filenames.

Do not invent account-level listing endpoints. P123 lacks broad listing endpoints for several object types; discover IDs through the browser UI when needed, then use API calls with known IDs.

## Output Conventions

Save extracted data, tables, JSON, CSVs, and reports under:

`p123-output/`

Use filenames that include the operation and date, for example:

- `simulated_strategies_top5_YYYYMMDD.csv`
- `ai_factor_models_top_YYYYMMDD.csv`
- `strategy_validation_<strategy-id>_YYYYMMDD.json`

Follow the global Markdown standards in `C:/Users/Eddy/.codex/rules/Markdown Standards.md`.

For this workspace:

- `docs/` Markdown is human-authored project documentation. New files should follow strict note metadata, tag, and index rules. Existing `docs/` filenames are historical audit paths; do not retroactively rename them unless explicitly asked.
- `p123-output/` Markdown is generated research/audit output. Keep stable machine-readable filenames and existing folder names, but apply Markdown metadata/tag/index hygiene to `.md` files: YAML frontmatter, final `## Tags`, creation/update dates, single H1, clean spacing, no tabs or trailing whitespace, and UTF-8.

Avoid writing generated artifacts into skill folders or the user's home directory.

## Compound Engineering

Be an active expert in the compound-engineering plugin. When a command, skill, or agent workflow would materially improve the work, recommend it clearly before doing it.

Good moments to recommend compound-engineering workflows:

- Use `ce-compound` after a solved P123 navigation/API/platform issue so the learning lands in `docs/solutions/`.
- Use `ce-plan` before a multi-step strategy research or implementation effort.
- Use `ce-debug` for unexplained API errors, browser automation failures, bad P123 formula behavior, or mismatched validation results.
- Use `ce-code-review` before committing non-trivial code, especially data pipelines, API wrappers, ranking-system XML generators, or backtest orchestration.
- Use `ce-sessions` when prior agent sessions may contain relevant P123 context.
- Use `ce-worktree` before isolated implementation work that should not disturb the current workspace.
- Use `ce-commit`, `ce-commit-push-pr`, or GitHub plugin workflows when the user asks to preserve or publish changes.

Recommendation means: explain the relevant command/skill and why it would help. Do not invoke a compound-engineering workflow unless the user asks for it or the current request explicitly triggers that skill.

## Safety Boundaries

Do not place live trades or rebalance live portfolios unless the user explicitly requests the exact action and the platform workflow makes the action clear.

Do not delete P123 objects, trained models, strategies, ranking systems, or universes unless the user explicitly asks for deletion and confirms the target.

For browser workflows that may spend credits, train AI Factors, run expensive validations, or alter account objects, summarize the action and ask for confirmation before starting.

Keep every Portfolio123 object created by agents prefixed with `codex_` unless the user explicitly names an object differently and confirms the exception. This applies to strategies, screens, ranking systems, universes, AI Factors, simulations, reports, and any other saved P123 account object. Examples: `codex_strategy_quality_smallcaps`, `codex_screen_value_momentum`, `codex_ranking_system_quality_v1`.

## Learned User Preferences
- The user wants compound-engineering skills recommended when they would materially improve Portfolio123 research workflows, but not invoked unless requested or explicitly triggered.
- The user prefers numbered options when a workflow requires a decision or consent.
## Learned Workspace Facts
- This workspace is for Portfolio123 strategy research using Chrome for logged-in platform workflows and the P123 API for supported data/backtest operations.
- Project-local P123 credentials are stored in a Windows DPAPI encrypted file and loaded through scripts/Import-Portfolio123Secrets.ps1; agents must not print secret values.
- Portfolio123 account objects created by agents must use the `codex_` prefix unless the user explicitly confirms a different name.
- Before non-trivial Portfolio123 work, agents should search `docs/solutions/` for compounded P123 workflow learnings.
- This workspace is a Git repository on branch `main`; `.codex/`, `p123-output/`, and `secrets/` are intentionally ignored.
- For Portfolio123 live `AIFactor(...)` strategy tests, predictor existence or dataset history does not imply full-history backtestability; verify the accepted native simulation window and consult the AI Factor validation workflow learning.
