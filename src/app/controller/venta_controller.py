from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.ventaDto import (
    VentaRequest,
    VentaResponse,
    VentaStatusRequest,
    VentaUpdateRequest,
)
from src.domain.services.venta_service import VentaService
from src.infrastructure.repository.createVentaRepository import VentaRepository

router = APIRouter(prefix="/ventas", tags=["ventas"])


def get_venta_service(db: Session = Depends(get_db)) -> VentaService:
    repo = VentaRepository(db)
    return VentaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[VentaService, Depends(get_venta_service)]


@router.post(
    "/",
    response_model=CreationResponse[VentaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_venta(
    payload: VentaRequest,
    service: ServiceDep,
) -> CreationResponse[VentaResponse]:
    try:
        created = service.create_venta(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return CreationResponse[VentaResponse](id=created.venta_id, data=created)


@router.get("/", response_model=list[VentaResponse])
def list_ventas(service: ServiceDep) -> list[VentaResponse]:
    return service.list_ventas()


@router.get("/buscar", response_model=list[VentaResponse])
def search_ventas(q: str, service: ServiceDep) -> list[VentaResponse]:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_ventas(q.strip())


@router.get("/{venta_id}", response_model=VentaResponse)
def get_venta(venta_id: int, service: ServiceDep) -> VentaResponse:
    venta = service.get_venta(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    return venta


@router.patch("/{venta_id}/estado", response_model=VentaResponse)
def update_venta_status(
    venta_id: int,
    payload: VentaStatusRequest,
    service: ServiceDep,
) -> VentaResponse:
    venta = service.update_venta_status(venta_id, payload)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    return venta


@router.put("/{venta_id}", response_model=VentaResponse)
def update_venta(
    venta_id: int,
    payload: VentaUpdateRequest,
    service: ServiceDep,
) -> VentaResponse:
    venta = service.update_venta(venta_id, payload)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    return venta
