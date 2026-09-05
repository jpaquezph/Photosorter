from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ProcessingStatus(Enum):
    """Estado final del procesamiento de una fotografia individual.

    Ver Docs/Contract Specification - Domain Models.md, seccion 10.3.
    """

    COPIED = "copied"
    SKIPPED = "skipped"
    OVERWRITTEN = "overwritten"
    FAILED = "failed"


@dataclass(frozen=True)
class ProcessingResult:
    """Resultado del procesamiento de una fotografia individual.

    Ver Docs/Contract Specification - Domain Models.md, seccion 10.
    """

    source_path: Path
    status: ProcessingStatus
    destination_path: Path | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_path", Path(self.source_path))

        if self.status in (ProcessingStatus.COPIED, ProcessingStatus.OVERWRITTEN):
            if self.destination_path is None:
                raise ValueError(f"{self.status} requiere destination_path")
            if self.error is not None:
                raise ValueError(f"{self.status} no deberia tener error")

        if self.status == ProcessingStatus.FAILED and not self.error:
            raise ValueError("FAILED requiere informacion de error")
