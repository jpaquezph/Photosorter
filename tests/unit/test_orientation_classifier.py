import pytest

from photosorter.domain.models.classification import Classification
from photosorter.domain.models.photo_metadata import PhotoMetadata
from photosorter.domain.services.orientation_classifier import OrientationClassifier


@pytest.fixture
def classifier() -> OrientationClassifier:
    return OrientationClassifier()


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        (6000, 4000, Classification.HORIZONTAL),
        (4000, 6000, Classification.VERTICAL),
        (4000, 4000, Classification.SQUARE),
    ],
)
def test_classifies_by_raw_dimensions_without_exif_orientation(
    classifier: OrientationClassifier, width: int, height: int, expected: Classification
) -> None:
    metadata = PhotoMetadata(width=width, height=height, format="JPEG")

    assert classifier.classify(metadata) == expected


@pytest.mark.parametrize("orientation", [1, 2, 3, 4, None])
def test_orientation_without_rotation_does_not_swap_dimensions(
    classifier: OrientationClassifier, orientation: int | None
) -> None:
    # 6000x4000 fisico, sin rotacion de 90/270 -> sigue siendo horizontal.
    metadata = PhotoMetadata(width=6000, height=4000, format="JPEG", orientation=orientation)

    assert classifier.classify(metadata) == Classification.HORIZONTAL


@pytest.mark.parametrize("orientation", [5, 6, 7, 8])
def test_orientation_with_90_or_270_rotation_swaps_dimensions(
    classifier: OrientationClassifier, orientation: int
) -> None:
    # CA-04: 6000x4000 fisico, pero el EXIF indica una rotacion de 90/270,
    # por lo que la orientacion visual final es vertical.
    metadata = PhotoMetadata(width=6000, height=4000, format="JPEG", orientation=orientation)

    assert classifier.classify(metadata) == Classification.VERTICAL


def test_square_stays_square_regardless_of_rotation(classifier: OrientationClassifier) -> None:
    metadata = PhotoMetadata(width=4000, height=4000, format="JPEG", orientation=6)

    assert classifier.classify(metadata) == Classification.SQUARE
