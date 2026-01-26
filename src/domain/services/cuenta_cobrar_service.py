from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from domain.dtos.abonoCuentaDto import AbonoCuentaRequest, AbonoCuentaResponse
from domain.dtos.cuentaCobrarDto import (
    CuentaCobrarRequest,
    CuentaCobrarResponse,
    CuentaCobrarUpdateRequest,
)
from domain.entities.abonoCuentaEntity import AbonoCuentaEntity
from domain.entities.cuentaCobrarEntity import CuentaCobrarEntity
from domain.enums.contabilidadEnums import CreditoEstado
from domain.interfaces.cuenta_cobrar_repository_interface import (
    CuentaCobrarRepositoryInterface,
)


class CuentaCobrarService:
    def __init__(self, repository: CuentaCobrarRepositoryInterface):
        self.repository = repository

    def create_cuenta(self, data: CuentaCobrarRequest) -> CuentaCobrarResponse:
        saldo = data.saldo_inicial if data.saldo_inicial is not None else data.total
        if saldo > data.total:
            raise ValueError("El saldo inicial no puede ser mayor al total")
        estado = data.estado or self._calcular_estado(data.total, saldo)
        entity = CuentaCobrarEntity(
            venta_id=data.venta_id,
            cliente_id=data.cliente_id,
            total=data.total,
            saldo=saldo,
            estado=estado,
            created_at=datetime.now(timezone.utc),
        )
        created = self.repository.create_cuenta(entity)
        return CuentaCobrarResponse.model_validate(created)

    def get_cuenta(self, cuenta_id: int) -> Optional[CuentaCobrarResponse]:
        cuenta = self.repository.get_cuenta(cuenta_id)
        if not cuenta:
            return None
        return CuentaCobrarResponse.model_validate(cuenta)

    def list_cuentas(
        self,
        *,
        cliente_id: Optional[UUID] = None,
        venta_id: Optional[int] = None,
        estado: Optional[CreditoEstado] = None,
    ) -> List[CuentaCobrarResponse]:
        cuentas = self.repository.list_cuentas(
            cliente_id=cliente_id, venta_id=venta_id, estado=estado
        )
        return [CuentaCobrarResponse.model_validate(c) for c in cuentas]

    def update_cuenta(
        self, cuenta_id: int, data: CuentaCobrarRequest
    ) -> Optional[CuentaCobrarResponse]:
        saldo = data.saldo_inicial if data.saldo_inicial is not None else data.total
        if saldo > data.total:
            raise ValueError("El saldo inicial no puede ser mayor al total")
        estado = data.estado or self._calcular_estado(data.total, saldo)
        entity = CuentaCobrarEntity(
            id=cuenta_id,
            venta_id=data.venta_id,
            cliente_id=data.cliente_id,
            total=data.total,
            saldo=saldo,
            estado=estado,
            updated_at=datetime.now(timezone.utc),
        )
        updated = self.repository.update_cuenta(cuenta_id, entity)
        if not updated:
            return None
        return CuentaCobrarResponse.model_validate(updated)

    def patch_cuenta(
        self, cuenta_id: int, data: CuentaCobrarUpdateRequest
    ) -> Optional[CuentaCobrarResponse]:
        current = self.repository.get_cuenta(cuenta_id)
        if not current:
            return None
        total = data.total if data.total is not None else current.total
        saldo = data.saldo if data.saldo is not None else current.saldo
        if saldo > total:
            raise ValueError("El saldo no puede ser mayor al total")
        estado = data.estado or self._calcular_estado(total, saldo)
        entity = CuentaCobrarEntity(
            id=cuenta_id,
            venta_id=data.venta_id if data.venta_id is not None else current.venta_id,
            cliente_id=(
                data.cliente_id if data.cliente_id is not None else current.cliente_id
            ),
            total=total,
            saldo=saldo,
            estado=estado,
            created_at=current.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        updated = self.repository.update_cuenta(cuenta_id, entity)
        if not updated:
            return None
        return CuentaCobrarResponse.model_validate(updated)

    def create_abono(
        self, cuenta_id: int, data: AbonoCuentaRequest
    ) -> Optional[AbonoCuentaResponse]:
        abono_entity = AbonoCuentaEntity(
            cuenta_id=cuenta_id,
            movimiento_id=0,
            monto=data.monto,
            fecha=data.fecha,
            concepto=data.concepto,
            caja_id=data.caja_id,
            usuario_id=data.usuario_id,
            venta_id=data.venta_id,
        )
        created = self.repository.create_abono(cuenta_id, abono_entity)
        if not created:
            return None
        return AbonoCuentaResponse.model_validate(created)

    def list_abonos(self, cuenta_id: int) -> List[AbonoCuentaResponse]:
        abonos = self.repository.list_abonos(cuenta_id)
        return [AbonoCuentaResponse.model_validate(a) for a in abonos]

    def _calcular_estado(self, total: Decimal, saldo: Decimal) -> CreditoEstado:
        if saldo <= Decimal("0.00"):
            return CreditoEstado.PAGADO
        if saldo < total:
            return CreditoEstado.PARCIAL
        return CreditoEstado.PENDIENTE
