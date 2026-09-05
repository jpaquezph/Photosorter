from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.conflict_resolution import ConflictResolution
from photosorter.domain.models.file_conflict import FileConflict


class ConflictDialog(QDialog):
    """Dialogo modal para pedirle al usuario que resuelva un FileConflict.

    Ver Docs/Requisitos V1.0.md, seccion 3.1 y 10, y
    Docs/System Architecture Document - SAD.md, seccion 14.

    V1 solo ofrece SKIP/OVERWRITE (ConflictResolution del Contract
    Specification); RENAME queda para una version futura.
    """

    def __init__(self, conflict: FileConflict, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("El archivo ya existe")
        self.setModal(True)
        # Si el usuario cierra el dialogo sin elegir (p.ej. con la X de la
        # ventana), se asume la opcion no destructiva por defecto.
        self._resolution: ConflictResolution = ConflictResolution.SKIP

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ya existe un archivo con el mismo nombre en el destino."))
        layout.addWidget(QLabel(f"Origen: {conflict.source_path}"))
        layout.addWidget(QLabel(f"Destino: {conflict.destination_path}"))

        self._apply_to_remaining = QCheckBox("Aplicar esta decision a los conflictos restantes")
        layout.addWidget(self._apply_to_remaining)

        buttons = QHBoxLayout()
        skip_button = QPushButton("Omitir")
        skip_button.clicked.connect(self._choose_skip)
        overwrite_button = QPushButton("Reemplazar")
        overwrite_button.clicked.connect(self._choose_overwrite)
        buttons.addWidget(skip_button)
        buttons.addWidget(overwrite_button)
        layout.addLayout(buttons)

    def _choose_skip(self) -> None:
        self._resolution = ConflictResolution.SKIP
        self.accept()

    def _choose_overwrite(self) -> None:
        self._resolution = ConflictResolution.OVERWRITE
        self.accept()

    def decision(self) -> ConflictDecision:
        return ConflictDecision(
            resolution=self._resolution,
            apply_to_remaining=self._apply_to_remaining.isChecked(),
        )
