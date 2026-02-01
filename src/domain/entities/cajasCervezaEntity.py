from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CajasCervezaEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    cantidad_cajas: int = Field(..., ge=0)
    entregado: bool = False
    fecha: Optional[datetime] = None
    cajero: Optional[str] = None
    actualizado_por: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("cajero", mode="before")
    def _strip_cajero(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @field_validator("actualizado_por", mode="before")
    def _strip_actualizado_por(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @classmethod
    def from_model(cls, obj: Any) -> "CajasCervezaEntity":
        return cls.model_validate(obj)
