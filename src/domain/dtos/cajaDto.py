from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CajaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    saldo_inicial: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))


class CajaResponse(BaseModel):
    id: int
    nombre: str
    saldo_inicial: Decimal
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CajaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    saldo_inicial: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
