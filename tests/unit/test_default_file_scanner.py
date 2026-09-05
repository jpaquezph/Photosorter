from pathlib import Path

import pytest

from photosorter.domain.interfaces.file_scanner import SourceFolderError
from photosorter.domain.models.app_settings import AppSettings
from photosorter.infrastructure.filesystem.default_file_scanner import DefaultFileScanner
from photosorter.infrastructure.image.composite_image_reader import CompositeImageReader
from photosorter.infrastructure.image.raw_image_reader import RawImageReader
from photosorter.infrastructure.image.standard_image_reader import StandardImageReader


@pytest.fixture
def photo_folder(tmp_path: Path) -> Path:
    (tmp_path / "IMG_0001.jpg").write_bytes(b"fake jpg")
    (tmp_path / "IMG_0002.png").write_bytes(b"fake png")
    (tmp_path / "notas.txt").write_text("no es una foto")
    sub = tmp_path / "CameraA"
    sub.mkdir()
    (sub / "IMG_0003.jpg").write_bytes(b"fake jpg")
    return tmp_path


@pytest.fixture
def scanner() -> DefaultFileScanner:
    reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
    return DefaultFileScanner(reader)


def test_non_recursive_only_scans_top_level_files(
    scanner: DefaultFileScanner, photo_folder: Path
) -> None:
    settings = AppSettings(
        source_path=photo_folder, destination_path=photo_folder / "Organizadas", recursive=False
    )

    photos = scanner.scan(settings)

    names = {photo.filename for photo in photos}
    assert names == {"IMG_0001.jpg", "IMG_0002.png"}


def test_recursive_scans_subfolders_too(scanner: DefaultFileScanner, photo_folder: Path) -> None:
    settings = AppSettings(
        source_path=photo_folder, destination_path=photo_folder / "Organizadas", recursive=True
    )

    photos = scanner.scan(settings)

    names = {photo.filename for photo in photos}
    assert names == {"IMG_0001.jpg", "IMG_0002.png", "IMG_0003.jpg"}


def test_ignores_non_image_files(scanner: DefaultFileScanner, photo_folder: Path) -> None:
    settings = AppSettings(
        source_path=photo_folder, destination_path=photo_folder / "Organizadas", recursive=True
    )

    photos = scanner.scan(settings)

    assert all(photo.filename != "notas.txt" for photo in photos)


def test_results_are_sorted_by_path(scanner: DefaultFileScanner, photo_folder: Path) -> None:
    settings = AppSettings(
        source_path=photo_folder, destination_path=photo_folder / "Organizadas", recursive=False
    )

    photos = scanner.scan(settings)

    paths = [photo.source_path for photo in photos]
    assert paths == sorted(paths)


def test_raises_when_source_folder_does_not_exist(
    scanner: DefaultFileScanner, tmp_path: Path
) -> None:
    settings = AppSettings(
        source_path=tmp_path / "no_existe", destination_path=tmp_path / "Organizadas"
    )

    with pytest.raises(SourceFolderError):
        scanner.scan(settings)


def test_raises_when_source_is_a_file_not_a_folder(
    scanner: DefaultFileScanner, tmp_path: Path
) -> None:
    a_file = tmp_path / "archivo.jpg"
    a_file.write_bytes(b"fake jpg")
    settings = AppSettings(source_path=a_file, destination_path=tmp_path / "Organizadas")

    with pytest.raises(SourceFolderError):
        scanner.scan(settings)
