from pathlib import Path

import pytest
from PIL import Image

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.photo import Photo
from photosorter.domain.services.orientation_classifier import OrientationClassifier
from photosorter.infrastructure.filesystem.copy_file_operator import CopyFileOperator
from photosorter.infrastructure.filesystem.default_destination_resolver import (
    DefaultDestinationResolver,
)
from photosorter.infrastructure.image.composite_image_reader import CompositeImageReader
from photosorter.infrastructure.image.raw_image_reader import RawImageReader
from photosorter.infrastructure.image.standard_image_reader import StandardImageReader

_RAW_FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "raw"


def _organize(photo: Photo, settings: AppSettings) -> Path:
    """Reproduce el flujo M1 completo: Reader -> Classifier -> Resolver -> Copy."""
    reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
    metadata = reader.read(photo)
    classification = OrientationClassifier().classify(metadata)
    destination = DefaultDestinationResolver().resolve(photo, classification, settings)
    CopyFileOperator().copy(photo.source_path, destination.path)
    return destination.path


def test_organizes_a_horizontal_jpeg_end_to_end(tmp_path: Path) -> None:
    source_dir = tmp_path / "Fotos"
    source_dir.mkdir()
    source_path = source_dir / "IMG_0001.JPG"
    Image.new("RGB", (200, 100), color="green").save(source_path)

    settings = AppSettings(
        source_path=source_dir, destination_path=source_dir / "Organizadas", recursive=False
    )

    destination = _organize(Photo(source_path=source_path), settings)

    assert destination == source_dir / "Organizadas" / "Horizontales" / "IMG_0001.JPG"
    assert destination.exists()
    assert source_path.exists()  # el original no se mueve ni se borra


def test_organizes_a_vertical_jpeg_end_to_end(tmp_path: Path) -> None:
    source_dir = tmp_path / "Fotos"
    source_dir.mkdir()
    source_path = source_dir / "IMG_0002.JPG"
    Image.new("RGB", (100, 200), color="blue").save(source_path)

    settings = AppSettings(
        source_path=source_dir, destination_path=source_dir / "Organizadas", recursive=False
    )

    destination = _organize(Photo(source_path=source_path), settings)

    assert destination == source_dir / "Organizadas" / "Verticales" / "IMG_0002.JPG"
    assert destination.exists()


def _sample_raw_files() -> list[Path]:
    if not _RAW_FIXTURES_DIR.is_dir():
        return []
    return [p for p in _RAW_FIXTURES_DIR.iterdir() if p.suffix.lower() == ".nef"]


@pytest.mark.skipif(
    not _sample_raw_files(), reason="No hay archivos RAW de muestra en tests/fixtures/raw/"
)
@pytest.mark.parametrize("raw_path", _sample_raw_files(), ids=lambda p: p.name)
def test_organizes_a_real_raw_file_end_to_end(tmp_path: Path, raw_path: Path) -> None:
    settings = AppSettings(
        source_path=raw_path.parent, destination_path=tmp_path / "Organizadas", recursive=False
    )

    destination = _organize(Photo(source_path=raw_path), settings)

    assert destination.exists()
    assert destination.stat().st_size == raw_path.stat().st_size
    assert raw_path.exists()  # el RAW original permanece intacto
