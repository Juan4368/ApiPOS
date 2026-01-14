from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.dtos.stockDto import StockRequest, StockResponse


class IStockService(ABC):
    @abstractmethod
    def create_stock(self, data: StockRequest) -> StockResponse:
        ...

    @abstractmethod
    def get_stock(self, stock_id: int) -> Optional[StockResponse]:
        ...

    @abstractmethod
    def list_stock(self) -> List[StockResponse]:
        ...

    @abstractmethod
    def search_stock(self, term: str) -> List[StockResponse]:
        ...
