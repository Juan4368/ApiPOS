from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from domain.entities.categoryEntity import CategoryEntity


class CategoryRepositoryInterface(ABC):
    """Contrato para repositorios de categorias en el dominio."""

    @abstractmethod
    def create_category(self, category_entity: CategoryEntity) -> CategoryEntity:
        """Persiste una categoria y devuelve la entidad creada."""
        raise NotImplementedError

    @abstractmethod
    def list_categories(self) -> List[CategoryEntity]:
        """Devuelve todas las categorias."""
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id: int) -> Optional[CategoryEntity]:
        """Devuelve una categoria por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def search_categories(self, term: str) -> List[CategoryEntity]:
        """Busca categorias por nombre, descripcion o estado."""
        raise NotImplementedError

    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        """Elimina una categoria por ID y devuelve True si fue borrada."""
        raise NotImplementedError

    @abstractmethod
    def update_category_status(
        self,
        category_id: int,
        estado: bool,
        actualizado_por_id: Optional[int] = None,
        fecha_actualizacion: Optional[datetime] = None,
    ) -> Optional[CategoryEntity]:
        """Actualiza el estado de la categoria y devuelve la entidad actualizada."""
        raise NotImplementedError
