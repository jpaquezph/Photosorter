from pathlib import Path

import pytest

from photosorter import beta_limiter


@pytest.fixture(autouse=True)
def _isolated_usage_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))


def test_starts_without_reaching_the_limit() -> None:
    assert beta_limiter.get_processed_count() == 0
    assert not beta_limiter.has_reached_limit()


def test_register_processed_accumulates_across_calls() -> None:
    beta_limiter.register_processed(4)
    beta_limiter.register_processed(3)

    assert beta_limiter.get_processed_count() == 7
    assert not beta_limiter.has_reached_limit()


def test_reaches_limit_once_max_photos_is_hit() -> None:
    beta_limiter.register_processed(beta_limiter.MAX_PHOTOS)

    assert beta_limiter.has_reached_limit()


def test_register_processed_ignores_non_positive_counts() -> None:
    beta_limiter.register_processed(0)
    beta_limiter.register_processed(-5)

    assert beta_limiter.get_processed_count() == 0
