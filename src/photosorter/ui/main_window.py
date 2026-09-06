from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from photosorter.application.cancellation_token import CancellationToken
from photosorter.application.sorter_service import SorterService
from photosorter.domain.models.app_settings import AppSettings
from photosorter.domain.models.file_conflict import FileConflict
from photosorter.domain.models.photo import Photo
from photosorter.domain.models.processing_result import ProcessingResult, ProcessingStatus
from photosorter.domain.models.processing_summary import ProcessingSummary
from photosorter.domain.models.progress_estimate import ProgressEstimate
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
from photosorter.ui.conflict_dialog import ConflictDialog
from photosorter.ui.qt_conflict_prompt import QtConflictPrompt
from photosorter.ui.sorter_worker import SorterWorker


class MainWindow(QMainWindow):
    """Ventana unica de PhotoSorter V1 (Requisitos V1.0, seccion 12).

    Este archivo es la unica parte del sistema que sabe que existe PySide6
    (SAD, seccion 4.1): arma AppSettings, corre SorterService en un
    SorterWorker (QThread) y solo actualiza widgets desde los slots que Qt
    entrega en el hilo principal.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PhotoSorter")
        self.resize(480, 320)

        self._image_reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
        self._conflict_prompt = QtConflictPrompt(self)
        self._conflict_prompt.decision_requested.connect(self._on_conflict_requested)

        self._worker: SorterWorker | None = None
        self._error_count = 0

        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        folder_row = QHBoxLayout()
        self._folder_edit = QLineEdit()
        self._folder_edit.setReadOnly(True)
        self._folder_edit.setPlaceholderText("Elegi una carpeta con fotografias...")
        browse_button = QPushButton("Examinar...")
        browse_button.clicked.connect(self._choose_folder)
        folder_row.addWidget(QLabel("Carpeta:"))
        folder_row.addWidget(self._folder_edit)
        folder_row.addWidget(browse_button)
        layout.addLayout(folder_row)

        self._recursive_checkbox = QCheckBox("Incluir subcarpetas")
        layout.addWidget(self._recursive_checkbox)

        self._start_button = QPushButton("SEPARAR FOTOS")
        self._start_button.clicked.connect(self._on_start_or_cancel_clicked)
        layout.addWidget(self._start_button)

        self._status_label = QLabel("Estado: -")
        layout.addWidget(self._status_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setValue(0)
        layout.addWidget(self._progress_bar)

        self._counts_label = QLabel("Encontradas: 0   Procesadas: 0   Errores: 0")
        layout.addWidget(self._counts_label)

        self._eta_label = QLabel("Tiempo restante estimado: --:--")
        layout.addWidget(self._eta_label)

        self._summary_label = QLabel("")
        self._summary_label.setWordWrap(True)
        layout.addWidget(self._summary_label)

        self._open_results_button = QPushButton("Abrir carpeta de resultados")
        self._open_results_button.clicked.connect(self._open_results_folder)
        self._open_results_button.hide()
        layout.addWidget(self._open_results_button)

        layout.addStretch(1)

    # --- Seleccion de carpeta ---

    def _choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self._folder_edit.setText(folder)

    # --- Inicio / cancelacion ---

    def _on_start_or_cancel_clicked(self) -> None:
        if self._worker is not None:
            self._cancellation_token.cancel()
            self._start_button.setEnabled(False)
            self._status_label.setText("Estado: cancelando...")
            return

        self._start_processing()

    def _start_processing(self) -> None:
        folder_text = self._folder_edit.text().strip()
        if not folder_text:
            QMessageBox.warning(self, "PhotoSorter", "Primero elegí una carpeta.")
            return

        # RF-05 / Requisitos V1.0, seccion 9: las carpetas Verticales/
        # Horizontales/Cuadradas se crean dentro de la carpeta seleccionada,
        # no en una carpeta de destino separada.
        source_path = Path(folder_text)
        settings = AppSettings(
            source_path=source_path,
            destination_path=source_path,
            recursive=self._recursive_checkbox.isChecked(),
        )

        sorter_service = SorterService(
            file_scanner=DefaultFileScanner(self._image_reader),
            image_reader=self._image_reader,
            classifier=OrientationClassifier(),
            destination_resolver=DefaultDestinationResolver(),
            conflict_service=ConflictService(CopyFileOperator(), self._conflict_prompt),
        )
        self._cancellation_token = CancellationToken()
        self._settings = settings
        self._error_count = 0

        self._worker = SorterWorker(sorter_service, settings, self._cancellation_token, self)
        self._worker.started.connect(self._on_started)
        self._worker.file_started.connect(self._on_file_started)
        self._worker.file_completed.connect(self._on_file_completed)
        self._worker.finished_processing.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)

        self._summary_label.setText("")
        self._open_results_button.hide()
        self._folder_edit.setEnabled(False)
        self._recursive_checkbox.setEnabled(False)
        self._start_button.setText("Cancelar")
        self._status_label.setText("Estado: iniciando...")

        self._worker.start()

    # --- Slots del worker (ejecutados en el hilo principal) ---

    def _on_started(self, total_files: int) -> None:
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(max(total_files, 1))
        self._progress_bar.setValue(0)
        self._update_counts(found=total_files, processed=0)
        self._eta_label.setText("Tiempo restante estimado: calculando...")

    def _on_file_started(self, photo: Photo) -> None:
        self._status_label.setText(f"Procesando {photo.filename}")

    def _on_file_completed(
        self,
        processed_count: int,
        total_files: int,
        result: ProcessingResult,
        estimate: ProgressEstimate,
    ) -> None:
        if result.status == ProcessingStatus.FAILED:
            self._error_count += 1
        self._progress_bar.setValue(processed_count)
        self._update_counts(found=total_files, processed=processed_count)
        self._eta_label.setText(
            f"Tiempo restante estimado: {self._format_duration(estimate.remaining_seconds)}"
        )

    def _on_finished(self, summary: ProcessingSummary) -> None:
        self._reset_controls_after_run()
        self._eta_label.setText("Tiempo restante estimado: --:--")

        if summary.cancelled:
            self._status_label.setText("Estado: proceso cancelado")
            self._summary_label.setText(
                "PROCESO CANCELADO\n"
                f"Procesadas: {summary.processed_files} / {summary.total_files}\n"
                f"Copiadas: {summary.copied_files + summary.overwritten_files}\n"
                f"Errores: {summary.failed_files}"
            )
        else:
            self._status_label.setText("Estado: proceso finalizado")
            self._summary_label.setText(
                "PROCESAMIENTO COMPLETADO\n"
                f"{summary.total_files} fotografias analizadas\n"
                f"Verticales: {summary.vertical_count}\n"
                f"Horizontales: {summary.horizontal_count}\n"
                f"Cuadradas: {summary.square_count}\n"
                f"Errores: {summary.failed_files}"
            )

        self._open_results_button.show()

    def _on_failed(self, message: str) -> None:
        self._reset_controls_after_run()
        self._status_label.setText("Estado: error")
        QMessageBox.critical(self, "PhotoSorter", message)

    def _reset_controls_after_run(self) -> None:
        self._worker = None
        self._folder_edit.setEnabled(True)
        self._recursive_checkbox.setEnabled(True)
        self._start_button.setEnabled(True)
        self._start_button.setText("SEPARAR FOTOS")

    def _update_counts(self, found: int, processed: int) -> None:
        self._counts_label.setText(
            f"Encontradas: {found}   Procesadas: {processed}   Errores: {self._error_count}"
        )

    @staticmethod
    def _format_duration(seconds: float) -> str:
        total_seconds = int(round(seconds))
        minutes, secs = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    # --- Conflictos ---

    def _on_conflict_requested(self, conflict: FileConflict) -> None:
        dialog = ConflictDialog(conflict, self)
        dialog.exec()
        self._conflict_prompt.provide_decision(dialog.decision())

    # --- Resultado ---

    def _open_results_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._settings.destination_path)))
