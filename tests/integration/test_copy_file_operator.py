from pathlib import Path

import pytest

from photosorter.domain.interfaces.file_operator import DestinationAlreadyExistsError
from photosorter.infrastructure.filesystem.copy_file_operator import CopyFileOperator


@pytest.fixture
def source_file(tmp_path: Path) -> Path:
    source = tmp_path / "origen" / "DSC_0001.JPG"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"contenido original")
    return source


def test_copies_file_content(tmp_path: Path, source_file: Path) -> None:
    destination = tmp_path / "Verticales" / "DSC_0001.JPG"

    CopyFileOperator().copy(source_file, destination)

    assert destination.read_bytes() == b"contenido original"


def test_creates_destination_directory_if_missing(tmp_path: Path, source_file: Path) -> None:
    destination = tmp_path / "Verticales" / "DSC_0001.JPG"
    assert not destination.parent.exists()

    CopyFileOperator().copy(source_file, destination)

    assert destination.parent.is_dir()


def test_does_not_fail_if_destination_directory_already_exists(
    tmp_path: Path, source_file: Path
) -> None:
    # CA-09: si Verticales/Horizontales/Cuadradas ya existen, no debe fallar
    # ni afectar el contenido existente.
    destination_dir = tmp_path / "Verticales"
    destination_dir.mkdir()
    existing_file = destination_dir / "otra_foto.jpg"
    existing_file.write_bytes(b"no tocar")

    CopyFileOperator().copy(source_file, destination_dir / "DSC_0001.JPG")

    assert existing_file.read_bytes() == b"no tocar"


def test_does_not_overwrite_existing_destination_by_default(
    tmp_path: Path, source_file: Path
) -> None:
    # CA-10 / D7: nunca se sobrescribe silenciosamente.
    destination = tmp_path / "Verticales" / "DSC_0001.JPG"
    destination.parent.mkdir()
    destination.write_bytes(b"archivo previo")

    with pytest.raises(DestinationAlreadyExistsError) as exc_info:
        CopyFileOperator().copy(source_file, destination)

    assert exc_info.value.source_path == source_file
    assert exc_info.value.destination_path == destination
    assert destination.read_bytes() == b"archivo previo"


def test_overwrites_when_explicitly_requested(tmp_path: Path, source_file: Path) -> None:
    destination = tmp_path / "Verticales" / "DSC_0001.JPG"
    destination.parent.mkdir()
    destination.write_bytes(b"archivo previo")

    CopyFileOperator().copy(source_file, destination, overwrite=True)

    assert destination.read_bytes() == b"contenido original"


def test_does_not_modify_or_move_the_source_file(tmp_path: Path, source_file: Path) -> None:
    destination = tmp_path / "Verticales" / "DSC_0001.JPG"

    CopyFileOperator().copy(source_file, destination)

    assert source_file.exists()
    assert source_file.read_bytes() == b"contenido original"
