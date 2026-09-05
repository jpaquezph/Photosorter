from pathlib import Path

import pytest

from photosorter.domain.models.photo import Photo
from photosorter.infrastructure.image.raw_image_reader import RawImageReader, SUPPORTED_EXTENSIONS

_FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "raw"


def _sample_raw_files() -> list[Path]:
    if not _FIXTURES_DIR.is_dir():
        return []
    return [p for p in _FIXTURES_DIR.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS]


class TestCanRead:
    def test_accepts_raw_extensions(self, tmp_path: Path) -> None:
        reader = RawImageReader()
        for ext in SUPPORTED_EXTENSIONS:
            photo = Photo(source_path=tmp_path / f"foto{ext}")
            assert reader.can_read(photo) is True

    def test_rejects_standard_extension(self, tmp_path: Path) -> None:
        reader = RawImageReader()
        photo = Photo(source_path=tmp_path / "foto.jpg")

        assert reader.can_read(photo) is False


@pytest.mark.skipif(
    not _sample_raw_files(),
    reason="No hay archivos RAW de muestra en tests/fixtures/raw/ (ver README ahi)",
)
@pytest.mark.parametrize("raw_path", _sample_raw_files(), ids=lambda p: p.name)
def test_reads_real_raw_samples(raw_path: Path) -> None:
    metadata = RawImageReader().read(Photo(source_path=raw_path))

    assert metadata.width > 0
    assert metadata.height > 0
    assert metadata.format
