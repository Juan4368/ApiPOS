from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity
from domain.enums.contabilidadEnums import CategoriaTipo
from domain.interfaces.contabilidad_categoria_repository_interface import (
    ContabilidadCategoriaRepositoryInterface,
)
from src.infrastructure.models.models import CategoriaContabilidad


class ContabilidadCategoriaRepository(ContabilidadCategoriaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_categoria(
        self, entity: ContabilidadCategoriaEntity
    ) -> ContabilidadCategoriaEntity:
        categoria_orm = CategoriaContabilidad(
            nombre=entity.nombre,
            tipo_categoria=self._to_tipo_categoria(entity.tipo_categoria),
        )
        self.db.add(categoria_orm)
        self.db.commit()
        self.db.refresh(categoria_orm)
        return ContabilidadCategoriaEntity.from_model(categoria_orm)

    def list_categorias(self) -> List[ContabilidadCategoriaEntity]:
        records = self.db.query(CategoriaContabilidad).order_by(CategoriaContabilidad.id).all()
        return [ContabilidadCategoriaEntity.from_model(record) for record in records]

    def get_categoria(self, categoria_id: int) -> Optional[ContabilidadCategoriaEntity]:
        record = self.db.get(CategoriaContabilidad, categoria_id)
        if not record:
            return None
        return ContabilidadCategoriaEntity.from_model(record)

    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaEntity]:
        record = (
            self.db.query(CategoriaContabilidad)
            .filter(CategoriaContabilidad.nombre.ilike(nombre))
            .first()
        )
        if not record:
            return None
        return ContabilidadCategoriaEntity.from_model(record)

    def update_categoria(
        self, categoria_id: int, entity: ContabilidadCategoriaEntity
    ) -> Optional[ContabilidadCategoriaEntity]:
        record = self.db.get(CategoriaContabilidad, categoria_id)
        if not record:
            return None
        record.nombre = entity.nombre
        record.tipo_categoria = self._to_tipo_categoria(entity.tipo_categoria)
        self.db.commit()
        self.db.refresh(record)
        return ContabilidadCategoriaEntity.from_model(record)

    def _to_tipo_categoria(self, tipo: CategoriaTipo) -> str:
        if isinstance(tipo, CategoriaTipo):
            return tipo.value
        return str(tipo)
