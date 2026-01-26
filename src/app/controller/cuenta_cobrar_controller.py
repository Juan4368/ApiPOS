from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.abonoCuentaDto import AbonoCuentaRequest, AbonoCuentaResponse
from src.domain.dtos.cuentaCobrarDto import (
    AbonoCuentaResultResponse,
    CuentaCobrarRequest,
    CuentaCobrarResponse,
    CuentaCobrarUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.enums.contabilidadEnums import CreditoEstado
from src.domain.services.cuenta_cobrar_service import CuentaCobrarService
from src.infrastructure.repository.createCuentaCobrarRepository import (
    CuentaCobrarRepository,
)

router = APIRouter(
    prefix="/contabilidad/cuentas-por-cobrar",
    tags=["contabilidad-cuentas-por-cobrar"],
)


def get_service(db: Session = Depends(get_db)) -> CuentaCobrarService:
    repo = CuentaCobrarRepository(db)
    return CuentaCobrarService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CuentaCobrarService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CuentaCobrarResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_cuenta(
    payload: CuentaCobrarRequest,
    service: ServiceDep,
) -> CreationResponse[CuentaCobrarResponse]:
    try:
        created = service.create_cuenta(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CuentaCobrarResponse](id=created.id, data=created)


@router.get("/", response_model=list[CuentaCobrarResponse])
def list_cuentas(
    service: ServiceDep,
    cliente_id: Optional[UUID] = None,
    venta_id: Optional[int] = None,
    estado: Optional[CreditoEstado] = None,
) -> list[CuentaCobrarResponse]:
    return service.list_cuentas(cliente_id=cliente_id, venta_id=venta_id, estado=estado)


@router.get("/{cuenta_id}", response_model=CuentaCobrarResponse)
def get_cuenta(cuenta_id: int, service: ServiceDep) -> CuentaCobrarResponse:
    cuenta = service.get_cuenta(cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    return cuenta


@router.put("/{cuenta_id}", response_model=CuentaCobrarResponse)
def update_cuenta(
    cuenta_id: int,
    payload: CuentaCobrarRequest,
    service: ServiceDep,
) -> CuentaCobrarResponse:
    cuenta = service.update_cuenta(cuenta_id, payload)
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    return cuenta


@router.patch("/{cuenta_id}", response_model=CuentaCobrarResponse)
def patch_cuenta(
    cuenta_id: int,
    payload: CuentaCobrarUpdateRequest,
    service: ServiceDep,
) -> CuentaCobrarResponse:
    cuenta = service.patch_cuenta(cuenta_id, payload)
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    return cuenta


@router.post(
    "/{cuenta_id}/abonos",
    response_model=CreationResponse[AbonoCuentaResultResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_abono(
    cuenta_id: int,
    payload: AbonoCuentaRequest,
    service: ServiceDep,
) -> CreationResponse[AbonoCuentaResultResponse]:
    try:
        created = service.create_abono(cuenta_id, payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if not created:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    cuenta = service.get_cuenta(cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    data = AbonoCuentaResultResponse(abono=created, cuenta=cuenta)
    return CreationResponse[AbonoCuentaResultResponse](id=created.id, data=data)


@router.get("/{cuenta_id}/abonos", response_model=list[AbonoCuentaResponse])
def list_abonos(cuenta_id: int, service: ServiceDep) -> list[AbonoCuentaResponse]:
    return service.list_abonos(cuenta_id)
