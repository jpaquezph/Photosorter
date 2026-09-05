from __future__ import annotations

from pathlib import Path

from photosorter.domain.interfaces.file_scanner import SourceFolderError
from photosorter.domain.interfaces.image_reader import ImageReader
from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.photo import Photo


class DefaultFileScanner:
    """FileScanner de V1: recorre una carpeta, con o sin subcarpetas.

    Ver Docs/Technical Design Document (TDD).md, seccion 19, y
    Docs/Requisitos V1.0.md, seccion 8 (CA-06).

    Delega en un ImageReader (ver domain/interfaces/image_reader.py) para
    decidir que archivos son fotografias soportadas, en vez de mantener su
    propia lista de extensiones (evita duplicar esa nomenclatura, TDD §18).
    """

    def __init__(self, image_reader: ImageReader) -> None:
        self._image_reader = image_reader

    def scan(self, settings: AppSettings) -> list[Photo]:
        source = settings.source_path

        if not source.exists():
            raise SourceFolderError(f"La carpeta no existe: {source}")
        if not source.is_dir():
            raise SourceFolderError(f"La ruta no es una carpeta: {source}")

        candidates: list[Path] = (
            [p for p in source.rglob("*") if p.is_file()]
            if settings.recursive
            else [p for p in source.iterdir() if p.is_file()]
        )

        photos: list[Photo] = []
        for path in candidates:
            photo = Photo(source_path=path)
            if self._image_reader.can_read(photo):
                photos.append(photo)

        return sorted(photos, key=lambda photo: photo.source_path)
