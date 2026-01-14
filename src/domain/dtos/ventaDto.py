from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class VentaDetalleRequest(BaseModel):
    producto_id: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=1)
    precio_unitario: Decimal = Field(..., ge=Decimal("0.00"))
    subtotal: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))


class VentaRequest(BaseModel):
    tipo_pago: str = Field(..., min_length=1)
    user_id: Optional[int] = None
    estado: bool = True
    impuesto: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    descuento: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    fecha: Optional[datetime] = None
    detalles: list[VentaDetalleRequest] = Field(default_factory=list)


class VentaDetalleResponse(BaseModel):
    venta_detalle_id: int
    venta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = {"from_attributes": True}


class VentaResponse(BaseModel):
    venta_id: int
    fecha: datetime
    subtotal: Decimal
    impuesto: Decimal
    descuento: Decimal
    total: Decimal
    tipo_pago: str
    estado: bool
    user_id: Optional[int]
    detalles: list[VentaDetalleResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}
