from __future__ import annotations
from typing import List, Optional

from domain.dtos.productsDto import (
    ProductRequest,
    ProductResponse,
    ProductStatusUpdate,
)
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
            margen=data.margen,
            iva=data.iva,
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

    def update_product(
        self, product_id: int, data: ProductRequest
    ) -> Optional[ProductResponse]:
        entity = ProductEntity(
            codigo_barras=data.codigo_barras,
            nombre=data.nombre,
            categoria_id=data.categoria_id,
            descripcion=data.descripcion,
            precio_venta=data.precio_venta,
            costo=data.costo,
            margen=data.margen,
            iva=data.iva,
            creado_por_id=data.creado_por_id,
            actualizado_por_id=data.actualizado_por_id,
            fecha_creacion=data.fecha_creacion,
            fecha_actualizacion=data.fecha_actualizacion,
            estado=data.estado,
        )
        updated = self.repository.update_product(product_id, entity)
        if not updated:
            return None
        return ProductResponse.model_validate(updated)

    def update_product_status(
        self, product_id: int, data: ProductStatusUpdate
    ) -> Optional[ProductResponse]:
        updated = self.repository.update_product_status(
            product_id,
            data.estado,
            actualizado_por_id=data.actualizado_por_id,
            fecha_actualizacion=data.fecha_actualizacion,
        )
        if not updated:
            return None
        return ProductResponse.model_validate(updated)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete_product(product_id)

    def import_products(self, items: List[ProductRequest]) -> tuple[int, int]:
        entities = [
            ProductEntity(
                codigo_barras=item.codigo_barras,
                nombre=item.nombre,
                categoria_id=item.categoria_id,
                descripcion=item.descripcion,
                precio_venta=item.precio_venta,
                costo=item.costo,
                margen=item.margen,
                iva=item.iva,
                creado_por_id=item.creado_por_id,
                actualizado_por_id=item.actualizado_por_id,
                fecha_creacion=item.fecha_creacion,
                fecha_actualizacion=item.fecha_actualizacion,
                estado=item.estado,
            )
            for item in items
        ]
        return self.repository.import_products(entities)
