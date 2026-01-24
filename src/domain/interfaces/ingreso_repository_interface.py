from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities.ingresoEntity import IngresoEntity


class IngresoRepositoryInterface(ABC):
    @abstractmethod
    def create_ingreso(self, entity: IngresoEntity) -> IngresoEntity:
        raise NotImplementedError

    @abstractmethod
    def get_ingreso(self, ingreso_id: UUID) -> Optional[IngresoEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_ingresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[IngresoEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_ingreso(self, ingreso_id: int, entity: IngresoEntity) -> Optional[IngresoEntity]:
        raise NotImplementedError

