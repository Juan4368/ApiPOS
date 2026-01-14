from __future__ import annotations

from typing import List, Optional

from domain.dtos.stockDto import StockRequest, StockResponse
from domain.entities.stockEntity import StockEntity
from domain.interfaces.IStockService import IStockService
from domain.interfaces.stock_repository_interface import StockRepositoryInterface


class StockService(IStockService):
    """Caso de uso para operaciones de stock."""

    def __init__(self, repository: StockRepositoryInterface):
        self.repository = repository

    def create_stock(self, data: StockRequest) -> StockResponse:
        entity = StockEntity(
            producto_id=data.producto_id,
            cantidad_actual=data.cantidad_actual,
            cantidad_minima=data.cantidad_minima,
            ultima_actualizacion=data.ultima_actualizacion,
            actualizado_por_id=data.actualizado_por_id,
            creado_por_id=data.creado_por_id,
        )
        created = self.repository.create_stock(entity)
        return StockResponse.model_validate(created)

    def list_stock(self) -> List[StockResponse]:
        stocks = self.repository.list_stock()
        return [StockResponse.model_validate(stock) for stock in stocks]

    def get_stock(self, stock_id: int) -> Optional[StockResponse]:
        stock = self.repository.get_stock(stock_id)
        if not stock:
            return None
        return StockResponse.model_validate(stock)

    def search_stock(self, term: str) -> List[StockResponse]:
        stocks = self.repository.search_stock(term)
        return [StockResponse.model_validate(stock) for stock in stocks]
