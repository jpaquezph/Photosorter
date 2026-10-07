#!/usr/bin/env bash
# Genera dist/PhotoSorter.app: bundle standalone de macOS para distribuir a
# testers, con el icono de la app embebido.
#
# Requiere haber corrido antes (una sola vez):
#   uv sync --dev
#   uv pip install pyinstaller
#
# Uso: desde la raiz del repo, ./packaging/build_mac.sh
#
# --onedir (no --onefile): en macOS un .app ya es el "unico archivo" que ve
# el usuario en Finder; --onefile + --windowed esta deprecado en PyInstaller
# (no tiene sentido combinarlos y rompe el firmado del bundle).
#
# Nota: el bundle resultante no esta firmado ni notarizado (Apple Developer
# ID). Al abrirlo en otra Mac, Gatekeeper lo va a marcar como de origen no
# identificado la primera vez (click derecho -> Abrir, o Ajustes del Sistema
# -> Privacidad y Seguridad -> "Abrir de todas formas").

set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

.venv/bin/pyinstaller \
    --onedir \
    --windowed \
    --name PhotoSorter \
    --icon "src/photosorter/resources/icon.icns" \
    --add-data "src/photosorter/resources:resources" \
    --paths src \
    --noconfirm \
    "packaging/run_photosorter.py"

echo "Listo: dist/PhotoSorter.app"
