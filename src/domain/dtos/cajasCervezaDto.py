from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CajasCervezaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    cantidad_cajas: int = Field(..., ge=0)
    entregado: bool = False
    fecha: Optional[datetime] = None
    cajero: Optional[str] = Field(default=None, max_length=150)
    actualizado_por: Optional[str] = Field(default=None, max_length=150)


class CajasCervezaResponse(BaseModel):
    id: int
    nombre: str
    cantidad_cajas: int
    entregado: bool
    fecha: datetime
    cajero: Optional[str] = None
    actualizado_por: Optional[str] = None

    model_config = {"from_attributes": True}


class CajasCervezaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    cantidad_cajas: Optional[int] = Field(default=None, ge=0)
    entregado: Optional[bool] = None
    fecha: Optional[datetime] = None
    cajero: Optional[str] = Field(default=None, max_length=150)
    actualizado_por: Optional[str] = Field(default=None, max_length=150)
