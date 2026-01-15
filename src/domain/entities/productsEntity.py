from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `product`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """

    producto_id: Optional[int] = None
    codigo_barras: Optional[str] = Field(default=None)
    nombre: str = Field(..., min_length=1)
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    precio_venta: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    costo: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    margen: Optional[Decimal] = None
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado: bool = True
    categoria_nombre: Optional[str] = None
    creado_por_nombre: Optional[str] = None
    actualizado_por_nombre: Optional[str] = None

    # Configuracion para Pydantic v2
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: lambda v: str(v)},
    )
    _max_price: ClassVar[Decimal] = Decimal("99999999.99")

    # Validadores
    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("codigo_barras", mode="before")
    def _ensure_codigo_barras(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @field_validator("precio_venta", "costo", mode="before")
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            val = v
        else:
            try:
                val = Decimal(str(v or "0"))
            except (InvalidOperation, ValueError):
                raise ValueError("El precio debe ser un numero valido") from None
        if val.is_nan() or val.is_infinite():
            raise ValueError("El precio debe ser un numero valido")
        try:
            val = val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise ValueError("El precio debe tener un formato valido") from None
        if val < 0:
            raise ValueError("El precio no puede ser negativo")
        if val > cls._max_price:
            raise ValueError("El precio excede el maximo permitido")
        return val

    @field_validator("margen", mode="before")
    def _ensure_decimal_margen(cls, v) -> Optional[Decimal]:
        if v is None:
            return None
        if isinstance(v, Decimal):
            val = v
        else:
            try:
                val = Decimal(str(v))
            except (InvalidOperation, ValueError):
                raise ValueError("El margen debe ser un numero valido") from None
        if val.is_nan() or val.is_infinite():
            raise ValueError("El margen debe ser un numero valido")
        try:
            val = val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise ValueError("El margen debe tener un formato valido") from None
        if val < 0:
            raise ValueError("El margen no puede ser negativo")
        if val > cls._max_price:
            raise ValueError("El margen excede el maximo permitido")
        return val

    @field_validator("categoria_id", mode="before")
    def _ensure_int_categoria(cls, v) -> Optional[int]:
        if v is None:
            return None
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            value = v.strip()
            if value == "":
                return None
            if value.isdigit():
                return int(value)
            return None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    def is_active(self) -> bool:
        return bool(self.estado)

    # Interoperabilidad
    @classmethod
    def from_model(cls, obj: Any) -> "ProductEntity":
        """
        Construye la entidad desde un objeto con atributos (por ejemplo, una instancia de SQLAlchemy).
        """
        return cls.model_validate(obj)
