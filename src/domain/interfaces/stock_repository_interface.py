from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.stockEntity import StockEntity


class StockRepositoryInterface(ABC):
    """Contrato para repositorios de stock en el dominio."""

    @abstractmethod
    def create_stock(self, stock_entity: StockEntity) -> StockEntity:
        """Persiste un stock y devuelve la entidad creada."""
        raise NotImplementedError

    @abstractmethod
    def list_stock(self) -> List[StockEntity]:
        """Devuelve todos los registros de stock."""
        raise NotImplementedError

    @abstractmethod
    def get_stock(self, stock_id: int) -> Optional[StockEntity]:
        """Devuelve un stock por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def search_stock(self, term: str) -> List[StockEntity]:
        """Busca stock por producto_id, cantidades o estado de texto."""
        raise NotImplementedError
