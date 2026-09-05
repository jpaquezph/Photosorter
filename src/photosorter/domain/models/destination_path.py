from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DestinationPath:
    """Ubicacion de destino calculada para una fotografia.

    Ver Docs/Contract Specification - Domain Models.md, seccion 7.
    Separado de Classification: la clasificacion dice que tipo de foto es,
    el destino dice donde debe copiarse.
    """

    path: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", Path(self.path))
