from __future__ import annotations

import threading


class CancellationToken:
    """Token cooperativo para cancelar un SorterService.run() en curso.

    Ver Docs/System Architecture Document - SAD.md, seccion 20-21: la UI
    corre SorterService en un worker separado del hilo principal, y pide
    la cancelacion llamando a cancel() desde el hilo de UI. El worker
    chequea is_cancelled entre archivo y archivo; no se interrumpe una
    copia en curso a la fuerza.
    """

    def __init__(self) -> None:
        self._event = threading.Event()

    def cancel(self) -> None:
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()
