from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.cajaSesionDto import (
    CajaSesionRequest,
    CajaSesionResponse,
    CajaSesionUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse, MessageResponse
from src.domain.services.caja_sesion_service import CajaSesionService
from src.infrastructure.repository.createCajaSesionRepository import CajaSesionRepository

router = APIRouter(prefix="/contabilidad/caja-sesiones", tags=["contabilidad-caja-sesiones"])


def get_service(db: Session = Depends(get_db)) -> CajaSesionService:
    repo = CajaSesionRepository(db)
    return CajaSesionService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CajaSesionService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CajaSesionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_caja_sesion(
    payload: CajaSesionRequest,
    service: ServiceDep,
) -> CreationResponse[CajaSesionResponse]:
    try:
        created = service.create_caja_sesion(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CajaSesionResponse](id=created.id, data=created)


@router.get("/", response_model=list[CajaSesionResponse])
def list_caja_sesiones(service: ServiceDep) -> list[CajaSesionResponse]:
    return service.list_caja_sesiones()


@router.get("/{sesion_id}", response_model=CajaSesionResponse)
def get_caja_sesion(sesion_id: int, service: ServiceDep) -> CajaSesionResponse:
    record = service.get_caja_sesion(sesion_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    return record


@router.put("/{sesion_id}", response_model=CajaSesionResponse)
def update_caja_sesion(
    sesion_id: int,
    payload: CajaSesionRequest,
    service: ServiceDep,
) -> CajaSesionResponse:
    record = service.update_caja_sesion(sesion_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    return record


@router.patch("/{sesion_id}", response_model=CajaSesionResponse)
def patch_caja_sesion(
    sesion_id: int,
    payload: CajaSesionUpdateRequest,
    service: ServiceDep,
) -> CajaSesionResponse:
    record = service.patch_caja_sesion(sesion_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    return record


@router.delete("/{sesion_id}", response_model=MessageResponse)
def delete_caja_sesion(
    sesion_id: int,
    service: ServiceDep,
) -> MessageResponse:
    deleted = service.delete_caja_sesion(sesion_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    return MessageResponse(message="Sesión eliminada")
