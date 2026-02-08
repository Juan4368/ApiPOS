from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.cajaDto import (
    CajaCerrarRequest,
    CajaRequest,
    CajaResponse,
    CajaUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.caja_service import CajaService
from src.infrastructure.repository.createCajaRepository import CajaRepository

router = APIRouter(prefix="/contabilidad/cajas", tags=["contabilidad-cajas"])


def get_service(db: Session = Depends(get_db)) -> CajaService:
    repo = CajaRepository(db)
    return CajaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CajaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CajaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_caja(
    payload: CajaRequest,
    service: ServiceDep,
) -> CreationResponse[CajaResponse]:
    try:
        created = service.create_caja(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CajaResponse](id=created.id, data=created)


@router.get("/", response_model=list[CajaResponse])
def list_cajas(service: ServiceDep) -> list[CajaResponse]:
    return service.list_cajas()


@router.get("/{caja_id}", response_model=CajaResponse)
def get_caja(caja_id: int, service: ServiceDep) -> CajaResponse:
    caja = service.get_caja(caja_id)
    if not caja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
    return caja


@router.put("/{caja_id}", response_model=CajaResponse)
def update_caja(
    caja_id: int,
    payload: CajaRequest,
    service: ServiceDep,
) -> CajaResponse:
    caja = service.update_caja(caja_id, payload)
    if not caja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
    return caja


@router.patch("/{caja_id}", response_model=CajaResponse)
def patch_caja(
    caja_id: int,
    payload: CajaUpdateRequest,
    service: ServiceDep,
) -> CajaResponse:
    caja = service.patch_caja(caja_id, payload)
    if not caja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
    return caja


@router.post("/{caja_id}/cerrar", response_model=CajaResponse)
def cerrar_caja(
    caja_id: int,
    payload: CajaCerrarRequest,
    service: ServiceDep,
) -> CajaResponse:
    try:
        caja = service.cerrar_caja(caja_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if not caja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
    return caja
