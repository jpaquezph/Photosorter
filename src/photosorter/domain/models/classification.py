from __future__ import annotations

from enum import Enum


class Classification(Enum):
    """Resultado de clasificar una fotografia segun ancho/alto.

    Ver Docs/Contract Specification - Domain Models.md, seccion 6.
    No existe un valor UNKNOWN: si no se puede clasificar, es un error.
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    SQUARE = "square"
