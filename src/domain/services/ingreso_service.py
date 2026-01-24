from __future__ import annotations

from datetime import date
from typing import List, Optional

from domain.dtos.ingresoDto import (
    IngresoRequest,
    IngresoResponse,
    IngresoUpdateRequest,
)
from domain.entities.ingresoEntity import IngresoEntity
from domain.interfaces.ingreso_repository_interface import IngresoRepositoryInterface


class IngresoService:
    def __init__(self, repository: IngresoRepositoryInterface):
        self.repository = repository

    def create_ingreso(self, data: IngresoRequest) -> IngresoResponse:
        entity = IngresoEntity(
            fecha=data.fecha,
            monto=data.monto,
            tipo_ingreso=data.tipo_ingreso,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            notas=data.notas,
            cliente=data.cliente,
        )
        created = self.repository.create_ingreso(entity)
        return IngresoResponse.model_validate(created)

    def get_ingreso(self, ingreso_id: int) -> Optional[IngresoResponse]:
        ingreso = self.repository.get_ingreso(ingreso_id)
        if not ingreso:
            return None
        return IngresoResponse.model_validate(ingreso)

    def list_ingresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[IngresoResponse]:
        ingresos = self.repository.list_ingresos(desde=desde, hasta=hasta)
        return [IngresoResponse.model_validate(i) for i in ingresos]

    def update_ingreso(
        self, ingreso_id: int, data: IngresoRequest
    ) -> Optional[IngresoResponse]:
        entity = IngresoEntity(
            id=ingreso_id,
            fecha=data.fecha,
            monto=data.monto,
            tipo_ingreso=data.tipo_ingreso,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            notas=data.notas,
            cliente=data.cliente,
        )
        updated = self.repository.update_ingreso(ingreso_id, entity)
        if not updated:
            return None
        return IngresoResponse.model_validate(updated)

    def patch_ingreso(
        self, ingreso_id: int, data: IngresoUpdateRequest
    ) -> Optional[IngresoResponse]:
        current = self.repository.get_ingreso(ingreso_id)
        if not current:
            return None
        fecha = current.fecha
        if data.fecha is not None:
            fecha = data.fecha
        entity = IngresoEntity(
            id=ingreso_id,
            fecha=fecha,
            monto=data.monto if data.monto is not None else current.monto,
            tipo_ingreso=(
                data.tipo_ingreso if data.tipo_ingreso is not None else current.tipo_ingreso
            ),
            categoria_contabilidad_id=(
                data.categoria_contabilidad_id
                if data.categoria_contabilidad_id is not None
                else current.categoria_contabilidad_id
            ),
            notas=data.notas if data.notas is not None else current.notas,
            cliente=data.cliente if data.cliente is not None else current.cliente,
        )
        updated = self.repository.update_ingreso(ingreso_id, entity)
        if not updated:
            return None
        return IngresoResponse.model_validate(updated)
