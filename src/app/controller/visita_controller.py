from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse, MessageResponse
from src.domain.dtos.visitaDto import (
    VisitaRequest,
    VisitaResponse,
    VisitaUpdateRequest,
)
from src.domain.services.visita_service import VisitaService
from src.infrastructure.repository.createVisitaRepository import VisitaRepository

router = APIRouter(prefix="/visitas", tags=["visitas"])


def get_service(db: Session = Depends(get_db)) -> VisitaService:
    repo = VisitaRepository(db)
    return VisitaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[VisitaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[VisitaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_visita(
    payload: VisitaRequest,
    service: ServiceDep,
) -> CreationResponse[VisitaResponse]:
    try:
        created = service.create_visita(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[VisitaResponse](id=created.id, data=created)


@router.get("/", response_model=list[VisitaResponse])
def list_visitas(
    service: ServiceDep,
    cliente_id: Optional[UUID] = None,
    usuario_id: Optional[int] = None,
) -> list[VisitaResponse]:
    return service.list_visitas(cliente_id=cliente_id, usuario_id=usuario_id)


@router.get("/{visita_id}", response_model=VisitaResponse)
def get_visita(visita_id: int, service: ServiceDep) -> VisitaResponse:
    record = service.get_visita(visita_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visita no encontrada")
    return record


@router.put("/{visita_id}", response_model=VisitaResponse)
def update_visita(
    visita_id: int,
    payload: VisitaRequest,
    service: ServiceDep,
) -> VisitaResponse:
    record = service.update_visita(visita_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visita no encontrada")
    return record


@router.patch("/{visita_id}", response_model=VisitaResponse)
def patch_visita(
    visita_id: int,
    payload: VisitaUpdateRequest,
    service: ServiceDep,
) -> VisitaResponse:
    record = service.patch_visita(visita_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visita no encontrada")
    return record


@router.delete("/{visita_id}", response_model=MessageResponse)
def delete_visita(
    visita_id: int,
    service: ServiceDep,
) -> MessageResponse:
    deleted = service.delete_visita(visita_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visita no encontrada")
    return MessageResponse(message="Visita eliminada")
