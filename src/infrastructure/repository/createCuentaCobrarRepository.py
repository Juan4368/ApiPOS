from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from domain.entities.abonoCuentaEntity import AbonoCuentaEntity
from domain.entities.cuentaCobrarEntity import CuentaCobrarEntity
from domain.enums.contabilidadEnums import CreditoEstado
from domain.interfaces.cuenta_cobrar_repository_interface import (
    CuentaCobrarRepositoryInterface,
)
from src.infrastructure.models.models import AbonoCuenta, CuentaCobrar, MovimientoFinanciero, Venta, VentaDetalle
from domain.entities.ventaDetalleEntity import VentaDetalleEntity


class CuentaCobrarRepository(CuentaCobrarRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_cuenta(self, entity: CuentaCobrarEntity) -> CuentaCobrarEntity:
        created_at = entity.created_at or datetime.now(timezone.utc)
        cuenta_orm = CuentaCobrar(
            venta_id=entity.venta_id,
            cliente_id=entity.cliente_id,
            total=entity.total,
            saldo=entity.saldo,
            estado=self._to_estado(entity.estado),
            created_at=created_at,
        )
        self.db.add(cuenta_orm)
        self.db.commit()
        self.db.refresh(cuenta_orm)
        return self._to_entity(cuenta_orm)

    def get_cuenta(self, cuenta_id: int) -> Optional[CuentaCobrarEntity]:
        record = (
            self.db.query(CuentaCobrar)
            .options(
                selectinload(CuentaCobrar.cliente),
                selectinload(CuentaCobrar.venta)
                .selectinload(Venta.detalles)
                .selectinload(VentaDetalle.producto),
            )
            .filter(CuentaCobrar.id == cuenta_id)
            .first()
        )
        if not record:
            return None
        return self._to_entity(record)

    def list_cuentas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        venta_id: Optional[int] = None,
        estado: Optional[CreditoEstado] = None,
    ) -> List[CuentaCobrarEntity]:
        query = self.db.query(CuentaCobrar)
        query = query.options(
            selectinload(CuentaCobrar.cliente),
            selectinload(CuentaCobrar.venta)
            .selectinload(Venta.detalles)
            .selectinload(VentaDetalle.producto),
        )
        if cliente_id is not None:
            query = query.filter(CuentaCobrar.cliente_id == cliente_id)
        if venta_id is not None:
            query = query.filter(CuentaCobrar.venta_id == venta_id)
        if estado is not None:
            query = query.filter(CuentaCobrar.estado == self._to_estado(estado))
        records = query.order_by(CuentaCobrar.created_at.desc()).all()
        return [self._to_entity(row) for row in records]

    def update_cuenta(
        self, cuenta_id: int, entity: CuentaCobrarEntity
    ) -> Optional[CuentaCobrarEntity]:
        record = self.db.get(CuentaCobrar, cuenta_id)
        if not record:
            return None
        record.venta_id = entity.venta_id
        record.cliente_id = entity.cliente_id
        record.total = entity.total
        record.saldo = entity.saldo
        record.estado = self._to_estado(entity.estado)
        record.updated_at = entity.updated_at or datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def create_abono(
        self, cuenta_id: int, abono: AbonoCuentaEntity
    ) -> Optional[AbonoCuentaEntity]:
        cuenta = self.db.get(CuentaCobrar, cuenta_id)
        if not cuenta:
            return None
        if cuenta.estado == CreditoEstado.ANULADO.value:
            raise ValueError("La cuenta esta anulada")
        if abono.caja_id is None:
            raise ValueError("caja_id es obligatorio para el abono")
        if abono.monto <= Decimal("0.00"):
            raise ValueError("El monto debe ser positivo")
        if cuenta.saldo <= Decimal("0.00"):
            raise ValueError("La cuenta ya esta pagada")
        if abono.monto > cuenta.saldo:
            raise ValueError("El abono no puede superar el saldo")

        concepto = abono.concepto or "Abono a credito"
        movimiento = MovimientoFinanciero(
            fecha=abono.fecha,
            tipo="INGRESO",
            monto=abono.monto,
            concepto=concepto,
            caja_id=abono.caja_id,
            usuario_id=abono.usuario_id,
            venta_id=abono.venta_id or cuenta.venta_id,
        )
        self.db.add(movimiento)
        self.db.flush()

        abono_orm = AbonoCuenta(
            cuenta_id=cuenta_id,
            movimiento_id=movimiento.id,
            monto=abono.monto,
            fecha=abono.fecha,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(abono_orm)

        cuenta.saldo = cuenta.saldo - abono.monto
        cuenta.estado = self._to_estado(self._calcular_estado(cuenta.total, cuenta.saldo))
        cuenta.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(abono_orm)
        return self._to_abono_entity(abono_orm)

    def list_abonos(self, cuenta_id: int) -> List[AbonoCuentaEntity]:
        records = (
            self.db.query(AbonoCuenta)
            .filter(AbonoCuenta.cuenta_id == cuenta_id)
            .order_by(AbonoCuenta.fecha.desc())
            .all()
        )
        return [self._to_abono_entity(row) for row in records]

    def _to_entity(self, record: CuentaCobrar) -> CuentaCobrarEntity:
        venta_detalles = None
        if record.venta and record.venta.detalles:
            venta_detalles = []
            for detalle in record.venta.detalles:
                venta_detalles.append(
                    VentaDetalleEntity(
                        venta_detalle_id=detalle.venta_detalle_id,
                        venta_id=detalle.venta_id,
                        producto_id=detalle.producto_id,
                        producto_nombre=detalle.producto.nombre if detalle.producto else None,
                        cantidad=detalle.cantidad,
                        precio_unitario=detalle.precio_unitario,
                        subtotal=detalle.subtotal,
                    )
                )
        return CuentaCobrarEntity(
            id=record.id,
            venta_id=record.venta_id,
            cliente_id=record.cliente_id,
            total=record.total,
            saldo=record.saldo,
            estado=CreditoEstado(record.estado),
            created_at=record.created_at,
            updated_at=record.updated_at,
            cliente_nombre=record.cliente.nombre if record.cliente else None,
            numero_factura=record.venta.numero_factura if record.venta else None,
            venta_detalles=venta_detalles,
        )

    def _to_abono_entity(self, record: AbonoCuenta) -> AbonoCuentaEntity:
        return AbonoCuentaEntity(
            id=record.id,
            cuenta_id=record.cuenta_id,
            movimiento_id=record.movimiento_id,
            monto=record.monto,
            fecha=record.fecha,
            created_at=record.created_at,
        )

    def _to_estado(self, estado: CreditoEstado) -> str:
        if isinstance(estado, CreditoEstado):
            return estado.value
        return str(estado)

    def _calcular_estado(self, total: Decimal, saldo: Decimal) -> CreditoEstado:
        if saldo <= Decimal("0.00"):
            return CreditoEstado.PAGADO
        if saldo < total:
            return CreditoEstado.PARCIAL
        return CreditoEstado.PENDIENTE
