from __future__ import annotations

import threading

from PySide6.QtCore import QObject, Signal

from photosorter.domain.models.conflict_decision import ConflictDecision
from photosorter.domain.models.file_conflict import FileConflict


class QtConflictPrompt(QObject):
    """ConflictPrompt (ver domain/interfaces/conflict_prompt.py) para PySide6.

    SorterService.run() se ejecuta en un worker thread (ver
    ui/sorter_worker.py) y llama a ask() de forma sincronica, bloqueante.
    Como los dialogos de Qt solo pueden mostrarse desde el hilo principal,
    ask() emite una senal (que Qt entrega en el hilo principal, porque este
    objeto vive ahi) y se bloquea en un threading.Event hasta que el hilo
    principal muestre el dialogo y llame a provide_decision().
    """

    decision_requested = Signal(object)  # FileConflict

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._event = threading.Event()
        self._decision: ConflictDecision | None = None

    def ask(self, conflict: FileConflict) -> ConflictDecision:
        self._event.clear()
        self._decision = None
        self.decision_requested.emit(conflict)
        self._event.wait()
        assert self._decision is not None
        return self._decision

    def provide_decision(self, decision: ConflictDecision) -> None:
        """Llamado desde el hilo principal, con la respuesta del usuario."""
        self._decision = decision
        self._event.set()
