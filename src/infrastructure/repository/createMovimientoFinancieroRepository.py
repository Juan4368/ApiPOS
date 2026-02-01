from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.movimientoFinancieroEntity import MovimientoFinancieroEntity
from domain.enums.contabilidadEnums import CategoriaTipo
from domain.interfaces.movimiento_financiero_repository_interface import (
    MovimientoFinancieroRepositoryInterface,
)
from src.infrastructure.models.models import MovimientoFinanciero


class MovimientoFinancieroRepository(MovimientoFinancieroRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_movimiento(
        self, entity: MovimientoFinancieroEntity
    ) -> MovimientoFinancieroEntity:
        movimiento_orm = MovimientoFinanciero(
            fecha=entity.fecha,
            tipo=self._to_tipo_movimiento(entity.tipo),
            monto=entity.monto,
            concepto=entity.concepto,
            nota=entity.nota,
            proveedor_id=entity.proveedor_id,
            caja_id=entity.caja_id,
            usuario_id=entity.usuario_id,
            venta_id=entity.venta_id,
        )
        self.db.add(movimiento_orm)
        self.db.commit()
        self.db.refresh(movimiento_orm)
        return self._to_entity(movimiento_orm)

    def get_movimiento(self, movimiento_id: int) -> Optional[MovimientoFinancieroEntity]:
        record = self.db.get(MovimientoFinanciero, movimiento_id)
        if not record:
            return None
        return self._to_entity(record)

    def list_movimientos(
        self,
        *,
        desde: Optional[date] = None,
        hasta: Optional[date] = None,
        caja_id: Optional[int] = None,
        tipo: Optional[CategoriaTipo] = None,
        proveedor_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        venta_id: Optional[int] = None,
    ) -> List[MovimientoFinancieroEntity]:
        query = self.db.query(MovimientoFinanciero)
        if desde:
            query = query.filter(
                MovimientoFinanciero.fecha >= datetime.combine(desde, time.min)
            )
        if hasta:
            query = query.filter(
                MovimientoFinanciero.fecha <= datetime.combine(hasta, time.max)
            )
        if caja_id is not None:
            query = query.filter(MovimientoFinanciero.caja_id == caja_id)
        if tipo is not None:
            query = query.filter(
                MovimientoFinanciero.tipo == self._to_tipo_movimiento(tipo)
            )
        if proveedor_id is not None:
            query = query.filter(MovimientoFinanciero.proveedor_id == proveedor_id)
        if usuario_id is not None:
            query = query.filter(MovimientoFinanciero.usuario_id == usuario_id)
        if venta_id is not None:
            query = query.filter(MovimientoFinanciero.venta_id == venta_id)
        records = query.order_by(MovimientoFinanciero.fecha.desc()).all()
        return [self._to_entity(record) for record in records]

    def update_movimiento(
        self, movimiento_id: int, entity: MovimientoFinancieroEntity
    ) -> Optional[MovimientoFinancieroEntity]:
        record = self.db.get(MovimientoFinanciero, movimiento_id)
        if not record:
            return None
        record.fecha = entity.fecha
        record.tipo = self._to_tipo_movimiento(entity.tipo)
        record.monto = entity.monto
        record.concepto = entity.concepto
        record.nota = entity.nota
        record.proveedor_id = entity.proveedor_id
        record.caja_id = entity.caja_id
        record.usuario_id = entity.usuario_id
        record.venta_id = entity.venta_id
        self.db.commit()
        self.db.refresh(record)
        return self._to_entity(record)

    def _to_tipo_movimiento(self, tipo: CategoriaTipo) -> str:
        if isinstance(tipo, CategoriaTipo):
            return tipo.value.upper()
        return str(tipo).upper()

    def _to_entity(self, record: MovimientoFinanciero) -> MovimientoFinancieroEntity:
        return MovimientoFinancieroEntity(
            id=record.id,
            fecha=record.fecha,
            tipo=CategoriaTipo(record.tipo),
            monto=record.monto,
            concepto=record.concepto,
            nota=record.nota,
            proveedor_id=record.proveedor_id,
            caja_id=record.caja_id,
            usuario_id=record.usuario_id,
            venta_id=record.venta_id,
            created_at=record.created_at,
        )
