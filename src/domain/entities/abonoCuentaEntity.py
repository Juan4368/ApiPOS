from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class AbonoCuentaEntity(BaseModel):
    id: Optional[int] = None
    cuenta_id: int
    movimiento_id: int
    monto: Decimal = Field(..., gt=Decimal("0.00"))
    fecha: datetime
    created_at: Optional[datetime] = None
    concepto: Optional[str] = None
    caja_id: Optional[int] = None
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )

    @classmethod
    def from_model(cls, obj: Any) -> "AbonoCuentaEntity":
        return cls.model_validate(obj)
