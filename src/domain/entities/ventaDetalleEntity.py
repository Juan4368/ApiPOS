from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VentaDetalleEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `venta_detalle`.
    """

    venta_detalle_id: Optional[int] = None
    venta_id: Optional[int] = None
    producto_id: int = Field(..., ge=1)
    producto_nombre: Optional[str] = None
    cantidad: int = Field(..., ge=1)
    precio_unitario: Decimal = Field(..., ge=Decimal("0.00"))
    descuento: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    subtotal: Decimal = Field(..., ge=Decimal("0.00"))

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )

    @field_validator("descuento", mode="before")
    @classmethod
    def _coerce_descuento_none(cls, value: Any) -> Decimal:
        if value is None:
            return Decimal("0.00")
        return value

    @classmethod
    def from_model(cls, obj: Any) -> "VentaDetalleEntity":
        return cls.model_validate(obj)
