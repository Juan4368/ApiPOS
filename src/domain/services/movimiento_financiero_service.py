from __future__ import annotations

from datetime import date
from typing import List, Optional

from domain.dtos.movimientoFinancieroDto import (
    MovimientoFinancieroRequest,
    MovimientoFinancieroResponse,
    MovimientoFinancieroUpdateRequest,
)
from domain.entities.movimientoFinancieroEntity import MovimientoFinancieroEntity
from domain.enums.contabilidadEnums import CategoriaTipo
from domain.interfaces.movimiento_financiero_repository_interface import (
    MovimientoFinancieroRepositoryInterface,
)


class MovimientoFinancieroService:
    def __init__(self, repository: MovimientoFinancieroRepositoryInterface):
        self.repository = repository

    def _normalize_proveedor_id(
        self, tipo: CategoriaTipo, proveedor_id: Optional[int]
    ) -> Optional[int]:
        if proveedor_id in (None, 0):
            return None
        if tipo == CategoriaTipo.INGRESO:
            return None
        return proveedor_id

    def create_movimiento(
        self, data: MovimientoFinancieroRequest
    ) -> MovimientoFinancieroResponse:
        entity = MovimientoFinancieroEntity(
            fecha=data.fecha,
            tipo=data.tipo,
            monto=data.monto,
            concepto=data.concepto,
            proveedor_id=self._normalize_proveedor_id(data.tipo, data.proveedor_id),
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            venta_id=data.venta_id,
        )
        created = self.repository.create_movimiento(entity)
        return MovimientoFinancieroResponse.model_validate(created)

    def get_movimiento(
        self, movimiento_id: int
    ) -> Optional[MovimientoFinancieroResponse]:
        movimiento = self.repository.get_movimiento(movimiento_id)
        if not movimiento:
            return None
        return MovimientoFinancieroResponse.model_validate(movimiento)

    def list_movimientos(
        self,
        *,
        desde: Optional[date] = None,
        hasta: Optional[date] = None,
        caja_id: Optional[int] = None,
        tipo: Optional[CategoriaTipo] = None,
        proveedor_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        venta_id: Optional[int] = None,
    ) -> List[MovimientoFinancieroResponse]:
        movimientos = self.repository.list_movimientos(
            desde=desde,
            hasta=hasta,
            caja_id=caja_id,
            tipo=tipo,
            proveedor_id=proveedor_id,
            usuario_id=usuario_id,
            venta_id=venta_id,
        )
        return [MovimientoFinancieroResponse.model_validate(m) for m in movimientos]

    def update_movimiento(
        self, movimiento_id: int, data: MovimientoFinancieroRequest
    ) -> Optional[MovimientoFinancieroResponse]:
        entity = MovimientoFinancieroEntity(
            id=movimiento_id,
            fecha=data.fecha,
            tipo=data.tipo,
            monto=data.monto,
            concepto=data.concepto,
            proveedor_id=self._normalize_proveedor_id(data.tipo, data.proveedor_id),
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            venta_id=data.venta_id,
        )
        updated = self.repository.update_movimiento(movimiento_id, entity)
        if not updated:
            return None
        return MovimientoFinancieroResponse.model_validate(updated)

    def patch_movimiento(
        self, movimiento_id: int, data: MovimientoFinancieroUpdateRequest
    ) -> Optional[MovimientoFinancieroResponse]:
        current = self.repository.get_movimiento(movimiento_id)
        if not current:
            return None
        next_tipo = data.tipo if data.tipo is not None else current.tipo
        next_proveedor_id = (
            data.proveedor_id if data.proveedor_id is not None else current.proveedor_id
        )
        entity = MovimientoFinancieroEntity(
            id=movimiento_id,
            fecha=data.fecha if data.fecha is not None else current.fecha,
            tipo=next_tipo,
            monto=data.monto if data.monto is not None else current.monto,
            concepto=data.concepto if data.concepto is not None else current.concepto,
            proveedor_id=self._normalize_proveedor_id(next_tipo, next_proveedor_id),
            caja_id=data.caja_id if data.caja_id is not None else current.caja_id,
            usuario_id=(
                data.usuario_id if data.usuario_id is not None else current.usuario_id
            ),
            venta_id=data.venta_id if data.venta_id is not None else current.venta_id,
            created_at=current.created_at,
        )
        updated = self.repository.update_movimiento(movimiento_id, entity)
        if not updated:
            return None
        return MovimientoFinancieroResponse.model_validate(updated)
