[CmdletBinding()]
param(
    [string]$Repo = (Join-Path $HOME 'Documents\GitHub\fusion-agentic-workflow'),
    # Optional: a previous checkout whose skill dirs should be removed from skills.external_dirs.
    [string]$OldRepo = '',
    [switch]$Apply,
    [switch]$ArchiveLegacyIdentity,
    [switch]$Launch
)
$ErrorActionPreference = 'Stop'
# Preview by default. No history, credentials, MCP registrations, or unrelated skills are deleted.
function Invoke-Hermes {
    param([string[]]$CliArgs)
    $result = & hermes @CliArgs
    if ($LASTEXITCODE -ne 0) { throw "Hermes failed: $($CliArgs -join ' ')" }
    return $result
}
function Normalize-Path([string]$Path) {
    return [IO.Path]::GetFullPath($Path).TrimEnd('\','/').Replace('\','/').ToLowerInvariant()
}
if (-not (Get-Command hermes -ErrorAction SilentlyContinue)) { throw 'hermes is not on PATH.' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'git is not on PATH.' }
$Repo = [IO.Path]::GetFullPath($Repo)
if (-not (Test-Path -LiteralPath (Join-Path $Repo '.git'))) { throw "Clone https://github.com/nvsdef/fusion-agentic-workflow.git into $Repo first." }
$remote = & git -C $Repo remote get-url origin
if ($LASTEXITCODE -ne 0 -or $remote -notmatch 'github\.com[:/]nvsdef/fusion-agentic-workflow(?:\.git)?$') { throw 'Unexpected repository origin; refusing migration.' }
$dirty = & git -C $Repo status --porcelain --untracked-files=no
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect repository.' }
if ($dirty) { throw 'Tracked repository edits exist. Commit/stash them before migration; this script will not overwrite skills.' }
$newDirs = @((Join-Path $Repo 'agents/cad-engineer/skills'), (Join-Path $Repo 'plugins/fusion-mcp/skills'))
foreach ($dir in $newDirs) { if (-not (Test-Path -LiteralPath $dir)) { throw "Missing skills: $dir" } }
$configPath = ((Invoke-Hermes -CliArgs @('config','path')) -join "`n").Trim()
if (-not (Test-Path -LiteralPath $configPath)) { throw "Config path does not exist: $configPath" }
$hermesHome = Split-Path -Parent $configPath
if ($hermesHome -match '[\\/]profiles[\\/]') { throw 'This script targets the default profile only. Switch to it explicitly before continuing.' }
$raw = (Invoke-Hermes -CliArgs @('config','get','skills.external_dirs','--json')) -join "`n"
$oldDirs = @($raw | ConvertFrom-Json | ForEach-Object { $_ } | ForEach-Object { [string]$_ })
if ($raw.TrimStart().StartsWith('{')) {
    $obj = $raw | ConvertFrom-Json
    $oldDirs = @($obj.PSObject.Properties | Sort-Object Name | ForEach-Object { [string]$_.Value })
}
if ($oldDirs.Count -eq 1 -and $oldDirs[0].StartsWith("['")) {
    # Recover the previous migration's rejected YAML-as-string value, without eval.
    $oldDirs = @([regex]::Matches($oldDirs[0], "'([^']*)'") | ForEach-Object { $_.Groups[1].Value })
}
$oldRoots = @()
if ($OldRepo) { $oldRoots = @((Normalize-Path (Join-Path $OldRepo 'agents/cad-engineer/skills')), (Normalize-Path (Join-Path $OldRepo 'plugins/fusion-mcp/skills'))) }
$keep = @($oldDirs | Where-Object { $_ -and (Normalize-Path $_) -notin $oldRoots })
$desired = @($keep + $newDirs | ForEach-Object { ([IO.Path]::GetFullPath($_)).Replace('\','/') } | Select-Object -Unique)
$known = @('slab-run','slab-product-spec','slab-build','fusion-api','fusion-mcp-core','fusion-mcp-driving','fusion-mcp-host','fusion-scratch-build','fusion-photoreal-render','fusion-2d-drawings','fusion-product-design')
$skillsRoot = Join-Path $hermesHome 'skills'
$legacy = @()
if (Test-Path -LiteralPath $skillsRoot) {
    # Only exact known CAD skill directory names containing SKILL.md; not text matches like 'diffusion'.
    $legacy = @(Get-ChildItem -LiteralPath $skillsRoot -Filter SKILL.md -File -Recurse | Where-Object {
        $_.Directory.Name -in $known -and -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint)
    } | ForEach-Object { $_.Directory.FullName } | Select-Object -Unique)
    foreach ($dir in $legacy) {
        $cursor = Get-Item -LiteralPath $dir
        while ($cursor -and $cursor.FullName -ne $skillsRoot) {
            if ($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing linked legacy skill directory: $dir" }
            $cursor = $cursor.Parent
        }
    }
}
$soul = Join-Path $hermesHome 'SOUL.md'
$legacySoul = $false
if (Test-Path -LiteralPath $soul) {
    $text = Get-Content -LiteralPath $soul -Raw
    $legacySoul = $text.Contains('# CAD Engineer') -and $text.Contains('SLAB')
}
Write-Host "Target workspace: $Repo"
Write-Host "Active Hermes home: $hermesHome"
Write-Host 'External skill directories after migration:'
$desired | ForEach-Object { Write-Host "  $_" }
Write-Host 'Exact-name installed Fusion skill folders to archive:'
$legacy | ForEach-Object { Write-Host "  $_" }
Write-Host "Legacy global CAD identity found: $legacySoul; archive requested: $ArchiveLegacyIdentity"
if (-not $Apply) {
    Write-Host 'PREVIEW ONLY. Rerun with -Apply. Add -ArchiveLegacyIdentity to remove the old global CAD identity after backing it up.'
    return
}
# Only fast-forward; never reset user changes or rewrite history.
& git -C $Repo pull --ff-only
if ($LASTEXITCODE -ne 0) { throw 'Git update failed; migration not applied.' }
$backup = Join-Path $hermesHome ('migration-backups\fusion-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
# Config backup stays private/local: it may contain sensitive configuration. Never upload it.
Copy-Item -LiteralPath $configPath -Destination (Join-Path $backup 'config.yaml')
$oldDirs | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $backup 'previous-external-dirs.json')
# This Hermes version's config set only coerces scalar values, not arrays.
# Use its supported editor entry point with a scoped, backed-up list editor.
$savedEditor = $env:EDITOR
$savedDirs = $env:FUSION_SKILL_DIRS_JSON
try {
    $env:EDITOR = Join-Path $PSScriptRoot 'hermes_skill_editor.cmd'
    $env:FUSION_SKILL_DIRS_JSON = ConvertTo-Json -InputObject @($desired) -Compress
    Invoke-Hermes -CliArgs @('config','edit') | Out-Host
} finally {
    $env:EDITOR = $savedEditor
    $env:FUSION_SKILL_DIRS_JSON = $savedDirs
}
$verifiedRaw = (Invoke-Hermes -CliArgs @('config','get','skills.external_dirs','--json')) -join "`n"
$verified = @($verifiedRaw | ConvertFrom-Json | ForEach-Object { $_ } | ForEach-Object { [string]$_ })
if (($verified -join '|') -ne ($desired -join '|')) { throw "Readback mismatch. Backup: $backup. No legacy folders were moved." }
$moves = @()
foreach ($dir in ($legacy | Sort-Object Length -Descending)) {
    if (-not (Test-Path -LiteralPath $dir)) { continue }
    $relative = $dir.Substring($skillsRoot.Length).TrimStart('\','/')
    $destination = Join-Path (Join-Path $backup 'skills') $relative
    New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
    Move-Item -LiteralPath $dir -Destination $destination
    $moves += @{from=$dir;to=$destination}
}
if ($ArchiveLegacyIdentity -and $legacySoul) {
    Move-Item -LiteralPath $soul -Destination (Join-Path $backup 'SOUL.md')
    $moves += @{from=$soul;to=(Join-Path $backup 'SOUL.md')}
}
$moves | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $backup 'moved-files.json')
Set-Location -LiteralPath $Repo
Write-Host "DONE. Backup: $backup"
Write-Host 'Unrelated skills, memories, sessions, credentials, MCP settings and approval policy were preserved.'
Write-Host 'Open this folder as the Hermes desktop project, then start a NEW chat. Do not resume the old CAD session.'
Write-Host 'CLI: hermes chat --in <repo> --skills slab-run --max-turns 150'
Write-Host 'Rollback: restore moved-files.json entries to their original paths and restore external_dirs using hermes config edit; do not replace newer config wholesale.'
if ($Launch) { & hermes chat --in $Repo --skills slab-run --max-turns 150 }
