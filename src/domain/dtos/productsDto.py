from __future__ import annotations
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field, field_validator


class ProductRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con productos (crear/actualizar).
    """
    nombre: str = Field(..., min_length=1, max_length=200)
    codigo_barras: Optional[str] = Field(...)
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    precio_venta: Decimal = Field(..., ge=Decimal("0.00"))
    costo: Decimal = Field(..., ge=Decimal("0.00"))
    margen: Optional[Decimal] = Field(None, ge=Decimal("0.00"))
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado: bool = True
    _max_price: ClassVar[Decimal] = Decimal("99999999.99")

    @field_validator("codigo_barras", mode="before")
    def _ensure_codigo_barras(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @field_validator("nombre", mode="before")
    def _ensure_nombre(cls, v: Any) -> str:
        if v is None:
            return v
        return str(v).strip()

    @field_validator("categoria_id", mode="before")
    def _ensure_int_categoria(cls, v: Any) -> Optional[int]:
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

    @field_validator("precio_venta", "costo", mode="before")
    def _ensure_decimal_price(cls, v: Any) -> Decimal:
        if isinstance(v, Decimal):
            value = v
        else:
            try:
                value = Decimal(str(v or "0"))
            except (InvalidOperation, ValueError):
                raise ValueError("El precio debe ser un numero valido") from None
        if value.is_nan() or value.is_infinite():
            raise ValueError("El precio debe ser un numero valido")
        try:
            value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise ValueError("El precio debe tener un formato valido") from None
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        if value > cls._max_price:
            raise ValueError("El precio excede el maximo permitido")
        return value

    @field_validator("margen", mode="before")
    def _ensure_decimal_margin(cls, v: Any) -> Optional[Decimal]:
        if v is None:
            return None
        if isinstance(v, Decimal):
            value = v
        else:
            try:
                value = Decimal(str(v))
            except (InvalidOperation, ValueError):
                raise ValueError("El margen debe ser un numero valido") from None
        if value.is_nan() or value.is_infinite():
            raise ValueError("El margen debe ser un numero valido")
        try:
            value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise ValueError("El margen debe tener un formato valido") from None
        if value < 0:
            raise ValueError("El margen no puede ser negativo")
        if value > cls._max_price:
            raise ValueError("El margen excede el maximo permitido")
        return value


class ProductStatusUpdate(BaseModel):
    """
    DTO para actualizar el estado de un producto.
    """

    estado: bool
    actualizado_por_id: Optional[int] = None
    fecha_actualizacion: Optional[datetime] = None


class ProductImportError(BaseModel):
    row: int
    message: str


class ProductImportResponse(BaseModel):
    created: int
    importados: int
    skipped: int
    invalid: int
    errors: list[ProductImportError] = Field(default_factory=list)


class ProductResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con productos.
    """
    producto_id: int
    codigo_barras: str
    nombre: str
    categoria_id: Optional[int]
    descripcion: Optional[str]
    precio_venta: Decimal
    costo: Decimal
    margen: Optional[Decimal] = None
    creado_por_id: Optional[int]
    actualizado_por_id: Optional[int]
    fecha_creacion: Optional[datetime]
    fecha_actualizacion: Optional[datetime]
    estado: bool
    categoria_nombre: Optional[str] = None
    creado_por_nombre: Optional[str] = None
    actualizado_por_nombre: Optional[str] = None

    class Config:
        from_attributes = True  # Permite construir desde objetos con atributos (ORM, entidades, etc.)
