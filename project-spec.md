<project_specification>
  <project_name>Portfolio123 AI Factor Simulated Strategy Build</project_name>
  <overview>Create a native Portfolio123 simulated strategy anchored on the previously identified top AI Factor model: AI Factor Base 87 Features Andreas 2 / extra trees medium 4 #2. The goal is to find the longest defensible simulation window that can produce greater than 20% CAGR and greater than 1.5 Sharpe ratio using Portfolio123 native validation. The work is for strategy research, not live trading, and all saved Portfolio123 objects must be clearly identified as Codex-created with the codex_ prefix. Success is measured by native P123 simulated strategy results, plus a candidate DNA log that makes the search auditable and repeatable.</overview>
  <technology_stack>Portfolio123 web platform; Portfolio123 API/DataMiner where supported; Chrome logged-in session for account workflows; PowerShell helper scripts for encrypted credential loading; local Markdown/CSV/JSON artifacts under p123-output.</technology_stack>
  <assumptions>
    - The user remains logged into Portfolio123 in Chrome or can refresh the session when needed.
    - The selected AI Factor and model are available in the user's account and can be referenced by P123 strategy formulas.
    - The strategy will use native P123 simulated strategy validation for final performance claims.
    - API screen backtests, if used, are exploratory only and must be labeled ESTIMATED (Tier 3).
    - The phrase "as far back as makes sense" means the longest window that is defensible given AI Factor/model availability, data history, and leakage constraints.
  </assumptions>
  <out_of_scope>
    - Live trading, live portfolio rebalancing, brokerage integration, or order placement.
    - Deleting or overwriting existing user-created P123 objects.
    - Storing plaintext credentials or browser session secrets in project files.
    - Declaring success from local Python backtests or API screen_backtest results alone.
    - Exhaustive brute-force optimization across many unrelated strategy families.
  </out_of_scope>
  <core_features>
    <feature name="Top AI Factor Confirmation">As a researcher, I need the top AI Factor/model re-confirmed in the account so the strategy uses the correct object and model identifiers. Acceptance criteria: the selected AI Factor is AI Factor Base 87 Features Andreas 2 / extra trees medium 4 #2 unless account verification shows it is unavailable; identifiers and relevant model metadata are saved to p123-output.</feature>
    <feature name="AI Factor Formula Integration">As a researcher, I need the correct P123 formula reference confirmed before testing strategy performance. Acceptance criteria: AIFactor() versus AIFactorValidation() is resolved inside the simulated strategy context; formula errors or model mismatches are fixed before any result is considered valid.</feature>
    <feature name="Native Simulated Strategy Creation">As a researcher, I need a saved native P123 simulated strategy with a codex_ name so I can distinguish AI-created work from my own objects. Acceptance criteria: all created P123 objects use codex_ prefixes, the strategy uses realistic liquidity/slippage assumptions, and no live portfolio action is taken.</feature>
    <feature name="Conservative Parameter Search">As a researcher, I need a narrow search over high-impact knobs to avoid overfitting. Acceptance criteria: candidate changes are limited to universe/liquidity filters, position count, rebalance cadence, AI rank thresholds, and simple sell/risk rules unless the user approves broader exploration.</feature>
    <feature name="Robustness Checks">As a researcher, I need adjacent-variant checks before accepting a winner. Acceptance criteria: any candidate meeting or nearly meeting greater than 20% CAGR and greater than 1.5 Sharpe is tested against nearby settings, and brittle one-off winners are rejected or clearly labeled as fragile.</feature>
    <feature name="Strategy DNA Log">As a researcher, I need an audit trail for every serious candidate. Acceptance criteria: the log captures AI Factor reference, universe/liquidity filters, position count, rebalance cadence, buy rules, sell rules, start date, CAGR, Sharpe, drawdown, turnover where available, and keep/reject rationale.</feature>
    <feature name="Final Report">As a researcher, I need a concise final summary of what worked and what failed. Acceptance criteria: the report includes final native P123 performance evidence, exact settings, closest rejected candidates, blockers if targets are not achieved, and next recommended experiments.</feature>
  </core_features>
  <database_schema>
    <table name="strategy_dna_log">candidate_id TEXT primary key; p123_object_name TEXT; ai_factor_name TEXT; ai_factor_model TEXT; formula_reference TEXT; universe_rules TEXT; liquidity_rules TEXT; position_count INTEGER; rebalance_frequency TEXT; buy_rules TEXT; sell_rules TEXT; start_date DATE; end_date DATE; cagr REAL; sharpe REAL; max_drawdown REAL; turnover REAL; validation_tier TEXT; status TEXT; rationale TEXT; artifact_path TEXT</table>
  </database_schema>
  <api_endpoints_summary>
    <endpoint>N/A - Use Portfolio123 API only for supported exploratory data, known-ID lookups, and backtest operations; browser-native P123 simulation is required for final validation.</endpoint>
  </api_endpoints_summary>
  <implementation_steps>
    1. Load Context And Credentials - Read project AGENTS.md, Portfolio123 skill docs, prior AI Factor output CSV, and load encrypted P123 credentials only if API access is needed. Dependencies: none.
    2. Confirm Top AI Factor Details - Re-open or re-query the top AI Factor/model from the account and capture exact object/model identifiers needed for formulas or strategy setup. Dependencies: step 1.
    3. Verify AI Factor Formula Integration - Test whether the selected AI Factor/model can be referenced in P123 strategy rules using the correct formula form. Resolve AIFactor() vs AIFactorValidation() before any candidate is treated as valid. Dependencies: step 2.
    4. Build Baseline Candidate Strategy - Create or configure a native simulated strategy with codex_ naming, realistic liquidity/slippage assumptions, top AI Factor buy logic, and simple sell logic. Dependencies: step 3.
    5. Run Native Baseline Simulation - Run the longest defensible native P123 simulation window and save settings/performance output under p123-output/. Dependencies: step 4.
    6. Tune High-Impact Parameters - Test a narrow set of changes: position count, rebalance frequency, liquidity minimums, AI rank threshold, and sell deterioration rules. Dependencies: step 5.
    7. Run Robustness Checks - For any candidate that clears or nearly clears the target, test adjacent variants and reject brittle one-off winners. Dependencies: step 6.
    8. Select Final Candidate - Choose the simplest native-validated strategy that best satisfies greater than 20% CAGR and greater than 1.5 Sharpe, or document why no candidate passed. Dependencies: step 7.
    9. Save Deliverables - Save final settings, candidate log, native performance evidence, and summary report under p123-output/. Dependencies: step 8.
    10. Recommend Learning Capture - If reusable P123 browser/API/formula lessons were discovered, recommend ce-compound so the workflow knowledge is preserved. Dependencies: step 9.
  </implementation_steps>
  <success_criteria>
    <functional>A native Portfolio123 simulated strategy is created with a codex_ name, uses the selected AI Factor correctly, and is validated over the longest defensible period. If no candidate meets the target, the closest candidates and blockers are documented.</functional>
    <ux>The user receives a clear concise report with exact settings, performance, evidence paths, and a distinction between user-created and Codex-created P123 objects.</ux>
    <technical>Secrets are never printed or written in plaintext; final performance claims come only from native P123 simulation; every serious candidate is captured in a strategy DNA log; adjacent-variant robustness checks are performed before accepting a winner.</technical>
  </success_criteria>
</project_specification>
