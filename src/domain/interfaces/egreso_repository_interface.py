from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities.egresoEntity import EgresoEntity


class EgresoRepositoryInterface(ABC):
    @abstractmethod
    def create_egreso(self, entity: EgresoEntity) -> EgresoEntity:
        raise NotImplementedError

    @abstractmethod
    def get_egreso(self, egreso_id: UUID) -> Optional[EgresoEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_egresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[EgresoEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_egreso(self, egreso_id: int, entity: EgresoEntity) -> Optional[EgresoEntity]:
        raise NotImplementedError

