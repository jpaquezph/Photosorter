from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProgressEstimate:
    """Estimacion de tiempo restante para terminar de procesar una carpeta.

    Se recalcula en SorterService despues de cada archivo procesado, a
    partir del tiempo promedio observado hasta el momento
    (average_seconds_per_file = elapsed_seconds / processed_files). En
    cargas grandes es la unica forma de que el usuario sepa cuanto falta,
    ya que el tamano y formato de cada foto hace variar mucho el tiempo
    por archivo.
    """

    elapsed_seconds: float
    average_seconds_per_file: float
    remaining_seconds: float

    def __post_init__(self) -> None:
        if self.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds no puede ser negativo")
        if self.average_seconds_per_file < 0:
            raise ValueError("average_seconds_per_file no puede ser negativo")
        if self.remaining_seconds < 0:
            raise ValueError("remaining_seconds no puede ser negativo")
