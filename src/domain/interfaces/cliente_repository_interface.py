from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.clienteEntity import ClienteEntity


class ClienteRepositoryInterface(ABC):
    @abstractmethod
    def create_cliente(
        self, entity: ClienteEntity, nombre_normalizado: Optional[str] = None
    ) -> ClienteEntity:
        ...

    @abstractmethod
    def get_cliente(self, cliente_id: UUID) -> Optional[ClienteEntity]:
        ...

    @abstractmethod
    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ClienteEntity]:
        ...

    @abstractmethod
    def list_clientes(self) -> List[ClienteEntity]:
        ...

    @abstractmethod
    def search_clientes(self, term: str) -> List[ClienteEntity]:
        ...

    @abstractmethod
    def update_cliente(
        self,
        cliente_id: UUID,
        nombre: Optional[str] = None,
        nombre_normalizado: Optional[str] = None,
        telefono: Optional[str] = None,
        email: Optional[str] = None,
        descuento_pesos: Optional[float] = None,
        descuento_porcentaje: Optional[float] = None,
    ) -> Optional[ClienteEntity]:
        ...
