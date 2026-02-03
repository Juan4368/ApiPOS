from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.cajaSesionEntity import CajaSesionEntity
from domain.interfaces.caja_sesion_repository_interface import (
    CajaSesionRepositoryInterface,
)
from src.infrastructure.models.models import CajaSesion


class CajaSesionRepository(CajaSesionRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_caja_sesion(self, entity: CajaSesionEntity) -> CajaSesionEntity:
        now = datetime.now(timezone.utc)
        fecha_apertura = entity.fecha_apertura or now
        created_at = entity.created_at or now
        record = CajaSesion(
            caja_id=entity.caja_id,
            usuario_id=entity.usuario_id,
            fecha_apertura=fecha_apertura,
            fecha_cierre=entity.fecha_cierre,
            created_at=created_at,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def get_open_by_caja_usuario(
        self, caja_id: int, usuario_id: int
    ) -> Optional[CajaSesionEntity]:
        record = (
            self.db.query(CajaSesion)
            .filter(
                CajaSesion.caja_id == caja_id,
                CajaSesion.usuario_id == usuario_id,
                CajaSesion.fecha_cierre.is_(None),
            )
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

    def get_caja_sesion(self, sesion_id: int) -> Optional[CajaSesionEntity]:
        record = self.db.get(CajaSesion, sesion_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_caja_sesiones(self) -> List[CajaSesionEntity]:
        records = self.db.query(CajaSesion).all()
        return [self._to_entity(row) for row in records]

    def update_caja_sesion(
        self, sesion_id: int, entity: CajaSesionEntity
    ) -> Optional[CajaSesionEntity]:
        record = self.db.get(CajaSesion, sesion_id)
        if not record:
            return None
        record.caja_id = entity.caja_id
        record.usuario_id = entity.usuario_id
        record.fecha_apertura = entity.fecha_apertura or record.fecha_apertura
        record.fecha_cierre = entity.fecha_cierre
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def delete_caja_sesion(self, sesion_id: int) -> bool:
        record = self.db.get(CajaSesion, sesion_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def _to_entity(self, record: CajaSesion) -> CajaSesionEntity:
        return CajaSesionEntity.from_model(record)
