from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from domain.dtos.visitaDto import (
    VisitaRequest,
    VisitaResponse,
    VisitaUpdateRequest,
)
from domain.entities.visitaEntity import VisitaEntity
from domain.interfaces.visita_repository_interface import VisitaRepositoryInterface


class VisitaService:
    def __init__(self, repository: VisitaRepositoryInterface):
        self.repository = repository

    def create_visita(self, data: VisitaRequest) -> VisitaResponse:
        entity = VisitaEntity(
            cliente_id=data.cliente_id,
            usuario_id=data.usuario_id,
            fecha=data.fecha,
            motivo=data.motivo,
        )
        created = self.repository.create_visita(entity)
        return VisitaResponse.model_validate(created)

    def get_visita(self, visita_id: int) -> Optional[VisitaResponse]:
        record = self.repository.get_visita(visita_id)
        if not record:
            return None
        return VisitaResponse.model_validate(record)

    def list_visitas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        usuario_id: Optional[int] = None,
    ) -> List[VisitaResponse]:
        records = self.repository.list_visitas(
            cliente_id=cliente_id,
            usuario_id=usuario_id,
        )
        return [VisitaResponse.model_validate(row) for row in records]

    def update_visita(
        self, visita_id: int, data: VisitaRequest
    ) -> Optional[VisitaResponse]:
        entity = VisitaEntity(
            id=visita_id,
            cliente_id=data.cliente_id,
            usuario_id=data.usuario_id,
            fecha=data.fecha,
            motivo=data.motivo,
        )
        updated = self.repository.update_visita(visita_id, entity)
        if not updated:
            return None
        return VisitaResponse.model_validate(updated)

    def patch_visita(
        self, visita_id: int, data: VisitaUpdateRequest
    ) -> Optional[VisitaResponse]:
        current = self.repository.get_visita(visita_id)
        if not current:
            return None
        entity = VisitaEntity(
            id=visita_id,
            cliente_id=(
                data.cliente_id if data.cliente_id is not None else current.cliente_id
            ),
            usuario_id=(
                data.usuario_id if data.usuario_id is not None else current.usuario_id
            ),
            fecha=data.fecha if data.fecha is not None else current.fecha,
            motivo=data.motivo if data.motivo is not None else current.motivo,
            created_at=current.created_at,
        )
        updated = self.repository.update_visita(visita_id, entity)
        if not updated:
            return None
        return VisitaResponse.model_validate(updated)

    def delete_visita(self, visita_id: int) -> bool:
        return self.repository.delete_visita(visita_id)
