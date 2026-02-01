from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.cajasCervezaEntity import CajasCervezaEntity


class CajasCervezaRepositoryInterface(ABC):
    @abstractmethod
    def create_cajas_cerveza(self, entity: CajasCervezaEntity) -> CajasCervezaEntity:
        raise NotImplementedError

    @abstractmethod
    def get_cajas_cerveza(self, cajas_id: int) -> Optional[CajasCervezaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_cajas_cerveza(self) -> List[CajasCervezaEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_cajas_cerveza(
        self, cajas_id: int, entity: CajasCervezaEntity
    ) -> Optional[CajasCervezaEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_cajas_cerveza(self, cajas_id: int) -> bool:
        raise NotImplementedError
