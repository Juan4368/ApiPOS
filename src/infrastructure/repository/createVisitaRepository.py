from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.visitaEntity import VisitaEntity
from domain.interfaces.visita_repository_interface import VisitaRepositoryInterface
from src.infrastructure.models.models import Visita
from utils.timezone import ensure_utc_minus_5, now_utc_minus_5


class VisitaRepository(VisitaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_visita(self, entity: VisitaEntity) -> VisitaEntity:
        now = now_utc_minus_5()
        fecha = ensure_utc_minus_5(entity.fecha) if entity.fecha else now
        created_at = ensure_utc_minus_5(entity.created_at) if entity.created_at else now
        record = Visita(
            cliente_id=entity.cliente_id,
            usuario_id=entity.usuario_id,
            fecha=fecha,
            motivo=entity.motivo,
            created_at=created_at,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def get_visita(self, visita_id: int) -> Optional[VisitaEntity]:
        record = self.db.get(Visita, visita_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_visitas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        usuario_id: Optional[int] = None,
    ) -> List[VisitaEntity]:
        query = self.db.query(Visita)
        if cliente_id is not None:
            query = query.filter(Visita.cliente_id == cliente_id)
        if usuario_id is not None:
            query = query.filter(Visita.usuario_id == usuario_id)
        records = query.order_by(Visita.fecha.desc()).all()
        return [self._to_entity(row) for row in records]

    def update_visita(
        self, visita_id: int, entity: VisitaEntity
    ) -> Optional[VisitaEntity]:
        record = self.db.get(Visita, visita_id)
        if not record:
            return None
        record.cliente_id = entity.cliente_id
        record.usuario_id = entity.usuario_id
        record.fecha = (
            ensure_utc_minus_5(entity.fecha) if entity.fecha else record.fecha
        )
        record.motivo = entity.motivo
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def delete_visita(self, visita_id: int) -> bool:
        record = self.db.get(Visita, visita_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def _to_entity(self, record: Visita) -> VisitaEntity:
        return VisitaEntity.from_model(record)
