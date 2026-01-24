from __future__ import annotations

from typing import List, Optional

from domain.dtos.contabilidadCategoriaDto import (
    ContabilidadCategoriaRequest,
    ContabilidadCategoriaResponse,
    ContabilidadCategoriaUpdateRequest,
)
from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity
from domain.interfaces.contabilidad_categoria_repository_interface import (
    ContabilidadCategoriaRepositoryInterface,
)


class ContabilidadCategoriaService:
    def __init__(self, repository: ContabilidadCategoriaRepositoryInterface):
        self.repository = repository

    def create_categoria(
        self, data: ContabilidadCategoriaRequest
    ) -> ContabilidadCategoriaResponse:
        entity = ContabilidadCategoriaEntity(
            nombre=data.nombre,
            codigo=data.codigo,
        )
        created = self.repository.create_categoria(entity)
        return ContabilidadCategoriaResponse.model_validate(created)

    def list_categorias(self) -> List[ContabilidadCategoriaResponse]:
        categorias = self.repository.list_categorias()
        return [ContabilidadCategoriaResponse.model_validate(c) for c in categorias]

    def get_categoria(self, categoria_id: int) -> Optional[ContabilidadCategoriaResponse]:
        categoria = self.repository.get_categoria(categoria_id)
        if not categoria:
            return None
        return ContabilidadCategoriaResponse.model_validate(categoria)

    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaResponse]:
        categoria = self.repository.get_by_nombre(nombre)
        if not categoria:
            return None
        return ContabilidadCategoriaResponse.model_validate(categoria)

    def update_categoria(
        self, categoria_id: int, data: ContabilidadCategoriaRequest
    ) -> Optional[ContabilidadCategoriaResponse]:
        entity = ContabilidadCategoriaEntity(
            id=categoria_id,
            nombre=data.nombre,
            codigo=data.codigo,
        )
        updated = self.repository.update_categoria(categoria_id, entity)
        if not updated:
            return None
        return ContabilidadCategoriaResponse.model_validate(updated)

    def patch_categoria(
        self, categoria_id: int, data: ContabilidadCategoriaUpdateRequest
    ) -> Optional[ContabilidadCategoriaResponse]:
        current = self.repository.get_categoria(categoria_id)
        if not current:
            return None
        entity = ContabilidadCategoriaEntity(
            id=categoria_id,
            nombre=data.nombre if data.nombre is not None else current.nombre,
            codigo=data.codigo if data.codigo is not None else current.codigo,
        )
        updated = self.repository.update_categoria(categoria_id, entity)
        if not updated:
            return None
        return ContabilidadCategoriaResponse.model_validate(updated)

