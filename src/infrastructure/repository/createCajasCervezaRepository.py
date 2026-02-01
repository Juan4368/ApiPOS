from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.cajasCervezaEntity import CajasCervezaEntity
from domain.interfaces.cajas_cerveza_repository_interface import (
    CajasCervezaRepositoryInterface,
)
from src.infrastructure.models.models import CajasCerveza


class CajasCervezaRepository(CajasCervezaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_cajas_cerveza(self, entity: CajasCervezaEntity) -> CajasCervezaEntity:
        fecha = entity.fecha or datetime.now(timezone.utc)
        record = CajasCerveza(
            nombre=entity.nombre,
            cantidad_cajas=entity.cantidad_cajas,
            entregado=entity.entregado,
            fecha=fecha,
            cajero=entity.cajero,
            actualizado_por=entity.actualizado_por,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def get_cajas_cerveza(self, cajas_id: int) -> Optional[CajasCervezaEntity]:
        record = self.db.get(CajasCerveza, cajas_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_cajas_cerveza(self) -> List[CajasCervezaEntity]:
        records = self.db.query(CajasCerveza).all()
        return [self._to_entity(row) for row in records]

    def update_cajas_cerveza(
        self, cajas_id: int, entity: CajasCervezaEntity
    ) -> Optional[CajasCervezaEntity]:
        record = self.db.get(CajasCerveza, cajas_id)
        if not record:
            return None
        record.nombre = entity.nombre
        record.cantidad_cajas = entity.cantidad_cajas
        record.entregado = entity.entregado
        record.fecha = entity.fecha or record.fecha
        record.cajero = entity.cajero
        record.actualizado_por = entity.actualizado_por
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def delete_cajas_cerveza(self, cajas_id: int) -> bool:
        record = self.db.get(CajasCerveza, cajas_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def _to_entity(self, record: CajasCerveza) -> CajasCervezaEntity:
        return CajasCervezaEntity.from_model(record)
