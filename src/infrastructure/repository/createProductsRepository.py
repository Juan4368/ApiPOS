from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.productsEntity import ProductEntity
from domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.infrastructure.models.models import Product


class ProductRepository(ProductRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con productos."""

    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_entity: ProductEntity) -> ProductEntity:
        """Crea un nuevo producto en la base de datos y devuelve la entidad."""
        fecha_creacion = product_entity.fecha_creacion or datetime.now(timezone.utc)
        fecha_actualizacion = product_entity.fecha_actualizacion or fecha_creacion
        product_orm = Product(
            producto_id=product_entity.producto_id,
            codigo_barras=product_entity.codigo_barras,
            nombre=product_entity.nombre,
            categoria_id=product_entity.categoria_id,
            descripcion=product_entity.descripcion,
            precio_venta=product_entity.precio_venta,
            costo=product_entity.costo,
            creado_por_id=product_entity.creado_por_id,
            actualizado_por_id=product_entity.actualizado_por_id,
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            estado=product_entity.estado,
        )

        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return ProductEntity.from_model(product_orm)

    def list_products(self) -> List[ProductEntity]:
        records = self.db.query(Product).all()
        return [ProductEntity.from_model(row) for row in records]

    def get_product(self, product_id: int) -> Optional[ProductEntity]:
        record = self.db.get(Product, product_id)
        if not record:
            return None
        return ProductEntity.from_model(record)

    def search_products(self, term: str) -> List[ProductEntity]:
        like_term = f"%{term}%"
        filters = [
            Product.nombre.ilike(like_term),
            Product.descripcion.ilike(like_term),
            Product.codigo_barras.ilike(like_term),
        ]

        try:
            price_value = Decimal(term)
            filters.append(Product.precio_venta == price_value)
            filters.append(Product.costo == price_value)
        except Exception:
            pass

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(Product.estado.is_(True))
        elif lowered in falsy:
            filters.append(Product.estado.is_(False))

        records = self.db.query(Product).filter(or_(*filters)).all()
        return [ProductEntity.from_model(row) for row in records]
