from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from datetime import date
from typing import List, Optional

from domain.dtos.ventaDto import (
    VentaRequest,
    VentaResponse,
    VentaDetallesUpdateRequest,
    VentaResumenResponse,
    VentaStatusRequest,
    VentaUpdateRequest,
    VentaDetalleRequest,
)
from domain.entities.ventaDetalleEntity import VentaDetalleEntity
from domain.entities.ventaEntity import VentaEntity
from domain.interfaces.IVentaService import IVentaService
from domain.interfaces.venta_repository_interface import VentaRepositoryInterface


class VentaService(IVentaService):
    """Caso de uso para operaciones de ventas."""

    def __init__(self, repository: VentaRepositoryInterface):
        self.repository = repository

    def _build_detalles(
        self, items: list[VentaDetalleEntity]
    ) -> tuple[Decimal, list[VentaDetalleEntity]]:
        subtotal = Decimal("0.00")
        detalles: list[VentaDetalleEntity] = []
        for item in items:
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
        return subtotal, detalles

    def _validate_stock(self, detalles: list[VentaDetalleEntity]) -> None:
        # Stock temporalmente aislado.
        return

    def _validate_stock_deltas(self, deltas: dict[int, int]) -> None:
        # Stock temporalmente aislado.
        return

    def _recalcular_impuesto_descuento(
        self,
        *,
        subtotal_actual: Decimal,
        impuesto_actual: Decimal,
        descuento_actual: Decimal,
        subtotal_nuevo: Decimal,
    ) -> tuple[Decimal, Decimal]:
        if subtotal_actual > Decimal("0.00"):
            impuesto_rate = impuesto_actual / subtotal_actual
            descuento_rate = descuento_actual / subtotal_actual
        else:
            impuesto_rate = Decimal("0.00")
            descuento_rate = Decimal("0.00")
        impuesto_nuevo = subtotal_nuevo * impuesto_rate
        descuento_nuevo = subtotal_nuevo * descuento_rate
        return impuesto_nuevo, descuento_nuevo

    def create_venta(self, data: VentaRequest) -> VentaResponse:
        es_credito = data.es_credito
        if data.tipo_pago is None:
            es_credito = True
        if not es_credito and not data.tipo_pago:
            raise ValueError("tipo_pago es obligatorio cuando no es credito")
        subtotal, detalles = self._build_detalles(
            [
                VentaDetalleEntity(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal,
                )
                for item in data.detalles
            ]
        )
        self._validate_stock(detalles)
        stock_deltas = None

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
            es_credito=es_credito,
            estado=data.estado,
            nota_venta=data.nota_venta,
            numero_factura=data.numero_factura,
            cliente_id=data.cliente_id,
            user_id=data.user_id,
        )
        created = self.repository.create_venta(venta_entity, detalles, stock_deltas)
        return VentaResponse.model_validate(created)

    def list_ventas(self) -> List[VentaResponse]:
        ventas = self.repository.list_ventas()
        return [VentaResponse.model_validate(venta) for venta in ventas]

    def list_ventas_resumen(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[VentaResumenResponse]:
        return self.repository.list_ventas_resumen(desde=desde, hasta=hasta)

    def get_venta(self, venta_id: int) -> Optional[VentaResponse]:
        venta = self.repository.get_venta(venta_id)
        if not venta:
            return None
        return VentaResponse.model_validate(venta)

    def search_ventas(self, term: str) -> List[VentaResponse]:
        ventas = self.repository.search_ventas(term)
        return [VentaResponse.model_validate(venta) for venta in ventas]

    def update_venta_status(
        self, venta_id: int, data: VentaStatusRequest
    ) -> Optional[VentaResponse]:
        updated = self.repository.update_venta_status(venta_id, data.estado)
        if not updated:
            return None
        return VentaResponse.model_validate(updated)

    def update_venta(
        self, venta_id: int, data: VentaUpdateRequest
    ) -> Optional[VentaResponse]:
        current = self.repository.get_venta(venta_id)
        if not current:
            return None

        detalles_entities: Optional[list[VentaDetalleEntity]] = None
        stock_deltas: Optional[dict[int, int]] = None
        if data.detalles is not None:
            subtotal, detalles_entities = self._build_detalles(
                [
                    VentaDetalleEntity(
                        producto_id=item.producto_id,
                        cantidad=item.cantidad,
                        precio_unitario=item.precio_unitario,
                        subtotal=item.subtotal,
                    )
                    for item in data.detalles
                ]
            )
            old_qtys: dict[int, int] = {}
            for detalle in current.detalles or []:
                old_qtys[detalle.producto_id] = old_qtys.get(detalle.producto_id, 0) + detalle.cantidad
            new_qtys: dict[int, int] = {}
            for detalle in detalles_entities:
                new_qtys[detalle.producto_id] = new_qtys.get(detalle.producto_id, 0) + detalle.cantidad
            stock_deltas = {}
            for producto_id in set(old_qtys) | set(new_qtys):
                stock_deltas[producto_id] = old_qtys.get(producto_id, 0) - new_qtys.get(producto_id, 0)
            self._validate_stock_deltas(stock_deltas)
        else:
            subtotal = current.subtotal

        impuesto = data.impuesto if data.impuesto is not None else current.impuesto
        descuento = data.descuento if data.descuento is not None else current.descuento
        total = subtotal + Decimal(impuesto) - Decimal(descuento)
        if "es_credito" in data.model_fields_set:
            es_credito = data.es_credito
        else:
            es_credito = current.es_credito
        if "tipo_pago" in data.model_fields_set:
            tipo_pago = data.tipo_pago
        else:
            tipo_pago = current.tipo_pago
        if tipo_pago is None:
            es_credito = True
        if not es_credito and not tipo_pago:
            raise ValueError("tipo_pago es obligatorio cuando no es credito")

        venta_entity = VentaEntity(
            venta_id=venta_id,
            fecha=data.fecha or current.fecha,
            subtotal=subtotal,
            impuesto=Decimal(impuesto),
            descuento=Decimal(descuento),
            total=total,
            tipo_pago=tipo_pago,
            es_credito=es_credito,
            estado=data.estado if data.estado is not None else current.estado,
            nota_venta=data.nota_venta if data.nota_venta is not None else current.nota_venta,
            numero_factura=(
                data.numero_factura
                if data.numero_factura is not None
                else current.numero_factura
            ),
            cliente_id=data.cliente_id if data.cliente_id is not None else current.cliente_id,
            user_id=data.user_id if data.user_id is not None else current.user_id,
        )
        updated = self.repository.update_venta(
            venta_entity, detalles_entities, stock_deltas
        )
        if not updated:
            return None
        return VentaResponse.model_validate(updated)

    def update_venta_detalles(
        self, venta_id: int, data: VentaDetallesUpdateRequest
    ) -> Optional[VentaResponse]:
        current = self.repository.get_venta(venta_id)
        if not current:
            return None
        subtotal_nuevo, detalles_entities = self._build_detalles(
            [
                VentaDetalleEntity(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal,
                )
                for item in data.detalles
            ]
        )
        self._validate_stock(detalles_entities)
        impuesto_nuevo, descuento_nuevo = self._recalcular_impuesto_descuento(
            subtotal_actual=Decimal(current.subtotal),
            impuesto_actual=Decimal(current.impuesto),
            descuento_actual=Decimal(current.descuento),
            subtotal_nuevo=subtotal_nuevo,
        )
        return self.update_venta(
            venta_id,
            VentaUpdateRequest(
                detalles=data.detalles,
                impuesto=impuesto_nuevo,
                descuento=descuento_nuevo,
            ),
        )

    def delete_venta_detalle(
        self, venta_id: int, producto_id: int
    ) -> Optional[VentaResponse]:
        current = self.repository.get_venta(venta_id)
        if not current:
            return None
        detalles_actuales = current.detalles or []
        detalles_filtrados = [
            detalle for detalle in detalles_actuales if detalle.producto_id != producto_id
        ]
        if len(detalles_filtrados) == len(detalles_actuales):
            return current
        detalles_request = [
            VentaDetalleRequest(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal,
            )
            for detalle in detalles_filtrados
        ]
        return self.update_venta_detalles(
            venta_id, VentaDetallesUpdateRequest(detalles=detalles_request)
        )
