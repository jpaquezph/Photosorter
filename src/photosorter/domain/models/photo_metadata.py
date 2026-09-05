from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PhotoMetadata:
    """Informacion tecnica obtenida de una fotografia por un ImageReader.

    Ver Docs/Contract Specification - Domain Models.md, seccion 5.
    """

    width: int
    height: int
    format: str
    camera_make: str | None = None
    camera_model: str | None = None
    lens: str | None = None
    orientation: int | None = None

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError(f"width debe ser > 0, recibido: {self.width}")
        if self.height <= 0:
            raise ValueError(f"height debe ser > 0, recibido: {self.height}")
        if not self.format:
            raise ValueError("format no puede estar vacio")
