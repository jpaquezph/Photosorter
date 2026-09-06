from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

# Paleta dark/profesional de main_window.py, duplicada aca a proposito (es
# un detalle de UI aislado, igual que RAW_EXTENSIONS en ui/thumbnail.py): la
# barra es opaca (tema sin transparencias > ~10%) y la cruz de cerrar
# siempre tiene tonalidad roja, no solo al pasar el mouse.
_BAR_BG = "#0B1626"
_TEXT = "#F2F5F8"
_BUTTON_BG = "#101D2F"
_BUTTON_BG_HOVER = "#294563"
_CLOSE_BG = "#E45B62"
_CLOSE_BG_HOVER = "#c94850"

BAR_HEIGHT = 34
_BUTTON_WIDTH = 46


class TitleBar(QWidget):
    """Barra de titulo propia de la ventana (sin marco nativo de Windows).

    Se necesita una barra propia porque el chrome nativo no permite darle a
    cada boton (minimizar/maximizar/cerrar) una transparencia distinta ni
    que el boton de cerrar tenga siempre tonalidad roja. Arrastrar la barra
    mueve la ventana y arrastrar los bordes de MainWindow la redimensiona,
    usando QWindow.startSystemMove()/startSystemResize() (ver main_window.py).
    """

    minimize_clicked = Signal()
    maximize_clicked = Signal()
    close_clicked = Signal()

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(BAR_HEIGHT)
        self.setStyleSheet(f"QWidget#titleBar {{ background-color: {_BAR_BG}; }}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(0)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color: {_TEXT}; font-weight: bold; background: transparent;"
        )
        layout.addWidget(title_label)
        layout.addStretch(1)

        self._minimize_button = self._make_button("–", _BUTTON_BG, _BUTTON_BG_HOVER)
        self._maximize_button = self._make_button("□", _BUTTON_BG, _BUTTON_BG_HOVER)
        self._close_button = self._make_button("✕", _CLOSE_BG, _CLOSE_BG_HOVER)

        self._minimize_button.clicked.connect(self.minimize_clicked)
        self._maximize_button.clicked.connect(self.maximize_clicked)
        self._close_button.clicked.connect(self.close_clicked)

        for button in (self._minimize_button, self._maximize_button, self._close_button):
            layout.addWidget(button)

    def _make_button(self, text: str, bg: str, bg_hover: str) -> QPushButton:
        button = QPushButton(text)
        button.setFixedSize(_BUTTON_WIDTH, BAR_HEIGHT)
        button.setCursor(Qt.CursorShape.ArrowCursor)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg};
                color: {_TEXT};
                border: none;
                border-radius: 0px;
                font-weight: bold;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
            }}
            """
        )
        return button

    # --- Arrastre de la ventana desde la barra de titulo ---

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.window().windowHandle()
            if window is not None:
                window.startSystemMove()
                return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximize_clicked.emit()
            return
        super().mouseDoubleClickEvent(event)
