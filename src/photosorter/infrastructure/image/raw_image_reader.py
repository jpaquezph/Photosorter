from __future__ import annotations

import rawpy

from photosorter.domain.interfaces.image_reader import ImageReaderError
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.photo_metadata import PhotoMetadata

# Formatos RAW evaluados en el RAW Spike (ver Docs/CONTEXTO.md).
# rawpy (LibRaw) los soporta a traves del mismo contrato ImageReader.
SUPPORTED_EXTENSIONS = {".nef", ".cr2", ".cr3", ".arw", ".dng", ".raf", ".orf", ".rw2"}

# LibRaw expone la rotacion necesaria en sizes.flip usando su propia
# codificacion (no la de EXIF): 0 = sin rotacion, 3 = 180 grados,
# 5 y 6 = 90/270 grados. OrientationClassifier solo necesita saber si hay
# que intercambiar ancho y alto, por lo que alcanza con mapear flip a un
# valor EXIF equivalente que pertenezca (o no) al set de 90/270 grados.
_FLIP_ROTATED_90_OR_270 = {5, 6}
_ORIENTATION_SWAPPED = 6  # cualquier valor EXIF dentro de {5,6,7,8} sirve
_ORIENTATION_NORMAL = 1


class RawImageReader:
    """ImageReader para formatos RAW, via rawpy (LibRaw).

    Ver Docs/System Architecture Document - SAD.md, seccion 11, y
    Docs/Technical Design Document (TDD).md, seccion 12/29 (RAW Spike).
    """

    def can_read(self, photo: Photo) -> bool:
        return photo.extension.lower() in SUPPORTED_EXTENSIONS

    def read(self, photo: Photo) -> PhotoMetadata:
        try:
            with rawpy.imread(str(photo.source_path)) as raw:
                sizes = raw.sizes
        except rawpy.LibRawError as exc:
            raise ImageReaderError(f"No se pudo leer el RAW: {photo.source_path}") from exc
        except OSError as exc:
            raise ImageReaderError(f"No se pudo leer el RAW: {photo.source_path}") from exc

        orientation = (
            _ORIENTATION_SWAPPED if sizes.flip in _FLIP_ROTATED_90_OR_270 else _ORIENTATION_NORMAL
        )

        return PhotoMetadata(
            width=sizes.width,
            height=sizes.height,
            format=photo.extension.lstrip(".").upper(),
            orientation=orientation,
        )
