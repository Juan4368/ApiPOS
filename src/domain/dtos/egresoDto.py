from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import MedioPago


class EgresoRequest(BaseModel):
    fecha: date
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    tipo_egreso: MedioPago
    notas: Optional[str] = None
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = Field(default=None, max_length=255)


class EgresoResponse(BaseModel):
    id: int
    fecha: date
    monto: Decimal
    tipo_egreso: MedioPago
    notas: Optional[str]
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = None

    model_config = {"from_attributes": True}


class EgresoUpdateRequest(BaseModel):
    fecha: Optional[date] = None
    monto: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    tipo_egreso: Optional[MedioPago] = None
    notas: Optional[str] = None
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = Field(default=None, max_length=255)
