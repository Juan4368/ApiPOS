from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import CreditoEstado
from domain.dtos.abonoCuentaDto import AbonoCuentaResponse
from domain.dtos.ventaDto import VentaDetalleResponse


class CuentaCobrarRequest(BaseModel):
    venta_id: Optional[int] = None
    cliente_id: Optional[UUID] = None
    total: Decimal = Field(..., ge=Decimal("0.00"))
    saldo_inicial: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    estado: Optional[CreditoEstado] = None


class CuentaCobrarResponse(BaseModel):
    id: int
    venta_id: Optional[int] = None
    cliente_id: Optional[UUID] = None
    total: Decimal
    saldo: Decimal
    estado: CreditoEstado
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cliente_nombre: Optional[str] = None
    numero_factura: Optional[str] = None
    venta_detalles: Optional[list[VentaDetalleResponse]] = None

    model_config = {"from_attributes": True}


class CuentaCobrarUpdateRequest(BaseModel):
    venta_id: Optional[int] = None
    cliente_id: Optional[UUID] = None
    total: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    saldo: Optional[Decimal] = Field(default=None, ge=Decimal("0.00"))
    estado: Optional[CreditoEstado] = None


class AbonoCuentaResultResponse(BaseModel):
    abono: AbonoCuentaResponse
    cuenta: CuentaCobrarResponse
