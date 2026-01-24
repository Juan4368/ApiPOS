from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.carteraDto import (
    CarteraRequest,
    CarteraResponse,
    CarteraUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.cartera_service import CarteraService
from src.infrastructure.repository.createCarteraRepository import CarteraRepository

router = APIRouter(prefix="/contabilidad/cartera", tags=["contabilidad-cartera"])


def get_service(db: Session = Depends(get_db)) -> CarteraService:
    repo = CarteraRepository(db)
    return CarteraService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CarteraService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CarteraResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_cartera(
    payload: CarteraRequest,
    service: ServiceDep,
) -> CreationResponse[CarteraResponse]:
    try:
        created = service.create_cartera(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CarteraResponse](id=created.cartera_id, data=created)


@router.get("/", response_model=list[CarteraResponse])
def list_cartera(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
) -> list[CarteraResponse]:
    return service.list_cartera(desde=desde, hasta=hasta)


@router.get("/{cartera_id}", response_model=CarteraResponse)
def get_cartera(cartera_id: int, service: ServiceDep) -> CarteraResponse:
    cartera = service.get_cartera(cartera_id)
    if not cartera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartera no encontrada")
    return cartera


@router.put("/{cartera_id}", response_model=CarteraResponse)
def update_cartera(
    cartera_id: int,
    payload: CarteraRequest,
    service: ServiceDep,
) -> CarteraResponse:
    cartera = service.update_cartera(cartera_id, payload)
    if not cartera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartera no encontrada")
    return cartera


@router.patch("/{cartera_id}", response_model=CarteraResponse)
def patch_cartera(
    cartera_id: int,
    payload: CarteraUpdateRequest,
    service: ServiceDep,
) -> CarteraResponse:
    cartera = service.patch_cartera(cartera_id, payload)
    if not cartera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartera no encontrada")
    return cartera
