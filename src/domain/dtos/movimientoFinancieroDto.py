from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import CategoriaTipo


class MovimientoFinancieroRequest(BaseModel):
    fecha: datetime
    tipo: CategoriaTipo
    monto: Decimal = Field(..., gt=Decimal("0.00"))
    concepto: str
    proveedor_id: Optional[int] = None
    caja_id: int
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None


class MovimientoFinancieroResponse(BaseModel):
    id: int
    fecha: datetime
    tipo: CategoriaTipo
    monto: Decimal
    concepto: str
    proveedor_id: Optional[int] = None
    caja_id: int
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MovimientoFinancieroUpdateRequest(BaseModel):
    fecha: Optional[datetime] = None
    tipo: Optional[CategoriaTipo] = None
    monto: Optional[Decimal] = Field(default=None, gt=Decimal("0.00"))
    concepto: Optional[str] = None
    proveedor_id: Optional[int] = None
    caja_id: Optional[int] = None
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None
