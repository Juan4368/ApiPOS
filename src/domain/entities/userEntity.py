from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `user`.
    """

    user_id: Optional[int] = None
    username: str = Field(..., min_length=1)
    email: Optional[str] = None
    password_hash: str = Field(..., min_length=1)
    thelefone_number: str = Field(..., min_length=1)
    is_active: bool = True
    is_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("username", "password_hash", "thelefone_number", mode="before")
    def _strip_required(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("Campo requerido")
        return value

    @field_validator("email", mode="before")
    def _strip_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @classmethod
    def from_model(cls, obj: Any) -> "UserEntity":
        return cls.model_validate(obj)
