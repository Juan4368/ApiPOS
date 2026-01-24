from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.egresoDto import (
    EgresoRequest,
    EgresoResponse,
    EgresoUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.egreso_service import EgresoService
from src.infrastructure.repository.createEgresoRepository import EgresoRepository

router = APIRouter(prefix="/contabilidad/egresos", tags=["contabilidad-egresos"])


def get_service(db: Session = Depends(get_db)) -> EgresoService:
    repo = EgresoRepository(db)
    return EgresoService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[EgresoService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[EgresoResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_egreso(
    payload: EgresoRequest,
    service: ServiceDep,
) -> CreationResponse[EgresoResponse]:
    try:
        created = service.create_egreso(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[EgresoResponse](id=created.id, data=created)


@router.get("/", response_model=list[EgresoResponse])
def list_egresos(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
) -> list[EgresoResponse]:
    return service.list_egresos(desde=desde, hasta=hasta)


@router.get("/{egreso_id}", response_model=EgresoResponse)
def get_egreso(egreso_id: int, service: ServiceDep) -> EgresoResponse:
    egreso = service.get_egreso(egreso_id)
    if not egreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Egreso no encontrado")
    return egreso


@router.put("/{egreso_id}", response_model=EgresoResponse)
def update_egreso(
    egreso_id: int,
    payload: EgresoRequest,
    service: ServiceDep,
) -> EgresoResponse:
    egreso = service.update_egreso(egreso_id, payload)
    if not egreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Egreso no encontrado")
    return egreso


@router.patch("/{egreso_id}", response_model=EgresoResponse)
def patch_egreso(
    egreso_id: int,
    payload: EgresoUpdateRequest,
    service: ServiceDep,
) -> EgresoResponse:
    egreso = service.patch_egreso(egreso_id, payload)
    if not egreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Egreso no encontrado")
    return egreso

