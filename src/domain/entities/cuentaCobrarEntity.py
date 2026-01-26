from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.enums.contabilidadEnums import CreditoEstado
from domain.entities.ventaDetalleEntity import VentaDetalleEntity


class CuentaCobrarEntity(BaseModel):
    id: Optional[int] = None
    venta_id: Optional[int] = None
    cliente_id: Optional[UUID] = None
    total: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    saldo: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    estado: CreditoEstado = CreditoEstado.PENDIENTE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cliente_nombre: Optional[str] = None
    numero_factura: Optional[str] = None
    venta_detalles: Optional[list[VentaDetalleEntity]] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )

    @classmethod
    def from_model(cls, obj: Any) -> "CuentaCobrarEntity":
        return cls.model_validate(obj)
