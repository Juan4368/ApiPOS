from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.ventaDetalleEntity import VentaDetalleEntity
from domain.entities.ventaEntity import VentaEntity


class VentaRepositoryInterface(ABC):
    """Contrato para repositorios de ventas en el dominio."""

    @abstractmethod
    def create_venta(
        self, venta_entity: VentaEntity, detalles: List[VentaDetalleEntity]
    ) -> VentaEntity:
        """Persiste una venta y sus detalles."""
        raise NotImplementedError

    @abstractmethod
    def list_ventas(self) -> List[VentaEntity]:
        """Devuelve todas las ventas."""
        raise NotImplementedError

    @abstractmethod
    def get_venta(self, venta_id: int) -> Optional[VentaEntity]:
        """Devuelve una venta por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def search_ventas(self, term: str) -> List[VentaEntity]:
        """Busca ventas por tipo_pago o montos."""
        raise NotImplementedError
