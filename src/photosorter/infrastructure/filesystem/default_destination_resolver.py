from __future__ import annotations

from pathlib import Path

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.classification import Classification
from photosorter.domain.models.destination_path import DestinationPath
from photosorter.domain.models.photo import Photo

# Nomenclatura de carpetas de V1 (Requisitos V1.0, seccion RF-05 y
# Contract Specification, seccion 7.4). Centralizada aca a proposito
# (TDD, seccion 18): si en el futuro se quiere personalizar el nombre de
# las carpetas, este es el unico lugar que deberia cambiar.
_FOLDER_NAMES = {
    Classification.VERTICAL: "Verticales",
    Classification.HORIZONTAL: "Horizontales",
    Classification.SQUARE: "Cuadradas",
}


class DefaultDestinationResolver:
    """DestinationResolver de V1: Verticales/Horizontales/Cuadradas.

    Ver Docs/Technical Design Document (TDD).md, seccion 20-21.
    Futuras estrategias (por fecha, por camara, etc.) se agregan como
    nuevas implementaciones de DestinationResolver, sin tocar esta clase.

    Cuando settings.recursive es True, se preserva la carpeta (o cadena de
    subcarpetas) de origen de cada foto: la clasificacion se agrega como
    ultima subcarpeta dentro de esa ruta en vez de mezclar todo en una
    unica Verticales/Horizontales en la raiz del destino. Con
    recursive=False no hay subcarpetas que preservar (CA-06), asi que el
    comportamiento es el mismo que en V1.
    """

    def resolve(
        self, photo: Photo, classification: Classification, settings: AppSettings
    ) -> DestinationPath:
        folder_name = _FOLDER_NAMES[classification]

        if settings.recursive:
            relative_dir = photo.source_path.parent.relative_to(settings.source_path)
            if relative_dir != Path("."):
                path = settings.destination_path / relative_dir / folder_name / photo.filename
                return DestinationPath(path=path)

        path = settings.destination_path / folder_name / photo.filename
        return DestinationPath(path=path)
