from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.dtos.ventaDto import (
    VentaRequest,
    VentaResponse,
    VentaStatusRequest,
    VentaUpdateRequest,
)


class IVentaService(ABC):
    @abstractmethod
    def create_venta(self, data: VentaRequest) -> VentaResponse:
        ...

    @abstractmethod
    def get_venta(self, venta_id: int) -> Optional[VentaResponse]:
        ...

    @abstractmethod
    def list_ventas(self) -> List[VentaResponse]:
        ...

    @abstractmethod
    def search_ventas(self, term: str) -> List[VentaResponse]:
        ...

    @abstractmethod
    def update_venta_status(
        self, venta_id: int, data: VentaStatusRequest
    ) -> Optional[VentaResponse]:
        ...

    @abstractmethod
    def update_venta(
        self, venta_id: int, data: VentaUpdateRequest
    ) -> Optional[VentaResponse]:
        ...
