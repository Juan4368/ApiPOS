from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class StockEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `stock`.
    """

    stock_id: Optional[int] = None
    producto_id: int = Field(..., ge=1)
    cantidad_actual: int = Field(..., ge=0)
    cantidad_minima: int = Field(..., ge=0)
    ultima_actualizacion: Optional[datetime] = None
    actualizado_por_id: Optional[int] = None
    creado_por_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "StockEntity":
        return cls.model_validate(obj)
