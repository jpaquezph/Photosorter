from pathlib import Path

from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.conflict_resolution import ConflictResolution
from photosorter.domain.models.processing_result import ProcessingStatus
from photosorter.domain.services.conflict_service import ConflictService
from photosorter.infrastructure.filesystem.copy_file_operator import CopyFileOperator


class _FixedConflictPrompt:
    def __init__(self, decision: ConflictDecision) -> None:
        self._decision = decision

    def ask(self, conflict) -> ConflictDecision:  # noqa: ANN001 - test double
        return self._decision


def test_skip_leaves_existing_destination_file_untouched(tmp_path: Path) -> None:
    source = tmp_path / "origen.jpg"
    source.write_bytes(b"nuevo contenido")
    destination = tmp_path / "Verticales" / "a.jpg"
    destination.parent.mkdir()
    destination.write_bytes(b"contenido previo")

    prompt = _FixedConflictPrompt(ConflictDecision(ConflictResolution.SKIP))
    service = ConflictService(CopyFileOperator(), prompt)

    result = service.copy(source, destination)

    assert result.status == ProcessingStatus.SKIPPED
    assert destination.read_bytes() == b"contenido previo"


def test_overwrite_replaces_existing_destination_file(tmp_path: Path) -> None:
    source = tmp_path / "origen.jpg"
    source.write_bytes(b"nuevo contenido")
    destination = tmp_path / "Verticales" / "a.jpg"
    destination.parent.mkdir()
    destination.write_bytes(b"contenido previo")

    prompt = _FixedConflictPrompt(ConflictDecision(ConflictResolution.OVERWRITE))
    service = ConflictService(CopyFileOperator(), prompt)

    result = service.copy(source, destination)

    assert result.status == ProcessingStatus.OVERWRITTEN
    assert destination.read_bytes() == b"nuevo contenido"
