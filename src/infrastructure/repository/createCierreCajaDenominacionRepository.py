from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.cierreCajaDenominacionEntity import CierreCajaDenominacionEntity
from domain.interfaces.cierre_caja_denominacion_repository_interface import (
    CierreCajaDenominacionRepositoryInterface,
)
from src.infrastructure.models.models import CierreCajaDenominacion


class CierreCajaDenominacionRepository(CierreCajaDenominacionRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_denominacion(
        self, entity: CierreCajaDenominacionEntity
    ) -> CierreCajaDenominacionEntity:
        fecha_conteo = entity.fecha_conteo or datetime.now(timezone.utc)
        record = CierreCajaDenominacion(
            caja_id=entity.caja_id,
            usuario_id=entity.usuario_id,
            denominacion=entity.denominacion,
            cantidad=entity.cantidad,
            subtotal=entity.subtotal,
            fecha_conteo=fecha_conteo,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def create_denominaciones(
        self, entities: List[CierreCajaDenominacionEntity]
    ) -> List[CierreCajaDenominacionEntity]:
        if not entities:
            return []
        records: list[CierreCajaDenominacion] = []
        for entity in entities:
            fecha_conteo = entity.fecha_conteo or datetime.now(timezone.utc)
            records.append(
                CierreCajaDenominacion(
                    caja_id=entity.caja_id,
                    usuario_id=entity.usuario_id,
                    denominacion=entity.denominacion,
                    cantidad=entity.cantidad,
                    subtotal=entity.subtotal,
                    fecha_conteo=fecha_conteo,
                )
            )
        self.db.add_all(records)
        self.db.commit()
        for record in records:
            self.db.refresh(record)
        return [self._to_entity(row) for row in records]

    def get_denominacion(self, denominacion_id: int) -> Optional[CierreCajaDenominacionEntity]:
        record = self.db.get(CierreCajaDenominacion, denominacion_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_denominaciones(self) -> List[CierreCajaDenominacionEntity]:
        records = self.db.query(CierreCajaDenominacion).all()
        return [self._to_entity(row) for row in records]

    def update_denominacion(
        self, denominacion_id: int, entity: CierreCajaDenominacionEntity
    ) -> Optional[CierreCajaDenominacionEntity]:
        record = self.db.get(CierreCajaDenominacion, denominacion_id)
        if not record:
            return None
        record.caja_id = entity.caja_id
        record.usuario_id = entity.usuario_id
        record.denominacion = entity.denominacion
        record.cantidad = entity.cantidad
        record.subtotal = entity.subtotal
        record.fecha_conteo = entity.fecha_conteo or record.fecha_conteo
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def delete_denominacion(self, denominacion_id: int) -> bool:
        record = self.db.get(CierreCajaDenominacion, denominacion_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def _to_entity(self, record: CierreCajaDenominacion) -> CierreCajaDenominacionEntity:
        return CierreCajaDenominacionEntity.from_model(record)
