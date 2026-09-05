from __future__ import annotations

from photosorter.domain.models.classification import Classification
from photosorter.domain.models.photo_metadata import PhotoMetadata

# Valores EXIF Orientation (estandar TIFF/EXIF) en los que la imagen esta
# rotada 90 o 270 grados respecto de como fueron almacenadas fisicamente
# width/height. En esos casos, la orientacion "visual" intercambia ancho y
# alto respecto de las dimensiones fisicas.
_ROTATED_90_OR_270 = {5, 6, 7, 8}


class OrientationClassifier:
    """Clasifica una PhotoMetadata como VERTICAL, HORIZONTAL o SQUARE.

    Ver Docs/Requisitos V1.0.md, seccion 3.2 (CA-04) y
    Docs/Technical Design Document (TDD).md, seccion 11.

    La clasificacion se basa en la orientacion VISUAL final de la fotografia,
    no unicamente en sus dimensiones fisicas almacenadas: si el EXIF indica
    una rotacion de 90/270 grados, ancho y alto se intercambian antes de
    clasificar. Esta es la unica fuente de verdad para esta regla; ningun
    otro componente debe reimplementarla (TDD, seccion 11, ultimo parrafo).
    """

    def classify(self, metadata: PhotoMetadata) -> Classification:
        width, height = self._visual_dimensions(metadata)

        if height > width:
            return Classification.VERTICAL
        if width > height:
            return Classification.HORIZONTAL
        return Classification.SQUARE

    @staticmethod
    def _visual_dimensions(metadata: PhotoMetadata) -> tuple[int, int]:
        if metadata.orientation in _ROTATED_90_OR_270:
            return metadata.height, metadata.width
        return metadata.width, metadata.height
