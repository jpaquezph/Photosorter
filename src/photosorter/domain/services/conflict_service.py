from __future__ import annotations

from pathlib import Path

from photosorter.domain.interfaces.conflict_prompt import ConflictPrompt
from photosorter.domain.interfaces.file_operator import DestinationAlreadyExistsError, FileOperator
from photosorter.domain.models.conflict_resolution import ConflictResolution
from photosorter.domain.models.file_conflict import FileConflict
from photosorter.domain.models.processing_result import ProcessingResult, ProcessingStatus


class ConflictService:
    """Copia un archivo resolviendo conflictos de destino cuando aparecen.

    Ver Docs/System Architecture Document - SAD.md, seccion 14: envuelve a
    FileOperator y, si el destino ya existe (DestinationAlreadyExistsError),
    construye un FileConflict y le pide una decision a un ConflictPrompt
    (implementado por la UI en M4).

    No maneja otros errores (lectura, filesystem, etc): esos son
    responsabilidad de quien orqueste el procesamiento completo (TDD,
    seccion 13-14), no de este servicio.

    Recuerda la decision cuando el usuario pide "aplicar a los restantes"
    (Requisitos V1.0, seccion 3.1) y la reutiliza sin volver a preguntar.
    """

    def __init__(self, file_operator: FileOperator, prompt: ConflictPrompt) -> None:
        self._file_operator = file_operator
        self._prompt = prompt
        self._remembered_resolution: ConflictResolution | None = None

    def copy(self, source_path: Path, destination_path: Path) -> ProcessingResult:
        try:
            self._file_operator.copy(source_path, destination_path)
        except DestinationAlreadyExistsError as exc:
            return self._resolve_conflict(exc)

        return ProcessingResult(
            source_path=source_path,
            status=ProcessingStatus.COPIED,
            destination_path=destination_path,
        )

    def _resolve_conflict(self, exc: DestinationAlreadyExistsError) -> ProcessingResult:
        conflict = FileConflict(
            source_path=exc.source_path, destination_path=exc.destination_path
        )

        if self._remembered_resolution is not None:
            resolution = self._remembered_resolution
        else:
            decision = self._prompt.ask(conflict)
            resolution = decision.resolution
            if decision.apply_to_remaining:
                self._remembered_resolution = resolution

        return self._apply_resolution(resolution, conflict)

    def _apply_resolution(
        self, resolution: ConflictResolution, conflict: FileConflict
    ) -> ProcessingResult:
        if resolution == ConflictResolution.SKIP:
            return ProcessingResult(
                source_path=conflict.source_path,
                status=ProcessingStatus.SKIPPED,
                destination_path=conflict.destination_path,
            )

        if resolution == ConflictResolution.OVERWRITE:
            self._file_operator.copy(
                conflict.source_path, conflict.destination_path, overwrite=True
            )
            return ProcessingResult(
                source_path=conflict.source_path,
                status=ProcessingStatus.OVERWRITTEN,
                destination_path=conflict.destination_path,
            )

        raise ValueError(f"ConflictResolution no soportada: {resolution}")
