param(
  [string]$Path = (Join-Path $PSScriptRoot '..\secrets\portfolio123.local.secrets.clixml')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertFrom-LocalSecureString {
  param([Parameter(Mandatory = $true)][securestring]$SecureString)

  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
  try {
    [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  }
  finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
  }
}

$resolved = Resolve-Path -LiteralPath $Path
$secrets = Import-Clixml -LiteralPath $resolved

$env:PORTFOLIO123_USERNAME = [string]$secrets.Portfolio123Username
$env:PORTFOLIO123_PASSWORD = ConvertFrom-LocalSecureString $secrets.Portfolio123Password
$env:P123_API_ID = ConvertFrom-LocalSecureString $secrets.P123ApiId
$env:P123_API_KEY = ConvertFrom-LocalSecureString $secrets.P123ApiKey

[pscustomobject]@{
  Loaded = $true
  SecretFile = $resolved.Path
  Variables = @(
    'PORTFOLIO123_USERNAME',
    'PORTFOLIO123_PASSWORD',
    'P123_API_ID',
    'P123_API_KEY'
  )
}
