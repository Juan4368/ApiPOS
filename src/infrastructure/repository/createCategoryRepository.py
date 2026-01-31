from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from domain.entities.categoryEntity import CategoryEntity
from domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.infrastructure.models.models import Categoria


class CategoryRepository(CategoryRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con categorias."""

    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category_entity: CategoryEntity) -> CategoryEntity:
        fecha_creacion = category_entity.fecha_creacion or datetime.now(timezone.utc)
        fecha_actualizacion = category_entity.fecha_actualizacion or fecha_creacion
        categoria_orm = Categoria(
            categoria_id=category_entity.categoria_id,
            nombre=category_entity.nombre,
            estado=category_entity.estado,
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            descripcion=category_entity.descripcion,
            creado_por_id=category_entity.creado_por_id,
            actualizado_por_id=category_entity.actualizado_por_id,
        )

        self.db.add(categoria_orm)
        self.db.commit()
        self.db.refresh(categoria_orm)
        return self._to_entity(categoria_orm)

    def list_categories(self) -> List[CategoryEntity]:
        records = (
            self.db.query(Categoria)
            .options(
                joinedload(Categoria.creado_por),
                joinedload(Categoria.actualizado_por),
            )
            .all()
        )
        return [self._to_entity(row) for row in records]

    def get_category(self, category_id: int) -> Optional[CategoryEntity]:
        record = (
            self.db.query(Categoria)
            .options(
                joinedload(Categoria.creado_por),
                joinedload(Categoria.actualizado_por),
            )
            .filter(Categoria.categoria_id == category_id)
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

    def search_categories(self, term: str) -> List[CategoryEntity]:
        like_term = f"%{term}%"
        filters = [
            Categoria.nombre.ilike(like_term),
            Categoria.descripcion.ilike(like_term),
        ]

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(Categoria.estado.is_(True))
        elif lowered in falsy:
            filters.append(Categoria.estado.is_(False))

        records = (
            self.db.query(Categoria)
            .options(
                joinedload(Categoria.creado_por),
                joinedload(Categoria.actualizado_por),
            )
            .filter(or_(*filters))
            .all()
        )
        return [self._to_entity(row) for row in records]

    def delete_category(self, category_id: int) -> bool:
        record = self.db.get(Categoria, category_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def update_category_status(
        self,
        category_id: int,
        estado: bool,
        actualizado_por_id: Optional[int] = None,
        fecha_actualizacion: Optional[datetime] = None,
    ) -> Optional[CategoryEntity]:
        record = self.db.get(Categoria, category_id)
        if not record:
            return None
        record.estado = estado
        if actualizado_por_id is not None:
            record.actualizado_por_id = actualizado_por_id
        record.fecha_actualizacion = fecha_actualizacion or datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Categoria) -> CategoryEntity:
        entity = CategoryEntity.from_model(record)
        entity.creado_por_nombre = (
            record.creado_por.username if record.creado_por else None
        )
        entity.actualizado_por_nombre = (
            record.actualizado_por.username if record.actualizado_por else None
        )
        return entity
