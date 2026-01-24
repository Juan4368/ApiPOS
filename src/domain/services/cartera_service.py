from __future__ import annotations

from datetime import date
from typing import List, Optional

from domain.dtos.carteraDto import (
    CarteraRequest,
    CarteraResponse,
    CarteraUpdateRequest,
)
from domain.entities.carteraEntity import CarteraEntity
from domain.interfaces.cartera_repository_interface import CarteraRepositoryInterface


class CarteraService:
    def __init__(self, repository: CarteraRepositoryInterface):
        self.repository = repository

    def create_cartera(self, data: CarteraRequest) -> CarteraResponse:
        entity = CarteraEntity(
            fecha=data.fecha,
            monto=data.monto,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            cliente=data.cliente,
            notas=data.notas,
        )
        created = self.repository.create_cartera(entity)
        return CarteraResponse.model_validate(created)

    def get_cartera(self, cartera_id: int) -> Optional[CarteraResponse]:
        cartera = self.repository.get_cartera(cartera_id)
        if not cartera:
            return None
        return CarteraResponse.model_validate(cartera)

    def list_cartera(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CarteraResponse]:
        records = self.repository.list_cartera(desde=desde, hasta=hasta)
        return [CarteraResponse.model_validate(record) for record in records]

    def update_cartera(
        self, cartera_id: int, data: CarteraRequest
    ) -> Optional[CarteraResponse]:
        entity = CarteraEntity(
            cartera_id=cartera_id,
            fecha=data.fecha,
            monto=data.monto,
            categoria_contabilidad_id=data.categoria_contabilidad_id,
            cliente=data.cliente,
            notas=data.notas,
        )
        updated = self.repository.update_cartera(cartera_id, entity)
        if not updated:
            return None
        return CarteraResponse.model_validate(updated)

    def patch_cartera(
        self, cartera_id: int, data: CarteraUpdateRequest
    ) -> Optional[CarteraResponse]:
        current = self.repository.get_cartera(cartera_id)
        if not current:
            return None
        entity = CarteraEntity(
            cartera_id=cartera_id,
            fecha=data.fecha if data.fecha is not None else current.fecha,
            monto=data.monto if data.monto is not None else current.monto,
            categoria_contabilidad_id=(
                data.categoria_contabilidad_id
                if data.categoria_contabilidad_id is not None
                else current.categoria_contabilidad_id
            ),
            cliente=data.cliente if data.cliente is not None else current.cliente,
            notas=data.notas if data.notas is not None else current.notas,
        )
        updated = self.repository.update_cartera(cartera_id, entity)
        if not updated:
            return None
        return CarteraResponse.model_validate(updated)
