from pathlib import Path

from PIL import Image

from photosorter.domain.models.photo import Photo
from photosorter.infrastructure.image.standard_image_reader import StandardImageReader


def _make_jpeg(path: Path, width: int, height: int, orientation: int | None = None) -> None:
    img = Image.new("RGB", (width, height), color="red")
    if orientation is not None:
        exif = Image.Exif()
        exif[274] = orientation  # tag EXIF Orientation
        img.save(path, exif=exif.tobytes())
    else:
        img.save(path)


class TestCanRead:
    def test_accepts_supported_extensions(self, tmp_path: Path) -> None:
        reader = StandardImageReader()
        for ext in [".jpg", ".jpeg", ".png", ".tiff", ".webp"]:
            photo = Photo(source_path=tmp_path / f"foto{ext}")
            assert reader.can_read(photo) is True

    def test_rejects_raw_extension(self, tmp_path: Path) -> None:
        reader = StandardImageReader()
        photo = Photo(source_path=tmp_path / "foto.nef")

        assert reader.can_read(photo) is False


class TestRead:
    def test_reads_dimensions_and_format(self, tmp_path: Path) -> None:
        image_path = tmp_path / "horizontal.jpg"
        _make_jpeg(image_path, width=200, height=100)

        metadata = StandardImageReader().read(Photo(source_path=image_path))

        assert metadata.width == 200
        assert metadata.height == 100
        assert metadata.format == "JPEG"

    def test_reads_exif_orientation_when_present(self, tmp_path: Path) -> None:
        image_path = tmp_path / "rotated.jpg"
        _make_jpeg(image_path, width=200, height=100, orientation=6)

        metadata = StandardImageReader().read(Photo(source_path=image_path))

        assert metadata.orientation == 6

    def test_orientation_is_none_when_absent(self, tmp_path: Path) -> None:
        image_path = tmp_path / "sin_exif.png"
        _make_jpeg(image_path, width=50, height=50)

        metadata = StandardImageReader().read(Photo(source_path=image_path))

        assert metadata.orientation is None
