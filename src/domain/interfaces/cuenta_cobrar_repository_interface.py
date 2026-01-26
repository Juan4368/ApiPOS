from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.abonoCuentaEntity import AbonoCuentaEntity
from domain.entities.cuentaCobrarEntity import CuentaCobrarEntity
from domain.enums.contabilidadEnums import CreditoEstado


class CuentaCobrarRepositoryInterface(ABC):
    @abstractmethod
    def create_cuenta(self, entity: CuentaCobrarEntity) -> CuentaCobrarEntity:
        raise NotImplementedError

    @abstractmethod
    def get_cuenta(self, cuenta_id: int) -> Optional[CuentaCobrarEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_cuentas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        venta_id: Optional[int] = None,
        estado: Optional[CreditoEstado] = None,
    ) -> List[CuentaCobrarEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_cuenta(
        self, cuenta_id: int, entity: CuentaCobrarEntity
    ) -> Optional[CuentaCobrarEntity]:
        raise NotImplementedError

    @abstractmethod
    def create_abono(
        self, cuenta_id: int, abono: AbonoCuentaEntity
    ) -> Optional[AbonoCuentaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_abonos(self, cuenta_id: int) -> List[AbonoCuentaEntity]:
        raise NotImplementedError
