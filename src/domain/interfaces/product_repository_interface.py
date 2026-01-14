from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.productsEntity import ProductEntity


class ProductRepositoryInterface(ABC):
    """Contrato para repositorios de productos en el dominio."""

    @abstractmethod
    def create_product(self, product_entity: ProductEntity) -> ProductEntity:
        """Persiste un producto y devuelve la entidad creada."""
        raise NotImplementedError

    @abstractmethod
    def list_products(self) -> List[ProductEntity]:
        """Devuelve todos los productos."""
        raise NotImplementedError

    @abstractmethod
    def get_product(self, product_id: int) -> Optional[ProductEntity]:
        """Devuelve un producto por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def search_products(self, term: str) -> List[ProductEntity]:
        """Busca productos por nombre, descripcion, codigo_barras, precio_venta, costo o estado."""
        raise NotImplementedError
