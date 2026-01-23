from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from domain.dtos.ventaDto import VentaRequest, VentaResponse
from domain.entities.ventaDetalleEntity import VentaDetalleEntity
from domain.entities.ventaEntity import VentaEntity
from domain.interfaces.IVentaService import IVentaService
from domain.interfaces.venta_repository_interface import VentaRepositoryInterface


class VentaService(IVentaService):
    """Caso de uso para operaciones de ventas."""

    def __init__(self, repository: VentaRepositoryInterface):
        self.repository = repository

    def create_venta(self, data: VentaRequest) -> VentaResponse:
        subtotal = Decimal("0.00")
        detalles: list[VentaDetalleEntity] = []
        for item in data.detalles:
            item_subtotal = item.subtotal
            if item_subtotal is None:
                item_subtotal = Decimal(item.cantidad) * Decimal(item.precio_unitario)
            subtotal += item_subtotal
            detalles.append(
                VentaDetalleEntity(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item_subtotal,
                )
            )

        impuesto = Decimal(data.impuesto)
        descuento = Decimal(data.descuento)
        total = subtotal + impuesto - descuento
        fecha = data.fecha or datetime.now(timezone.utc)

        venta_entity = VentaEntity(
            fecha=fecha,
            subtotal=subtotal,
            impuesto=impuesto,
            descuento=descuento,
            total=total,
            tipo_pago=data.tipo_pago,
            estado=data.estado,
            nota_venta=data.nota_venta,
            cliente_id=data.cliente_id,
            user_id=data.user_id,
        )
        created = self.repository.create_venta(venta_entity, detalles)
        return VentaResponse.model_validate(created)

    def list_ventas(self) -> List[VentaResponse]:
        ventas = self.repository.list_ventas()
        return [VentaResponse.model_validate(venta) for venta in ventas]

    def get_venta(self, venta_id: int) -> Optional[VentaResponse]:
        venta = self.repository.get_venta(venta_id)
        if not venta:
            return None
        return VentaResponse.model_validate(venta)

    def search_ventas(self, term: str) -> List[VentaResponse]:
        ventas = self.repository.search_ventas(term)
        return [VentaResponse.model_validate(venta) for venta in ventas]
