from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ClienteRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    nombre_normalizado: Optional[str] = Field(default=None, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)
    descuento_pesos: Optional[float] = None
    descuento_porcentaje: Optional[float] = None


class ClienteResponse(BaseModel):
    id: UUID
    nombre: str
    nombre_normalizado: str
    telefono: Optional[str]
    email: Optional[str]
    created_at: Optional[datetime] = None
    descuento_pesos: Optional[float] = None
    descuento_porcentaje: Optional[float] = None

    model_config = {"from_attributes": True}


class ClienteUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=255)
    nombre_normalizado: Optional[str] = Field(default=None, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)
    descuento_pesos: Optional[float] = None
    descuento_porcentaje: Optional[float] = None
