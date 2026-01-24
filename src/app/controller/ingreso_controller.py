from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.ingresoDto import (
    IngresoRequest,
    IngresoResponse,
    IngresoUpdateRequest,
)
from src.domain.services.ingreso_service import IngresoService
from src.infrastructure.repository.createIngresoRepository import IngresoRepository

router = APIRouter(prefix="/contabilidad/ingresos", tags=["contabilidad-ingresos"])


def get_service(db: Session = Depends(get_db)) -> IngresoService:
    repo = IngresoRepository(db)
    return IngresoService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[IngresoService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[IngresoResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_ingreso(
    payload: IngresoRequest,
    service: ServiceDep,
) -> CreationResponse[IngresoResponse]:
    try:
        created = service.create_ingreso(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[IngresoResponse](id=created.id, data=created)


@router.get("/", response_model=list[IngresoResponse])
def list_ingresos(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
) -> list[IngresoResponse]:
    return service.list_ingresos(desde=desde, hasta=hasta)


@router.get("/{ingreso_id}", response_model=IngresoResponse)
def get_ingreso(ingreso_id: int, service: ServiceDep) -> IngresoResponse:
    ingreso = service.get_ingreso(ingreso_id)
    if not ingreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso no encontrado")
    return ingreso


@router.put("/{ingreso_id}", response_model=IngresoResponse)
def update_ingreso(
    ingreso_id: int,
    payload: IngresoRequest,
    service: ServiceDep,
) -> IngresoResponse:
    ingreso = service.update_ingreso(ingreso_id, payload)
    if not ingreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso no encontrado")
    return ingreso


@router.patch("/{ingreso_id}", response_model=IngresoResponse)
def patch_ingreso(
    ingreso_id: int,
    payload: IngresoUpdateRequest,
    service: ServiceDep,
) -> IngresoResponse:
    ingreso = service.patch_ingreso(ingreso_id, payload)
    if not ingreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso no encontrado")
    return ingreso

