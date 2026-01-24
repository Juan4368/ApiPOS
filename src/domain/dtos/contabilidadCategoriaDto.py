from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ContabilidadCategoriaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    codigo: str = Field(..., min_length=1, max_length=50)


class ContabilidadCategoriaResponse(BaseModel):
    id: int
    nombre: str
    codigo: str

    model_config = {"from_attributes": True}


class ContabilidadCategoriaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    codigo: Optional[str] = Field(default=None, min_length=1, max_length=50)

