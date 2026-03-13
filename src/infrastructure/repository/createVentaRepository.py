from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import or_, text
from sqlalchemy.orm import Session, selectinload

from domain.entities.ventaDetalleEntity import VentaDetalleEntity
from domain.entities.ventaEntity import VentaEntity
from domain.dtos.ventaDto import VentaResumenResponse
from domain.interfaces.venta_repository_interface import VentaRepositoryInterface
from src.infrastructure.models.models import (
    Cliente,
    CuentaCobrar,
    MovimientoFinanciero,
    Stock,
    User,
    Venta,
    VentaDetalle,
)
from utils.timezone import end_of_day, now_utc_minus_5, start_of_day


class VentaRepository(VentaRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con ventas."""

    def __init__(self, db: Session):
        self.db = db

    def create_venta(
        self,
        venta_entity: VentaEntity,
        detalles: List[VentaDetalleEntity],
        stock_deltas: Optional[dict[int, int]] = None,
    ) -> VentaEntity:
        numero_factura = venta_entity.numero_factura
        if not numero_factura:
            self.db.execute(text("CREATE SEQUENCE IF NOT EXISTS venta_numero_factura_seq"))
            next_value = self.db.execute(
                text("SELECT nextval('venta_numero_factura_seq')")
            ).scalar_one()
            numero_factura = f"POS-{int(next_value):06d}"
        venta_orm = Venta(
            venta_id=venta_entity.venta_id,
            fecha=venta_entity.fecha,
            subtotal=venta_entity.subtotal,
            impuesto=venta_entity.impuesto,
            descuento=venta_entity.descuento,
            total=venta_entity.total,
            tipo_pago=venta_entity.tipo_pago,
            es_credito=venta_entity.es_credito,
            estado=venta_entity.estado,
            nota_venta=venta_entity.nota_venta,
            numero_factura=numero_factura,
            cliente_id=venta_entity.cliente_id,
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
                descuento=detalle.descuento,
                subtotal=detalle.subtotal,
            )
            for detalle in detalles
        ]
        if detalle_orms:
            self.db.add_all(detalle_orms)

        if venta_entity.es_credito:
            existing = (
                self.db.query(CuentaCobrar)
                .filter(CuentaCobrar.venta_id == venta_orm.venta_id)
                .first()
            )
            if not existing:
                cuenta = CuentaCobrar(
                    venta_id=venta_orm.venta_id,
                    cliente_id=venta_orm.cliente_id,
                    total=venta_orm.total,
                    saldo=venta_orm.total,
                    estado="PENDIENTE",
                )
                self.db.add(cuenta)

        self._apply_stock_deltas(stock_deltas or {})
        self.db.commit()
        self.db.refresh(venta_orm)
        venta_orm.detalles = detalle_orms
        return VentaEntity.from_model(venta_orm)

    def list_ventas(self) -> List[VentaEntity]:
        records = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles).selectinload(VentaDetalle.producto))
            .all()
        )
        return [VentaEntity.from_model(row) for row in records]

    def list_ventas_resumen(
        self,
        *,
        desde: Optional[date] = None,
        hasta: Optional[date] = None,
    ) -> List[VentaResumenResponse]:
        query = (
            self.db.query(
                Venta.fecha,
                Venta.numero_factura,
                Cliente.nombre.label("cliente_nombre"),
                Venta.subtotal,
                Venta.descuento,
                Venta.total,
                Venta.estado,
                Venta.tipo_pago,
                Venta.es_credito,
                Venta.nota_venta,
                User.username.label("usuario_nombre"),
            )
            .outerjoin(Cliente, Venta.cliente_id == Cliente.id)
            .outerjoin(User, Venta.user_id == User.user_id)
        )
        if desde:
            query = query.filter(Venta.fecha >= start_of_day(desde))
        if hasta:
            query = query.filter(Venta.fecha <= end_of_day(hasta))
        records = query.order_by(Venta.fecha.desc()).all()
        return [
            VentaResumenResponse.model_validate(dict(row._mapping)) for row in records
        ]

    def get_stock_cantidades(self, producto_ids: list[int]) -> dict[int, int]:
        if not producto_ids:
            return {}
        records = (
            self.db.query(Stock.producto_id, Stock.cantidad_actual)
            .filter(Stock.producto_id.in_(producto_ids))
            .all()
        )
        return {int(row.producto_id): int(row.cantidad_actual) for row in records}

    def get_venta(self, venta_id: int) -> Optional[VentaEntity]:
        record = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles).selectinload(VentaDetalle.producto))
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
            .options(selectinload(Venta.detalles).selectinload(VentaDetalle.producto))
            .filter(or_(*filters))
            .all()
        )
        return [VentaEntity.from_model(row) for row in records]

    def update_venta_status(self, venta_id: int, estado: bool) -> Optional[VentaEntity]:
        record = self.db.get(Venta, venta_id)
        if not record:
            return None
        record.estado = estado
        self.db.commit()
        self.db.refresh(record)
        return VentaEntity.from_model(record)

    def anular_venta(
        self,
        venta_id: int,
        *,
        motivo: Optional[str] = None,
        stock_deltas: Optional[dict[int, int]] = None,
    ) -> Optional[VentaEntity]:
        record = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles).selectinload(VentaDetalle.producto))
            .filter(Venta.venta_id == venta_id)
            .first()
        )
        if not record:
            return None

        if not bool(record.estado):
            return VentaEntity.from_model(record)

        motivo_texto = (motivo or "").strip()
        nota_anulacion = f"[ANULADA] Venta anulada. Motivo: {motivo_texto or 'sin motivo'}"
        if record.nota_venta:
            record.nota_venta = f"{record.nota_venta} | {nota_anulacion}"
        else:
            record.nota_venta = nota_anulacion
        record.estado = False

        cuenta = (
            self.db.query(CuentaCobrar)
            .filter(CuentaCobrar.venta_id == record.venta_id)
            .order_by(CuentaCobrar.id.desc())
            .first()
        )
        if cuenta is not None:
            cuenta.estado = "ANULADO"
            cuenta.saldo = Decimal("0.00")
            cuenta.updated_at = now_utc_minus_5()

        movimientos = (
            self.db.query(MovimientoFinanciero)
            .filter(MovimientoFinanciero.venta_id == record.venta_id)
            .all()
        )
        for mov in movimientos:
            tipo_reverso = "EGRESO" if mov.tipo == "INGRESO" else "INGRESO"
            self.db.add(
                MovimientoFinanciero(
                    fecha=now_utc_minus_5(),
                    tipo=tipo_reverso,
                    monto=mov.monto,
                    concepto=f"ANULACION VENTA #{record.venta_id}",
                    nota=f"Reverso movimiento #{mov.id}. {motivo_texto}".strip(),
                    proveedor_id=None,
                    caja_id=mov.caja_id,
                    usuario_id=mov.usuario_id,
                    venta_id=record.venta_id,
                )
            )

        self._apply_stock_deltas(stock_deltas or {})
        self.db.commit()
        self.db.refresh(record)
        return VentaEntity.from_model(record)

    def update_venta(
        self,
        venta_entity: VentaEntity,
        detalles: Optional[List[VentaDetalleEntity]] = None,
        stock_deltas: Optional[dict[int, int]] = None,
    ) -> Optional[VentaEntity]:
        record = (
            self.db.query(Venta)
            .options(selectinload(Venta.detalles).selectinload(VentaDetalle.producto))
            .filter(Venta.venta_id == venta_entity.venta_id)
            .first()
        )
        if not record:
            return None

        record.fecha = venta_entity.fecha
        record.subtotal = venta_entity.subtotal
        record.impuesto = venta_entity.impuesto
        record.descuento = venta_entity.descuento
        record.total = venta_entity.total
        record.tipo_pago = venta_entity.tipo_pago
        record.es_credito = venta_entity.es_credito
        record.estado = venta_entity.estado
        record.nota_venta = venta_entity.nota_venta
        record.numero_factura = venta_entity.numero_factura
        record.cliente_id = venta_entity.cliente_id
        record.user_id = venta_entity.user_id

        tipo_pago = (record.tipo_pago or "").strip().lower()
        should_be_credito = bool(record.es_credito) or tipo_pago == "credito"
        if should_be_credito:
            cuentas_activas = (
                self.db.query(CuentaCobrar)
                .filter(
                    CuentaCobrar.venta_id == record.venta_id,
                    CuentaCobrar.estado != "ANULADO",
                )
                .all()
            )
            if not cuentas_activas:
                cuenta = CuentaCobrar(
                    venta_id=record.venta_id,
                    cliente_id=record.cliente_id,
                    total=record.total,
                    saldo=record.total,
                    estado="PENDIENTE",
                )
                self.db.add(cuenta)
            else:
                for cuenta in cuentas_activas:
                    cuenta.cliente_id = record.cliente_id
                    cuenta.updated_at = now_utc_minus_5()
        else:
            cuentas = (
                self.db.query(CuentaCobrar)
                .filter(
                    CuentaCobrar.venta_id == record.venta_id,
                    CuentaCobrar.estado != "ANULADO",
                )
                .all()
            )
            for cuenta in cuentas:
                cuenta.estado = "ANULADO"
                cuenta.saldo = Decimal("0.00")
                cuenta.updated_at = now_utc_minus_5()

        detalle_orms: list[VentaDetalle] = []
        if detalles is not None:
            self.db.query(VentaDetalle).filter(
                VentaDetalle.venta_id == record.venta_id
            ).delete(synchronize_session=False)
            detalle_orms = [
                VentaDetalle(
                    venta_id=record.venta_id,
                    producto_id=detalle.producto_id,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                    descuento=detalle.descuento,
                    subtotal=detalle.subtotal,
                )
                for detalle in detalles
            ]
            if detalle_orms:
                self.db.add_all(detalle_orms)

        self._apply_stock_deltas(stock_deltas or {})
        self.db.commit()
        self.db.refresh(record)
        if detalles is not None:
            record.detalles = detalle_orms
        return VentaEntity.from_model(record)

    def _apply_stock_deltas(self, deltas: dict[int, int]) -> None:
        # Deshabilitado temporalmente: no validar ni ajustar stock.
        return
        if not deltas:
            return
        now = now_utc_minus_5()
        for producto_id, delta in deltas.items():
            if delta == 0:
                continue
            record = (
                self.db.query(Stock)
                .filter(Stock.producto_id == producto_id)
                .with_for_update()
                .first()
            )
            if not record:
                raise ValueError(f"Stock no encontrado para producto {producto_id}")
            nueva_cantidad = int(record.cantidad_actual) + int(delta)
            if nueva_cantidad < 0:
                raise ValueError(
                    f"Stock insuficiente para producto {producto_id} "
                    f"(disponible {record.cantidad_actual}, ajuste {delta})"
                )
            record.cantidad_actual = nueva_cantidad
            record.ultima_actualizacion = now
