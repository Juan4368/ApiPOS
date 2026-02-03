from __future__ import annotations

from typing import List, Optional

from domain.dtos.cajaSesionDto import (
    CajaSesionRequest,
    CajaSesionResponse,
    CajaSesionUpdateRequest,
)
from domain.entities.cajaSesionEntity import CajaSesionEntity
from domain.interfaces.caja_sesion_repository_interface import (
    CajaSesionRepositoryInterface,
)


class CajaSesionService:
    def __init__(self, repository: CajaSesionRepositoryInterface):
        self.repository = repository

    def create_caja_sesion(self, data: CajaSesionRequest) -> CajaSesionResponse:
        if data.usuario_id is not None:
            abierta = self.repository.get_open_by_caja_usuario(data.caja_id, data.usuario_id)
            if abierta:
                raise ValueError(
                    "El usuario ya tiene una sesion abierta en esta caja y debe cerrarla primero."
                )
        entity = CajaSesionEntity(
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            fecha_apertura=data.fecha_apertura,
            fecha_cierre=data.fecha_cierre,
        )
        created = self.repository.create_caja_sesion(entity)
        return CajaSesionResponse.model_validate(created)

    def list_caja_sesiones(self) -> List[CajaSesionResponse]:
        records = self.repository.list_caja_sesiones()
        return [CajaSesionResponse.model_validate(row) for row in records]

    def get_caja_sesion(self, sesion_id: int) -> Optional[CajaSesionResponse]:
        record = self.repository.get_caja_sesion(sesion_id)
        if not record:
            return None
        return CajaSesionResponse.model_validate(record)

    def update_caja_sesion(
        self, sesion_id: int, data: CajaSesionRequest
    ) -> Optional[CajaSesionResponse]:
        entity = CajaSesionEntity(
            id=sesion_id,
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            fecha_apertura=data.fecha_apertura,
            fecha_cierre=data.fecha_cierre,
        )
        updated = self.repository.update_caja_sesion(sesion_id, entity)
        if not updated:
            return None
        return CajaSesionResponse.model_validate(updated)

    def patch_caja_sesion(
        self, sesion_id: int, data: CajaSesionUpdateRequest
    ) -> Optional[CajaSesionResponse]:
        current = self.repository.get_caja_sesion(sesion_id)
        if not current:
            return None
        entity = CajaSesionEntity(
            id=sesion_id,
            caja_id=data.caja_id if data.caja_id is not None else current.caja_id,
            usuario_id=(
                data.usuario_id if data.usuario_id is not None else current.usuario_id
            ),
            fecha_apertura=(
                data.fecha_apertura
                if data.fecha_apertura is not None
                else current.fecha_apertura
            ),
            fecha_cierre=(
                data.fecha_cierre
                if data.fecha_cierre is not None
                else current.fecha_cierre
            ),
            created_at=current.created_at,
        )
        updated = self.repository.update_caja_sesion(sesion_id, entity)
        if not updated:
            return None
        return CajaSesionResponse.model_validate(updated)

    def delete_caja_sesion(self, sesion_id: int) -> bool:
        return self.repository.delete_caja_sesion(sesion_id)
