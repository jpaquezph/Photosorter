# Photosorter
App de fotografia

Aplicacion de escritorio para Windows que organiza fotografias en carpetas segun su orientacion (Verticales/Horizontales/Cuadradas), sin modificar los archivos originales.

Documentacion completa en `Docs/` (objetivo, requisitos, arquitectura, diseno tecnico y contratos de dominio) y el registro de avance sesion a sesion en `Docs/CONTEXTO.md`.

## Desarrollo

Requiere Python 3.11+ y [uv](https://docs.astral.sh/uv/).

```
uv sync --dev
uv run pytest
```

Para validar `RawImageReader` con archivos RAW reales (NEF, CR2, CR3, ARW, DNG, RAF, ORF, RW2), copialos a `tests/fixtures/raw/` (no se versionan, ver README ahi).
