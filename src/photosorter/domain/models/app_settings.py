from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    """Configuracion necesaria para ejecutar una operacion de organizacion.

    Ver Docs/Contract Specification - Domain Models.md, seccion 11.
    No representa configuracion visual de la aplicacion.
    """

    source_path: Path
    destination_path: Path
    recursive: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_path", Path(self.source_path))
        object.__setattr__(self, "destination_path", Path(self.destination_path))
