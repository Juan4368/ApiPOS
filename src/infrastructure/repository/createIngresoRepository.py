from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.ingresoEntity import IngresoEntity
from domain.enums.contabilidadEnums import MedioPago
from domain.interfaces.ingreso_repository_interface import IngresoRepositoryInterface
from src.infrastructure.models.models import Ingreso


class IngresoRepository(IngresoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_ingreso(self, entity: IngresoEntity) -> IngresoEntity:
        ingreso_orm = Ingreso(
            monto=entity.monto,
            fecha=entity.fecha,
            tipo_ingreso=self._to_tipo_ingreso(entity.tipo_ingreso),
            categoria_contabilidad_id=entity.categoria_contabilidad_id,
            notas=entity.notas,
            cliente=entity.cliente,
        )
        self.db.add(ingreso_orm)
        self.db.commit()
        self.db.refresh(ingreso_orm)
        return self._to_entity(ingreso_orm)

    def get_ingreso(self, ingreso_id: int) -> Optional[IngresoEntity]:
        record = self.db.get(Ingreso, ingreso_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_ingresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[IngresoEntity]:
        query = self.db.query(Ingreso)
        if desde:
            query = query.filter(Ingreso.fecha >= datetime.combine(desde, time.min))
        if hasta:
            query = query.filter(Ingreso.fecha <= datetime.combine(hasta, time.max))
        records = query.order_by(Ingreso.fecha.desc()).all()
        return [self._to_entity(record) for record in records]

    def update_ingreso(self, ingreso_id: int, entity: IngresoEntity) -> Optional[IngresoEntity]:
        record = self.db.get(Ingreso, ingreso_id)
        if not record:
            return None
        record.monto = entity.monto
        record.fecha = entity.fecha
        record.tipo_ingreso = self._to_tipo_ingreso(entity.tipo_ingreso)
        record.categoria_contabilidad_id = entity.categoria_contabilidad_id
        record.notas = entity.notas
        record.cliente = entity.cliente
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_tipo_ingreso(self, medio_pago: MedioPago) -> str:
        if isinstance(medio_pago, MedioPago):
            return medio_pago.value.lower()
        return str(medio_pago).lower()

    def _to_entity(self, record: Ingreso) -> IngresoEntity:
        return IngresoEntity(
            id=record.ingreso_id,
            fecha=record.fecha,
            monto=record.monto,
            tipo_ingreso=MedioPago(record.tipo_ingreso.upper()),
            categoria_contabilidad_id=record.categoria_contabilidad_id,
            notas=record.notas,
            cliente=record.cliente,
        )
