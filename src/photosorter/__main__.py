from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from photosorter.ui.main_window import STYLE_SHEET, MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    # A nivel de aplicacion (no solo en MainWindow) para que dialogos como
    # ConflictDialog y los QMessageBox hereden la misma paleta.
    app.setStyleSheet(STYLE_SHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
