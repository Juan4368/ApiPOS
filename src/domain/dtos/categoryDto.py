from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con categorias (crear/actualizar).
    """

    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    estado: bool = True
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None


class CategoryResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con categorias.
    """

    categoria_id: int
    nombre: str
    descripcion: Optional[str]
    estado: bool
    fecha_creacion: Optional[datetime]
    fecha_actualizacion: Optional[datetime]
    creado_por_id: Optional[int]
    actualizado_por_id: Optional[int]
    creado_por_nombre: Optional[str] = None
    actualizado_por_nombre: Optional[str] = None

    model_config = {"from_attributes": True}


class CategoryStatusRequest(BaseModel):
    """
    DTO para actualizar el estado de una categoria.
    """

    estado: bool
    actualizado_por_id: Optional[int] = None
    fecha_actualizacion: Optional[datetime] = None
