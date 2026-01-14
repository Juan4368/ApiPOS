from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `product`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """

    producto_id: Optional[int] = None
    codigo_barras: str = Field(..., min_length=1)
    nombre: str = Field(..., min_length=1)
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    precio_venta: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    costo: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado: bool = True

    # Configuracion para Pydantic v2
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )

    # Validadores
    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("precio_venta", "costo", mode="before")
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            val = v
        else:
            val = Decimal(str(v or "0"))
        if val < 0:
            raise ValueError("El precio no puede ser negativo")
        return val

    @field_validator("categoria_id", mode="before")
    def _ensure_int_categoria(cls, v) -> Optional[int]:
        if v is None:
            return None
        return int(v)

    def is_active(self) -> bool:
        return bool(self.estado)

    # Interoperabilidad
    @classmethod
    def from_model(cls, obj: Any) -> "ProductEntity":
        """
        Construye la entidad desde un objeto con atributos (por ejemplo, una instancia de SQLAlchemy).
        """
        return cls.model_validate(obj)
