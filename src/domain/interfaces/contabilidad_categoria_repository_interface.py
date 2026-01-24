from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity


class ContabilidadCategoriaRepositoryInterface(ABC):
    @abstractmethod
    def create_categoria(
        self, entity: ContabilidadCategoriaEntity
    ) -> ContabilidadCategoriaEntity:
        raise NotImplementedError

    @abstractmethod
    def list_categorias(self) -> List[ContabilidadCategoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_categoria(self, categoria_id: int) -> Optional[ContabilidadCategoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_categoria(
        self, categoria_id: int, entity: ContabilidadCategoriaEntity
    ) -> Optional[ContabilidadCategoriaEntity]:
        raise NotImplementedError

