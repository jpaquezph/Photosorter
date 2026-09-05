from pathlib import Path

from PIL import Image

from photosorter.domain.models.photo import Photo
from photosorter.infrastructure.image.composite_image_reader import CompositeImageReader
from photosorter.infrastructure.image.raw_image_reader import RawImageReader
from photosorter.infrastructure.image.standard_image_reader import StandardImageReader


def test_dispatches_to_the_reader_that_supports_the_format(tmp_path: Path) -> None:
    image_path = tmp_path / "foto.jpg"
    Image.new("RGB", (100, 50), color="blue").save(image_path)

    reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
    photo = Photo(source_path=image_path)

    assert reader.can_read(photo) is True
    metadata = reader.read(photo)
    assert metadata.width == 100
    assert metadata.height == 50


def test_can_read_is_false_when_no_reader_supports_the_format(tmp_path: Path) -> None:
    reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
    photo = Photo(source_path=tmp_path / "documento.pdf")

    assert reader.can_read(photo) is False
