from __future__ import annotations

from enum import Enum


class ConflictResolution(Enum):
    """Decision tomada por el usuario frente a un FileConflict.

    Ver Docs/Contract Specification - Domain Models.md, seccion 9.
    RENAME queda fuera del contrato de V1 hasta que se incorpore al PRD.
    """

    SKIP = "skip"
    OVERWRITE = "overwrite"
