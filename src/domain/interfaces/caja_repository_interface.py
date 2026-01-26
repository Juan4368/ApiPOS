from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.cajaEntity import CajaEntity


class CajaRepositoryInterface(ABC):
    @abstractmethod
    def create_caja(self, entity: CajaEntity) -> CajaEntity:
        raise NotImplementedError

    @abstractmethod
    def get_caja(self, caja_id: int) -> Optional[CajaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_cajas(self) -> List[CajaEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_caja(self, caja_id: int, entity: CajaEntity) -> Optional[CajaEntity]:
        raise NotImplementedError
