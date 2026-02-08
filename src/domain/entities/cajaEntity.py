from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.enums.contabilidadEnums import CajaEstado


class CajaEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    saldo_inicial: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    estado: CajaEstado = CajaEstado.ABIERTA
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    cierre_caja: Optional[datetime] = None
    saldo_final_efectivo: Optional[Decimal] = None
    diferencia: Optional[Decimal] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @classmethod
    def from_model(cls, obj: Any) -> "CajaEntity":
        return cls.model_validate(obj)
