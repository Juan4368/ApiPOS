from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from domain.entities.ventaDetalleEntity import VentaDetalleEntity
from domain.entities.ventaEntity import VentaEntity
from domain.interfaces.venta_repository_interface import VentaRepositoryInterface
from src.infrastructure.models.models import Venta, VentaDetalle


class VentaRepository(VentaRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con ventas."""

    def __init__(self, db: Session):
        self.db = db

    def create_venta(
        self, venta_entity: VentaEntity, detalles: List[VentaDetalleEntity]
    ) -> VentaEntity:
        venta_orm = Venta(
            venta_id=venta_entity.venta_id,
            fecha=venta_entity.fecha,
            subtotal=venta_entity.subtotal,
            impuesto=venta_entity.impuesto,
            descuento=venta_entity.descuento,
            total=venta_entity.total,
            tipo_pago=venta_entity.tipo_pago,
            estado=venta_entity.estado,
            user_id=venta_entity.user_id,
        )
        self.db.add(venta_orm)
        self.db.flush()

        detalle_orms = [
            VentaDetalle(
                venta_id=venta_orm.venta_id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal,
            )
            for detalle in detalles
        ]
        if detalle_orms:
            self.db.add_all(detalle_orms)

        self.db.commit()
        self.db.refresh(venta_orm)
        venta_orm.detalles = detalle_orms
        return VentaEntity.from_model(venta_orm)

    def list_ventas(self) -> List[VentaEntity]:
        records = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles))
            .all()
        )
        return [VentaEntity.from_model(row) for row in records]

    def get_venta(self, venta_id: int) -> Optional[VentaEntity]:
        record = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles))
            .filter(Venta.venta_id == venta_id)
            .first()
        )
        if not record:
            return None
        return VentaEntity.from_model(record)

    def search_ventas(self, term: str) -> List[VentaEntity]:
        like_term = f"%{term}%"
        filters = [
            Venta.tipo_pago.ilike(like_term),
        ]

        try:
            value = Decimal(term)
            filters.append(Venta.total == value)
        except Exception:
            pass

        records = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles))
            .filter(or_(*filters))
            .all()
        )
        return [VentaEntity.from_model(row) for row in records]
