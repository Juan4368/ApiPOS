from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.proveedorEntity import ProveedorEntity


class ProveedorRepositoryInterface(ABC):
    @abstractmethod
    def create_proveedor(
        self, entity: ProveedorEntity, nombre_normalizado: Optional[str] = None
    ) -> ProveedorEntity:
        raise NotImplementedError

    @abstractmethod
    def get_proveedor(self, proveedor_id: int) -> Optional[ProveedorEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ProveedorEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_proveedores(self) -> List[ProveedorEntity]:
        raise NotImplementedError

    @abstractmethod
    def search_proveedores(self, term: str) -> List[ProveedorEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_proveedor(self, proveedor_id: int, entity: ProveedorEntity) -> Optional[ProveedorEntity]:
        raise NotImplementedError
