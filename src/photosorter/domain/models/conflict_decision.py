from __future__ import annotations

from dataclasses import dataclass

from photosorter.domain.models.conflict_resolution import ConflictResolution


@dataclass(frozen=True)
class ConflictDecision:
    """Decision del usuario frente a un FileConflict, mas el alcance que pidio.

    Extiende ConflictResolution (Contract Specification, seccion 9) para
    cubrir el requisito de Requisitos V1.0, seccion 3.1:

    "la aplicacion debera permitir al usuario seleccionar una accion y,
    opcionalmente, aplicar dicha accion a todos los conflictos restantes
    del procesamiento."

    No forma parte del Contract Specification baseline; se agrega en M2
    porque ConflictResolution por si sola no alcanza para representar
    "aplicar a los restantes" (ver Docs/CONTEXTO.md).
    """

    resolution: ConflictResolution
    apply_to_remaining: bool = False
