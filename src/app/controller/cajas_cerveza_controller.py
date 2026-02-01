from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.cajasCervezaDto import (
    CajasCervezaRequest,
    CajasCervezaResponse,
    CajasCervezaUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse, MessageResponse
from src.domain.services.cajas_cerveza_service import CajasCervezaService
from src.infrastructure.repository.createCajasCervezaRepository import (
    CajasCervezaRepository,
)

router = APIRouter(prefix="/cajas-cerveza", tags=["cajas-cerveza"])


def get_service(db: Session = Depends(get_db)) -> CajasCervezaService:
    repo = CajasCervezaRepository(db)
    return CajasCervezaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CajasCervezaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CajasCervezaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_cajas_cerveza(
    payload: CajasCervezaRequest,
    service: ServiceDep,
) -> CreationResponse[CajasCervezaResponse]:
    try:
        created = service.create_cajas_cerveza(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CajasCervezaResponse](id=created.id, data=created)


@router.get("/", response_model=list[CajasCervezaResponse])
def list_cajas_cerveza(service: ServiceDep) -> list[CajasCervezaResponse]:
    return service.list_cajas_cerveza()


@router.get("/{cajas_id}", response_model=CajasCervezaResponse)
def get_cajas_cerveza(
    cajas_id: int,
    service: ServiceDep,
) -> CajasCervezaResponse:
    record = service.get_cajas_cerveza(cajas_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.put("/{cajas_id}", response_model=CajasCervezaResponse)
def update_cajas_cerveza(
    cajas_id: int,
    payload: CajasCervezaRequest,
    service: ServiceDep,
) -> CajasCervezaResponse:
    record = service.update_cajas_cerveza(cajas_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.patch("/{cajas_id}", response_model=CajasCervezaResponse)
def patch_cajas_cerveza(
    cajas_id: int,
    payload: CajasCervezaUpdateRequest,
    service: ServiceDep,
) -> CajasCervezaResponse:
    record = service.patch_cajas_cerveza(cajas_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return record


@router.delete("/{cajas_id}", response_model=MessageResponse)
def delete_cajas_cerveza(
    cajas_id: int,
    service: ServiceDep,
) -> MessageResponse:
    deleted = service.delete_cajas_cerveza(cajas_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )
    return MessageResponse(message="Registro eliminado")
