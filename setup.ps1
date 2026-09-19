param([switch]$SkipAddin, [switch]$ReplaceAddin, [string]$AddinTarget = '', [string]$CacheDir = '')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git first: https://git-scm.com/download/win' }
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'Install uv first: https://docs.astral.sh/uv/getting-started/installation/' }
if (-not $SkipAddin -and -not $AddinTarget -and (Get-Process Fusion360 -ErrorAction SilentlyContinue)) { throw 'Close Fusion before add-in installation, or use -SkipAddin to prepare dependencies only.' }
& uv sync --frozen
if ($LASTEXITCODE -ne 0) { throw 'Helper dependency installation failed' }
$argsList = @('run','--frozen','python','scripts/setup/bootstrap.py')
if ($SkipAddin) { $argsList += '--skip-addin' }
if ($ReplaceAddin) { $argsList += '--replace-addin' }
if ($AddinTarget) { $argsList += @('--addin-target',$AddinTarget) }
if ($CacheDir) { $argsList += @('--cache-dir',$CacheDir) }
& uv @argsList
if ($LASTEXITCODE -ne 0) { throw 'MCP preparation failed; see output above' }
& uv run --frozen python scripts/setup/doctor.py
if ($LASTEXITCODE -ne 0) { throw 'Local readiness check failed' }
Write-Host 'Local setup complete. Follow SETUP.md for first-time Fusion activation and client consent.'
