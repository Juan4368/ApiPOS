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
    numero_contacto: Optional[str] = Field(None, max_length=50)
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
    numero_contacto: Optional[str]
    creado_at: Optional[datetime]
    actualizado_at: Optional[datetime]

    model_config = {"from_attributes": True}


class UserStatusRequest(BaseModel):
    """
    DTO para actualizar el estado del usuario.
    """

    activo: bool
    actualizado_at: Optional[datetime] = None


class UserUpdateRequest(BaseModel):
    """
    DTO para actualizar datos del usuario.
    """

    correo: Optional[str] = Field(None, min_length=1, max_length=255)
    contrasena_hash: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[str] = Field(None, min_length=1)
    activo: Optional[bool] = None
    nombre_completo: Optional[str] = Field(None, max_length=150)
    numero_contacto: Optional[str] = Field(None, max_length=50)
    actualizado_at: Optional[datetime] = None
