from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProveedorRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)


class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str]
    email: Optional[str]
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProveedorUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)
