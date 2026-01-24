from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from domain.entities.carteraEntity import CarteraEntity


class CarteraRepositoryInterface(ABC):
    @abstractmethod
    def create_cartera(self, entity: CarteraEntity) -> CarteraEntity:
        raise NotImplementedError

    @abstractmethod
    def get_cartera(self, cartera_id: int) -> Optional[CarteraEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_cartera(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CarteraEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_cartera(self, cartera_id: int, entity: CarteraEntity) -> Optional[CarteraEntity]:
        raise NotImplementedError
