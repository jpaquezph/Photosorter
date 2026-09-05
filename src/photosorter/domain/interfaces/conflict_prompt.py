from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.file_conflict import FileConflict


class ConflictPrompt(Protocol):
    """Contrato para pedir una decision humana frente a un FileConflict.

    Ver Docs/System Architecture Document - SAD.md, seccion 14 (flujo
    FileOperator -> FileConflict -> ConflictService -> UI -> User Decision).

    El dominio no conoce PySide6: en V1 la UI (M4) implementara este
    contrato mostrando origen/destino y las opciones SKIP/OVERWRITE, mas el
    checkbox de "aplicar a los restantes" (Requisitos V1.0, seccion 3.1).
    """

    def ask(self, conflict: FileConflict) -> ConflictDecision:
        ...
