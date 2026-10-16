[CmdletBinding()]
param(
    [switch]$Install,
    [string]$PythonExe = '',
    [string]$BlenderExe = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$cacheRoot = Join-Path $projectRoot '.display-tools'
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
$blenderVersion = '4.5.14'
$blenderArchive = "blender-$blenderVersion-windows-x64.zip"
$blenderHash = 'b9533d2397ac1984db4466fb23a7a4649391cca93f6e84209f9bcc60d071c8b9'
$portableBlender = Join-Path $cacheRoot "blender-$blenderVersion-windows-x64\blender.exe"
if (!(Test-Path -LiteralPath 'C:\Windows\Fonts\arialbd.ttf')) { throw 'Arial Bold fehlt; fuer dieselbe Textdarstellung zuerst die Windows-Schrift pruefen. Siehe TOOLCHAIN.md.' }

function Run-Checked([string]$Exe, [string[]]$Arguments) {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Command failed ($LASTEXITCODE): $Exe" }
}
function Find-Python {
    if ($PythonExe) { return (Get-Item -LiteralPath $PythonExe).FullName }
    if (Test-Path -LiteralPath $venvPython) { return $venvPython }
    $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) { return $bundledPython }
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($launcher) {
        $found = & $launcher.Source -3 -c 'import sys; print(sys.executable)' 2>$null
        if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $found)) { return $found }
    }
    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command -and $command.Source -notmatch 'WindowsApps') { return $command.Source }
    throw 'Python fehlt. Python 3.12 x64 von python.org installieren oder -PythonExe mit dem echten python.exe-Pfad angeben. Danach erneut ausfuehren.'
}

$python = Find-Python
Run-Checked $python @('-c', 'import sys; assert (3,11) <= sys.version_info[:2] < (3,14), ''Python 3.11 bis 3.13 erforderlich''; print(sys.version)')
if ($Install) {
    if (!(Test-Path -LiteralPath $venvPython)) { Run-Checked $python @('-m', 'venv', (Join-Path $projectRoot '.venv')) }
    $python = $venvPython
    Run-Checked $python @('-m', 'pip', 'install', '-r', (Join-Path $PSScriptRoot 'display-requirements.txt'))
}
# Fail before downloading Blender when Python dependencies are missing or differ.
Run-Checked $python @('-c', 'import importlib.metadata as m; expected={''Pillow'':''12.3.0'',''numpy'':''2.3.5'',''imageio-ffmpeg'':''0.6.0''}; actual={p:m.version(p) for p in expected}; print(actual); assert actual==expected, ''Pakete fehlen oder weichen ab. Mit -Install einrichten.''')
if (!$BlenderExe -and (Test-Path -LiteralPath $portableBlender)) { $BlenderExe = $portableBlender }
if (!$BlenderExe) {
    $command = Get-Command blender -ErrorAction SilentlyContinue
    if ($command) {
        $version = & $command.Source --version
        if ($LASTEXITCODE -eq 0 -and $version[0] -eq "Blender $blenderVersion LTS") { $BlenderExe = $command.Source }
    }
}
if (!$BlenderExe -and $Install) {
    if (![Environment]::Is64BitOperatingSystem -or $env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { throw 'Dieses Setup ist fuer Windows x64; andere Plattformen siehe TOOLCHAIN.md.' }
    New-Item -ItemType Directory -Path $cacheRoot -Force | Out-Null
    $archivePath = Join-Path $cacheRoot $blenderArchive
    if (!(Test-Path -LiteralPath $archivePath)) {
        $downloadPath = "$archivePath.download"
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -UseBasicParsing -Uri "https://download.blender.org/release/Blender4.5/$blenderArchive" -OutFile $downloadPath
        if ((Get-FileHash -LiteralPath $downloadPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $blenderHash) { throw 'Blender-Download: SHA-256 stimmt nicht. Datei wird nicht ausgefuehrt.' }
        Move-Item -LiteralPath $downloadPath -Destination $archivePath -Force
    }
    if ((Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $blenderHash) { throw 'Blender-Archiv: SHA-256 stimmt nicht.' }
    Expand-Archive -LiteralPath $archivePath -DestinationPath $cacheRoot -Force
    $BlenderExe = $portableBlender
}
if (!$BlenderExe) { throw 'Blender 4.5.14 LTS fehlt. Mit -Install einrichten oder -BlenderExe angeben.' }
$BlenderExe = (Get-Item -LiteralPath $BlenderExe).FullName
$version = & $BlenderExe --version
if ($LASTEXITCODE -ne 0 -or $version[0] -ne "Blender $blenderVersion LTS") { throw 'Blender muss Version 4.5.14 LTS sein.' }
Write-Output $version[0]
Run-Checked $python @('-c', 'import imageio_ffmpeg,subprocess; f=imageio_ffmpeg.get_ffmpeg_exe(); print(f); subprocess.run([f,''-version''],check=True,stdout=subprocess.DEVNULL)')
if ($Install) {
    New-Item -ItemType Directory -Path $cacheRoot -Force | Out-Null
    @{ python=$python; blender=$BlenderExe; checkedAt=(Get-Date -Format o) } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $cacheRoot 'toolchain.json') -Encoding UTF8
}
Write-Output "VERIFIED: Python=$python"
Write-Output "VERIFIED: Blender=$BlenderExe"
Write-Output 'Werkzeuge verfuegbar. Es wurde kein Produktionsrender gestartet.'
