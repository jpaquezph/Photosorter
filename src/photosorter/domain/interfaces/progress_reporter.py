from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.photo import Photo
from photosorter.domain.models.processing_result import ProcessingResult
from photosorter.domain.models.processing_summary import ProcessingSummary


class ProgressReporter(Protocol):
    """Contrato para que SorterService informe avance sin conocer la UI.

    Ver Docs/Technical Design Document (TDD).md, seccion 23-24, y
    Docs/Requisitos V1.0.md, seccion 12-15 (pantalla de progreso y resumen).

    La UI (M4, PySide6) implementa esto para actualizar la barra de
    progreso y el texto de estado; en tests o scripts sin UI se usa
    NullProgressReporter.
    """

    def on_started(self, total_files: int) -> None:
        ...

    def on_file_started(self, photo: Photo) -> None:
        ...

    def on_file_completed(
        self, processed_count: int, total_files: int, result: ProcessingResult
    ) -> None:
        ...

    def on_finished(self, summary: ProcessingSummary) -> None:
        ...
