from __future__ import annotations

import shutil
from pathlib import Path

from photosorter.domain.interfaces.file_operator import DestinationAlreadyExistsError


class CopyFileOperator:
    """FileOperator de V1: copia archivos sin modificar el origen.

    Ver Docs/Technical Design Document (TDD).md, seccion 7.5, y
    decision de diseno D1 (operacion segura) y D7 (sin sobrescritura
    silenciosa).
    """

    def copy(self, source_path: Path, destination_path: Path, *, overwrite: bool = False) -> None:
        source_path = Path(source_path)
        destination_path = Path(destination_path)

        # CA-09: si la carpeta de destino (Verticales/Horizontales/Cuadradas)
        # ya existe, no debe fallar ni tocar su contenido.
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        if destination_path.exists() and not overwrite:
            raise DestinationAlreadyExistsError(source_path, destination_path)

        # copy2 preserva metadata (fechas, permisos) y nunca modifica el
        # origen (CA-07).
        shutil.copy2(source_path, destination_path)
