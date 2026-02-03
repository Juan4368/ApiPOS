from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.cajaSesionEntity import CajaSesionEntity


class CajaSesionRepositoryInterface(ABC):
    @abstractmethod
    def create_caja_sesion(self, entity: CajaSesionEntity) -> CajaSesionEntity:
        raise NotImplementedError

    @abstractmethod
    def get_open_by_caja_usuario(
        self, caja_id: int, usuario_id: int
    ) -> Optional[CajaSesionEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_caja_sesion(self, sesion_id: int) -> Optional[CajaSesionEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_caja_sesiones(self) -> List[CajaSesionEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_caja_sesion(
        self, sesion_id: int, entity: CajaSesionEntity
    ) -> Optional[CajaSesionEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_caja_sesion(self, sesion_id: int) -> bool:
        raise NotImplementedError
