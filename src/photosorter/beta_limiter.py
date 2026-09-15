"""Limite de uso para la fase beta publica (TEMPORAL).

Bloquea la seleccion de carpeta y el inicio del procesamiento una vez que,
en total y entre corridas (no se resetea al reiniciar la app), se
procesaron MAX_PHOTOS fotografias en esta instalacion; y recorta cualquier
corrida al cupo restante para que nunca se pase de MAX_PHOTOS en total.

Para sacarlo en la proxima fase:
1. Borrar este archivo.
2. En ui/main_window.py, borrar el import y todos los bloques marcados con
   el comentario "BETA:" (el chequeo en _choose_folder, el metodo
   _show_beta_limit_dialog, el chequeo y el argumento max_photos en
   _start_processing, y el registro + aviso en _on_finished).

SorterService.run() y SorterWorker quedan con un parametro generico
`max_photos` (no menciona "beta"): no hace falta tocarlos, simplemente
dejar de pasarle un valor (o pasar None) al no wirearlo mas desde aca.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

MAX_PHOTOS = 10

LIMIT_MESSAGE = (
    "Se llego al limite de la fase beta.\n\n"
    "Por favor dejanos un comentario para avanzar con el desarrollo."
)


def _usage_file() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    directory = Path(base) / "PhotoSorter"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "beta_usage.json"


def get_processed_count() -> int:
    try:
        data = json.loads(_usage_file().read_text(encoding="utf-8"))
        return int(data.get("processed_photos", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def register_processed(count: int) -> None:
    if count <= 0:
        return
    total = get_processed_count() + count
    _usage_file().write_text(json.dumps({"processed_photos": total}), encoding="utf-8")


def has_reached_limit() -> bool:
    return get_processed_count() >= MAX_PHOTOS


def remaining_allowance() -> int:
    return max(MAX_PHOTOS - get_processed_count(), 0)
