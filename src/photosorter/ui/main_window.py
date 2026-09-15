from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPointF, Qt, QUrl, Signal
from PySide6.QtGui import (
    QCloseEvent,
    QColor,
    QDesktopServices,
    QImage,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
    QResizeEvent,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStyle,
    QStyleOptionButton,
    QVBoxLayout,
    QWidget,
)

from photosorter import beta_limiter  # BETA: sacar este import al retirar el limite
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
from photosorter.ui.title_bar import BAR_HEIGHT, TitleBar

# Paleta "dark, moderna y profesional": fondo, panel, tarjeta/control, borde
# sutil, azul principal, texto primario/secundario y rojo de error/cierre.
# Hardcodeada a proposito: es la identidad visual de la app, no un valor de
# configuracion. Las transparencias reales del tema se mantienen bajas
# (~5-10%), salvo el glow decorativo del bloque de resultados.
BG = "#07111F"
PANEL = "#0B1626"
CARD = "#101D2F"
BORDER = "#294563"
ACCENT = "#6195E5"
ACCENT_HOVER = "#4f7fce"
TEXT_PRIMARY = "#F2F5F8"
TEXT_SECONDARY = "#B8C2CF"
ERROR = "#E45B62"
ERROR_HOVER = "#c94850"

PROGRESS_GRADIENT_START = "#f26110"
PROGRESS_GRADIENT_END = "#f48229"

BUTTON_RADIUS = 10
GALLERY_NAV_SIZE = 40

BODY_MARGIN = 16
_RESIZE_MARGIN = 6

# Tamanios de la vista previa y de cada celda de la mini galeria, como
# fraccion del area total de la ventana (ancho x alto). La vista previa se
# agranda un poco respecto del pedido original (12%) para que sea el
# elemento visualmente protagonista de la seccion.
PREVIEW_AREA_FRACTION = 0.18
THUMBNAIL_AREA_FRACTION = 0.013
# "Procesando ahora" + "Galeria" se tratan como una unica seccion que ocupa
# ~40% del area total de la ventana.
MEDIA_SECTION_AREA_FRACTION = 0.40
GALLERY_COLUMNS = 3
GALLERY_ROWS = 2
GALLERY_SIZE = GALLERY_COLUMNS * GALLERY_ROWS  # 6 miniaturas, seccion "Grilla de Miniaturas"

# Stylesheet a nivel de aplicacion (ver __main__.py): asi los dialogos
# (ConflictDialog, QMessageBox) heredan la misma paleta sin duplicar reglas.
STYLE_SHEET = f"""
QWidget#appRoot, QDialog, QMessageBox {{
    background-color: {BG};
}}
QPushButton {{
    background-color: {ACCENT};
    color: {TEXT_PRIMARY};
    border: 1px solid {ACCENT};
    border-radius: {BUTTON_RADIUS}px;
    padding: 6px 14px;
}}
QPushButton:hover {{
    background-color: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
}}
QPushButton:disabled {{
    background-color: {BORDER};
    border-color: {BORDER};
    color: {TEXT_SECONDARY};
}}
QPushButton#galleryNavButton {{
    background-color: {CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {GALLERY_NAV_SIZE // 2}px;
    padding: 0px;
    font-weight: bold;
}}
QPushButton#galleryNavButton:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
    background-color: {CARD};
}}
QPushButton#galleryNavButton:disabled {{
    color: {TEXT_SECONDARY};
    border-color: {BORDER};
    background-color: {CARD};
}}
QLineEdit {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 3px 6px;
    background-color: {CARD};
    color: {TEXT_PRIMARY};
}}
QCheckBox {{
    background: transparent;
    color: {TEXT_PRIMARY};
}}
QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {BORDER};
    border-radius: 3px;
    background-color: {CARD};
}}
QCheckBox::indicator:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
}}
QFrame#leftPanel, QFrame#mediaFrame {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}
QFrame#previewStage {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
}}
QFrame#resultsFrame {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
}}
QLabel {{
    background: transparent;
    color: {TEXT_PRIMARY};
}}
QLabel#panelTitle {{
    color: {ACCENT};
    font-weight: bold;
}}
QLabel#secondaryLabel {{
    color: {TEXT_SECONDARY};
}}
QProgressBar {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    text-align: center;
    color: {TEXT_PRIMARY};
    background-color: {CARD};
}}
QProgressBar::chunk {{
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 {PROGRESS_GRADIENT_START}, stop: 1 {PROGRESS_GRADIENT_END}
    );
    border-radius: 3px;
}}
QPushButton#errorsToggle {{
    background-color: {CARD};
    color: {ERROR};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 10px;
    text-align: left;
    font-weight: bold;
}}
QPushButton#errorsToggle:hover {{
    border-color: {ERROR};
}}
QPlainTextEdit#errorsText {{
    background-color: {CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px;
}}
"""


class _ThumbnailCell(QLabel):
    """Una celda cuadrada de la mini galeria (seccion 'Grilla de Miniaturas').

    Bordes sutiles por defecto; la celda seleccionada (click del usuario)
    resalta con el azul principal de la paleta.
    """

    clicked = Signal(int)

    def __init__(self, slot: int) -> None:
        super().__init__()
        self._slot = slot
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_selected(False)

    def set_selected(self, selected: bool) -> None:
        border_color = ACCENT if selected else BORDER
        border_width = 2 if selected else 1
        self.setStyleSheet(
            f"background-color: {CARD}; color: {TEXT_SECONDARY};"
            f"border: {border_width}px solid {border_color}; border-radius: 4px;"
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - override de Qt
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._slot)
        super().mousePressEvent(event)


class _CheckBox(QCheckBox):
    """QCheckBox con un tilde dibujado a mano sobre el indicator al marcarlo.

    El relleno solido de QCheckBox::indicator:checked (ver STYLE_SHEET) no
    alcanza como feedback visual de que la opcion esta activa; Qt Style
    Sheets no soporta un ::indicator:checked con imagen sin apuntar a un
    archivo o recurso Qt, asi que el tilde se dibuja a mano (sin assets),
    igual que el resaltado de seleccion de _ThumbnailCell.
    """

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802 - override de Qt
        super().paintEvent(event)
        if not self.isChecked():
            return

        option = QStyleOptionButton()
        self.initStyleOption(option)
        rect = self.style().subElementRect(
            QStyle.SubElement.SE_CheckBoxIndicator, option, self
        )

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(TEXT_PRIMARY))
        pen.setWidthF(1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Tilde de dos segmentos (estilo Material Design), en coordenadas
        # relativas al indicator para no depender de su tamanio exacto.
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        start = QPointF(x + w * 0.22, y + h * 0.55)
        middle = QPointF(x + w * 0.42, y + h * 0.75)
        end = QPointF(x + w * 0.80, y + h * 0.28)
        painter.drawLine(start, middle)
        painter.drawLine(middle, end)


class MainWindow(QMainWindow):
    """Ventana unica de PhotoSorter V1 (Requisitos V1.0, seccion 12).

    Este archivo es la unica parte del sistema que sabe que existe PySide6
    (SAD, seccion 4.1): arma AppSettings, corre SorterService en un
    SorterWorker (QThread) y solo actualiza widgets desde los slots que Qt
    entrega en el hilo principal.

    Ventana sin marco nativo (ver ui/title_bar.py): se necesita control por
    boton sobre color (la cruz de cerrar siempre en rojo, distinta del resto),
    algo que el chrome de Windows no permite. Arrastrar los bordes
    redimensiona via QWindow.startSystemResize().
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PhotoSorter")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(1040, 680)
        self.setMinimumSize(860, 560)

        self._image_reader = CompositeImageReader([RawImageReader(), StandardImageReader()])
        self._conflict_prompt = QtConflictPrompt(self)
        self._conflict_prompt.decision_requested.connect(self._on_conflict_requested)

        self._worker: SorterWorker | None = None
        self._error_count = 0
        # (source_path, mensaje) de cada archivo que termino en FAILED,
        # en el orden en que ocurrieron. Alimenta el desplegable de
        # errores (parte inferior del panel de configuracion).
        self._error_log: list[tuple[Path, str]] = []

        # Historial de (Photo, QImage | None) en el orden en que se van
        # procesando: alimenta la vista previa y la mini galeria.
        self._history: list[tuple[Photo, QImage | None]] = []
        self._gallery_offset = 0
        self._gallery_follow = True
        # None = seguir mostrando la ultima foto procesada; si el usuario
        # hace click en una miniatura, queda fijada esa seleccion.
        self._selected_index: int | None = None

        self._build_ui()
        self._apply_media_sizes()

    def _build_ui(self) -> None:
        central = QWidget(self)
        central.setObjectName("appRoot")
        self.setCentralWidget(central)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self._title_bar = TitleBar("PhotoSorter")
        self._title_bar.minimize_clicked.connect(self.showMinimized)
        self._title_bar.maximize_clicked.connect(self._toggle_maximize)
        self._title_bar.close_clicked.connect(self.close)
        outer_layout.addWidget(self._title_bar)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(BODY_MARGIN, BODY_MARGIN, BODY_MARGIN, BODY_MARGIN)
        body_layout.setSpacing(BODY_MARGIN)
        body_layout.addWidget(self._build_left_panel(), 1)
        body_layout.addWidget(self._build_media_section(), 0)
        outer_layout.addWidget(body, 1)

    def _toggle_maximize(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # --- Cierre de la ventana (cruz de la barra de titulo, Alt+F4, etc.) ---

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802 - override de Qt
        worker = self._worker
        if worker is None:
            if self._confirm("¿Seguro que querés cerrar PhotoSorter?"):
                event.accept()
            else:
                event.ignore()
            return

        # Se frena el procesamiento (entre archivo y archivo, sin
        # interrumpir una copia en curso; ver CancellationToken) mientras
        # se espera la respuesta del usuario, y se retoma tal cual estaba
        # si decide no cerrar.
        self._cancellation_token.pause()
        confirmed = self._confirm(
            "Hay un proceso de organizacion en curso.\n"
            "¿Seguro que querés cancelarlo y cerrar PhotoSorter?"
        )

        if not confirmed:
            self._cancellation_token.resume()
            event.ignore()
            return

        self._cancellation_token.cancel()
        worker.wait(5000)
        event.accept()

    # --- Redimensionar arrastrando los bordes (ventana sin marco nativo) ---

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            edges = self._resize_edges(event.position().toPoint())
            window = self.windowHandle()
            if edges and window is not None:
                window.startSystemResize(edges)
                return
        super().mousePressEvent(event)

    def _resize_edges(self, pos) -> Qt.Edge:
        edges = Qt.Edge(0)
        rect = self.rect()
        margin = _RESIZE_MARGIN
        if pos.x() <= margin:
            edges |= Qt.Edge.LeftEdge
        elif pos.x() >= rect.width() - margin:
            edges |= Qt.Edge.RightEdge
        if pos.y() <= margin:
            edges |= Qt.Edge.TopEdge
        elif pos.y() >= rect.height() - margin:
            edges |= Qt.Edge.BottomEdge
        return edges

    # --- Panel izquierdo: configuracion y estado de procesamiento ---

    def _build_left_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("leftPanel")
        layout = QVBoxLayout(panel)

        title = QLabel("Configuracion")
        title.setObjectName("panelTitle")
        layout.addWidget(title)

        folder_row = QHBoxLayout()
        folder_label = QLabel("Carpeta:")
        folder_label.setObjectName("secondaryLabel")
        self._folder_edit = QLineEdit()
        self._folder_edit.setReadOnly(True)
        self._folder_edit.setPlaceholderText("Elegi una carpeta con fotografias...")
        browse_button = QPushButton("Examinar...")
        browse_button.clicked.connect(self._choose_folder)
        folder_row.addWidget(folder_label)
        folder_row.addWidget(self._folder_edit)
        folder_row.addWidget(browse_button)
        layout.addLayout(folder_row)

        self._recursive_checkbox = _CheckBox("Incluir subcarpetas")
        layout.addWidget(self._recursive_checkbox)

        self._start_button = QPushButton("SEPARAR FOTOS")
        self._start_button.clicked.connect(self._on_start_or_cancel_clicked)
        layout.addWidget(self._start_button)

        self._status_label = QLabel("Estado: -")
        self._status_label.setObjectName("secondaryLabel")
        layout.addWidget(self._status_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setValue(0)
        layout.addWidget(self._progress_bar)

        layout.addWidget(self._build_results_frame())

        self._open_results_button = QPushButton("Abrir carpeta de resultados")
        self._open_results_button.clicked.connect(self._open_results_folder)
        self._open_results_button.hide()
        layout.addWidget(self._open_results_button)

        layout.addStretch(1)
        layout.addWidget(self._build_errors_panel())
        return panel

    def _build_errors_panel(self) -> QFrame:
        # Desplegable pegado a la parte inferior de la ventana (RF de
        # detalle de errores): colapsado por defecto para no competir con
        # el resto del panel, oculto por completo mientras no haya errores.
        frame = QFrame()
        frame.setObjectName("errorsFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._errors_toggle = QPushButton()
        self._errors_toggle.setObjectName("errorsToggle")
        self._errors_toggle.setCheckable(True)
        self._errors_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self._errors_toggle.clicked.connect(self._on_errors_toggle_clicked)
        layout.addWidget(self._errors_toggle)

        self._errors_text = QPlainTextEdit()
        self._errors_text.setObjectName("errorsText")
        self._errors_text.setReadOnly(True)
        self._errors_text.setMaximumHeight(140)
        self._errors_text.hide()
        layout.addWidget(self._errors_text)

        self._errors_frame = frame
        self._reset_errors_panel()
        frame.hide()
        return frame

    def _build_results_frame(self) -> QFrame:
        # Tratado como una sub-seccion aparte (tarjeta propia), con un
        # resplandor exterior sutil en el azul principal: un efecto de
        # contenedor, no aplicado letra por letra.
        frame = QFrame()
        frame.setObjectName("resultsFrame")
        layout = QVBoxLayout(frame)

        self._counts_label = QLabel("Encontradas: 0   Procesadas: 0   Errores: 0")
        layout.addWidget(self._counts_label)

        self._eta_label = QLabel("Tiempo restante estimado: --:--")
        self._eta_label.setObjectName("secondaryLabel")
        layout.addWidget(self._eta_label)

        self._summary_label = QLabel("")
        self._summary_label.setWordWrap(True)
        layout.addWidget(self._summary_label)

        glow_color = QColor(ACCENT)
        glow_color.setAlpha(26)  # ~10%: el resto del tema evita transparencias mayores
        glow = QGraphicsDropShadowEffect(frame)
        glow.setColor(glow_color)
        glow.setBlurRadius(36)
        glow.setOffset(0, 0)
        frame.setGraphicsEffect(glow)
        return frame

    # --- Seccion derecha: "Procesando ahora" + "Galeria" como una unidad ---

    def _build_media_section(self) -> QFrame:
        section = QFrame()
        section.setObjectName("mediaFrame")
        self._media_frame = section
        layout = QVBoxLayout(section)

        preview_title = QLabel("Procesando ahora")
        preview_title.setObjectName("panelTitle")
        layout.addWidget(preview_title)

        # "Escenario" oscuro alrededor de la vista previa: la vuelve el
        # elemento visualmente protagonista de la seccion.
        preview_stage = QFrame()
        preview_stage.setObjectName("previewStage")
        preview_stage_layout = QVBoxLayout(preview_stage)
        preview_stage_layout.setContentsMargins(14, 14, 14, 14)
        self._preview_label = QLabel("Sin vista previa")
        self._preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._preview_label.setStyleSheet(f"color: {TEXT_SECONDARY};")
        preview_stage_layout.addWidget(self._preview_label)
        layout.addWidget(preview_stage, alignment=Qt.AlignmentFlag.AlignHCenter)

        gallery_title = QLabel("Galeria")
        gallery_title.setObjectName("panelTitle")
        layout.addWidget(gallery_title)

        grid = QGridLayout()
        grid.setSpacing(4)
        self._thumbnail_cells: list[_ThumbnailCell] = []
        for index in range(GALLERY_SIZE):
            cell = _ThumbnailCell(slot=index)
            cell.clicked.connect(self._on_thumbnail_clicked)
            self._thumbnail_cells.append(cell)
            grid.addWidget(cell, index // GALLERY_COLUMNS, index % GALLERY_COLUMNS)
        grid_wrapper = QHBoxLayout()
        grid_wrapper.addStretch(1)
        grid_wrapper.addLayout(grid)
        grid_wrapper.addStretch(1)
        layout.addLayout(grid_wrapper)

        nav_row = QHBoxLayout()
        nav_row.addStretch(1)
        self._gallery_prev_button = QPushButton("◀")
        self._gallery_prev_button.setObjectName("galleryNavButton")
        self._gallery_prev_button.setFixedSize(GALLERY_NAV_SIZE, GALLERY_NAV_SIZE)
        self._gallery_prev_button.clicked.connect(self._on_gallery_prev)
        self._gallery_next_button = QPushButton("▶")
        self._gallery_next_button.setObjectName("galleryNavButton")
        self._gallery_next_button.setFixedSize(GALLERY_NAV_SIZE, GALLERY_NAV_SIZE)
        self._gallery_next_button.clicked.connect(self._on_gallery_next)
        nav_row.addWidget(self._gallery_prev_button)
        nav_row.addSpacing(12)
        nav_row.addWidget(self._gallery_next_button)
        nav_row.addStretch(1)
        layout.addLayout(nav_row)

        layout.addStretch(1)
        self._update_gallery_nav_buttons()
        return section

    # --- Tamanios dependientes del tamanio de la ventana ---

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802 - override de Qt
        super().resizeEvent(event)
        self._apply_media_sizes()

    def _apply_media_sizes(self) -> None:
        width = max(self.width(), 1)
        height = max(self.height(), 1)
        total_area = width * height

        # La seccion "Procesando ahora" + "Galeria" ocupa un ~40% del area
        # total de la ventana, con la altura ajustada al alto disponible del
        # cuerpo (bajo la barra de titulo) para que su borde inferior quede
        # a la misma altura que el panel de configuracion.
        content_height = max(height - BAR_HEIGHT - 2 * BODY_MARGIN, 1)
        section_area = total_area * MEDIA_SECTION_AREA_FRACTION
        max_section_width = max(width - 3 * BODY_MARGIN - 260, 220)
        section_width = min(
            max(int(section_area / content_height), 220),
            max_section_width,
        )
        self._media_frame.setFixedSize(section_width, content_height)

        preview_area = total_area * PREVIEW_AREA_FRACTION
        preview_h = max(int((preview_area * 3 / 4) ** 0.5), 60)
        preview_w = max(int(preview_h * 4 / 3), 80)
        self._preview_label.setFixedSize(preview_w, preview_h)

        thumb_side = max(int((total_area * THUMBNAIL_AREA_FRACTION) ** 0.5), 28)
        for cell in self._thumbnail_cells:
            cell.setFixedSize(thumb_side, thumb_side)

        self._refresh_preview_pixmap()
        self._refresh_gallery_pixmaps()

    # --- Seleccion de carpeta ---

    def _choose_folder(self) -> None:
        # BETA: sacar este chequeo (y _show_beta_limit_dialog) al retirar el limite.
        if beta_limiter.has_reached_limit():
            self._show_beta_limit_dialog()
            return
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self._folder_edit.setText(folder)

    def _show_beta_limit_dialog(self) -> None:  # BETA: sacar este metodo al retirar el limite
        box = QMessageBox(
            QMessageBox.Icon.Information, "PhotoSorter", beta_limiter.LIMIT_MESSAGE, parent=self
        )
        box.addButton("Cerrar", QMessageBox.ButtonRole.RejectRole)
        box.exec()

    # --- Inicio / cancelacion ---

    def _on_start_or_cancel_clicked(self) -> None:
        if self._worker is not None:
            self._request_cancel()
            return

        self._start_processing()

    def _request_cancel(self) -> None:
        # Mismo criterio que closeEvent: se pausa (entre archivo y
        # archivo) mientras se pregunta, y se retoma tal cual estaba si el
        # usuario se arrepiente.
        self._cancellation_token.pause()
        confirmed = self._confirm("¿Seguro que querés cancelar el proceso de organización?")

        if not confirmed:
            self._cancellation_token.resume()
            return

        self._cancellation_token.cancel()
        self._start_button.setEnabled(False)
        self._status_label.setText("Estado: cancelando...")

    def _start_processing(self) -> None:
        # BETA: sacar este chequeo al retirar el limite.
        if beta_limiter.has_reached_limit():
            self._show_beta_limit_dialog()
            return

        folder_text = self._folder_edit.text().strip()
        if not folder_text:
            self._warn("Primero elegí una carpeta.")
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
        self._error_log = []
        self._reset_errors_panel()
        self._history = []
        self._gallery_offset = 0
        self._gallery_follow = True
        self._selected_index = None
        self._refresh_preview_pixmap()
        self._refresh_gallery_pixmaps()
        self._update_gallery_nav_buttons()

        self._worker = SorterWorker(
            sorter_service,
            settings,
            self._cancellation_token,
            self,
            # BETA: sacar este argumento al retirar el limite.
            max_photos=beta_limiter.remaining_allowance(),
        )
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

    def _on_file_started(self, photo: Photo, image: QImage | None) -> None:
        self._status_label.setText(f"Procesando {photo.filename}")

        self._history.append((photo, image))
        if self._gallery_follow:
            self._gallery_offset = max(0, len(self._history) - GALLERY_SIZE)

        self._refresh_preview_pixmap()
        self._refresh_gallery_pixmaps()
        self._update_gallery_nav_buttons()

    def _on_file_completed(
        self,
        processed_count: int,
        total_files: int,
        result: ProcessingResult,
        estimate: ProgressEstimate,
    ) -> None:
        if result.status == ProcessingStatus.FAILED:
            self._error_count += 1
            self._record_error(result)
        self._progress_bar.setValue(processed_count)
        self._update_counts(found=total_files, processed=processed_count)
        self._eta_label.setText(
            f"Tiempo restante estimado: {self._format_duration(estimate.remaining_seconds)}"
        )

    def _on_finished(self, summary: ProcessingSummary) -> None:
        self._reset_controls_after_run()
        self._eta_label.setText("Tiempo restante estimado: --:--")
        # BETA: sacar esta linea al retirar el limite.
        beta_limiter.register_processed(summary.processed_files)

        if summary.total_files == 0:
            self._status_label.setText("Estado: sin fotografías")
            self._warn("Esta carpeta no contiene imágenes.")
            return

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

        # BETA: sacar este bloque al retirar el limite.
        if beta_limiter.has_reached_limit():
            self._summary_label.setText(
                self._summary_label.text() + "\n\n" + beta_limiter.LIMIT_MESSAGE
            )

        self._open_results_button.show()

    def _on_failed(self, message: str) -> None:
        self._reset_controls_after_run()
        self._status_label.setText("Estado: error")
        self._critical(message)

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

    # --- Vista previa actual ---

    def _current_preview_index(self) -> int | None:
        if self._selected_index is not None:
            return self._selected_index
        if self._history:
            return len(self._history) - 1
        return None

    def _refresh_preview_pixmap(self) -> None:
        index = self._current_preview_index()
        image = self._history[index][1] if index is not None else None
        if image is None:
            # No llamar setPixmap aca: un QPixmap nulo pisa el texto (QLabel
            # solo puede mostrar uno de los dos a la vez).
            self._preview_label.setText("Sin vista previa")
            return

        pixmap = QPixmap.fromImage(image).scaled(
            self._preview_label.width(),
            self._preview_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._preview_label.setText("")
        self._preview_label.setPixmap(pixmap)

    # --- Mini galeria ---

    def _refresh_gallery_pixmaps(self) -> None:
        for slot, cell in enumerate(self._thumbnail_cells):
            index = self._gallery_offset + slot
            cell.set_selected(index == self._selected_index)

            if index >= len(self._history):
                # Menos de 6 fotos disponibles todavia: la celda queda
                # vacia con su tamanio fijo, no se agranda el resto.
                cell.setText("")
                cell.setPixmap(QPixmap())
                continue

            _, image = self._history[index]
            if image is None:
                cell.setPixmap(QPixmap())
                cell.setText("?")
                continue

            pixmap = QPixmap.fromImage(image).scaled(
                cell.width(),
                cell.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            cell.setText("")
            cell.setPixmap(pixmap)

    def _on_thumbnail_clicked(self, slot: int) -> None:
        index = self._gallery_offset + slot
        if index >= len(self._history):
            return
        self._selected_index = index
        # Ademas de fijar la vista previa, se deja de seguir el
        # procesamiento en vivo: si no, la grilla se sigue corriendo hacia
        # las fotos nuevas y un segundo click termina cayendo sobre una
        # miniatura distinta a la que el usuario ve en pantalla.
        self._gallery_follow = False
        self._refresh_preview_pixmap()
        self._refresh_gallery_pixmaps()
        self._update_gallery_nav_buttons()

    def _on_gallery_prev(self) -> None:
        self._gallery_offset = max(0, self._gallery_offset - 1)
        self._gallery_follow = False
        self._refresh_gallery_pixmaps()
        self._update_gallery_nav_buttons()

    def _on_gallery_next(self) -> None:
        max_offset = max(0, len(self._history) - GALLERY_SIZE)
        self._gallery_offset = min(max_offset, self._gallery_offset + 1)
        self._gallery_follow = self._gallery_offset >= max_offset
        self._refresh_gallery_pixmaps()
        self._update_gallery_nav_buttons()

    def _update_gallery_nav_buttons(self) -> None:
        max_offset = max(0, len(self._history) - GALLERY_SIZE)
        self._gallery_prev_button.setEnabled(self._gallery_offset > 0)
        self._gallery_next_button.setEnabled(self._gallery_offset < max_offset)

    # --- Conflictos ---

    def _on_conflict_requested(self, conflict: FileConflict) -> None:
        dialog = ConflictDialog(conflict, self)
        dialog.exec()
        self._conflict_prompt.provide_decision(dialog.decision())

    # --- Resultado ---

    def _open_results_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._settings.destination_path)))

    # --- Desplegable de errores ---

    def _record_error(self, result: ProcessingResult) -> None:
        # result.error ya viene armado por ImageReader/SorterService con
        # que paso (ver TDD, seccion 13-14): aca solo se le suma el
        # archivo puntual y se muestra, sin re-parsear logs de texto.
        message = result.error or "Error desconocido"
        self._error_log.append((result.source_path, message))
        self._errors_text.setPlainText(
            "\n".join(f"-> {path}: {msg}" for path, msg in self._formatted_error_log())
        )
        self._errors_frame.show()
        self._set_errors_toggle_text()
        # Ultimo error visible sin que el usuario tenga que desplazarse.
        self._errors_text.verticalScrollBar().setValue(
            self._errors_text.verticalScrollBar().maximum()
        )

    def _formatted_error_log(self) -> list[tuple[str, str]]:
        return [(self._relative_to_source(path), message) for path, message in self._error_log]

    def _relative_to_source(self, path: Path) -> str:
        source = getattr(self, "_settings", None)
        if source is not None:
            return str(path.relative_to(source.source_path))
        return str(path)

    def _reset_errors_panel(self) -> None:
        self._errors_text.clear()
        self._errors_toggle.setChecked(False)
        self._errors_text.hide()
        self._set_errors_toggle_text()
        self._errors_frame.hide()

    def _set_errors_toggle_text(self) -> None:
        expanded = self._errors_toggle.isChecked()
        arrow = "▾" if expanded else "▸"
        count = len(self._error_log)
        label = "error" if count == 1 else "errores"
        self._errors_toggle.setText(f"{arrow} {count} {label} - ver detalle")

    def _on_errors_toggle_clicked(self) -> None:
        expanded = self._errors_toggle.isChecked()
        self._errors_text.setVisible(expanded)
        self._set_errors_toggle_text()

    # --- Dialogos ---

    def _warn(self, message: str) -> None:
        box = QMessageBox(QMessageBox.Icon.Warning, "PhotoSorter", message, parent=self)
        box.exec()

    def _critical(self, message: str) -> None:
        box = QMessageBox(QMessageBox.Icon.Critical, "PhotoSorter", message, parent=self)
        box.exec()

    def _confirm(self, message: str) -> bool:
        box = QMessageBox(QMessageBox.Icon.Question, "PhotoSorter", message, parent=self)
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setDefaultButton(QMessageBox.StandardButton.No)
        return box.exec() == QMessageBox.StandardButton.Yes
