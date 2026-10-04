from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from photosorter.ui.assets import ICON_PATH
from photosorter.ui.main_window import STYLE_SHEET, MainWindow


def main() -> None:
    if sys.platform == "win32":
        # Identidad propia de AppUserModelID: evita que Windows agrupe la
        # ventana bajo el icono generico de python.exe en la barra de tareas.
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Photosorter.App")

    app = QApplication(sys.argv)
    # A nivel de aplicacion (no solo en MainWindow) para que dialogos como
    # ConflictDialog y los QMessageBox hereden la misma paleta.
    app.setStyleSheet(STYLE_SHEET)
    icon = QIcon(str(ICON_PATH))
    app.setWindowIcon(icon)
    window = MainWindow()
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
