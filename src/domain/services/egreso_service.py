from __future__ import annotations

from datetime import date
from typing import List, Optional

from domain.dtos.egresoDto import EgresoRequest, EgresoResponse, EgresoUpdateRequest
from domain.entities.egresoEntity import EgresoEntity
from domain.interfaces.egreso_repository_interface import EgresoRepositoryInterface


class EgresoService:
    def __init__(self, repository: EgresoRepositoryInterface):
        self.repository = repository

    def create_egreso(self, data: EgresoRequest) -> EgresoResponse:
        entity = EgresoEntity(
            fecha=data.fecha,
            monto=data.monto,
            tipo_egreso=data.tipo_egreso,
            notas=data.notas,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            cliente=data.cliente,
        )
        created = self.repository.create_egreso(entity)
        return EgresoResponse.model_validate(created)

    def get_egreso(self, egreso_id: int) -> Optional[EgresoResponse]:
        egreso = self.repository.get_egreso(egreso_id)
        if not egreso:
            return None
        return EgresoResponse.model_validate(egreso)

    def list_egresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[EgresoResponse]:
        egresos = self.repository.list_egresos(desde=desde, hasta=hasta)
        return [EgresoResponse.model_validate(e) for e in egresos]

    def update_egreso(
        self, egreso_id: int, data: EgresoRequest
    ) -> Optional[EgresoResponse]:
        entity = EgresoEntity(
            id=egreso_id,
            fecha=data.fecha,
            monto=data.monto,
            tipo_egreso=data.tipo_egreso,
            notas=data.notas,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            cliente=data.cliente,
        )
        updated = self.repository.update_egreso(egreso_id, entity)
        if not updated:
            return None
        return EgresoResponse.model_validate(updated)

    def patch_egreso(
        self, egreso_id: int, data: EgresoUpdateRequest
    ) -> Optional[EgresoResponse]:
        current = self.repository.get_egreso(egreso_id)
        if not current:
            return None
        entity = EgresoEntity(
            id=egreso_id,
            fecha=data.fecha if data.fecha is not None else current.fecha,
            monto=data.monto if data.monto is not None else current.monto,
            tipo_egreso=data.tipo_egreso if data.tipo_egreso is not None else current.tipo_egreso,
            notas=(
                data.notas if data.notas is not None else current.notas
            ),
            categoria_contabilidad_id=(
                data.categoria_contabilidad_id
                if data.categoria_contabilidad_id is not None
                else current.categoria_contabilidad_id
            ),
            cliente=data.cliente if data.cliente is not None else current.cliente,
        )
        updated = self.repository.update_egreso(egreso_id, entity)
        if not updated:
            return None
        return EgresoResponse.model_validate(updated)
