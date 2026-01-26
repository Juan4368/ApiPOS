from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class VentaDetalleRequest(BaseModel):
    producto_id: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=1)
    precio_unitario: Decimal = Field(..., ge=Decimal("0.00"))
    subtotal: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))


class VentaRequest(BaseModel):
    tipo_pago: Optional[str] = Field(default=None, min_length=1, description="Si es null, se considera credito.")
    es_credito: bool = Field(default=False, description="Se fuerza a true si tipo_pago es null.")
    user_id: Optional[int] = None
    estado: bool = True
    nota_venta: Optional[str] = None
    numero_factura: Optional[str] = Field(None, max_length=50)
    cliente_id: Optional[UUID] = None
    impuesto: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    descuento: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    fecha: Optional[datetime] = None
    detalles: list[VentaDetalleRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def _auto_credito(self) -> "VentaRequest":
        if self.tipo_pago is None:
            self.es_credito = True
        return self


class VentaDetalleResponse(BaseModel):
    venta_detalle_id: int
    venta_id: int
    producto_id: int
    producto_nombre: Optional[str] = None
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
    tipo_pago: Optional[str] = None
    es_credito: bool = False
    estado: bool
    nota_venta: Optional[str]
    numero_factura: Optional[str]
    cliente_id: Optional[UUID]
    user_id: Optional[int]
    detalles: list[VentaDetalleResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class VentaStatusRequest(BaseModel):
    """
    DTO para actualizar el estado de una venta.
    """

    estado: bool


class VentaUpdateRequest(BaseModel):
    """
    DTO para actualizar datos de una venta.
    """

    fecha: Optional[datetime] = None
    impuesto: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    descuento: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    tipo_pago: Optional[str] = Field(default=None, min_length=1, description="Si se envia null, se marca credito.")
    es_credito: Optional[bool] = Field(default=None, description="Se fuerza a true si tipo_pago es null.")
    estado: Optional[bool] = None
    nota_venta: Optional[str] = None
    numero_factura: Optional[str] = Field(default=None, max_length=50)
    cliente_id: Optional[UUID] = None
    user_id: Optional[int] = None
    detalles: Optional[list[VentaDetalleRequest]] = None
