from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Photo:
    """Representa un archivo de fotografia identificado para ser procesado.

    Ver Docs/Contract Specification - Domain Models.md, seccion 4.
    """

    source_path: Path

    def __post_init__(self) -> None:
        if self.source_path is None:
            raise ValueError("source_path no puede ser None")

        path = Path(self.source_path)
        if str(path) == "":
            raise ValueError("source_path no puede estar vacio")

        # No se exige que el archivo exista (eso es responsabilidad del
        # componente que interactua con el filesystem), pero si existe y es
        # un directorio, es un estado invalido.
        if path.exists() and path.is_dir():
            raise ValueError(f"source_path debe apuntar a un archivo, no a un directorio: {path}")

        object.__setattr__(self, "source_path", path)

    @property
    def filename(self) -> str:
        return self.source_path.name

    @property
    def extension(self) -> str:
        return self.source_path.suffix
