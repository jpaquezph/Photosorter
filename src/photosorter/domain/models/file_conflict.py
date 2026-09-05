from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileConflict:
    """Representa una colision entre el archivo a copiar y uno ya existente.

    Ver Docs/Contract Specification - Domain Models.md, seccion 8.
    Debe conservar las rutas completas para que la UI pueda distinguir
    archivos con el mismo nombre provenientes de carpetas distintas.
    """

    source_path: Path
    destination_path: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_path", Path(self.source_path))
        object.__setattr__(self, "destination_path", Path(self.destination_path))
