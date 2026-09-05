from pathlib import Path

from photosorter.domain.interfaces.file_operator import DestinationAlreadyExistsError
from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.conflict_resolution import ConflictResolution
from photosorter.domain.models.file_conflict import FileConflict
from photosorter.domain.models.processing_result import ProcessingStatus
from photosorter.domain.services.conflict_service import ConflictService


class FakeFileOperator:
    """Simula FileOperator sin tocar el filesystem, para tests unitarios."""

    def __init__(self, existing_destinations: set[Path] | None = None) -> None:
        self.existing = set(existing_destinations or set())
        self.calls: list[tuple[Path, Path, bool]] = []

    def copy(self, source_path: Path, destination_path: Path, *, overwrite: bool = False) -> None:
        self.calls.append((source_path, destination_path, overwrite))
        if destination_path in self.existing and not overwrite:
            raise DestinationAlreadyExistsError(source_path, destination_path)
        self.existing.add(destination_path)


class ScriptedConflictPrompt:
    """ConflictPrompt de prueba que devuelve decisiones predefinidas en orden."""

    def __init__(self, decisions: list[ConflictDecision]) -> None:
        self._decisions = list(decisions)
        self.asked_conflicts: list[FileConflict] = []

    def ask(self, conflict: FileConflict) -> ConflictDecision:
        self.asked_conflicts.append(conflict)
        return self._decisions.pop(0)


def test_copies_normally_when_there_is_no_conflict() -> None:
    file_operator = FakeFileOperator()
    prompt = ScriptedConflictPrompt([])
    service = ConflictService(file_operator, prompt)

    result = service.copy(Path("origen/a.jpg"), Path("Horizontales/a.jpg"))

    assert result.status == ProcessingStatus.COPIED
    assert result.destination_path == Path("Horizontales/a.jpg")
    assert prompt.asked_conflicts == []


def test_skip_resolution_does_not_overwrite_and_reports_skipped() -> None:
    destination = Path("Verticales/a.jpg")
    file_operator = FakeFileOperator(existing_destinations={destination})
    prompt = ScriptedConflictPrompt([ConflictDecision(ConflictResolution.SKIP)])
    service = ConflictService(file_operator, prompt)

    result = service.copy(Path("origen/a.jpg"), destination)

    assert result.status == ProcessingStatus.SKIPPED
    assert len(prompt.asked_conflicts) == 1
    # No debe haber un segundo intento de copia con overwrite=True.
    assert [c for c in file_operator.calls if c[2] is True] == []


def test_overwrite_resolution_copies_with_overwrite_and_reports_overwritten() -> None:
    destination = Path("Verticales/a.jpg")
    file_operator = FakeFileOperator(existing_destinations={destination})
    prompt = ScriptedConflictPrompt([ConflictDecision(ConflictResolution.OVERWRITE)])
    service = ConflictService(file_operator, prompt)

    result = service.copy(Path("origen/a.jpg"), destination)

    assert result.status == ProcessingStatus.OVERWRITTEN
    assert (Path("origen/a.jpg"), destination, True) in file_operator.calls


def test_apply_to_remaining_overwrite_is_remembered_without_asking_again() -> None:
    dest_a = Path("Verticales/a.jpg")
    dest_b = Path("Verticales/b.jpg")
    file_operator = FakeFileOperator(existing_destinations={dest_a, dest_b})
    prompt = ScriptedConflictPrompt(
        [ConflictDecision(ConflictResolution.OVERWRITE, apply_to_remaining=True)]
    )
    service = ConflictService(file_operator, prompt)

    first = service.copy(Path("origen/a.jpg"), dest_a)
    second = service.copy(Path("origen/b.jpg"), dest_b)

    assert first.status == ProcessingStatus.OVERWRITTEN
    assert second.status == ProcessingStatus.OVERWRITTEN
    # Solo se pregunto una vez; la segunda vez se reutilizo la decision.
    assert len(prompt.asked_conflicts) == 1


def test_apply_to_remaining_skip_is_remembered_without_asking_again() -> None:
    dest_a = Path("Verticales/a.jpg")
    dest_b = Path("Verticales/b.jpg")
    file_operator = FakeFileOperator(existing_destinations={dest_a, dest_b})
    prompt = ScriptedConflictPrompt(
        [ConflictDecision(ConflictResolution.SKIP, apply_to_remaining=True)]
    )
    service = ConflictService(file_operator, prompt)

    first = service.copy(Path("origen/a.jpg"), dest_a)
    second = service.copy(Path("origen/b.jpg"), dest_b)

    assert first.status == ProcessingStatus.SKIPPED
    assert second.status == ProcessingStatus.SKIPPED
    assert len(prompt.asked_conflicts) == 1


def test_without_apply_to_remaining_each_conflict_is_asked_again() -> None:
    dest_a = Path("Verticales/a.jpg")
    dest_b = Path("Verticales/b.jpg")
    file_operator = FakeFileOperator(existing_destinations={dest_a, dest_b})
    prompt = ScriptedConflictPrompt(
        [
            ConflictDecision(ConflictResolution.SKIP, apply_to_remaining=False),
            ConflictDecision(ConflictResolution.OVERWRITE, apply_to_remaining=False),
        ]
    )
    service = ConflictService(file_operator, prompt)

    first = service.copy(Path("origen/a.jpg"), dest_a)
    second = service.copy(Path("origen/b.jpg"), dest_b)

    assert first.status == ProcessingStatus.SKIPPED
    assert second.status == ProcessingStatus.OVERWRITTEN
    assert len(prompt.asked_conflicts) == 2
