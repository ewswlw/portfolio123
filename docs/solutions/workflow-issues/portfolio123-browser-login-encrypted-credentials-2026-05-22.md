---
title: Portfolio123 Browser Login with Encrypted Project Credentials
created_at: 2026-05-22 12:17 America/New_York
date: 2026-05-22
category: workflow-issues
module: Portfolio123 authentication workflow
problem_type: workflow_issue
component: authentication
severity: medium
applies_when:
  - "Logging into Portfolio123 through the Codex in-app Browser plugin"
  - "The user provides Portfolio123 web credentials and asks to store them for future use"
  - "A project-local encrypted `secrets/portfolio123.local.secrets.clixml` file exists"
  - "Future P123 work needs reusable login credentials without exposing secrets"
tags:
  - portfolio123
  - authentication
  - browser-plugin
  - encrypted-secrets
  - dpapi
  - credential-handling
  - algo-trading/portfolio123
  - work/solutions
  - work/workflow-issues
created: 2026-05-22
updated: 2026-05-28
description: "Portfolio123 workflow learning that records the issue, fix, and reuse guidance for Portfolio123 Browser Login with Encrypted Project Credentials."
---

# Portfolio123 Browser Login with Encrypted Project Credentials

## Context

The user asked Codex to use the in-app Browser plugin to log into Portfolio123 and to store the supplied credentials somewhere in the project for future logins. The workspace already had an encrypted DPAPI secret file at `secrets/portfolio123.local.secrets.clixml` plus `scripts/Import-Portfolio123Secrets.ps1`, so the right workflow was to use the supplied credentials for the immediate browser login while verifying that the reusable project storage already existed and matched.

This matters because Portfolio123 account work often needs authenticated browser state, but the project rules explicitly prohibit writing P123 passwords, API keys, cookies, tokens, or session values into repo files, docs, logs, screenshots, or chat output.

## Guidance

Use the Browser plugin when the user explicitly asks for the in-app browser or when a P123 browser login needs to be established inside Codex. For Portfolio123-specific work, load the Portfolio123 skill first so authentication and validation rules are in scope.

For the login itself:

1. Open `https://www.portfolio123.com/`.
2. If the page shows `Sign In`, navigate to `https://www.portfolio123.com/login.jsp` when clicking the nav link is unreliable.
3. Fill `input[name="LoginUsername"]` and `input[name="LoginPassword"]`.
4. Submit the login form.
5. Verify success by landing on `https://www.portfolio123.com/app/dashboard` with the title `Dashboard - Portfolio123`.

For credential persistence:

1. Prefer the existing encrypted file: `secrets/portfolio123.local.secrets.clixml`.
2. Load it through `scripts/Import-Portfolio123Secrets.ps1` when commands need environment variables.
3. If the user supplies credentials, compare them to the encrypted secret file without printing the password or API keys.
4. If the encrypted file already matches, leave it unchanged.
5. If it does not match, update only the DPAPI-encrypted file, keeping the plaintext out of docs, logs, terminal output, screenshots, and chat.

The import script sets these environment variables for the current PowerShell process:

```powershell
.\scripts\Import-Portfolio123Secrets.ps1
```

```text
PORTFOLIO123_USERNAME
PORTFOLIO123_PASSWORD
P123_API_ID
P123_API_KEY
```

Do not print those values. When a command needs them, pass them through environment variables.

## Why This Matters

The encrypted local secret file gives future agents a durable way to authenticate without normalizing plaintext credential storage. DPAPI encryption also scopes the file to the current Windows user and machine, which fits this workspace's local-research setup better than a portable plaintext `.env`.

The Browser plugin login establishes an authenticated Codex in-app browser session, which is useful for immediate P123 UI workflows. The encrypted secret file is separate from browser session state: it supports future scripted login or API work, but it does not expose cookies or session tokens.

## When to Apply

- The user asks Codex to log into Portfolio123 through the in-app Browser plugin.
- The user provides P123 credentials and asks to store them for repeated use.
- The current task only needs authentication setup, not creation, deletion, rebalancing, training, or other account-changing P123 actions.
- A future workflow needs credentials available as environment variables without hard-coding them.

## Examples

Verify the encrypted file has the expected fields without printing secret values:

```powershell
$secrets = Import-Clixml -LiteralPath 'secrets/portfolio123.local.secrets.clixml'
[pscustomobject]@{
  HasUsername = -not [string]::IsNullOrWhiteSpace([string]$secrets.Portfolio123Username)
  HasPassword = $null -ne $secrets.Portfolio123Password
  HasApiId = $null -ne $secrets.P123ApiId
  HasApiKey = $null -ne $secrets.P123ApiKey
}
```

For a private equality check, convert a `SecureString` only inside the current process and immediately zero the unmanaged buffer:

```powershell
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secrets.Portfolio123Password)
try {
  $existingPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
}
finally {
  [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
}
```

Use the comparison result only as a boolean, such as `Portfolio123WebCredentialsMatch = True`; never print the password itself.

## Related

- `AGENTS.md` section `Authentication And Secrets`
- `scripts/Import-Portfolio123Secrets.ps1`
- `docs/solutions/workflow-issues/portfolio123-browser-navigation-ai-factors-2026-05-16.md`

---

## Tags

#portfolio123 #authentication #browser-plugin #encrypted-secrets #dpapi #credential-handling #algo-trading/portfolio123 #work/solutions #work/workflow-issues
