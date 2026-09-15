from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from photosorter.application.cancellation_token import CancellationToken
from photosorter.application.sorter_service import SorterService
from photosorter.domain.interfaces.file_scanner import SourceFolderError
from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.processing_result import ProcessingResult
from photosorter.domain.models.processing_summary import ProcessingSummary
from photosorter.domain.models.progress_estimate import ProgressEstimate
from photosorter.ui.thumbnail import load_preview_image


class SorterWorker(QThread):
    """Corre SorterService.run() fuera del hilo de UI (SAD, seccion 20).

    Implementa el Protocol ProgressReporter emitiendo senales Qt en vez de
    tocar widgets directamente: los widgets solo se actualizan en los slots
    conectados, que Qt entrega en el hilo principal.
    """

    # Se usa "object" (no el tipo Python concreto) para los payloads
    # complejos: es la forma recomendada en PySide6 de cruzar objetos
    # Python arbitrarios entre hilos via QueuedConnection.
    started = Signal(int)
    # La miniatura (QImage o None) se extrae aca, en el hilo de fondo, para
    # no bloquear la UI decodificando RAW/JPEG cada vez que arranca un
    # archivo (ver ui/thumbnail.py).
    file_started = Signal(object, object)  # Photo, QImage | None
    file_completed = Signal(int, int, object, object)  # processed, total, result, estimate
    finished_processing = Signal(object)  # ProcessingSummary
    failed = Signal(str)

    def __init__(
        self,
        sorter_service: SorterService,
        settings: AppSettings,
        cancellation_token: CancellationToken,
        parent=None,
        max_photos: int | None = None,
    ) -> None:
        super().__init__(parent)
        self._sorter_service = sorter_service
        self._settings = settings
        self._cancellation_token = cancellation_token
        self._max_photos = max_photos

    # --- ProgressReporter ---

    def on_started(self, total_files: int) -> None:
        self.started.emit(total_files)

    def on_file_started(self, photo: Photo) -> None:
        image = load_preview_image(photo.source_path)
        self.file_started.emit(photo, image)

    def on_file_completed(
        self,
        processed_count: int,
        total_files: int,
        result: ProcessingResult,
        estimate: ProgressEstimate,
    ) -> None:
        self.file_completed.emit(processed_count, total_files, result, estimate)

    def on_finished(self, summary: ProcessingSummary) -> None:
        self.finished_processing.emit(summary)

    # --- QThread ---

    def run(self) -> None:
        try:
            self._sorter_service.run(
                self._settings,
                progress_reporter=self,
                cancellation_token=self._cancellation_token,
                max_photos=self._max_photos,
            )
        except SourceFolderError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # noqa: BLE001 - ultima red de seguridad del worker
            self.failed.emit(f"Error inesperado: {exc}")
