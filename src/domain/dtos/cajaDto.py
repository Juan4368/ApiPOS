from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import CajaEstado


class CajaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    saldo_inicial: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    estado: CajaEstado = CajaEstado.ABIERTA
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None


class CajaResponse(BaseModel):
    id: int
    nombre: str
    saldo_inicial: Decimal
    estado: CajaEstado
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CajaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    saldo_inicial: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    estado: Optional[CajaEstado] = None
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
