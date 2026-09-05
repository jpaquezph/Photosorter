from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.photo import Photo


class SourceFolderError(Exception):
    """Se lanza cuando la carpeta de origen no es valida para escanear.

    Ver Docs/Requisitos V1.0.md, seccion 7 (la carpeta debe existir, ser
    legible y accesible) y Docs/Technical Design Document (TDD).md,
    seccion 13.3 (errores de configuracion, a detectar antes de procesar).
    """


class FileScanner(Protocol):
    """Contrato para encontrar las fotografias a procesar en una carpeta.

    Ver Docs/Technical Design Document (TDD).md, seccion 7.1.
    No lee metadata, no clasifica, no copia archivos: solo encuentra.
    """

    def scan(self, settings: AppSettings) -> list[Photo]:
        ...
