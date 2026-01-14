from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.stockEntity import StockEntity
from domain.interfaces.stock_repository_interface import StockRepositoryInterface
from src.infrastructure.models.models import Stock


class StockRepository(StockRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con stock."""

    def __init__(self, db: Session):
        self.db = db

    def create_stock(self, stock_entity: StockEntity) -> StockEntity:
        ultima_actualizacion = stock_entity.ultima_actualizacion or datetime.now(timezone.utc)
        stock_orm = Stock(
            stock_id=stock_entity.stock_id,
            producto_id=stock_entity.producto_id,
            cantidad_actual=stock_entity.cantidad_actual,
            cantidad_minima=stock_entity.cantidad_minima,
            ultima_actualizacion=ultima_actualizacion,
            actualizado_por_id=stock_entity.actualizado_por_id,
            creado_por_id=stock_entity.creado_por_id,
        )

        self.db.add(stock_orm)
        self.db.commit()
        self.db.refresh(stock_orm)
        return StockEntity.from_model(stock_orm)

    def list_stock(self) -> List[StockEntity]:
        records = self.db.query(Stock).all()
        return [StockEntity.from_model(row) for row in records]

    def get_stock(self, stock_id: int) -> Optional[StockEntity]:
        record = self.db.get(Stock, stock_id)
        if not record:
            return None
        return StockEntity.from_model(record)

    def search_stock(self, term: str) -> List[StockEntity]:
        filters = []

        try:
            int_value = int(term)
            filters.append(Stock.producto_id == int_value)
            filters.append(Stock.cantidad_actual == int_value)
            filters.append(Stock.cantidad_minima == int_value)
        except Exception:
            pass

        records = (
            self.db.query(Stock).filter(or_(*filters)).all()
            if filters
            else self.db.query(Stock).all()
        )
        return [StockEntity.from_model(row) for row in records]
