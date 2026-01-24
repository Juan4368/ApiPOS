from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.entities.ventaDetalleEntity import VentaDetalleEntity


class VentaEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `venta`.
    """

    venta_id: Optional[int] = None
    fecha: Optional[datetime] = None
    subtotal: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    impuesto: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    descuento: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    tipo_pago: str = Field(..., min_length=1)
    estado: bool = True
    nota_venta: Optional[str] = None
    numero_factura: Optional[str] = None
    cliente_id: Optional[UUID] = None
    user_id: Optional[int] = None
    detalles: Optional[list[VentaDetalleEntity]] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )

    @classmethod
    def from_model(cls, obj: Any) -> "VentaEntity":
        return cls.model_validate(obj)
