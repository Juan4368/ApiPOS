from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con usuarios (crear/actualizar).
    """

    username: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=254)
    password_hash: str = Field(..., min_length=1, max_length=255)
    telephone_number: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: bool = True
    is_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con usuarios.
    """

    user_id: int
    username: str
    email: Optional[str]
    telephone_number: Optional[str]
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class UserStatusRequest(BaseModel):
    """
    DTO para actualizar el estado del usuario.
    """

    is_active: bool
    updated_at: Optional[datetime] = None


class UserUpdateRequest(BaseModel):
    """
    DTO para actualizar datos del usuario.
    """

    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=254)
    password_hash: Optional[str] = Field(None, min_length=1, max_length=255)
    telephone_number: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    last_login_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
