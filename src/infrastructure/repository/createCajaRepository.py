from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.cajaEntity import CajaEntity
from domain.interfaces.caja_repository_interface import CajaRepositoryInterface
from src.infrastructure.models.models import Caja


class CajaRepository(CajaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_caja(self, entity: CajaEntity) -> CajaEntity:
        created_at = entity.created_at or datetime.now(timezone.utc)
        caja_orm = Caja(
            nombre=entity.nombre,
            saldo_inicial=entity.saldo_inicial,
            created_at=created_at,
        )
        self.db.add(caja_orm)
        self.db.commit()
        self.db.refresh(caja_orm)
        return self._to_entity(caja_orm)

    def get_caja(self, caja_id: int) -> Optional[CajaEntity]:
        record = self.db.get(Caja, caja_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_cajas(self) -> List[CajaEntity]:
        records = self.db.query(Caja).all()
        return [self._to_entity(row) for row in records]

    def update_caja(self, caja_id: int, entity: CajaEntity) -> Optional[CajaEntity]:
        record = self.db.get(Caja, caja_id)
        if not record:
            return None
        record.nombre = entity.nombre
        record.saldo_inicial = entity.saldo_inicial
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Caja) -> CajaEntity:
        return CajaEntity.from_model(record)
