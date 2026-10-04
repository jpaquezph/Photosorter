from __future__ import annotations

import sys
from pathlib import Path

# En un ejecutable de PyInstaller los recursos van sueltos junto al .exe,
# extraidos a sys._MEIPASS (ver pyproject.toml / script de build); en
# desarrollo caen adentro del paquete photosorter.
_BASE_DIR = Path(getattr(sys, "_MEIPASS", None) or Path(__file__).parent.parent)

ICON_PATH = _BASE_DIR / "resources" / "icon.ico"
# Marca sin fondo y con el trazo en claro, pensada para la paleta oscura de
# la app (ver resources/_build_icon.py).
LOGO_PATH = _BASE_DIR / "resources" / "logo.png"
