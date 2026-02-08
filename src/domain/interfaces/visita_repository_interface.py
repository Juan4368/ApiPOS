from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.visitaEntity import VisitaEntity


class VisitaRepositoryInterface(ABC):
    @abstractmethod
    def create_visita(self, entity: VisitaEntity) -> VisitaEntity:
        raise NotImplementedError

    @abstractmethod
    def get_visita(self, visita_id: int) -> Optional[VisitaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_visitas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        usuario_id: Optional[int] = None,
    ) -> List[VisitaEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_visita(
        self, visita_id: int, entity: VisitaEntity
    ) -> Optional[VisitaEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_visita(self, visita_id: int) -> bool:
        raise NotImplementedError
