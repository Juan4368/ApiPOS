from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CarteraRequest(BaseModel):
    fecha: datetime
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = Field(default=None, max_length=150)
    notas: Optional[str] = Field(default=None, max_length=255)


class CarteraResponse(BaseModel):
    cartera_id: int
    fecha: datetime
    monto: Decimal
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = None
    notas: Optional[str] = None

    model_config = {"from_attributes": True}


class CarteraUpdateRequest(BaseModel):
    fecha: Optional[datetime] = None
    monto: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    categoria_contabilidad_id: Optional[int] = None
    cliente: Optional[str] = Field(default=None, max_length=150)
    notas: Optional[str] = Field(default=None, max_length=255)
