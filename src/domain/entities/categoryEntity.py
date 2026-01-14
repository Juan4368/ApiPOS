from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `categoria`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """

    categoria_id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    estado: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    descripcion: Optional[str] = None
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @classmethod
    def from_model(cls, obj: Any) -> "CategoryEntity":
        return cls.model_validate(obj)
