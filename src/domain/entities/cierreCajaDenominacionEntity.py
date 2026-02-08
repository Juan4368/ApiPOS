from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

DENOMINACIONES_PERMITIDAS = {
    Decimal("2000"),
    Decimal("5000"),
    Decimal("10000"),
    Decimal("20000"),
    Decimal("50000"),
    Decimal("100000"),
}


class CierreCajaDenominacionEntity(BaseModel):
    id: Optional[int] = None
    caja_id: int
    usuario_id: Optional[int] = None
    denominacion: Decimal = Field(..., ge=Decimal("0.00"))
    cantidad: int = Field(..., ge=0)
    subtotal: Decimal = Field(..., ge=Decimal("0.00"))
    fecha_conteo: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("denominacion")
    def _validar_denominacion(cls, value: Decimal) -> Decimal:
        if value not in DENOMINACIONES_PERMITIDAS:
            raise ValueError("Denominacion no permitida")
        return value

    @classmethod
    def from_model(cls, obj: Any) -> "CierreCajaDenominacionEntity":
        return cls.model_validate(obj)
