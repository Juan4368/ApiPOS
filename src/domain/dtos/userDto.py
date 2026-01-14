from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con usuarios (crear/actualizar).
    """

    correo: str = Field(..., min_length=1, max_length=255)
    contrasena_hash: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1)
    activo: bool = True
    nombre_completo: Optional[str] = Field(None, max_length=150)
    creado_at: Optional[datetime] = None
    actualizado_at: Optional[datetime] = None


class UserResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con usuarios.
    """

    user_id: int
    correo: str
    role: str
    activo: bool
    nombre_completo: Optional[str]
    creado_at: Optional[datetime]
    actualizado_at: Optional[datetime]

    model_config = {"from_attributes": True}
