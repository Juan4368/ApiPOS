from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClienteEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `clientes`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """

    id: Optional[UUID] = None
    nombre: str = Field(..., min_length=1)
    nombre_normalizado: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    descuento_pesos: Optional[float] = None
    descuento_porcentaje: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("telefono", "email", mode="before")
    def _strip_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @classmethod
    def from_model(cls, obj: Any) -> "ClienteEntity":
        return cls.model_validate(obj)
