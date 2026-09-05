from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.classification import Classification
from photosorter.domain.models.destination_path import DestinationPath
from photosorter.domain.models.photo import Photo


class DestinationResolver(Protocol):
    """Contrato para determinar donde debe terminar una fotografia.

    Ver Docs/Technical Design Document (TDD).md, seccion 7.4.
    No copia archivos: solo calcula la ruta de destino.
    """

    def resolve(
        self, photo: Photo, classification: Classification, settings: AppSettings
    ) -> DestinationPath:
        ...
