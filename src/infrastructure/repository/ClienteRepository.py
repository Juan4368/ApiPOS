from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.clienteEntity import ClienteEntity
from domain.interfaces.cliente_repository_interface import ClienteRepositoryInterface
from src.infrastructure.models.models import Cliente


class ClienteRepository(ClienteRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con clientes."""

    def __init__(self, db: Session):
        self.db = db

    def create_cliente(
        self, entity: ClienteEntity, nombre_normalizado: Optional[str] = None
    ) -> ClienteEntity:
        normalized = (
            nombre_normalizado
            or entity.nombre_normalizado
            or (entity.nombre or "").strip().lower()
        )
        created_at = entity.created_at or datetime.now(timezone.utc)
        cliente_orm = Cliente(
            id=entity.id,
            nombre=entity.nombre,
            nombre_normalizado=normalized,
            telefono=entity.telefono,
            email=entity.email,
            created_at=created_at,
        )

        self.db.add(cliente_orm)
        self.db.commit()
        self.db.refresh(cliente_orm)
        return self._to_entity(cliente_orm)

    def get_cliente(self, cliente_id: UUID) -> Optional[ClienteEntity]:
        record = self.db.get(Cliente, cliente_id)
        if not record:
            return None
        return self._to_entity(record)

    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ClienteEntity]:
        record = (
            self.db.query(Cliente)
            .filter(Cliente.nombre_normalizado == nombre_normalizado)
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

    def list_clientes(self) -> List[ClienteEntity]:
        records = self.db.query(Cliente).all()
        return [self._to_entity(row) for row in records]

    def search_clientes(self, term: str) -> List[ClienteEntity]:
        like_term = f"%{term}%"
        filters = [
            Cliente.nombre.ilike(like_term),
            Cliente.nombre_normalizado.ilike(like_term),
            Cliente.telefono.ilike(like_term),
            Cliente.email.ilike(like_term),
        ]

        records = self.db.query(Cliente).filter(or_(*filters)).all()
        return [self._to_entity(row) for row in records]

    def _to_entity(self, record: Cliente) -> ClienteEntity:
        return ClienteEntity.from_model(record)
