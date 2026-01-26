from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProveedorEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    telefono: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None

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
    def from_model(cls, obj: Any) -> "ProveedorEntity":
        return cls.model_validate(obj)
