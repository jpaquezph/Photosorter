from __future__ import annotations

from photosorter.domain.models.photo import Photo
from photosorter.domain.models.processing_result import ProcessingResult
from photosorter.domain.models.processing_summary import ProcessingSummary
from photosorter.domain.models.progress_estimate import ProgressEstimate


class NullProgressReporter:
    """ProgressReporter que no hace nada.

    Default de SorterService.run() cuando no hay UI (scripts, tests).
    """

    def on_started(self, total_files: int) -> None:
        pass

    def on_file_started(self, photo: Photo) -> None:
        pass

    def on_file_completed(
        self,
        processed_count: int,
        total_files: int,
        result: ProcessingResult,
        estimate: ProgressEstimate,
    ) -> None:
        pass

    def on_finished(self, summary: ProcessingSummary) -> None:
        pass
