from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.dtos.clienteDto import ClienteRequest, ClienteResponse, ClienteUpdateRequest


class IClientService(ABC):
    @abstractmethod
    def create_cliente(self, data: ClienteRequest) -> ClienteResponse:
        ...

    @abstractmethod
    def get_cliente(self, cliente_id: UUID) -> Optional[ClienteResponse]:
        ...

    @abstractmethod
    def list_clientes(self) -> List[ClienteResponse]:
        ...

    @abstractmethod
    def search_clientes(self, term: str) -> List[ClienteResponse]:
        ...

    @abstractmethod
    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ClienteResponse]:
        ...

    @abstractmethod
    def update_cliente(self, cliente_id: UUID, data: ClienteRequest) -> Optional[ClienteResponse]:
        ...

    @abstractmethod
    def patch_cliente(
        self, cliente_id: UUID, data: ClienteUpdateRequest
    ) -> Optional[ClienteResponse]:
        ...
