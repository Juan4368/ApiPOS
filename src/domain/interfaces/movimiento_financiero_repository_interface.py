from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from domain.entities.movimientoFinancieroEntity import MovimientoFinancieroEntity
from domain.enums.contabilidadEnums import CategoriaTipo


class MovimientoFinancieroRepositoryInterface(ABC):
    @abstractmethod
    def create_movimiento(
        self, entity: MovimientoFinancieroEntity
    ) -> MovimientoFinancieroEntity:
        raise NotImplementedError

    @abstractmethod
    def get_movimiento(self, movimiento_id: int) -> Optional[MovimientoFinancieroEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_movimientos(
        self,
        *,
        desde: Optional[date] = None,
        hasta: Optional[date] = None,
        caja_id: Optional[int] = None,
        tipo: Optional[CategoriaTipo] = None,
        proveedor_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        venta_id: Optional[int] = None,
    ) -> List[MovimientoFinancieroEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_movimiento(
        self, movimiento_id: int, entity: MovimientoFinancieroEntity
    ) -> Optional[MovimientoFinancieroEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_movimiento(self, movimiento_id: int) -> Optional[MovimientoFinancieroEntity]:
        raise NotImplementedError
