# CONTEXTO.md

**Propósito:** este archivo es un registro vivo de las decisiones técnicas y el avance de código que se va tomando/generando en las charlas de desarrollo de PhotoSorter. No reemplaza a los documentos formales (`Objetivo, principios y requerimientos.md`, `Requisitos V1.0.md`, `System Architecture Document - SAD.md`, `Technical Design Document (TDD).md`, `Contract Specification — Domain Models.md`); los complementa con el "qué se hizo y por qué" sesión a sesión.

Cada sesión de trabajo agrega una entrada nueva al final del historial, sin reescribir las anteriores. Si una decisión previa cambia, se anota el cambio en la nueva entrada en vez de editar la vieja (para conservar la trazabilidad).

---

## Stack definido (estado actual)

| Capa | Elección |
|---|---|
| Lenguaje | Python 3.11+ |
| GUI | PySide6 (Qt Widgets) |
| Formatos estándar (JPG/PNG/TIFF/WEBP) | Pillow |
| RAW (NEF/CR2/CR3/ARW/DNG/RAF/ORF/RW2) | rawpy (wrapper de LibRaw) |
| Gestión de dependencias | uv |
| Testing | pytest |
| Packaging | PyInstaller (`--onedir`) + instalador con Inno Setup |
| Logging | `logging` estándar de Python |

No se mezclan tecnologías web (React/Electron/TypeScript/PHP) con el backend Python: la app es un único proceso Python + Qt, sin Node ni navegador embebido, para cumplir con el requisito de bajo consumo de recursos (RNF-04) y mantener una sola stack de lenguaje en toda la aplicación.

## Estado actual del proyecto

Fase: **Milestone M4 completo** (aplicación de escritorio funcional de punta a punta con interfaz PySide6). Falta solo el packaging (M5, PyInstaller) para tener un `.exe` distribuible.

Documentación existente en `Docs/`:
- Objetivo, principios y requerimientos
- Requisitos V1.0
- System Architecture Document (SAD)
- Technical Design Document (TDD)
- Contract Specification — Domain Models

Estructura de código (`src/photosorter/`):
- `domain/models/`: `Photo`, `PhotoMetadata`, `Classification`, `DestinationPath`, `FileConflict`, `ConflictResolution`, `ConflictDecision` (extensión propia), `ProcessingResult` + `ProcessingStatus` (resultado de una foto), `ProcessingSummary` (resultado agregado de toda la carpeta — extensión propia), `AppSettings`. Todos dataclasses `frozen=True` con validación en `__post_init__`.
- `domain/interfaces/`: `ImageReader` (+ `ImageReaderError`), `Classifier`, `DestinationResolver`, `FileOperator` (+ `DestinationAlreadyExistsError`), `ConflictPrompt`, `FileScanner` (+ `SourceFolderError`), `ProgressReporter` — todos `Protocol`.
- `domain/services/`: `OrientationClassifier`, `ConflictService`.
- `infrastructure/image/`: `StandardImageReader` (Pillow), `RawImageReader` (rawpy), `CompositeImageReader`.
- `infrastructure/filesystem/`: `DefaultDestinationResolver`, `CopyFileOperator`, `DefaultFileScanner` (recorre una carpeta con/sin recursividad, delega en un `ImageReader` para saber qué archivos son fotos soportadas).
- `application/`: `SorterService`, `CancellationToken`, `NullProgressReporter`.
- `ui/`: **primer código en esta capa.** `MainWindow` (la única ventana, `QMainWindow`), `SorterWorker` (`QThread` que corre `SorterService.run()` e implementa `ProgressReporter` emitiendo señales Qt), `QtConflictPrompt` (implementa `ConflictPrompt` cruzando de worker thread a UI thread), `ConflictDialog` (`QDialog` con botones Omitir/Reemplazar + checkbox "aplicar a los restantes").
- `__main__.py`: entry point (`python -m photosorter`, o el comando `photosorter` una vez instalado — ver `[project.scripts]` en `pyproject.toml`).

Pendiente de implementar: el packaging con PyInstaller (M5) para generar el `.exe` distribuible sin Python.

Tests automatizados: 73 pasan, 0 se saltean (2 RAWs reales de muestra en `tests/fixtures/raw/`, no versionados). La UI en sí se validó con scripts de smoke-test manuales (no forman parte de la suite de pytest) que corrieron la app real de punta a punta — ver historial de esta sesión para el detalle.

Próximo paso técnico definido: **Milestone M5** — Packaging: generar el `.exe` con PyInstaller (`--onedir`) y probarlo en un Windows sin Python instalado, siguiendo TDD §34.

---

## Historial de sesiones

### 2026-09-05 — Definición de stack y arranque de documentación de contexto

- Se revisó toda la carpeta `Docs/` para tener el contexto completo del proyecto (objetivo, requisitos, arquitectura, diseño técnico, contratos de dominio).
- Se cerró la decisión pendiente del **RAW Spike** (TDD §29): se elige **rawpy** como librería de lectura RAW, salvo que aparezcan problemas concretos al probar con el dataset real de RAWs del usuario.
- Se confirmó el resto del stack (ver tabla arriba), reutilizando lo ya propuesto en SAD/TDD (Python + PySide6 + Pillow + PyInstaller) y agregando las piezas que faltaban (rawpy, uv, pytest, Inno Setup).
- Se decidió explícitamente **no mezclar la interfaz gráfica con tecnologías web** (React/Electron/TypeScript) para no romper el requisito de bajo consumo de recursos ni la simplicidad arquitectónica ya definida en el SAD.
- Se creó este archivo (`CONTEXTO.md`) para llevar un registro incremental de las decisiones y el avance de código en cada sesión.
- **Pendiente para la próxima sesión:** arrancar M0 — scaffolding del proyecto (`pyproject.toml`, estructura `src/photosorter/{domain,application,infrastructure}`, `tests/`) y primeros modelos de dominio (`Photo`, `PhotoMetadata`, `Classification`) con `OrientationClassifier` y sus tests.

### 2026-09-05 (continuación) — Scaffolding del proyecto y Milestone M0

- **Entorno:** la máquina no tenía Python instalado (solo el stub de Microsoft Store). Se instaló **Python 3.12.10** vía `winget install Python.Python.3.12` y luego **uv** vía `pip install --user uv`. Se agregó `C:\Users\Guido\AppData\Roaming\Python\Python312\Scripts` al PATH de usuario para que `uv` quede disponible en terminales nuevas.
- Se creó `pyproject.toml` (build backend `hatchling`, paquete en `src/photosorter`, dependencias `pyside6`, `pillow`, `rawpy`; dev-dependency `pytest`; `pythonpath = ["src"]` para que pytest encuentre el paquete sin instalarlo en modo editable aparte).
- Se corrió `uv sync --dev`: instaló las 14 dependencias sin problemas, incluyendo `rawpy` (no hubo que buscar alternativa al RAW Spike).
- Se implementaron los 9 modelos de dominio del Contract Specification (`Photo`, `PhotoMetadata`, `Classification`, `DestinationPath`, `FileConflict`, `ConflictResolution`, `ProcessingResult`, `ProcessingStatus`, `AppSettings`) como dataclasses inmutables con validación de invariantes en `__post_init__`.
  - **Nota de naming:** el Contract Specification (documento baseline de dominio) define `ProcessingResult` como el resultado de **una fotografía individual** (con `ProcessingStatus`), mientras que el SAD/TDD usan el mismo nombre para el **resumen global** del procesamiento (total, verticales, horizontales, etc.). Se priorizó la definición del Contract Specification por ser el documento más específico y reciente. El modelo de resumen global (agregado) todavía no está formalizado — se define cuando se escriba el "Application Workflow Contract" mencionado en el TDD (§41), probablemente como `ProcessingSummary` para evitar la colisión de nombres.
- Se implementó `OrientationClassifier` (domain/services) cumpliendo CA-01 a CA-04 de Requisitos V1.0: clasifica por `width`/`height`, e intercambia ancho/alto cuando el EXIF Orientation indica una rotación de 90° o 270° (valores 5, 6, 7, 8), para que la clasificación sea por orientación visual y no solo física.
- Se implementó `ImageReader` (Protocol) + `ImageReaderError`, y dos implementaciones en `infrastructure/image/`:
  - `StandardImageReader` (Pillow) para JPG/JPEG/PNG/TIFF/WEBP, leyendo dimensiones, formato y el tag EXIF Orientation (274).
  - `RawImageReader` (rawpy/LibRaw) para NEF/CR2/CR3/ARW/DNG/RAF/ORF/RW2, usando `raw.sizes` para dimensiones y `sizes.flip` (codificación propia de LibRaw, distinta de EXIF) para determinar si hay que intercambiar ancho/alto.
  - `CompositeImageReader`: agrupa una lista de readers y delega en el primero que reconozca la extensión, para que el resto del sistema no necesite saber que existen implementaciones separadas.
- Tests (`tests/unit/`): modelos, `OrientationClassifier` (casos de la tabla de Requisitos + rotaciones EXIF), `StandardImageReader` (generando imágenes reales con Pillow, incluyendo con/sin EXIF orientation), `RawImageReader` (extensiones soportadas; la lectura real se saltea si no hay archivos de muestra) y `CompositeImageReader`. **Resultado: 37 passed, 1 skipped.**
- Se creó `tests/fixtures/raw/` (con README) como lugar para que el usuario deje sus RAWs reales de prueba; el contenido no se versiona (`.gitignore`), solo el README.
- Se creó `.gitignore` (venv, `__pycache__`, cache de pytest, build/dist de PyInstaller, dataset RAW local).
- Se actualizó `README.md` con instrucciones de setup (`uv sync --dev`, `uv run pytest`).
- **Pendiente para la próxima sesión:** Milestone M1 — `DestinationResolver` (Classification + AppSettings → DestinationPath) y `FileOperator`/`CopyFileOperator` (crear carpetas `Verticales/Horizontales/Cuadradas/` y copiar archivos reales), con sus tests de integración.

### 2026-09-05 (continuación 2) — Validación de RawImageReader con archivos reales

El usuario subió dos NEF reales a `tests/fixtures/raw/` (no versionados) y se corrió `test_reads_real_raw_samples` contra ambos:

- `Test_Raw_NEF.NEF`: 6036×4020, `sizes.flip=0` (sin rotación) → `Classification.HORIZONTAL`. Correcto.
- `Test_RAW_NEF_Vertical.NEF`: mismas dimensiones físicas 6036×4020, pero `sizes.flip=5` (rotación 90°/270°, cámara girada al disparar) → orientación mapeada a 6, swap de ancho/alto → `Classification.VERTICAL`. Correcto.

Este segundo archivo valida con datos reales el caso más importante del proyecto (CA-04, Requisitos V1.0 §3.2): la clasificación usa la orientación **visual** final, no las dimensiones físicas crudas del sensor. Antes solo estaba probado con datos EXIF sintéticos; ahora también con un RAW real de Nikon. **Resultado: 4/4 tests de `test_raw_image_reader.py` pasan** (ya no hay skip).

No se modificó código de producción en esta entrada, solo se validó el ya existente. Si en el futuro aparecen RAWs de otras marcas (Canon, Sony, Fuji, Olympus, Panasonic) conviene sumarlos también a `tests/fixtures/raw/` para ampliar la cobertura real del RAW Spike.

### 2026-09-05 (continuación 3) — Milestone M1: organización y copia de archivos

- Se agregaron dos contratos nuevos en `domain/interfaces/`:
  - `DestinationResolver.resolve(photo, classification, settings) -> DestinationPath` (TDD §7.4).
  - `FileOperator.copy(source_path, destination_path, *, overwrite=False) -> None`, junto con `DestinationAlreadyExistsError` (TDD §7.5).
- **Decisión de diseño — dónde vive la regla "no sobrescribir silenciosamente" (D7):** se implementó directamente en `CopyFileOperator`, no se pospuso hasta el `ConflictService` de M2. Si el destino ya existe y no se pide `overwrite=True`, lanza `DestinationAlreadyExistsError` (con `source_path`/`destination_path` para que M2 pueda armar un `FileConflict` a partir de la excepción) en vez de sobrescribir o fallar silenciosamente. Esto es consistente con D7 del TDD, que es una regla no negociable desde V1, no algo que dependa de que exista una UI de conflictos todavía.
- **Decisión de diseño — qué representa `DestinationPath.path`:** los documentos tienen un ejemplo ambiguo (Contract Spec §7.3 muestra solo la carpeta, `Verticales/`, pero TDD §9.5 y §16 muestran la ruta completa con nombre de archivo). Se resolvió a favor de la **ruta completa** (`carpeta_destino / NombreCarpetaClasificación / nombre_archivo_original`), porque es lo que `FileOperator.copy()` necesita directamente y es lo que usa la mayoría de los ejemplos del TDD.
- Se implementó `DefaultDestinationResolver` (`infrastructure/filesystem/`): mapea `Classification` → `Verticales/Horizontales/Cuadradas` mediante un diccionario centralizado (para no dispersar esa nomenclatura por el código, como pide TDD §18) y arma la ruta final conservando el nombre original del archivo (TDD §17, "V1 mantendrá los nombres originales").
- Se implementó `CopyFileOperator` (`infrastructure/filesystem/`) usando `shutil.copy2` (preserva metadata, nunca toca el origen): crea las carpetas de destino si faltan (`mkdir(parents=True, exist_ok=True)`, cumple CA-09) y respeta la regla de no-sobrescritura descrita arriba.
- Tests nuevos:
  - `tests/unit/test_default_destination_resolver.py`: mapeo de las 3 clasificaciones, conservación de nombre de archivo, y el caso documentado de colisión entre subcarpetas con el mismo nombre de archivo (queda igual a propósito; la resolución es responsabilidad de M2).
  - `tests/integration/test_copy_file_operator.py`: copia real a disco, creación de carpetas, CA-09 (no rompe carpeta existente), CA-10/D7 (no sobrescribe por defecto, sí con `overwrite=True`), y que el original nunca se modifica.
  - `tests/integration/test_organize_photos_flow.py`: flujo M1 completo de punta a punta (`Photo → ImageReader → OrientationClassifier → DefaultDestinationResolver → CopyFileOperator`) con JPEGs sintéticos (horizontal y vertical) **y con los dos RAWs reales** de `tests/fixtures/raw/` — el NEF vertical termina copiado en `Organizadas/Verticales/`, con el mismo tamaño de archivo que el original y sin tocarlo.
- Nota: se decidió ubicar los tests de `CopyFileOperator` y del flujo end-to-end en `tests/integration/` (no `tests/unit/`) porque tocan filesystem real, siguiendo la estructura de carpetas de tests ya prevista en el TDD §32 (unit/integration/e2e). Es la primera vez que se usa esa carpeta.
- **Resultado: 54 tests pasan, 0 se saltean.**
- Todavía no existe `SorterService` (el orquestador) ni `FileScanner`: por ahora el "flujo M1" se arma manualmente en el test (`_organize()`), no hay un componente de aplicación que lo haga. Eso se resuelve cuando se implemente la orquestación (más adelante en el roadmap, junto con progreso/cancelación).
- **Pendiente para la próxima sesión:** Milestone M2 — `FileConflict`, `ConflictResolution` (ya existen como modelos de dominio) y un `ConflictService` que capture `DestinationAlreadyExistsError`, arme el `FileConflict` y aplique la `ConflictResolution` (SKIP/OVERWRITE) que decida el usuario.

### 2026-09-05 (continuación 4) — Milestone M2: manejo de conflictos

- **Modelo nuevo (extensión, no está en el Contract Specification baseline):** `ConflictDecision` (`domain/models/conflict_decision.py`) = `ConflictResolution` + `apply_to_remaining: bool`. Se agregó porque `ConflictResolution` por sí sola (SKIP/OVERWRITE) no alcanza para cubrir Requisitos V1.0 §3.1: *"la aplicación deberá permitir al usuario seleccionar una acción y, opcionalmente, aplicar dicha acción a todos los conflictos restantes"*. Queda documentado acá para que quede claro que es una decisión de esta sesión y no algo que viniera ya especificado.
- Se agregó el contrato `ConflictPrompt` (`domain/interfaces/conflict_prompt.py`): `ask(conflict: FileConflict) -> ConflictDecision`. Es lo que la UI (PySide6, M4) va a implementar para mostrarle el conflicto al usuario y devolver su decisión. El dominio no sabe nada de Qt, solo de este contrato.
- Se implementó `ConflictService` (`domain/services/conflict_service.py`): envuelve a `FileOperator` y, cuando salta `DestinationAlreadyExistsError` (la excepción que ya lanzaba `CopyFileOperator` desde M1), arma un `FileConflict`, le pregunta a `ConflictPrompt`, y aplica la `ConflictResolution` resultante. Devuelve siempre un `ProcessingResult` (`COPIED`, `SKIPPED` u `OVERWRITTEN`), nunca deja escapar la excepción de conflicto.
  - Guarda la decisión en memoria (`_remembered_resolution`) cuando `apply_to_remaining=True`, y la reutiliza automáticamente en conflictos siguientes sin volver a preguntar — así se cumple el requisito de "aplicar a los restantes" sin tener que tocar la UI todavía.
  - **Decisión de alcance:** `ConflictService` solo atrapa `DestinationAlreadyExistsError`. Cualquier otro error (lectura corrupta, permisos, disco lleno, etc.) se sigue propagando tal cual — esa política de errores por-archivo (CA-08, TDD §13-14) es responsabilidad del futuro `SorterService` (M3), no de este servicio.
- Tests nuevos:
  - `tests/unit/test_conflict_service.py`: usa un `FakeFileOperator` y un `ScriptedConflictPrompt` (test doubles, sin tocar disco) para probar la lógica pura de `ConflictService` — sin conflicto, SKIP, OVERWRITE, y las dos variantes de "recordar decisión" (SKIP y OVERWRITE) vs. preguntar en cada conflicto si no se pidió aplicar a los restantes.
  - `tests/integration/test_conflict_service_with_real_files.py`: mismo servicio pero con `CopyFileOperator` real sobre `tmp_path`, para confirmar que el wiring funciona con archivos de verdad (SKIP no toca el archivo existente, OVERWRITE sí reemplaza el contenido).
- **Resultado: 62 tests pasan, 0 se saltean.**
- **Pendiente para la próxima sesión:** Milestone M3 — `FileScanner` (recorrido de carpeta, recursivo o no) y `SorterService` (el orquestador que conecta todo: Scanner → Reader → Classifier → Resolver → ConflictService, con progreso, cancelación cooperativa, logging, y la política de "un error individual no detiene el resto" de CA-08).

### 2026-09-05 (continuación 5) — Milestone M3: FileScanner, SorterService y capa Application

- **Se resolvió la ambigüedad de naming que quedó pendiente desde M0** (ver entrada de M0 arriba): se creó `domain/models/processing_summary.py` con `ProcessingSummary` (total, procesados, copiados/omitidos/sobrescritos/fallidos, conteos por clasificación, `cancelled`). Es el modelo "agregado" que el SAD/TDD llamaban `ProcessingResult`; se usó otro nombre para no chocar con el `ProcessingResult` del Contract Specification (que es por-foto). Es una extensión propia, no está en el Contract Specification baseline.
- Se agregó `FileScanner` (`domain/interfaces/file_scanner.py`, + `SourceFolderError`) y su implementación `DefaultFileScanner` (`infrastructure/filesystem/`):
  - Recorre `settings.source_path` con `Path.iterdir()` (no recursivo) o `Path.rglob("*")` (recursivo), filtrando solo archivos (no carpetas).
  - **Decisión de diseño:** en vez de mantener su propia lista de extensiones soportadas, recibe un `ImageReader` por constructor y usa `can_read()` para decidir qué archivos son fotos válidas — así no se duplica la nomenclatura de formatos entre `Scanner` y los `ImageReader` (ya advertido en TDD §18).
  - Valida la carpeta de origen *antes* de escanear (existe, es una carpeta) y lanza `SourceFolderError` si no, siguiendo TDD §13.3 ("errores de configuración, a detectar antes de procesar").
  - Ordena el resultado por path para que el procesamiento sea determinístico.
- Se agregó el contrato `ProgressReporter` (`domain/interfaces/progress_reporter.py`): `on_started`, `on_file_started`, `on_file_completed`, `on_finished`. Se consolidaron los 8 eventos del TDD (§23) en estos 4 callbacks — `PROGRESS_UPDATED` va incluido en los argumentos de `on_file_completed` (processed_count/total_files), y `CONFLICT_DETECTED`/`ERROR_OCCURRED` no necesitan callback propio porque ya se reflejan en el `ProcessingResult` (status `OVERWRITTEN`/`SKIPPED`/`FAILED`) que llega en `on_file_completed`.
- Se creó la capa **`application/`** (primera vez que se usa, hasta ahora todo vivía en `domain/` e `infrastructure/`):
  - `CancellationToken`: wrapper cooperativo sobre `threading.Event` (SAD §20-21) — la UI (M4) lo va a crear, pasarlo a `SorterService.run()` en el worker thread, y llamar `.cancel()` desde el hilo principal.
  - `NullProgressReporter`: implementación vacía de `ProgressReporter`, default cuando no se pasa uno (scripts, tests).
  - `SorterService`: el orquestador. `run(settings, progress_reporter=None, cancellation_token=None) -> ProcessingSummary`. Por cada foto: lee metadata → clasifica → resuelve destino → copia vía `ConflictService`. Usa `logging.getLogger(__name__)` por defecto (inyectable), con mensajes en el formato que pedía TDD §26 (`"Processing started"`, `"DSC_0001.NEF -> VERTICAL (copied)"`, etc.).
  - **Política de errores (CA-08):** `_process_photo()` atrapa `(ImageReaderError, OSError)` por cada foto individualmente y la marca `FAILED` sin frenar el resto del batch. Cualquier otro tipo de excepción (bugs de programación, `ValueError` de un modelo mal construido) se sigue propagando y detiene todo — a propósito, para no ocultar errores reales de la aplicación.
  - No se creó una capa `infrastructure/logging/` separada (estaba prevista en la estructura de carpetas del TDD §32): se decidió usar el módulo `logging` estándar directamente, inyectado por constructor. Se consideró que envolverlo agregaría una abstracción sin beneficio concreto para V1 (TDD §4.4, "no implementar abstracciones sin utilidad").
- Tests nuevos:
  - `tests/unit/test_default_file_scanner.py`: no-recursivo vs. recursivo, ignora archivos no-imagen, orden determinístico, y las dos validaciones de carpeta inválida.
  - `tests/integration/test_sorter_service.py`: `SorterService` armado con todos los componentes reales (menos el `ConflictPrompt`, que es un test double fijo) — carpeta mixta con un archivo corrupto (CA-08, no frena el resto), resolución de conflictos end-to-end, un `ProgressReporter` que graba todos los callbacks, cancelación cooperativa a mitad de proceso, y verificación de logs clave (`caplog`).
- **Resultado: 73 tests pasan, 0 se saltean.**
- Con esto ya está probado, sin UI, el flujo completo que describe el algoritmo conceptual del TDD (§10): carpeta → fotos → clasificación → destino → copia/conflicto → resumen, con progreso, cancelación y logging.
- **Pendiente para la próxima sesión:** Milestone M4 — UI PySide6. Implementar `ConflictPrompt` (diálogo con SKIP/OVERWRITE + checkbox "aplicar a los restantes") y `ProgressReporter` (actualiza barra de progreso y texto de estado) concretos sobre Qt, correr `SorterService.run()` en un `QThread` para no bloquear la ventana, y armar la pantalla única descripta en Requisitos V1.0 §12.

### 2026-09-05 (continuación 6) — Milestone M4: interfaz de escritorio con PySide6

- **Decisión de diseño importante, resuelve otra inconsistencia entre documentos:** Requisitos V1.0 (RF-05 y sección 9) muestra las carpetas `Verticales/Horizontales/Cuadradas` creándose **directamente dentro de la carpeta seleccionada** por el usuario (sin carpeta intermedia), y la pantalla de la sección 12 solo tiene **un** campo de carpeta. En cambio, el Contract Specification (§11.3) y el SAD/TDD ejemplifican `AppSettings` con un `destination_path` distinto al `source_path` (ej. `C:/Fotos/Organizadas`). Como Requisitos V1.0 es el documento de comportamiento de producto (y coincide exactamente con el mockup de UI, que no tiene un segundo campo de "carpeta de destino"), la UI arma `AppSettings(source_path=carpeta, destination_path=carpeta, recursive=...)` — incluir subcarpetas o no es la única opción que ve el usuario. El modelo `AppSettings` sigue soportando `destination_path` distinto de `source_path` (útil a futuro, y ya probado así en los tests de M1-M3), pero la V1 de la UI no expone esa distinción.
- Se creó la capa **`ui/`** (primera vez que se usa):
  - `MainWindow` (`ui/main_window.py`): la única ventana de la V1, siguiendo el mockup de Requisitos V1.0 §12 — campo de carpeta (solo lectura + botón "Examinar..." con `QFileDialog`), checkbox "Incluir subcarpetas", botón que alterna entre "SEPARAR FOTOS" y "Cancelar", label de estado ("Procesando X.NEF"), barra de progreso, contadores (Encontradas/Procesadas/Errores), resumen final y botón "Abrir carpeta de resultados" (`QDesktopServices.openUrl`). Es el único archivo del proyecto que conoce PySide6 a nivel de armado de pantalla; arma los componentes reales (`CompositeImageReader`, `DefaultFileScanner`, `OrientationClassifier`, `DefaultDestinationResolver`, `CopyFileOperator`) y los pasa a `SorterService`.
  - `SorterWorker` (`ui/sorter_worker.py`): subclase de `QThread` que implementa el Protocol `ProgressReporter` (duck typing) emitiendo señales Qt (`started`, `file_started`, `file_completed`, `finished_processing`, `failed`) en vez de tocar widgets directamente — los widgets solo se actualizan en los slots, que Qt entrega en el hilo principal. Los payloads complejos (`Photo`, `ProcessingResult`, `ProcessingSummary`) se declaran como `Signal(object)` en vez del tipo Python concreto (es la forma recomendada en PySide6 para cruzar objetos arbitrarios entre hilos).
  - `QtConflictPrompt` (`ui/qt_conflict_prompt.py`): implementa `ConflictPrompt`. Como `SorterService.run()` corre en el worker thread y `ask()` es una llamada síncrona y bloqueante, pero los diálogos de Qt solo pueden mostrarse desde el hilo principal, `ask()` emite una señal (que Qt entrega en el hilo principal porque el objeto vive ahí) y se bloquea en un `threading.Event` hasta que el hilo principal llama a `provide_decision()` después de cerrar el diálogo. Validado en la práctica (ver más abajo): no hubo deadlocks ni condiciones de carrera.
  - `ConflictDialog` (`ui/conflict_dialog.py`): `QDialog` con origen/destino del conflicto, botones "Omitir"/"Reemplazar" (V1 solo soporta SKIP/OVERWRITE, `RENAME` queda para el futuro) y checkbox "Aplicar esta decisión a los conflictos restantes". Si se cierra sin elegir (ej. con la X), por seguridad se asume SKIP (la opción no destructiva).
  - `src/photosorter/__main__.py`: entry point (`QApplication` + `MainWindow`). Se agregó `[project.scripts] photosorter = "photosorter.__main__:main"` en `pyproject.toml` para poder correr `uv run photosorter` además de `python -m photosorter`.
- **Validación real de la UI** (no son tests de pytest, son scripts de smoke-test corridos manualmente en esta sesión, ver conversación):
  1. Se lanzó la app de verdad y se confirmó visualmente (captura de pantalla) que la ventana coincide con el mockup.
  2. Un script instanció `MainWindow` con una `QApplication` real, seteó la carpeta directamente (sin diálogo nativo), clickeó "SEPARAR FOTOS" de verdad, y dejó correr el `QThread` real con 2 fotos (una ya con conflicto preexistente) — el diálogo de conflicto apareció de verdad y se clickeó "Reemplazar" mediante `QTimer`, confirmando que el cruce de hilos (`QtConflictPrompt`) funciona sin deadlock. Resultado: resumen final `"PROCESAMIENTO COMPLETADO / 2 fotografias analizadas / Verticales: 1 / Horizontales: 1 / Cuadradas: 0 / Errores: 0"`, exactamente el formato de Requisitos V1.0 §15.
  3. Un segundo script probó cancelación real con 301 archivos (300 válidos + 1 corrupto): cancelar a mitad de camino dio `"PROCESO CANCELADO / Procesadas: 21 / 301 / Copiadas: 20 / Errores: 1"`, y los controles de la ventana volvieron correctamente al estado inicial ("SEPARAR FOTOS" habilitado). Confirma cancelación cooperativa real (no solo simulada con test doubles como en M3) y que un archivo corrupto no frena el resto (CA-08) también dentro del hilo real de Qt.
- No se agregaron tests de UI a la suite de pytest (no hay `pytest-qt` instalado); la cobertura de pytest sigue siendo la lógica de dominio/aplicación (73 tests). La UI se considera validada por los smoke-tests manuales de esta sesión, no por tests automatizados repetibles — **queda pendiente evaluar si vale la pena sumar `pytest-qt` más adelante** para tener regresión automática de la UI.
- **Resultado: 73 tests de pytest siguen pasando** (no se tocó dominio/aplicación en esta sesión), más la validación manual de la UI descripta arriba.
- **Pendiente para la próxima sesión:** Milestone M5 — Packaging con PyInstaller: generar el `.exe` (`--onedir`), verificar que `rawpy`/LibRaw se empaquete correctamente (es una dependencia con binarios nativos), y probar la app en un Windows limpio sin Python. Después de eso, la V1 completa del roadmap (TDD §39) estaría cerrada.
