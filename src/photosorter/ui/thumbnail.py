from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QImage

# Mismo set que RawImageReader (infrastructure/image/raw_image_reader.py):
# aqui se duplica a proposito porque es un detalle de UI (que formatos
# necesitan pasar por rawpy para previsualizarse) y no de lectura de
# metadata de dominio.
_RAW_EXTENSIONS = {".nef", ".cr2", ".cr3", ".arw", ".dng", ".raf", ".orf", ".rw2"}


def load_preview_image(path: Path) -> QImage | None:
    """Carga una previsualizacion liviana de `path` para la UI.

    Para RAW se usa la miniatura JPEG/bitmap embebida (rapida, no decodifica
    el sensor completo); para el resto, Qt decodifica el archivo
    directamente. Devuelve None si no se puede generar una previsualizacion:
    esto nunca debe interrumpir el procesamiento real del archivo.
    """
    try:
        if path.suffix.lower() in _RAW_EXTENSIONS:
            image = _load_raw_thumbnail(path)
        else:
            image = QImage(str(path))
    except Exception:
        return None

    if image is None or image.isNull():
        return None
    return image


def _load_raw_thumbnail(path: Path) -> QImage | None:
    import rawpy

    with rawpy.imread(str(path)) as raw:
        try:
            thumb = raw.extract_thumb()
        except (rawpy.LibRawNoThumbnailError, rawpy.LibRawUnsupportedThumbnailError):
            return None

        if thumb.format == rawpy.ThumbFormat.JPEG:
            image = QImage.fromData(thumb.data, "JPG")
        else:
            height, width, channels = thumb.data.shape
            fmt = QImage.Format.Format_RGB888 if channels == 3 else QImage.Format.Format_RGBA8888
            image = QImage(
                thumb.data.tobytes(), width, height, width * channels, fmt
            ).copy()
        return image
