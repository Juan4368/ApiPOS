from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StockRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con stock (crear/actualizar).
    """

    producto_id: int = Field(..., ge=1)
    cantidad_actual: int = Field(..., ge=0)
    cantidad_minima: int = Field(..., ge=0)
    ultima_actualizacion: Optional[datetime] = None
    actualizado_por_id: Optional[int] = None
    creado_por_id: Optional[int] = None


class StockResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con stock.
    """

    stock_id: int
    producto_id: int
    cantidad_actual: int
    cantidad_minima: int
    ultima_actualizacion: Optional[datetime]
    actualizado_por_id: Optional[int]
    creado_por_id: Optional[int]

    model_config = {"from_attributes": True}
