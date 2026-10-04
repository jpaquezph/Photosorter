"""Punto de entrada para el build de PyInstaller (ver packaging/build.ps1).

No forma parte del paquete distribuido via pip/uv: PyInstaller necesita un
script, no un modulo `-m`, para analizar el arbol de imports.
"""

from photosorter.__main__ import main

if __name__ == "__main__":
    main()
