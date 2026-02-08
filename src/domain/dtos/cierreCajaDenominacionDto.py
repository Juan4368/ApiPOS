from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

DENOMINACIONES_PERMITIDAS = {
    Decimal("2000"),
    Decimal("5000"),
    Decimal("10000"),
    Decimal("20000"),
    Decimal("50000"),
    Decimal("100000"),
}


class CierreCajaDenominacionRequest(BaseModel):
    caja_id: int
    usuario_id: Optional[int] = None
    denominacion: Decimal = Field(..., ge=Decimal("0.00"))
    cantidad: int = Field(..., ge=0)
    fecha_conteo: Optional[datetime] = None

    @field_validator("denominacion")
    def _validar_denominacion(cls, value: Decimal) -> Decimal:
        if value not in DENOMINACIONES_PERMITIDAS:
            raise ValueError("Denominacion no permitida")
        return value


class CierreCajaDenominacionResponse(BaseModel):
    id: int
    caja_id: int
    usuario_id: Optional[int] = None
    denominacion: Decimal
    cantidad: int
    subtotal: Decimal
    fecha_conteo: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CierreCajaDenominacionUpdateRequest(BaseModel):
    caja_id: Optional[int] = None
    usuario_id: Optional[int] = None
    denominacion: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    cantidad: Optional[int] = Field(default=None, ge=0)
    fecha_conteo: Optional[datetime] = None

    @field_validator("denominacion")
    def _validar_denominacion(cls, value: Optional[Decimal]) -> Optional[Decimal]:
        if value is None:
            return value
        if value not in DENOMINACIONES_PERMITIDAS:
            raise ValueError("Denominacion no permitida")
        return value
