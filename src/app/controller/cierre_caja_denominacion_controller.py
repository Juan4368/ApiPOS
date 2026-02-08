from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.cierreCajaDenominacionDto import (
    CierreCajaDenominacionRequest,
    CierreCajaDenominacionResponse,
    CierreCajaDenominacionUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse, MessageResponse
from src.domain.services.cierre_caja_denominacion_service import (
    CierreCajaDenominacionService,
)
from src.infrastructure.repository.createCierreCajaDenominacionRepository import (
    CierreCajaDenominacionRepository,
)

router = APIRouter(
    prefix="/contabilidad/cierre-caja-denominaciones",
    tags=["contabilidad-cierre-caja-denominaciones"],
)


def get_service(db: Session = Depends(get_db)) -> CierreCajaDenominacionService:
    repo = CierreCajaDenominacionRepository(db)
    return CierreCajaDenominacionService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CierreCajaDenominacionService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CierreCajaDenominacionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_denominacion(
    payload: CierreCajaDenominacionRequest,
    service: ServiceDep,
) -> CreationResponse[CierreCajaDenominacionResponse]:
    try:
        created = service.create_denominacion(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CierreCajaDenominacionResponse](id=created.id, data=created)


@router.post(
    "/bulk",
    response_model=list[CierreCajaDenominacionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_denominaciones_bulk(
    payload: list[CierreCajaDenominacionRequest],
    service: ServiceDep,
) -> list[CierreCajaDenominacionResponse]:
    try:
        return service.create_denominaciones(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[CierreCajaDenominacionResponse])
def list_denominaciones(service: ServiceDep) -> list[CierreCajaDenominacionResponse]:
    return service.list_denominaciones()


@router.get("/{denominacion_id}", response_model=CierreCajaDenominacionResponse)
def get_denominacion(
    denominacion_id: int,
    service: ServiceDep,
) -> CierreCajaDenominacionResponse:
    record = service.get_denominacion(denominacion_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.put("/{denominacion_id}", response_model=CierreCajaDenominacionResponse)
def update_denominacion(
    denominacion_id: int,
    payload: CierreCajaDenominacionRequest,
    service: ServiceDep,
) -> CierreCajaDenominacionResponse:
    record = service.update_denominacion(denominacion_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.patch("/{denominacion_id}", response_model=CierreCajaDenominacionResponse)
def patch_denominacion(
    denominacion_id: int,
    payload: CierreCajaDenominacionUpdateRequest,
    service: ServiceDep,
) -> CierreCajaDenominacionResponse:
    record = service.patch_denominacion(denominacion_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.delete("/{denominacion_id}", response_model=MessageResponse)
def delete_denominacion(
    denominacion_id: int,
    service: ServiceDep,
) -> MessageResponse:
    deleted = service.delete_denominacion(denominacion_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return MessageResponse(message="Registro eliminado")
