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

Fase: **Milestone M1 completo** (dominio + lectura de imágenes + organización/copia de archivos, sin UI todavía).

Documentación existente en `Docs/`:
- Objetivo, principios y requerimientos
- Requisitos V1.0
- System Architecture Document (SAD)
- Technical Design Document (TDD)
- Contract Specification — Domain Models

Estructura de código (`src/photosorter/`):
- `domain/models/`: `Photo`, `PhotoMetadata`, `Classification`, `DestinationPath`, `FileConflict`, `ConflictResolution`, `ProcessingResult` + `ProcessingStatus`, `AppSettings` (dataclasses `frozen=True` con validación en `__post_init__`, según Contract Specification).
- `domain/interfaces/`: `ImageReader` (+ `ImageReaderError`), `Classifier`, `DestinationResolver`, `FileOperator` (+ `DestinationAlreadyExistsError`) — todos `Protocol`.
- `domain/services/`: `OrientationClassifier` (única fuente de verdad para la regla de orientación visual, incluyendo EXIF).
- `infrastructure/image/`: `StandardImageReader` (Pillow: JPG/JPEG/PNG/TIFF/WEBP), `RawImageReader` (rawpy: NEF/CR2/CR3/ARW/DNG/RAF/ORF/RW2), `CompositeImageReader` (delega en el primero que sepa leer el archivo).
- `infrastructure/filesystem/`: `DefaultDestinationResolver` (mapea Classification → Verticales/Horizontales/Cuadradas), `CopyFileOperator` (copia sin sobrescribir por defecto, crea carpetas destino si faltan).

Pendiente de implementar (todavía no existe en el código): `FileScanner` (buscar archivos en una carpeta, con/sin recursividad), `ConflictService`/`FileConflict`/`ConflictResolution` wireados a una decisión de usuario, `SorterService` (orquestador), progreso/cancelación/logging, y toda la UI (PySide6).

Tests: 54 pasan, 0 se saltean (ya hay 2 RAWs reales de muestra en `tests/fixtures/raw/`, no versionados — uno horizontal sin rotación y uno vertical con rotación de cámara).

Próximo paso técnico definido: **Milestone M2** — `FileConflict` + `ConflictResolution` + `ConflictService`, para decidir qué hacer cuando el destino ya existe (hoy `CopyFileOperator` ya lo detecta y lanza `DestinationAlreadyExistsError`, pero todavía no hay quién capture ese error y le pregunte al usuario).

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
