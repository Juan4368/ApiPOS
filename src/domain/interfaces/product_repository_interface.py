from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
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

    @abstractmethod
    def update_product(
        self, product_id: int, product_entity: ProductEntity
    ) -> Optional[ProductEntity]:
        """Actualiza un producto y devuelve la entidad o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def update_product_status(
        self,
        product_id: int,
        estado: bool,
        actualizado_por_id: Optional[int] = None,
        fecha_actualizacion: Optional[datetime] = None,
    ) -> Optional[ProductEntity]:
        """Actualiza el estado del producto y devuelve la entidad o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto y devuelve True si existia."""
        raise NotImplementedError

    @abstractmethod
    def import_products(self, products: List[ProductEntity]) -> tuple[int, int]:
        """Importa productos en lote y devuelve (creados, omitidos)."""
        raise NotImplementedError
