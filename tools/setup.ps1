# tools/setup.ps1 — Windows bootstrap for the bm project.
# Run from the repo root in PowerShell:  powershell -ExecutionPolicy Bypass -File tools\setup.ps1
#
# NOTE: authored on macOS, NOT yet tested on a Windows machine.
# If something fails, the two things it does are simple enough to do by hand:
#   1. Download gbdk-win64.zip from the GBDK-2020 release and unzip to tools\gbdk\
#   2. git clone --depth 1 --filter=blob:none --sparse the pokecrystal repo (gfx + audio)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$GbdkVersion = "4.5.0"
$GbdkArchive = "gbdk-win64.zip"
$GbdkUrl = "https://github.com/gbdk-2020/gbdk-2020/releases/download/$GbdkVersion/$GbdkArchive"

if (-not (Test-Path "tools\gbdk\bin\lcc.exe")) {
    Write-Host "==> Downloading GBDK-2020 $GbdkVersion (win64)"
    Invoke-WebRequest -Uri $GbdkUrl -OutFile "tools\$GbdkArchive"
    Expand-Archive -Path "tools\$GbdkArchive" -DestinationPath "tools\" -Force
    Remove-Item "tools\$GbdkArchive"
} else {
    Write-Host "==> GBDK already present at tools\gbdk\"
}

if (-not (Test-Path "gfx\pokecrystal-src\.git")) {
    Write-Host "==> Sparse-cloning pret/pokecrystal for asset source"
    git clone --depth 1 --filter=blob:none --sparse `
        https://github.com/pret/pokecrystal.git gfx\pokecrystal-src
    Push-Location gfx\pokecrystal-src
    git sparse-checkout set gfx audio
    git checkout
    Pop-Location
} else {
    Write-Host "==> pokecrystal-src already present"
}

Write-Host "==> Done. Build with GBDK's make, e.g.:  tools\gbdk\bin\make.exe"
Write-Host "    (or GNU make if you have it on PATH)"
