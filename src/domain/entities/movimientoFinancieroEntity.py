from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from domain.enums.contabilidadEnums import CategoriaTipo


class MovimientoFinancieroEntity(BaseModel):
    id: Optional[int] = None
    fecha: datetime
    tipo: CategoriaTipo
    monto: Decimal = Field(..., gt=Decimal("0.00"))
    concepto: str
    nota: Optional[str] = None
    proveedor_id: Optional[int] = None
    caja_id: int
    usuario_id: Optional[int] = None
    venta_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "MovimientoFinancieroEntity":
        return cls.model_validate(obj)
