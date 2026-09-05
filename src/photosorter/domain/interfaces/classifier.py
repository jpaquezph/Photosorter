from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.classification import Classification
from photosorter.domain.models.photo_metadata import PhotoMetadata


class Classifier(Protocol):
    """Contrato para determinar la Classification de una PhotoMetadata.

    Ver Docs/Contract Specification - Domain Models.md, seccion 6, y
    Docs/Technical Design Document (TDD).md, seccion 7.3.
    """

    def classify(self, metadata: PhotoMetadata) -> Classification:
        ...
