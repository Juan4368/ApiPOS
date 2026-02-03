from __future__ import annotations

from enum import Enum


class CategoriaTipo(str, Enum):
    INGRESO = "INGRESO"
    EGRESO = "EGRESO"


class MedioPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA = "TRANSFERENCIA"


class CreditoEstado(str, Enum):
    PENDIENTE = "PENDIENTE"
    PARCIAL = "PARCIAL"
    PAGADO = "PAGADO"
    ANULADO = "ANULADO"


class CajaEstado(str, Enum):
    ABIERTA = "ABIERTA"
    CERRADA = "CERRADA"

