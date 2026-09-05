from __future__ import annotations

import logging
from collections import Counter

from photosorter.application.cancellation_token import CancellationToken
from photosorter.application.null_progress_reporter import NullProgressReporter
from photosorter.domain.interfaces.classifier import Classifier
from photosorter.domain.interfaces.destination_resolver import DestinationResolver
from photosorter.domain.interfaces.file_scanner import FileScanner
from photosorter.domain.interfaces.image_reader import ImageReader, ImageReaderError
from photosorter.domain.interfaces.progress_reporter import ProgressReporter
from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.classification import Classification
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.processing_result import ProcessingResult, ProcessingStatus
from photosorter.domain.models.processing_summary import ProcessingSummary
from photosorter.domain.services.conflict_service import ConflictService

_logger = logging.getLogger(__name__)


class SorterService:
    """Orquesta el procesamiento completo de una carpeta de fotografias.

    Ver Docs/System Architecture Document - SAD.md, seccion 5: coordina
    FileScanner, ImageReader, Classifier, DestinationResolver y
    ConflictService, sin conocer los detalles internos de cada uno.

    Politica de errores (TDD, seccion 13-14, CA-08): un error al leer una
    fotografia individual no detiene el resto del procesamiento; se
    registra como ProcessingStatus.FAILED y se continua con la siguiente.
    """

    def __init__(
        self,
        file_scanner: FileScanner,
        image_reader: ImageReader,
        classifier: Classifier,
        destination_resolver: DestinationResolver,
        conflict_service: ConflictService,
        logger: logging.Logger | None = None,
    ) -> None:
        self._file_scanner = file_scanner
        self._image_reader = image_reader
        self._classifier = classifier
        self._destination_resolver = destination_resolver
        self._conflict_service = conflict_service
        self._logger = logger or _logger

    def run(
        self,
        settings: AppSettings,
        progress_reporter: ProgressReporter | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> ProcessingSummary:
        reporter = progress_reporter or NullProgressReporter()
        token = cancellation_token or CancellationToken()

        self._logger.info("Processing started")
        self._logger.info("Source: %s", settings.source_path)
        self._logger.info("Recursive: %s", settings.recursive)

        photos = self._file_scanner.scan(settings)
        total_files = len(photos)
        self._logger.info("Files found: %d", total_files)
        reporter.on_started(total_files)

        status_counts: Counter[ProcessingStatus] = Counter()
        classification_counts: Counter[Classification] = Counter()
        processed = 0
        cancelled = False

        for photo in photos:
            if token.is_cancelled:
                cancelled = True
                break

            reporter.on_file_started(photo)
            result, classification = self._process_photo(photo, settings)
            processed += 1
            status_counts[result.status] += 1
            if classification is not None:
                classification_counts[classification] += 1
            reporter.on_file_completed(processed, total_files, result)

        summary = ProcessingSummary(
            total_files=total_files,
            processed_files=processed,
            copied_files=status_counts[ProcessingStatus.COPIED],
            skipped_files=status_counts[ProcessingStatus.SKIPPED],
            overwritten_files=status_counts[ProcessingStatus.OVERWRITTEN],
            failed_files=status_counts[ProcessingStatus.FAILED],
            vertical_count=classification_counts[Classification.VERTICAL],
            horizontal_count=classification_counts[Classification.HORIZONTAL],
            square_count=classification_counts[Classification.SQUARE],
            cancelled=cancelled,
        )

        self._logger.info("Processing cancelled" if cancelled else "Processing finished")
        reporter.on_finished(summary)
        return summary

    def _process_photo(
        self, photo: Photo, settings: AppSettings
    ) -> tuple[ProcessingResult, Classification | None]:
        try:
            metadata = self._image_reader.read(photo)
            classification = self._classifier.classify(metadata)
        except (ImageReaderError, OSError) as exc:
            self._logger.error("%s -> ERROR: %s", photo.filename, exc)
            return (
                ProcessingResult(
                    source_path=photo.source_path, status=ProcessingStatus.FAILED, error=str(exc)
                ),
                None,
            )

        destination = self._destination_resolver.resolve(photo, classification, settings)

        try:
            result = self._conflict_service.copy(photo.source_path, destination.path)
        except OSError as exc:
            self._logger.error("%s -> ERROR: %s", photo.filename, exc)
            return (
                ProcessingResult(
                    source_path=photo.source_path, status=ProcessingStatus.FAILED, error=str(exc)
                ),
                classification,
            )

        self._logger.info(
            "%s -> %s (%s)", photo.filename, classification.value.upper(), result.status.value
        )
        return result, classification
