from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from domain.enums.contabilidadEnums import MedioPago


class IngresoEntity(BaseModel):
    id: Optional[int] = None
    fecha: datetime
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    tipo_ingreso: MedioPago
    categoria_contabilidad_id: Optional[int] = None
    notas: Optional[str] = None
    cliente: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "IngresoEntity":
        return cls.model_validate(obj)
