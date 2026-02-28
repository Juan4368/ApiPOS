from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.egresoEntity import EgresoEntity
from domain.enums.contabilidadEnums import MedioPago
from domain.interfaces.egreso_repository_interface import EgresoRepositoryInterface
from src.infrastructure.models.models import Egreso
from utils.timezone import end_of_day, start_of_day


class EgresoRepository(EgresoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_egreso(self, entity: EgresoEntity) -> EgresoEntity:
        egreso_orm = Egreso(
            monto=entity.monto,
            fecha=start_of_day(entity.fecha),
            tipo_egreso=self._to_tipo_egreso(entity.tipo_egreso),
            categoria_contabilidad_id=entity.categoria_contabilidad_id,
            notas=entity.notas,
            cliente=entity.cliente,
        )
        self.db.add(egreso_orm)
        self.db.commit()
        self.db.refresh(egreso_orm)
        return self._to_entity(egreso_orm)

    def get_egreso(self, egreso_id: int) -> Optional[EgresoEntity]:
        record = self.db.get(Egreso, egreso_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_egresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[EgresoEntity]:
        query = self.db.query(Egreso)
        if desde:
            query = query.filter(Egreso.fecha >= start_of_day(desde))
        if hasta:
            query = query.filter(Egreso.fecha <= end_of_day(hasta))
        records = query.order_by(Egreso.fecha.desc()).all()
        return [self._to_entity(record) for record in records]

    def update_egreso(self, egreso_id: int, entity: EgresoEntity) -> Optional[EgresoEntity]:
        record = self.db.get(Egreso, egreso_id)
        if not record:
            return None
        record.monto = entity.monto
        record.fecha = start_of_day(entity.fecha)
        record.tipo_egreso = self._to_tipo_egreso(entity.tipo_egreso)
        record.categoria_contabilidad_id = entity.categoria_contabilidad_id
        record.notas = entity.notas
        record.cliente = entity.cliente
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_tipo_egreso(self, medio_pago: MedioPago) -> str:
        if isinstance(medio_pago, MedioPago):
            return medio_pago.value.lower()
        return str(medio_pago).lower()

    def _to_entity(self, record: Egreso) -> EgresoEntity:
        return EgresoEntity(
            id=record.egreso_id,
            fecha=record.fecha.date(),
            monto=record.monto,
            tipo_egreso=MedioPago(record.tipo_egreso.upper()),
            notas=record.notas,
            categoria_contabilidad_id=record.categoria_contabilidad_id,
            cliente=record.cliente,
        )
