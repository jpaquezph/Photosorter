from __future__ import annotations

from PIL import Image, UnidentifiedImageError

from photosorter.domain.interfaces.image_reader import ImageReaderError
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.photo_metadata import PhotoMetadata

# Tag EXIF estandar para la orientacion (ver especificacion Exif/TIFF).
_EXIF_ORIENTATION_TAG = 274

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp"}


class StandardImageReader:
    """ImageReader para formatos raster convencionales, via Pillow.

    Ver Docs/System Architecture Document - SAD.md, seccion 11.
    """

    def can_read(self, photo: Photo) -> bool:
        return photo.extension.lower() in SUPPORTED_EXTENSIONS

    def read(self, photo: Photo) -> PhotoMetadata:
        try:
            with Image.open(photo.source_path) as img:
                width, height = img.size
                image_format = img.format or photo.extension.lstrip(".").upper()
                exif = img.getexif()
                orientation = exif.get(_EXIF_ORIENTATION_TAG)
        except (UnidentifiedImageError, OSError) as exc:
            # Mensaje corto a proposito (sin la ruta): quien llama ya sabe
            # que archivo es (Photo/ProcessingResult.source_path) y lo
            # muestra por separado; repetirla ahi hace ilegible el
            # desplegable de errores cuando hay muchos (ver UI).
            raise ImageReaderError("No se pudo leer la imagen") from exc

        return PhotoMetadata(
            width=width,
            height=height,
            format=image_format,
            orientation=orientation,
        )
