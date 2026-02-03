from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CajaSesionRequest(BaseModel):
    caja_id: int
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None


class CajaSesionResponse(BaseModel):
    id: int
    caja_id: int
    usuario_id: Optional[int] = None
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CajaSesionUpdateRequest(BaseModel):
    caja_id: Optional[int] = None
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
