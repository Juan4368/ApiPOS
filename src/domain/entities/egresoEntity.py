from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from domain.enums.contabilidadEnums import MedioPago


class EgresoEntity(BaseModel):
    id: Optional[int] = None
    fecha: date
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    tipo_egreso: MedioPago
    notas: Optional[str] = None
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "EgresoEntity":
        return cls.model_validate(obj)
