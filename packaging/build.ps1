# Genera dist/PhotoSorter.exe: un unico ejecutable standalone para
# distribuir a testers, con el icono de la app embebido.
#
# Requiere haber corrido antes (una sola vez):
#   uv sync --dev
#   .venv\Scripts\pip.exe install pyinstaller
#
# Uso: desde la raiz del repo, .\packaging\build.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

& ".venv\Scripts\pyinstaller.exe" `
    --onefile `
    --windowed `
    --name PhotoSorter `
    --icon "src\photosorter\resources\icon.ico" `
    --add-data "src\photosorter\resources;resources" `
    --paths src `
    --noconfirm `
    "packaging\run_photosorter.py"

Write-Host "Listo: dist\PhotoSorter.exe"
