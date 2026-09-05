from pathlib import Path

import pytest

from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.photo_metadata import PhotoMetadata
from photosorter.domain.models.processing_result import ProcessingResult, ProcessingStatus


class TestPhoto:
    def test_valid_photo(self) -> None:
        photo = Photo(source_path=Path("C:/Fotos/Vacaciones/IMG_1234.CR3"))

        assert photo.filename == "IMG_1234.CR3"
        assert photo.extension == ".CR3"

    def test_rejects_none_path(self) -> None:
        with pytest.raises(ValueError):
            Photo(source_path=None)  # type: ignore[arg-type]

    def test_rejects_empty_path(self) -> None:
        with pytest.raises(ValueError):
            Photo(source_path=Path(""))

    def test_rejects_existing_directory(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            Photo(source_path=tmp_path)


class TestPhotoMetadata:
    def test_valid_metadata(self) -> None:
        metadata = PhotoMetadata(width=6000, height=4000, format="JPEG")

        assert metadata.width == 6000
        assert metadata.height == 4000

    @pytest.mark.parametrize("width", [0, -1])
    def test_rejects_non_positive_width(self, width: int) -> None:
        with pytest.raises(ValueError):
            PhotoMetadata(width=width, height=100, format="JPEG")

    @pytest.mark.parametrize("height", [0, -1])
    def test_rejects_non_positive_height(self, height: int) -> None:
        with pytest.raises(ValueError):
            PhotoMetadata(width=100, height=height, format="JPEG")

    def test_rejects_empty_format(self) -> None:
        with pytest.raises(ValueError):
            PhotoMetadata(width=100, height=100, format="")


class TestProcessingResult:
    def test_copied_requires_destination_path(self) -> None:
        with pytest.raises(ValueError):
            ProcessingResult(source_path=Path("a.jpg"), status=ProcessingStatus.COPIED)

    def test_copied_with_destination_is_valid(self) -> None:
        result = ProcessingResult(
            source_path=Path("a.jpg"),
            status=ProcessingStatus.COPIED,
            destination_path=Path("Horizontales/a.jpg"),
        )

        assert result.error is None

    def test_failed_requires_error(self) -> None:
        with pytest.raises(ValueError):
            ProcessingResult(source_path=Path("a.jpg"), status=ProcessingStatus.FAILED)

    def test_failed_with_error_is_valid(self) -> None:
        result = ProcessingResult(
            source_path=Path("a.jpg"), status=ProcessingStatus.FAILED, error="corrupto"
        )

        assert result.destination_path is None


class TestAppSettings:
    def test_defaults_to_non_recursive(self) -> None:
        settings = AppSettings(
            source_path=Path("C:/Fotos"), destination_path=Path("C:/Fotos/Organizadas")
        )

        assert settings.recursive is False
