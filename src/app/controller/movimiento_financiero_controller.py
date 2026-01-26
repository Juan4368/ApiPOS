from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.movimientoFinancieroDto import (
    MovimientoFinancieroRequest,
    MovimientoFinancieroResponse,
    MovimientoFinancieroUpdateRequest,
)
from src.domain.enums.contabilidadEnums import CategoriaTipo
from src.domain.services.movimiento_financiero_service import (
    MovimientoFinancieroService,
)
from src.infrastructure.repository.createMovimientoFinancieroRepository import (
    MovimientoFinancieroRepository,
)

router = APIRouter(
    prefix="/contabilidad/movimientos-financieros",
    tags=["contabilidad-movimientos-financieros"],
)


def get_service(db: Session = Depends(get_db)) -> MovimientoFinancieroService:
    repo = MovimientoFinancieroRepository(db)
    return MovimientoFinancieroService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[MovimientoFinancieroService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[MovimientoFinancieroResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_movimiento(
    payload: MovimientoFinancieroRequest,
    service: ServiceDep,
) -> CreationResponse[MovimientoFinancieroResponse]:
    try:
        created = service.create_movimiento(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[MovimientoFinancieroResponse](id=created.id, data=created)


@router.get("/", response_model=list[MovimientoFinancieroResponse])
def list_movimientos(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
    caja_id: Optional[int] = None,
    tipo: Optional[CategoriaTipo] = None,
    proveedor_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    venta_id: Optional[int] = None,
) -> list[MovimientoFinancieroResponse]:
    return service.list_movimientos(
        desde=desde,
        hasta=hasta,
        caja_id=caja_id,
        tipo=tipo,
        proveedor_id=proveedor_id,
        usuario_id=usuario_id,
        venta_id=venta_id,
    )


@router.get("/{movimiento_id}", response_model=MovimientoFinancieroResponse)
def get_movimiento(movimiento_id: int, service: ServiceDep) -> MovimientoFinancieroResponse:
    movimiento = service.get_movimiento(movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
    return movimiento


@router.put("/{movimiento_id}", response_model=MovimientoFinancieroResponse)
def update_movimiento(
    movimiento_id: int,
    payload: MovimientoFinancieroRequest,
    service: ServiceDep,
) -> MovimientoFinancieroResponse:
    movimiento = service.update_movimiento(movimiento_id, payload)
    if not movimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
    return movimiento


@router.patch("/{movimiento_id}", response_model=MovimientoFinancieroResponse)
def patch_movimiento(
    movimiento_id: int,
    payload: MovimientoFinancieroUpdateRequest,
    service: ServiceDep,
) -> MovimientoFinancieroResponse:
    movimiento = service.patch_movimiento(movimiento_id, payload)
    if not movimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
    return movimiento
