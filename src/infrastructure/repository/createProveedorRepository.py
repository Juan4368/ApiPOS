from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from domain.entities.proveedorEntity import ProveedorEntity
from domain.interfaces.proveedor_repository_interface import ProveedorRepositoryInterface
from src.infrastructure.models.models import Proveedor


class ProveedorRepository(ProveedorRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_proveedor(
        self, entity: ProveedorEntity, nombre_normalizado: Optional[str] = None
    ) -> ProveedorEntity:
        created_at = entity.created_at or datetime.now(timezone.utc)
        proveedor_orm = Proveedor(
            nombre=entity.nombre,
            telefono=entity.telefono,
            email=entity.email,
            created_at=created_at,
        )
        self.db.add(proveedor_orm)
        self.db.commit()
        self.db.refresh(proveedor_orm)
        return self._to_entity(proveedor_orm)

    def get_proveedor(self, proveedor_id: int) -> Optional[ProveedorEntity]:
        record = self.db.get(Proveedor, proveedor_id)
        if not record:
            return None
        return self._to_entity(record)

    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ProveedorEntity]:
        record = (
            self.db.query(Proveedor)
            .filter(func.lower(Proveedor.nombre) == nombre_normalizado)
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

    def list_proveedores(self) -> List[ProveedorEntity]:
        records = self.db.query(Proveedor).all()
        return [self._to_entity(row) for row in records]

    def search_proveedores(self, term: str) -> List[ProveedorEntity]:
        like_term = f"%{term}%"
        filters = [
            Proveedor.nombre.ilike(like_term),
            Proveedor.telefono.ilike(like_term),
            Proveedor.email.ilike(like_term),
        ]
        records = self.db.query(Proveedor).filter(or_(*filters)).all()
        return [self._to_entity(row) for row in records]

    def update_proveedor(
        self, proveedor_id: int, entity: ProveedorEntity
    ) -> Optional[ProveedorEntity]:
        record = self.db.get(Proveedor, proveedor_id)
        if not record:
            return None
        record.nombre = entity.nombre
        record.telefono = entity.telefono
        record.email = entity.email
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Proveedor) -> ProveedorEntity:
        return ProveedorEntity.from_model(record)
