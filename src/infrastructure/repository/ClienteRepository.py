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
            descuento_pesos=entity.descuento_pesos,
            descuento_porcentaje=entity.descuento_porcentaje,
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

    def update_cliente(
        self,
        cliente_id: UUID,
        nombre: Optional[str] = None,
        nombre_normalizado: Optional[str] = None,
        telefono: Optional[str] = None,
        email: Optional[str] = None,
        descuento_pesos: Optional[float] = None,
        descuento_porcentaje: Optional[float] = None,
    ) -> Optional[ClienteEntity]:
        record = self.db.get(Cliente, cliente_id)
        if not record:
            return None

        if nombre is not None:
            record.nombre = nombre
        if nombre_normalizado is not None:
            record.nombre_normalizado = nombre_normalizado
        if telefono is not None:
            record.telefono = telefono
        if email is not None:
            record.email = email
        if descuento_pesos is not None:
            record.descuento_pesos = descuento_pesos
        if descuento_porcentaje is not None:
            record.descuento_porcentaje = descuento_porcentaje

        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Cliente) -> ClienteEntity:
        return ClienteEntity.from_model(record)
