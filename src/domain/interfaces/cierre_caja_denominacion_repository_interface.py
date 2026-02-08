from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.cierreCajaDenominacionEntity import CierreCajaDenominacionEntity


class CierreCajaDenominacionRepositoryInterface(ABC):
    @abstractmethod
    def create_denominacion(
        self, entity: CierreCajaDenominacionEntity
    ) -> CierreCajaDenominacionEntity:
        raise NotImplementedError

    @abstractmethod
    def create_denominaciones(
        self, entities: List[CierreCajaDenominacionEntity]
    ) -> List[CierreCajaDenominacionEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_denominacion(self, denominacion_id: int) -> Optional[CierreCajaDenominacionEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_denominaciones(self) -> List[CierreCajaDenominacionEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_denominacion(
        self, denominacion_id: int, entity: CierreCajaDenominacionEntity
    ) -> Optional[CierreCajaDenominacionEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_denominacion(self, denominacion_id: int) -> bool:
        raise NotImplementedError
