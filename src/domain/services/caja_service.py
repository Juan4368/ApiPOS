from __future__ import annotations

from typing import List, Optional

from domain.dtos.cajaDto import CajaRequest, CajaResponse, CajaUpdateRequest
from domain.entities.cajaEntity import CajaEntity
from domain.interfaces.caja_repository_interface import CajaRepositoryInterface


class CajaService:
    def __init__(self, repository: CajaRepositoryInterface):
        self.repository = repository

    def create_caja(self, data: CajaRequest) -> CajaResponse:
        entity = CajaEntity(
            nombre=data.nombre,
            saldo_inicial=data.saldo_inicial,
            estado=data.estado,
            usuario_id=data.usuario_id,
            fecha_apertura=data.fecha_apertura,
            fecha_cierre=data.fecha_cierre,
        )
        created = self.repository.create_caja(entity)
        return CajaResponse.model_validate(created)

    def get_caja(self, caja_id: int) -> Optional[CajaResponse]:
        caja = self.repository.get_caja(caja_id)
        if not caja:
            return None
        return CajaResponse.model_validate(caja)

    def list_cajas(self) -> List[CajaResponse]:
        cajas = self.repository.list_cajas()
        return [CajaResponse.model_validate(c) for c in cajas]

    def update_caja(self, caja_id: int, data: CajaRequest) -> Optional[CajaResponse]:
        entity = CajaEntity(
            id=caja_id,
            nombre=data.nombre,
            saldo_inicial=data.saldo_inicial,
            estado=data.estado,
            usuario_id=data.usuario_id,
            fecha_apertura=data.fecha_apertura,
            fecha_cierre=data.fecha_cierre,
        )
        updated = self.repository.update_caja(caja_id, entity)
        if not updated:
            return None
        return CajaResponse.model_validate(updated)

    def patch_caja(
        self, caja_id: int, data: CajaUpdateRequest
    ) -> Optional[CajaResponse]:
        current = self.repository.get_caja(caja_id)
        if not current:
            return None
        entity = CajaEntity(
            id=caja_id,
            nombre=data.nombre if data.nombre is not None else current.nombre,
            saldo_inicial=(
                data.saldo_inicial if data.saldo_inicial is not None else current.saldo_inicial
            ),
            estado=data.estado if data.estado is not None else current.estado,
            usuario_id=data.usuario_id if data.usuario_id is not None else current.usuario_id,
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
        updated = self.repository.update_caja(caja_id, entity)
        if not updated:
            return None
        return CajaResponse.model_validate(updated)
