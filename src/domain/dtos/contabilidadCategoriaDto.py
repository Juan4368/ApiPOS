from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import CategoriaTipo


class ContabilidadCategoriaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    tipo_categoria: CategoriaTipo


class ContabilidadCategoriaResponse(BaseModel):
    id: int
    nombre: str
    tipo_categoria: CategoriaTipo

    model_config = {"from_attributes": True}


class ContabilidadCategoriaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    tipo_categoria: Optional[CategoriaTipo] = None

