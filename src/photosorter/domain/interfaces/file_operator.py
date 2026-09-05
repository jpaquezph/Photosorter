from __future__ import annotations

from pathlib import Path
from typing import Protocol


class DestinationAlreadyExistsError(Exception):
    """Se lanza cuando el archivo de destino ya existe y no se pidio overwrite.

    Ver Docs/System Architecture Document - SAD.md, seccion 14/15, y
    decision de diseno D7 del TDD: no se sobrescribe silenciosamente.

    Quien orquesta el procesamiento (ConflictService, a incorporar en M2)
    debe capturar este error, construir un FileConflict y pedirle al
    usuario una ConflictResolution.
    """

    def __init__(self, source_path: Path, destination_path: Path) -> None:
        super().__init__(f"El destino ya existe: {destination_path} (origen: {source_path})")
        self.source_path = source_path
        self.destination_path = destination_path


class FileOperator(Protocol):
    """Contrato para ejecutar la operacion de archivo sobre una fotografia.

    Ver Docs/Technical Design Document (TDD).md, seccion 7.5.
    V1 solo tiene CopyFileOperator; MoveFileOperator queda para el futuro
    sin necesidad de modificar este contrato.
    """

    def copy(self, source_path: Path, destination_path: Path, *, overwrite: bool = False) -> None:
        """Copia source_path a destination_path.

        Crea los directorios intermedios de destination_path si no existen.
        Si destination_path ya existe y overwrite es False, lanza
        DestinationAlreadyExistsError sin tocar el archivo existente ni el
        origen.
        """
        ...
