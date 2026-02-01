from __future__ import annotations

from typing import List, Optional

from domain.dtos.cajasCervezaDto import (
    CajasCervezaRequest,
    CajasCervezaResponse,
    CajasCervezaUpdateRequest,
)
from domain.entities.cajasCervezaEntity import CajasCervezaEntity
from domain.interfaces.cajas_cerveza_repository_interface import (
    CajasCervezaRepositoryInterface,
)


class CajasCervezaService:
    def __init__(self, repository: CajasCervezaRepositoryInterface):
        self.repository = repository

    def create_cajas_cerveza(
        self, data: CajasCervezaRequest
    ) -> CajasCervezaResponse:
        entity = CajasCervezaEntity(
            nombre=data.nombre,
            cantidad_cajas=data.cantidad_cajas,
            entregado=data.entregado,
            fecha=data.fecha,
            cajero=data.cajero,
            actualizado_por=data.actualizado_por,
        )
        created = self.repository.create_cajas_cerveza(entity)
        return CajasCervezaResponse.model_validate(created)

    def list_cajas_cerveza(self) -> List[CajasCervezaResponse]:
        records = self.repository.list_cajas_cerveza()
        return [CajasCervezaResponse.model_validate(row) for row in records]

    def get_cajas_cerveza(
        self, cajas_id: int
    ) -> Optional[CajasCervezaResponse]:
        record = self.repository.get_cajas_cerveza(cajas_id)
        if not record:
            return None
        return CajasCervezaResponse.model_validate(record)

    def update_cajas_cerveza(
        self, cajas_id: int, data: CajasCervezaRequest
    ) -> Optional[CajasCervezaResponse]:
        entity = CajasCervezaEntity(
            id=cajas_id,
            nombre=data.nombre,
            cantidad_cajas=data.cantidad_cajas,
            entregado=data.entregado,
            fecha=data.fecha,
            cajero=data.cajero,
            actualizado_por=data.actualizado_por,
        )
        updated = self.repository.update_cajas_cerveza(cajas_id, entity)
        if not updated:
            return None
        return CajasCervezaResponse.model_validate(updated)

    def patch_cajas_cerveza(
        self, cajas_id: int, data: CajasCervezaUpdateRequest
    ) -> Optional[CajasCervezaResponse]:
        current = self.repository.get_cajas_cerveza(cajas_id)
        if not current:
            return None
        entity = CajasCervezaEntity(
            id=cajas_id,
            nombre=data.nombre if data.nombre is not None else current.nombre,
            cantidad_cajas=(
                data.cantidad_cajas
                if data.cantidad_cajas is not None
                else current.cantidad_cajas
            ),
            entregado=data.entregado if data.entregado is not None else current.entregado,
            fecha=data.fecha if data.fecha is not None else current.fecha,
            cajero=data.cajero if data.cajero is not None else current.cajero,
            actualizado_por=(
                data.actualizado_por
                if data.actualizado_por is not None
                else current.actualizado_por
            ),
        )
        updated = self.repository.update_cajas_cerveza(cajas_id, entity)
        if not updated:
            return None
        return CajasCervezaResponse.model_validate(updated)

    def delete_cajas_cerveza(self, cajas_id: int) -> bool:
        return self.repository.delete_cajas_cerveza(cajas_id)
