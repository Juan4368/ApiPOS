from __future__ import annotations

from typing import List, Optional

from domain.dtos.categoryDto import (
    CategoryRequest,
    CategoryResponse,
    CategoryStatusRequest,
)
from domain.entities.categoryEntity import CategoryEntity
from domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)
from domain.interfaces.ICategoryService import ICategoryService


class CategoryService(ICategoryService):
    """Caso de uso para operaciones de categorias."""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    def create_category(self, data: CategoryRequest) -> CategoryResponse:
        entity = CategoryEntity(
            nombre=data.nombre,
            descripcion=data.descripcion,
            estado=data.estado,
            creado_por_id=data.creado_por_id,
            actualizado_por_id=data.actualizado_por_id,
            fecha_creacion=data.fecha_creacion,
            fecha_actualizacion=data.fecha_actualizacion,
        )
        created = self.repository.create_category(entity)
        return CategoryResponse.model_validate(created)

    def list_categories(self) -> List[CategoryResponse]:
        categorias = self.repository.list_categories()
        return [CategoryResponse.model_validate(cat) for cat in categorias]

    def get_category(self, category_id: int) -> Optional[CategoryResponse]:
        categoria = self.repository.get_category(category_id)
        if not categoria:
            return None
        return CategoryResponse.model_validate(categoria)

    def search_categories(self, term: str) -> List[CategoryResponse]:
        categorias = self.repository.search_categories(term)
        return [CategoryResponse.model_validate(cat) for cat in categorias]

    def delete_category(self, category_id: int) -> bool:
        return self.repository.delete_category(category_id)

    def update_category_status(
        self, category_id: int, data: CategoryStatusRequest
    ) -> Optional[CategoryResponse]:
        updated = self.repository.update_category_status(
            category_id=category_id,
            estado=data.estado,
            actualizado_por_id=data.actualizado_por_id,
            fecha_actualizacion=data.fecha_actualizacion,
        )
        if not updated:
            return None
        return CategoryResponse.model_validate(updated)
