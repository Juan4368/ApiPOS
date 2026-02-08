from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from domain.dtos.cierreCajaDenominacionDto import (
    CierreCajaDenominacionRequest,
    CierreCajaDenominacionResponse,
    CierreCajaDenominacionUpdateRequest,
)
from domain.entities.cierreCajaDenominacionEntity import CierreCajaDenominacionEntity
from domain.interfaces.cierre_caja_denominacion_repository_interface import (
    CierreCajaDenominacionRepositoryInterface,
)


class CierreCajaDenominacionService:
    def __init__(self, repository: CierreCajaDenominacionRepositoryInterface):
        self.repository = repository

    def create_denominacion(
        self, data: CierreCajaDenominacionRequest
    ) -> CierreCajaDenominacionResponse:
        entity = CierreCajaDenominacionEntity(
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            denominacion=data.denominacion,
            cantidad=data.cantidad,
            subtotal=self._subtotal(data.denominacion, data.cantidad),
            fecha_conteo=data.fecha_conteo,
        )
        created = self.repository.create_denominacion(entity)
        return CierreCajaDenominacionResponse.model_validate(created)

    def create_denominaciones(
        self, data: List[CierreCajaDenominacionRequest]
    ) -> List[CierreCajaDenominacionResponse]:
        entities = [
            CierreCajaDenominacionEntity(
                caja_id=row.caja_id,
                usuario_id=row.usuario_id,
                denominacion=row.denominacion,
                cantidad=row.cantidad,
                subtotal=self._subtotal(row.denominacion, row.cantidad),
                fecha_conteo=row.fecha_conteo,
            )
            for row in data
        ]
        created = self.repository.create_denominaciones(entities)
        return [CierreCajaDenominacionResponse.model_validate(row) for row in created]

    def list_denominaciones(self) -> List[CierreCajaDenominacionResponse]:
        records = self.repository.list_denominaciones()
        return [CierreCajaDenominacionResponse.model_validate(row) for row in records]

    def get_denominacion(
        self, denominacion_id: int
    ) -> Optional[CierreCajaDenominacionResponse]:
        record = self.repository.get_denominacion(denominacion_id)
        if not record:
            return None
        return CierreCajaDenominacionResponse.model_validate(record)

    def update_denominacion(
        self, denominacion_id: int, data: CierreCajaDenominacionRequest
    ) -> Optional[CierreCajaDenominacionResponse]:
        entity = CierreCajaDenominacionEntity(
            id=denominacion_id,
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            denominacion=data.denominacion,
            cantidad=data.cantidad,
            subtotal=self._subtotal(data.denominacion, data.cantidad),
            fecha_conteo=data.fecha_conteo,
        )
        updated = self.repository.update_denominacion(denominacion_id, entity)
        if not updated:
            return None
        return CierreCajaDenominacionResponse.model_validate(updated)

    def patch_denominacion(
        self, denominacion_id: int, data: CierreCajaDenominacionUpdateRequest
    ) -> Optional[CierreCajaDenominacionResponse]:
        current = self.repository.get_denominacion(denominacion_id)
        if not current:
            return None
        denominacion = (
            data.denominacion if data.denominacion is not None else current.denominacion
        )
        cantidad = data.cantidad if data.cantidad is not None else current.cantidad
        entity = CierreCajaDenominacionEntity(
            id=denominacion_id,
            caja_id=data.caja_id if data.caja_id is not None else current.caja_id,
            usuario_id=(
                data.usuario_id if data.usuario_id is not None else current.usuario_id
            ),
            denominacion=denominacion,
            cantidad=cantidad,
            subtotal=self._subtotal(denominacion, cantidad),
            fecha_conteo=(
                data.fecha_conteo
                if data.fecha_conteo is not None
                else current.fecha_conteo
            ),
        )
        updated = self.repository.update_denominacion(denominacion_id, entity)
        if not updated:
            return None
        return CierreCajaDenominacionResponse.model_validate(updated)

    def delete_denominacion(self, denominacion_id: int) -> bool:
        return self.repository.delete_denominacion(denominacion_id)

    def _subtotal(self, denominacion: Decimal, cantidad: int) -> Decimal:
        return (denominacion * Decimal(cantidad)).quantize(Decimal("0.01"))
