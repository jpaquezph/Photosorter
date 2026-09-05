from __future__ import annotations

from typing import Protocol

from photosorter.domain.models.photo import Photo
from photosorter.domain.models.photo_metadata import PhotoMetadata


class ImageReaderError(Exception):
    """Se lanza cuando un ImageReader no puede leer una fotografia.

    Representa un error de lectura individual (archivo corrupto, formato no
    soportado, etc). Quien orquesta el procesamiento decide si continua con
    el resto de las fotografias (ver TDD, seccion 13.1 y 14).
    """


class ImageReader(Protocol):
    """Contrato para obtener PhotoMetadata a partir de un Photo.

    Ver Docs/Technical Design Document (TDD).md, seccion 7.2.
    Implementaciones concretas (StandardImageReader, RawImageReader) viven
    en infrastructure/image y no deben conocerse entre si.
    """

    def can_read(self, photo: Photo) -> bool:
        """Indica si esta implementacion sabe leer el formato de photo."""
        ...

    def read(self, photo: Photo) -> PhotoMetadata:
        """Lee photo y devuelve su PhotoMetadata.

        Lanza ImageReaderError si el archivo no puede leerse.
        """
        ...
