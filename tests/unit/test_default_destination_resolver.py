from pathlib import Path

import pytest

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.classification import Classification
from photosorter.domain.models.photo import Photo
from photosorter.infrastructure.filesystem.default_destination_resolver import (
    DefaultDestinationResolver,
)


@pytest.fixture
def settings() -> AppSettings:
    return AppSettings(
        source_path=Path("C:/Fotos"),
        destination_path=Path("C:/Fotos/Organizadas"),
        recursive=False,
    )


@pytest.mark.parametrize(
    ("classification", "expected_folder"),
    [
        (Classification.VERTICAL, "Verticales"),
        (Classification.HORIZONTAL, "Horizontales"),
        (Classification.SQUARE, "Cuadradas"),
    ],
)
def test_resolves_to_expected_folder(
    settings: AppSettings, classification: Classification, expected_folder: str
) -> None:
    photo = Photo(source_path=Path("C:/Fotos/CameraA/DSC_0001.NEF"))
    resolver = DefaultDestinationResolver()

    destination = resolver.resolve(photo, classification, settings)

    assert destination.path == Path("C:/Fotos/Organizadas") / expected_folder / "DSC_0001.NEF"


def test_keeps_original_filename(settings: AppSettings) -> None:
    photo = Photo(source_path=Path("C:/Fotos/CameraB/IMG_9999.JPG"))
    resolver = DefaultDestinationResolver()

    destination = resolver.resolve(photo, Classification.HORIZONTAL, settings)

    assert destination.path.name == "IMG_9999.JPG"


def test_different_source_subfolders_resolve_to_same_destination(settings: AppSettings) -> None:
    # Documenta el comportamiento esperado (TDD, seccion 18/1330): dos fotos
    # con el mismo nombre en subcarpetas distintas colisionan en el mismo
    # destino. Esto es intencional; el manejo del conflicto es
    # responsabilidad de ConflictService/FileOperator, no del resolver.
    resolver = DefaultDestinationResolver()
    photo_a = Photo(source_path=Path("C:/Fotos/CameraA/DSC_0001.NEF"))
    photo_b = Photo(source_path=Path("C:/Fotos/CameraB/DSC_0001.NEF"))

    destination_a = resolver.resolve(photo_a, Classification.VERTICAL, settings)
    destination_b = resolver.resolve(photo_b, Classification.VERTICAL, settings)

    assert destination_a.path == destination_b.path
