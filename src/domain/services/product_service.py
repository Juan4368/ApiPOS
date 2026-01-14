from __future__ import annotations
from typing import List, Optional

from domain.dtos.productsDto import ProductRequest, ProductResponse
from domain.entities.productsEntity import ProductEntity
from domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class ProductService:
    """Caso de uso para operaciones de productos."""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, data: ProductRequest) -> ProductResponse:
        """Crea un producto usando el repositorio."""
        entity = ProductEntity(
            codigo_barras=data.codigo_barras,
            nombre=data.nombre,
            categoria_id=data.categoria_id,
            descripcion=data.descripcion,
            precio_venta=data.precio_venta,
            costo=data.costo,
            creado_por_id=data.creado_por_id,
            actualizado_por_id=data.actualizado_por_id,
            fecha_creacion=data.fecha_creacion,
            fecha_actualizacion=data.fecha_actualizacion,
            estado=data.estado,
        )
        created = self.repository.create_product(entity)
        return ProductResponse.model_validate(created)

    def list_products(self) -> List[ProductResponse]:
        productos = self.repository.list_products()
        return [ProductResponse.model_validate(prod) for prod in productos]

    def get_product(self, product_id: int) -> Optional[ProductResponse]:
        producto = self.repository.get_product(product_id)
        if not producto:
            return None
        return ProductResponse.model_validate(producto)

    def search_products(self, term: str) -> List[ProductResponse]:
        productos = self.repository.search_products(term)
        return [ProductResponse.model_validate(prod) for prod in productos]
