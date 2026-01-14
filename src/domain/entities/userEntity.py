from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `user`.
    """

    user_id: Optional[int] = None
    correo: str = Field(..., min_length=1)
    contrasena_hash: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    activo: bool = True
    creado_at: Optional[datetime] = None
    actualizado_at: Optional[datetime] = None
    nombre_completo: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("correo", "contrasena_hash", "role", mode="before")
    def _strip_required(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("Campo requerido")
        return value

    @field_validator("nombre_completo", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @classmethod
    def from_model(cls, obj: Any) -> "UserEntity":
        return cls.model_validate(obj)
