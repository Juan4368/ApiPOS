from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CajaEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    saldo_inicial: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @classmethod
    def from_model(cls, obj: Any) -> "CajaEntity":
        return cls.model_validate(obj)
