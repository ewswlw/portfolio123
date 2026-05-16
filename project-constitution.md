# Project Constitution
## Technology Stack
- Portfolio123 web platform through the user's logged-in Chrome session
- Portfolio123 API/DataMiner access through `P123_API_ID` and `P123_API_KEY` environment variables
- PowerShell 5+ for local credential loading and artifact checks
- Local workspace artifacts under `p123-output/`
## Project Structure
- `AGENTS.md` - workspace operating rules, P123 naming conventions, validation hierarchy, and secret handling
- `docs/solutions/` - compounded Portfolio123 workflow learnings
- `p123-output/` - local CSV, JSON, screenshots, candidate logs, and final reports
- `scripts/` - local helper scripts such as encrypted Portfolio123 credential loading
- `secrets/` - Windows DPAPI encrypted local secrets, never plaintext credentials
## Executable Commands
- Build: `Write-Output 'No build step required for Portfolio123 strategy workflow workspace'`
- Test: `Get-ChildItem -LiteralPath .\AGENTS.md, .\scripts\Import-Portfolio123Secrets.ps1`
## Hard Boundaries
- Never print, log, commit, or store plaintext Portfolio123 passwords, API keys, cookies, tokens, or session values.
- Never report final strategy performance from local Python or API screen backtests; final claims require native Portfolio123 simulated strategy output.
- Never create Portfolio123 account objects without the `codex_` prefix unless the user explicitly confirms the exception.
- Never place live trades, rebalance live portfolios, or delete P123 objects unless the user explicitly requests and confirms the exact action.
- Never force an older simulation start date if the AI Factor, model, or data availability makes the result invalid or misleading.
