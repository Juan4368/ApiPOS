from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class CarteraEntity(BaseModel):
    cartera_id: Optional[int] = None
    fecha: datetime
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = None
    notas: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "CarteraEntity":
        return cls.model_validate(obj)
