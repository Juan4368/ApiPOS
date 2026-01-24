from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.carteraEntity import CarteraEntity
from domain.interfaces.cartera_repository_interface import CarteraRepositoryInterface
from src.infrastructure.models.models import Cartera


class CarteraRepository(CarteraRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_cartera(self, entity: CarteraEntity) -> CarteraEntity:
        cartera_orm = Cartera(
            monto=entity.monto,
            fecha=entity.fecha,
            categoria_contabilidad_id=entity.categoria_contabilidad_id,
            cliente=entity.cliente,
            notas=entity.notas,
        )
        self.db.add(cartera_orm)
        self.db.commit()
        self.db.refresh(cartera_orm)
        return self._to_entity(cartera_orm)

    def get_cartera(self, cartera_id: int) -> Optional[CarteraEntity]:
        record = self.db.get(Cartera, cartera_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_cartera(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CarteraEntity]:
        query = self.db.query(Cartera)
        if desde:
            query = query.filter(Cartera.fecha >= datetime.combine(desde, time.min))
        if hasta:
            query = query.filter(Cartera.fecha <= datetime.combine(hasta, time.max))
        records = query.order_by(Cartera.fecha.desc()).all()
        return [self._to_entity(record) for record in records]

    def update_cartera(self, cartera_id: int, entity: CarteraEntity) -> Optional[CarteraEntity]:
        record = self.db.get(Cartera, cartera_id)
        if not record:
            return None
        record.monto = entity.monto
        record.fecha = entity.fecha
        record.categoria_contabilidad_id = entity.categoria_contabilidad_id
        record.cliente = entity.cliente
        record.notas = entity.notas
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Cartera) -> CarteraEntity:
        return CarteraEntity(
            cartera_id=record.cartera_id,
            fecha=record.fecha,
            monto=record.monto,
            categoria_contabilidad_id=record.categoria_contabilidad_id,
            cliente=record.cliente,
            notas=record.notas,
        )
