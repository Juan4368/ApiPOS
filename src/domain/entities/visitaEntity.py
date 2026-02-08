from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VisitaEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla visitas.
    Configurada con from_attributes=True para aceptar objetos ORM o con atributos.
    """

    id: Optional[int] = None
    cliente_id: Optional[UUID] = None
    usuario_id: Optional[int] = None
    fecha: Optional[datetime] = None
    motivo: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("motivo", mode="before")
    def _strip_motivo(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @classmethod
    def from_model(cls, obj: Any) -> "VisitaEntity":
        return cls.model_validate(obj)
