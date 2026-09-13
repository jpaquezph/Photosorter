from __future__ import annotations

import threading


class CancellationToken:
    """Token cooperativo para cancelar o pausar un SorterService.run() en curso.

    Ver Docs/System Architecture Document - SAD.md, seccion 20-21: la UI
    corre SorterService en un worker separado del hilo principal, y pide
    la cancelacion llamando a cancel() desde el hilo de UI. El worker
    chequea is_cancelled entre archivo y archivo; no se interrumpe una
    copia en curso a la fuerza.

    La pausa (pause()/resume()) sigue la misma logica cooperativa: el
    worker se detiene en wait_if_paused(), entre archivo y archivo, y
    sigue esperando ahi hasta que alguien llame resume() o cancel() (por
    ejemplo, mientras la UI muestra un dialogo de confirmacion al cerrar
    la ventana; ver MainWindow.closeEvent).
    """

    def __init__(self) -> None:
        self._cancelled = threading.Event()
        self._not_paused = threading.Event()
        self._not_paused.set()

    def cancel(self) -> None:
        self._cancelled.set()
        # Si estaba pausado, cancel() debe poder notarse: no tiene sentido
        # dejar el worker bloqueado esperando un resume() que no llegara.
        self._not_paused.set()

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled.is_set()

    def pause(self) -> None:
        self._not_paused.clear()

    def resume(self) -> None:
        self._not_paused.set()

    @property
    def is_paused(self) -> bool:
        return not self._not_paused.is_set()

    def wait_if_paused(self) -> None:
        self._not_paused.wait()
