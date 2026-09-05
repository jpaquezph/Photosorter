from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessingSummary:
    """Resultado global de procesar una carpeta completa de fotografias.

    Ver Docs/Requisitos V1.0.md, seccion 15, y
    Docs/Technical Design Document (TDD).md, seccion 6.7.

    Se llama "Summary" (no "ProcessingResult") a proposito, para no chocar
    con el modelo `ProcessingResult` del Contract Specification (seccion
    10), que representa el resultado de UNA fotografia individual. Ver
    Docs/CONTEXTO.md para el detalle de esta decision de naming, planteada
    en M0 y resuelta recien en M3.
    """

    total_files: int
    processed_files: int
    copied_files: int
    skipped_files: int
    overwritten_files: int
    failed_files: int
    vertical_count: int
    horizontal_count: int
    square_count: int
    cancelled: bool = False
