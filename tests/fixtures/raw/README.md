# Dataset RAW de prueba

Esta carpeta esta pensada para el **RAW Spike** (ver `Docs/Technical Design Document (TDD).md`, seccion 28-29).

Poné acá tus archivos RAW reales de distintas marcas (NEF, CR2, CR3, ARW, DNG, RAF, ORF, RW2) para validar `RawImageReader`. El contenido de esta carpeta **no se sube al repositorio** (ver `.gitignore`); solo queda este README como referencia.

`tests/unit/test_raw_image_reader.py` recorre automáticamente los archivos que encuentre acá. Si la carpeta está vacía, esos tests se saltean (skip) en vez de fallar.
