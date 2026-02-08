from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class VisitaRequest(BaseModel):
    cliente_id: Optional[UUID] = None
    usuario_id: Optional[int] = None
    fecha: Optional[datetime] = None
    motivo: Optional[str] = Field(default=None, max_length=255)


class VisitaResponse(BaseModel):
    id: int
    cliente_id: Optional[UUID]
    usuario_id: Optional[int]
    fecha: datetime
    motivo: Optional[str]
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class VisitaUpdateRequest(BaseModel):
    cliente_id: Optional[UUID] = None
    usuario_id: Optional[int] = None
    fecha: Optional[datetime] = None
    motivo: Optional[str] = Field(default=None, max_length=255)
