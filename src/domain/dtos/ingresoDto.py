from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import MedioPago


class IngresoRequest(BaseModel):
    fecha: datetime
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    tipo_ingreso: MedioPago
    categoria_contabilidad_id: Optional[int] = None
    notas: Optional[str] = None
    cliente: Optional[str] = Field(default=None, max_length=150)


class IngresoResponse(BaseModel):
    id: int
    fecha: datetime
    monto: Decimal
    tipo_ingreso: MedioPago
    categoria_contabilidad_id: Optional[int] = None
    notas: Optional[str]
    cliente: Optional[str] = None

    model_config = {"from_attributes": True}


class IngresoUpdateRequest(BaseModel):
    fecha: Optional[datetime] = None
    monto: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    tipo_ingreso: Optional[MedioPago] = None
    categoria_contabilidad_id: Optional[int] = None
    notas: Optional[str] = None
    cliente: Optional[str] = Field(default=None, max_length=150)
