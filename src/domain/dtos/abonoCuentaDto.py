from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class AbonoCuentaRequest(BaseModel):
    fecha: datetime
    monto: Decimal = Field(..., gt=Decimal("0.00"))
    concepto: str
    caja_id: int
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None


class AbonoCuentaResponse(BaseModel):
    id: int
    cuenta_id: int
    movimiento_id: int
    monto: Decimal
    fecha: datetime
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
