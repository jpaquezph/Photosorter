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


def test_different_source_subfolders_resolve_to_same_destination_when_not_recursive(
    settings: AppSettings,
) -> None:
    # Documenta el comportamiento esperado (TDD, seccion 18/1330) para
    # recursive=False: dos fotos con el mismo nombre en subcarpetas
    # distintas colisionan en el mismo destino. Esto es intencional; el
    # manejo del conflicto es responsabilidad de ConflictService/
    # FileOperator, no del resolver. Con recursive=True el resolver
    # preserva la subcarpeta de origen (ver tests mas abajo), asi que la
    # colision deja de darse en ese modo.
    resolver = DefaultDestinationResolver()
    photo_a = Photo(source_path=Path("C:/Fotos/CameraA/DSC_0001.NEF"))
    photo_b = Photo(source_path=Path("C:/Fotos/CameraB/DSC_0001.NEF"))

    destination_a = resolver.resolve(photo_a, Classification.VERTICAL, settings)
    destination_b = resolver.resolve(photo_b, Classification.VERTICAL, settings)

    assert destination_a.path == destination_b.path


@pytest.fixture
def recursive_settings() -> AppSettings:
    return AppSettings(
        source_path=Path("C:/Fotos"),
        destination_path=Path("C:/Fotos/Organizadas"),
        recursive=True,
    )


def test_preserves_root_subfolder_when_recursive(recursive_settings: AppSettings) -> None:
    photo = Photo(source_path=Path("C:/Fotos/Musica/cancion.jpg"))
    resolver = DefaultDestinationResolver()

    destination = resolver.resolve(photo, Classification.VERTICAL, recursive_settings)

    assert destination.path == (
        Path("C:/Fotos/Organizadas") / "Musica" / "Verticales" / "cancion.jpg"
    )


def test_preserves_nested_subfolders_when_recursive(recursive_settings: AppSettings) -> None:
    photo = Photo(source_path=Path("C:/Fotos/Musica/Vacaciones/cancion.jpg"))
    resolver = DefaultDestinationResolver()

    destination = resolver.resolve(photo, Classification.HORIZONTAL, recursive_settings)

    assert destination.path == (
        Path("C:/Fotos/Organizadas") / "Musica" / "Vacaciones" / "Horizontales" / "cancion.jpg"
    )


def test_different_root_subfolders_keep_separate_destinations_when_recursive(
    recursive_settings: AppSettings,
) -> None:
    resolver = DefaultDestinationResolver()
    photo_musica = Photo(source_path=Path("C:/Fotos/Musica/foto.jpg"))
    photo_inmuebles = Photo(source_path=Path("C:/Fotos/Inmuebles/foto.jpg"))

    destination_musica = resolver.resolve(photo_musica, Classification.VERTICAL, recursive_settings)
    destination_inmuebles = resolver.resolve(
        photo_inmuebles, Classification.VERTICAL, recursive_settings
    )

    assert destination_musica.path != destination_inmuebles.path
    assert destination_musica.path == (
        Path("C:/Fotos/Organizadas") / "Musica" / "Verticales" / "foto.jpg"
    )
    assert destination_inmuebles.path == (
        Path("C:/Fotos/Organizadas") / "Inmuebles" / "Verticales" / "foto.jpg"
    )


def test_falls_back_to_flat_layout_when_recursive_but_photo_is_at_source_root(
    recursive_settings: AppSettings,
) -> None:
    photo = Photo(source_path=Path("C:/Fotos/foto.jpg"))
    resolver = DefaultDestinationResolver()

    destination = resolver.resolve(photo, Classification.SQUARE, recursive_settings)

    assert destination.path == Path("C:/Fotos/Organizadas") / "Cuadradas" / "foto.jpg"
