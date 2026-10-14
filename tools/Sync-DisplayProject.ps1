[CmdletBinding()]
param(
    [ValidateSet('Sync','Publish')][string]$Mode = 'Sync',
    [string]$LocalRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$SharedRoot = '\\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld'
)
$ErrorActionPreference = 'Stop'
$LocalRoot = [IO.Path]::GetFullPath($LocalRoot).TrimEnd('\')
$SharedRoot = [IO.Path]::GetFullPath($SharedRoot).TrimEnd('\')
if ($LocalRoot -eq $SharedRoot) { throw 'Use a local Git clone; the NAS copy is for reading.' }
$gitDir = & git -C $LocalRoot rev-parse --absolute-git-dir
if ($LASTEXITCODE -ne 0) { throw 'LocalRoot must be a Git checkout.' }
$statePath = Join-Path $gitDir 'display-nas-state.json'
$state = $null
$baseline = @{}
if (Test-Path -LiteralPath $statePath) {
    $state = Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($state.sharedRoot -ne $SharedRoot) { throw 'Stored state belongs to another NAS folder.' }
    foreach ($p in $state.hashes.PSObject.Properties) { $baseline[$p.Name] = [string]$p.Value }
}
function Get-Hash([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash }
function Check-Relative([string]$Relative) {
    if ($Relative -match '(^|/)(\.\.?|\.git|\.codex|__pycache__)(/|$)' -or [IO.Path]::IsPathRooted($Relative)) { throw "Forbidden project path: $Relative" }
    if ($Relative -in @('README.md','AGENTS.md','PC-UEBERGREIFEND.md','.gitignore','tools/Sync-DisplayProject.ps1')) { return }
    if ($Relative -notmatch '^ledshow-seefeld/' -or $Relative -notmatch '(\.(md|html|css|js|py|sh|mp4|avi|png|jpg|jpeg|webp|gif|json|ttf|otf)|/\.gitkeep)$') { throw "Not an approved display file: $Relative" }
}
function Inventory([string]$Root,[string[]]$Paths) {
    $map = @{}
    foreach ($relative in $Paths) {
        Check-Relative $relative
        $file = Join-Path $Root $relative
        if (Test-Path -LiteralPath $file -PathType Leaf) {
            $cursor = Get-Item -LiteralPath $file -Force
            while ($cursor.FullName.TrimEnd('\') -ne $Root) {
                if ($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked path forbidden: $relative" }
                $cursor = Get-Item -LiteralPath (Split-Path -Parent $cursor.FullName) -Force
            }
            $map[$relative] = Get-Hash $file
        }
    }
    return $map
}
function Copy-Verified([string]$From,[string]$To,[string]$Relative,[string]$Expected) {
    $source = Join-Path $From $Relative
    if ((Get-Hash $source) -ne $Expected) { throw "Source changed during transfer: $Relative" }
    $target = Join-Path $To $Relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
    if ((Get-Hash $target) -ne $Expected) { throw "SHA-256 verification failed: $Relative" }
}
$paths = @(& git -C $LocalRoot -c core.quotepath=false ls-files | Sort-Object -Unique)
if ($LASTEXITCODE -ne 0 -or !$paths.Count) { throw 'No Git-selected project files.' }
$parent = Split-Path -Parent $SharedRoot
if (!(Test-Path -LiteralPath $parent)) { throw 'NAS parent unavailable; local files preserved.' }
if (!(Test-Path -LiteralPath $SharedRoot)) {
    if ($Mode -eq 'Sync') { throw 'NAS project absent; first publish from the reviewed source clone.' }
    New-Item -ItemType Directory -Path $SharedRoot | Out-Null
}
$lockPath = Join-Path $parent ((Split-Path -Leaf $SharedRoot) + '.sync.lock')
$lock = $null
try {
    $lock = [IO.File]::Open($lockPath,[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
    $local = Inventory $LocalRoot $paths
    $shared = Inventory $SharedRoot $paths
    $push = @()
    $pull = @()
    foreach ($relative in $paths) {
        $l = $local[$relative]; $s = $shared[$relative]; $b = $baseline[$relative]
        if (!$l) { throw "Missing selected local file; deletions are never propagated: $relative" }
        if ($l -eq $s) { continue }
        if (!$b) {
            if ($s) { throw "Initial conflict; nothing copied: $relative" }
            if ($Mode -eq 'Publish') { $push += $relative }
            continue
        }
        if (!$s) { throw "NAS file missing; inspect before restoring: $relative" }
        if ($l -ne $b -and $s -ne $b) { throw "CONFLICT; reconcile both versions first; nothing copied: $relative" }
        if ($l -eq $b) { $pull += $relative }
        elseif ($Mode -eq 'Publish') { $push += $relative }
    }
    # All conflicts checked before any copy; cooperating clients share this SMB lock.
    foreach ($relative in $push) { Copy-Verified $LocalRoot $SharedRoot $relative $local[$relative] }
    foreach ($relative in $pull) { Copy-Verified $SharedRoot $LocalRoot $relative $shared[$relative] }
    $afterLocal = Inventory $LocalRoot $paths
    $afterShared = Inventory $SharedRoot $paths
    $next = @{}
    foreach ($relative in $paths) {
        if ($afterLocal[$relative] -eq $afterShared[$relative]) { $next[$relative] = $afterShared[$relative] }
        elseif ($baseline.ContainsKey($relative)) { $next[$relative] = $baseline[$relative] }
    }
    @{ sharedRoot=$SharedRoot; checkedAt=(Get-Date -Format o); hashes=$next } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $statePath -Encoding UTF8
    Write-Output ("VERIFIED: $($next.Count) matching files; $($push.Count) published; $($pull.Count) received. $SharedRoot")
} finally { if ($lock) { $lock.Dispose() } }
