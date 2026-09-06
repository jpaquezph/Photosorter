from pathlib import Path

from PIL import Image

from photosorter.application.cancellation_token import CancellationToken
from photosorter.application.sorter_service import SorterService
from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.conflict_resolution import ConflictResolution
from photosorter.domain.models.processing_result import ProcessingStatus
from photosorter.domain.services.conflict_service import ConflictService
from photosorter.domain.services.orientation_classifier import OrientationClassifier
from photosorter.infrastructure.filesystem.copy_file_operator import CopyFileOperator
from photosorter.infrastructure.filesystem.default_destination_resolver import (
    DefaultDestinationResolver,
)
from photosorter.infrastructure.filesystem.default_file_scanner import DefaultFileScanner
from photosorter.infrastructure.image.composite_image_reader import CompositeImageReader
from photosorter.infrastructure.image.raw_image_reader import RawImageReader
from photosorter.infrastructure.image.standard_image_reader import StandardImageReader


class _FixedConflictPrompt:
    def __init__(self, decision: ConflictDecision) -> None:
        self._decision = decision
        self.asked = 0

    def ask(self, conflict) -> ConflictDecision:  # noqa: ANN001 - test double
        self.asked += 1
        return self._decision


class _RecordingProgressReporter:
    def __init__(self) -> None:
        self.started_with: int | None = None
        self.files_started: list[str] = []
        self.files_completed: list[tuple[int, int, ProcessingStatus]] = []
        self.estimates: list = []
        self.summary = None

    def on_started(self, total_files: int) -> None:
        self.started_with = total_files

    def on_file_started(self, photo) -> None:  # noqa: ANN001 - test double
        self.files_started.append(photo.filename)

    def on_file_completed(self, processed_count, total_files, result, estimate) -> None:  # noqa: ANN001
        self.files_completed.append((processed_count, total_files, result.status))
        self.estimates.append(estimate)

    def on_finished(self, summary) -> None:  # noqa: ANN001 - test double
        self.summary = summary


def _build_sorter_service(conflict_prompt, clock=None) -> SorterService:  # noqa: ANN001
    reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
    return SorterService(
        file_scanner=DefaultFileScanner(reader),
        image_reader=reader,
        classifier=OrientationClassifier(),
        destination_resolver=DefaultDestinationResolver(),
        conflict_service=ConflictService(CopyFileOperator(), conflict_prompt),
        clock=clock,
    )


def test_organizes_a_mixed_folder_and_continues_after_a_corrupt_file(tmp_path: Path) -> None:
    Image.new("RGB", (200, 100), color="red").save(tmp_path / "horizontal.jpg")
    Image.new("RGB", (100, 200), color="blue").save(tmp_path / "vertical.jpg")
    # CA-08: extension valida, contenido invalido -> debe fallar sin frenar el resto.
    (tmp_path / "corrupta.jpg").write_bytes(b"esto no es una imagen")

    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    service = _build_sorter_service(_FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP)))

    summary = service.run(settings)

    assert summary.total_files == 3
    assert summary.processed_files == 3
    assert summary.copied_files == 2
    assert summary.failed_files == 1
    assert summary.horizontal_count == 1
    assert summary.vertical_count == 1
    assert (tmp_path / "Organizadas" / "Horizontales" / "horizontal.jpg").exists()
    assert (tmp_path / "Organizadas" / "Verticales" / "vertical.jpg").exists()
    assert not summary.cancelled


def test_resolves_conflicts_using_the_conflict_prompt(tmp_path: Path) -> None:
    Image.new("RGB", (200, 100), color="green").save(tmp_path / "horizontal.jpg")
    existing = tmp_path / "Organizadas" / "Horizontales" / "horizontal.jpg"
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"version previa")

    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    prompt = _FixedConflictPrompt(ConflictDecision(ConflictResolution.OVERWRITE))
    service = _build_sorter_service(prompt)

    summary = service.run(settings)

    assert summary.overwritten_files == 1
    assert prompt.asked == 1
    assert existing.read_bytes() != b"version previa"


def test_reports_progress_for_every_file(tmp_path: Path) -> None:
    Image.new("RGB", (200, 100), color="red").save(tmp_path / "a.jpg")
    Image.new("RGB", (200, 100), color="blue").save(tmp_path / "b.jpg")

    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    reporter = _RecordingProgressReporter()
    service = _build_sorter_service(_FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP)))

    summary = service.run(settings, progress_reporter=reporter)

    assert reporter.started_with == 2
    assert set(reporter.files_started) == {"a.jpg", "b.jpg"}
    assert [c[0] for c in reporter.files_completed] == [1, 2]
    assert all(c[1] == 2 for c in reporter.files_completed)
    assert reporter.summary == summary


def test_reports_time_remaining_estimate_based_on_average_time_per_file(
    tmp_path: Path,
) -> None:
    Image.new("RGB", (200, 100), color="red").save(tmp_path / "a.jpg")
    Image.new("RGB", (200, 100), color="blue").save(tmp_path / "b.jpg")

    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    reporter = _RecordingProgressReporter()
    # Reloj falso: 0s al arrancar, 10s tras el primer archivo, 20s tras el segundo.
    fake_clock = iter([0.0, 10.0, 20.0])
    service = _build_sorter_service(
        _FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP)),
        clock=lambda: next(fake_clock),
    )

    service.run(settings, progress_reporter=reporter)

    first_estimate, second_estimate = reporter.estimates
    assert first_estimate.elapsed_seconds == 10.0
    assert first_estimate.average_seconds_per_file == 10.0
    assert first_estimate.remaining_seconds == 10.0
    assert second_estimate.elapsed_seconds == 20.0
    assert second_estimate.remaining_seconds == 0.0


def test_cancellation_stops_processing_remaining_files(tmp_path: Path) -> None:
    Image.new("RGB", (200, 100), color="red").save(tmp_path / "a.jpg")
    Image.new("RGB", (200, 100), color="blue").save(tmp_path / "b.jpg")
    Image.new("RGB", (200, 100), color="green").save(tmp_path / "c.jpg")

    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    token = CancellationToken()

    class _CancelAfterFirstFile(_RecordingProgressReporter):
        def on_file_completed(self, processed_count, total_files, result, estimate) -> None:  # noqa: ANN001
            super().on_file_completed(processed_count, total_files, result, estimate)
            token.cancel()

    reporter = _CancelAfterFirstFile()
    service = _build_sorter_service(_FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP)))

    summary = service.run(settings, progress_reporter=reporter, cancellation_token=token)

    assert summary.cancelled is True
    assert summary.processed_files == 1
    assert summary.total_files == 3


def test_logs_key_processing_events(tmp_path: Path, caplog) -> None:  # noqa: ANN001
    Image.new("RGB", (200, 100), color="red").save(tmp_path / "a.jpg")
    settings = AppSettings(
        source_path=tmp_path, destination_path=tmp_path / "Organizadas", recursive=False
    )
    service = _build_sorter_service(_FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP)))

    with caplog.at_level("INFO"):
        service.run(settings)

    messages = " | ".join(caplog.messages)
    assert "Processing started" in messages
    assert "Files found: 1" in messages
    assert "Processing finished" in messages
