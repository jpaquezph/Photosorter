from __future__ import annotations

from photosorter.domain.interfaces.image_reader import ImageReader, ImageReaderError
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.photo_metadata import PhotoMetadata


class CompositeImageReader:
    """Delega en el primer ImageReader de una lista que sepa leer el Photo.

    Permite que el resto del sistema dependa de un unico ImageReader sin
    conocer que existen implementaciones separadas para RAW y formatos
    estandar (ver Docs/System Architecture Document - SAD.md, seccion 8).
    """

    def __init__(self, readers: list[ImageReader]) -> None:
        self._readers = readers

    def can_read(self, photo: Photo) -> bool:
        return any(reader.can_read(photo) for reader in self._readers)

    def read(self, photo: Photo) -> PhotoMetadata:
        for reader in self._readers:
            if reader.can_read(photo):
                return reader.read(photo)
        raise ImageReaderError(f"Ningun reader soporta el formato: {photo.extension}")
