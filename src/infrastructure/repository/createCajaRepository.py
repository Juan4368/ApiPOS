from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from domain.entities.cajaEntity import CajaEntity
from domain.enums.contabilidadEnums import CajaEstado
from domain.interfaces.caja_repository_interface import CajaRepositoryInterface
from src.infrastructure.models.models import (
    Caja,
    CajaSesion,
    CierreCajaDenominacion,
    MovimientoFinanciero,
)


class CajaRepository(CajaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_caja(self, entity: CajaEntity) -> CajaEntity:
        created_at = entity.created_at or datetime.now(timezone.utc)
        caja_orm = Caja(
            nombre=entity.nombre,
            saldo_inicial=entity.saldo_inicial,
            estado=entity.estado,
            usuario_id=entity.usuario_id,
            fecha_apertura=entity.fecha_apertura,
            fecha_cierre=entity.fecha_cierre,
            cierre_caja=entity.cierre_caja,
            saldo_final_efectivo=entity.saldo_final_efectivo,
            diferencia=entity.diferencia,
            created_at=created_at,
        )
        self.db.add(caja_orm)
        self.db.commit()
        self.db.refresh(caja_orm)
        return self._to_entity(caja_orm)

    def get_caja(self, caja_id: int) -> Optional[CajaEntity]:
        record = self.db.get(Caja, caja_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_cajas(self) -> List[CajaEntity]:
        records = self.db.query(Caja).all()
        return [self._to_entity(row) for row in records]

    def update_caja(self, caja_id: int, entity: CajaEntity) -> Optional[CajaEntity]:
        record = self.db.get(Caja, caja_id)
        if not record:
            return None
        record.nombre = entity.nombre
        record.saldo_inicial = entity.saldo_inicial
        record.estado = entity.estado
        record.usuario_id = entity.usuario_id
        record.fecha_apertura = entity.fecha_apertura
        record.fecha_cierre = entity.fecha_cierre
        record.cierre_caja = entity.cierre_caja
        record.saldo_final_efectivo = entity.saldo_final_efectivo
        record.diferencia = entity.diferencia
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def cerrar_caja(
        self,
        caja_id: int,
        *,
        usuario_id: Optional[int] = None,
    ) -> Optional[CajaEntity]:
        record = self.db.get(Caja, caja_id)
        if not record:
            return None

        cierre_time = datetime.now(timezone.utc)
        fecha_apertura = record.fecha_apertura

        ingresos_query = self.db.query(
            func.coalesce(func.sum(MovimientoFinanciero.monto), 0)
        ).filter(
            MovimientoFinanciero.caja_id == caja_id,
            MovimientoFinanciero.tipo == "INGRESO",
            MovimientoFinanciero.fecha <= cierre_time,
        )
        egresos_query = self.db.query(
            func.coalesce(func.sum(MovimientoFinanciero.monto), 0)
        ).filter(
            MovimientoFinanciero.caja_id == caja_id,
            MovimientoFinanciero.tipo == "EGRESO",
            MovimientoFinanciero.fecha <= cierre_time,
        )
        if fecha_apertura is not None:
            ingresos_query = ingresos_query.filter(
                MovimientoFinanciero.fecha >= fecha_apertura
            )
            egresos_query = egresos_query.filter(
                MovimientoFinanciero.fecha >= fecha_apertura
            )
        total_ingresos = Decimal(ingresos_query.scalar() or 0)
        total_egresos = Decimal(egresos_query.scalar() or 0)

        ultimo_conteo = (
            self.db.query(func.max(CierreCajaDenominacion.fecha_conteo))
            .filter(CierreCajaDenominacion.caja_id == caja_id)
            .scalar()
        )
        if ultimo_conteo is None:
            raise ValueError("No hay conteo de denominaciones para esta caja")

        saldo_final_efectivo = Decimal(
            self.db.query(func.coalesce(func.sum(CierreCajaDenominacion.subtotal), 0))
            .filter(
                CierreCajaDenominacion.caja_id == caja_id,
                CierreCajaDenominacion.fecha_conteo == ultimo_conteo,
            )
            .scalar()
            or 0
        )

        saldo_teorico = (
            Decimal(record.saldo_inicial) + total_ingresos - total_egresos
        ).quantize(Decimal("0.01"))
        diferencia = (saldo_final_efectivo - saldo_teorico).quantize(Decimal("0.01"))

        record.estado = CajaEstado.CERRADA
        record.fecha_cierre = cierre_time
        record.cierre_caja = cierre_time
        record.saldo_final_efectivo = saldo_final_efectivo.quantize(Decimal("0.01"))
        record.diferencia = diferencia
        if usuario_id is not None:
            record.usuario_id = usuario_id

        open_session = (
            self.db.query(CajaSesion)
            .filter(
                CajaSesion.caja_id == caja_id,
                CajaSesion.fecha_cierre.is_(None),
            )
            .order_by(CajaSesion.fecha_apertura.desc())
            .first()
        )
        if open_session:
            open_session.fecha_cierre = cierre_time

        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_entity(self, record: Caja) -> CajaEntity:
        return CajaEntity.from_model(record)
