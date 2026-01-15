from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

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
            margen=product_entity.margen,
            creado_por_id=product_entity.creado_por_id,
            actualizado_por_id=product_entity.actualizado_por_id,
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            estado=product_entity.estado,
        )

        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return self._to_entity(product_orm)

    def list_products(self) -> List[ProductEntity]:
        records = (
            self.db.query(Product)
            .options(
                joinedload(Product.categoria),
                joinedload(Product.creado_por),
                joinedload(Product.actualizado_por),
            )
            .all()
        )
        return [self._to_entity(row) for row in records]

    def get_product(self, product_id: int) -> Optional[ProductEntity]:
        record = (
            self.db.query(Product)
            .options(
                joinedload(Product.categoria),
                joinedload(Product.creado_por),
                joinedload(Product.actualizado_por),
            )
            .filter(Product.producto_id == product_id)
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

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

        records = (
            self.db.query(Product)
            .options(
                joinedload(Product.categoria),
                joinedload(Product.creado_por),
                joinedload(Product.actualizado_por),
            )
            .filter(or_(*filters))
            .all()
        )
        return [self._to_entity(row) for row in records]

    def update_product(
        self, product_id: int, product_entity: ProductEntity
    ) -> Optional[ProductEntity]:
        record = (
            self.db.query(Product)
            .options(
                joinedload(Product.categoria),
                joinedload(Product.creado_por),
                joinedload(Product.actualizado_por),
            )
            .filter(Product.producto_id == product_id)
            .first()
        )
        if not record:
            return None

        record.codigo_barras = product_entity.codigo_barras
        record.nombre = product_entity.nombre
        record.categoria_id = product_entity.categoria_id
        record.descripcion = product_entity.descripcion
        record.precio_venta = product_entity.precio_venta
        record.costo = product_entity.costo
        record.margen = product_entity.margen
        record.estado = product_entity.estado
        record.creado_por_id = product_entity.creado_por_id
        record.actualizado_por_id = product_entity.actualizado_por_id
        if product_entity.fecha_creacion is not None:
            record.fecha_creacion = product_entity.fecha_creacion
        record.fecha_actualizacion = (
            product_entity.fecha_actualizacion or datetime.now(timezone.utc)
        )

        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def update_product_status(
        self,
        product_id: int,
        estado: bool,
        actualizado_por_id: Optional[int] = None,
        fecha_actualizacion: Optional[datetime] = None,
    ) -> Optional[ProductEntity]:
        record = (
            self.db.query(Product)
            .options(
                joinedload(Product.categoria),
                joinedload(Product.creado_por),
                joinedload(Product.actualizado_por),
            )
            .filter(Product.producto_id == product_id)
            .first()
        )
        if not record:
            return None

        record.estado = estado
        if actualizado_por_id is not None:
            record.actualizado_por_id = actualizado_por_id
        record.fecha_actualizacion = fecha_actualizacion or datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def import_products(self, products: List[ProductEntity]) -> tuple[int, int]:
        if not products:
            return 0, 0

        codes = [p.codigo_barras for p in products if p.codigo_barras]
        existing_codes = set()
        if codes:
            rows = (
                self.db.query(Product.codigo_barras)
                .filter(Product.codigo_barras.in_(codes))
                .all()
            )
            existing_codes = {row[0] for row in rows}

        seen = set()
        created = 0
        skipped = 0
        for entity in products:
            code = entity.codigo_barras
            if code and (code in existing_codes or code in seen):
                skipped += 1
                continue
            if code:
                seen.add(code)

            fecha_creacion = entity.fecha_creacion or datetime.now(timezone.utc)
            fecha_actualizacion = entity.fecha_actualizacion or fecha_creacion
            product_orm = Product(
                producto_id=entity.producto_id,
                codigo_barras=entity.codigo_barras,
                nombre=entity.nombre,
                categoria_id=entity.categoria_id,
                descripcion=entity.descripcion,
                precio_venta=entity.precio_venta,
                costo=entity.costo,
                margen=entity.margen,
                creado_por_id=entity.creado_por_id,
                actualizado_por_id=entity.actualizado_por_id,
                fecha_creacion=fecha_creacion,
                fecha_actualizacion=fecha_actualizacion,
                estado=entity.estado,
            )
            self.db.add(product_orm)
            created += 1

        if created:
            self.db.commit()
        return created, skipped

    def _to_entity(self, record: Product) -> ProductEntity:
        entity = ProductEntity.from_model(record)
        entity.categoria_nombre = (
            record.categoria.nombre if record.categoria else None
        )
        entity.creado_por_nombre = (
            record.creado_por.nombre_completo if record.creado_por else None
        )
        entity.actualizado_por_nombre = (
            record.actualizado_por.nombre_completo if record.actualizado_por else None
        )
        return entity
